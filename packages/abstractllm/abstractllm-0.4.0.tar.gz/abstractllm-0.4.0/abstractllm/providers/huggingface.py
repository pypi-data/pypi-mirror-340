"""
HuggingFace provider for AbstractLLM.

This module provides direct integration with HuggingFace models using the transformers library.
"""

from typing import Dict, Any, Optional, Union, Generator, AsyncGenerator, List, ClassVar, Tuple
import os
import asyncio
import logging
import time
import gc
from concurrent.futures import ThreadPoolExecutor
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    AutoModelForVision2Seq,
    AutoProcessor,
    TextIteratorStreamer,
    BlipProcessor,
    BlipForConditionalGeneration,
    AutoConfig,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    LlavaForConditionalGeneration,
    LlavaProcessor
)
from pathlib import Path
from PIL import Image

from abstractllm.interface import AbstractLLMInterface, ModelParameter, ModelCapability
from abstractllm.utils.logging import log_request, log_response, log_request_url
from abstractllm.media.factory import MediaFactory
from abstractllm.exceptions import (
    UnsupportedOperationError, 
    ModelNotFoundError, 
    FileProcessingError, 
    UnsupportedFeatureError, 
    ImageProcessingError,
    GenerationError
)
from abstractllm.media.image import ImageInput
from abstractllm.utils.config import ConfigurationManager

# Configure logger
logger = logging.getLogger("abstractllm.providers.huggingface")

# Default timeout in seconds for generation
DEFAULT_GENERATION_TIMEOUT = 60

# Models that support vision capabilities with their specific architectures
VISION_CAPABLE_MODELS = {
    "Salesforce/blip-image-captioning-base": "vision_seq2seq",
    "Salesforce/blip-image-captioning-large": "vision_seq2seq",
    "liuhaotian/llava-v1.5-7b": "llava",
    "llava-hf/llava-1.5-7b-hf": "llava",
    "llava-hf/llava-v1.6-mistral-7b-hf": "llava",
    "microsoft/git-base": "vision_encoder",
    "microsoft/git-large": "vision_encoder"
}

# Model architecture to class mapping
MODEL_CLASSES = {
    "vision_seq2seq": (BlipProcessor, BlipForConditionalGeneration),
    "vision_causal_lm": (AutoProcessor, AutoModelForCausalLM),
    "vision_encoder": (AutoProcessor, AutoModelForVision2Seq),
    "causal_lm": (AutoTokenizer, AutoModelForCausalLM),
    "llava": (LlavaProcessor, LlavaForConditionalGeneration)
}

class HuggingFaceProvider(AbstractLLMInterface):
    """
    HuggingFace implementation using Transformers.
    """
    
    # Class-level model cache
    _model_cache: ClassVar[Dict[Tuple[str, str, bool, bool], Tuple[Any, Any, float]]] = {}
    _max_cached_models = 3
    
    def __init__(self, config: Optional[Dict[Union[str, ModelParameter], Any]] = None):
        """Initialize the HuggingFace provider."""
        super().__init__(config)
        
        # Set default configuration for HuggingFace
        default_config = {
            ModelParameter.MODEL: "microsoft/Phi-4-mini-instruct",
            ModelParameter.TEMPERATURE: 0.7,
            ModelParameter.MAX_TOKENS: 1024,
            ModelParameter.DEVICE: self._get_optimal_device(),
            "trust_remote_code": True,
            "load_in_8bit": True,  # Enable 8-bit quantization by default
            "load_in_4bit": False,
            "device_map": "auto",
            "attn_implementation": "flash_attention_2",  # More memory efficient attention
            "load_timeout": 300,
            "generation_timeout": DEFAULT_GENERATION_TIMEOUT,
            "torch_dtype": "auto",
            "low_cpu_mem_usage": True
        }
        
        # Merge defaults with provided config
        self.config_manager.merge_with_defaults(default_config)
        
        # Initialize model components
        self._model = None
        self._tokenizer = None
        self._processor = None
        self._model_loaded = False
        self._model_type = "causal"  # Default model type
        
        # Log initialization
        model = self.config_manager.get_param(ModelParameter.MODEL)
        logger.info(f"Initialized HuggingFace provider with model: {model}")
    
    @staticmethod
    def _get_optimal_device() -> str:
        """Determine the optimal device for model loading."""
        try:
            if torch.cuda.is_available():
                logger.info(f"CUDA detected with {torch.cuda.device_count()} device(s)")
                return "cuda"
            if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                logger.info("MPS (Apple Silicon) detected")
                return "mps"
        except Exception as e:
            logger.warning(f"Error detecting optimal device: {e}")
        
        logger.info("Using CPU for model inference")
        return "cpu"
    
    def _get_model_architecture(self, model_name: str) -> str:
        """Determine the model architecture type based on the model name."""
        # Check exact matches first
        if model_name in VISION_CAPABLE_MODELS:
            return VISION_CAPABLE_MODELS[model_name]
            
        # Then check patterns
        if "llava" in model_name.lower():
            return "llava"
        if any(vision_model in model_name.lower() for vision_model in ["blip", "git"]):
            return "vision_seq2seq"
        return "causal_lm"
    
    def _get_model_classes(self, model_type: str) -> Tuple[Any, Any]:
        """Get the appropriate processor and model classes based on model type."""
        if model_type not in MODEL_CLASSES:
            logger.warning(f"Unknown model type {model_type}, falling back to causal_lm")
            model_type = "causal_lm"
            
        return MODEL_CLASSES[model_type]
    
    def load_model(self) -> None:
        """Load the model and tokenizer/processor."""
        try:
            # Get configuration parameters
            model_name = self.config_manager.get_param(ModelParameter.MODEL)
            cache_dir = self.config_manager.get_param("cache_dir")
            device = self.config_manager.get_param("device", "cpu")
            trust_remote_code = self.config_manager.get_param("trust_remote_code", True)
            use_auth_token = self.config_manager.get_param(ModelParameter.API_KEY)

            # Handle HuggingFace Hub authentication
            if use_auth_token:
                import huggingface_hub
                huggingface_hub.login(token=use_auth_token)

            # Determine model architecture and get appropriate classes
            self._model_type = self._get_model_architecture(model_name)
            processor_class, model_class = self._get_model_classes(self._model_type)
            
            logger.info(f"Loading {model_name} as {self._model_type} architecture")

            # Load processor/tokenizer first for vision models
            if self._model_type in ["vision_seq2seq", "llava"]:
                self._processor = processor_class.from_pretrained(
                    model_name,
                    cache_dir=cache_dir,
                    trust_remote_code=trust_remote_code,
                    use_auth_token=use_auth_token
                )
                # For LLaVA models, get the tokenizer from the processor
                if self._model_type == "llava":
                    self._tokenizer = self._processor.tokenizer
                    # Ensure special tokens are set
                    if self._tokenizer.pad_token is None:
                        self._tokenizer.pad_token = self._tokenizer.eos_token
                    if self._tokenizer.bos_token is None:
                        self._tokenizer.bos_token = self._tokenizer.eos_token
            else:
                # For causal models, load tokenizer directly
                self._tokenizer = processor_class.from_pretrained(
                    model_name,
                    cache_dir=cache_dir,
                    trust_remote_code=trust_remote_code,
                    use_auth_token=use_auth_token
                )
                # Add special tokens if needed
                if self._tokenizer.pad_token is None:
                    self._tokenizer.pad_token = self._tokenizer.eos_token
                if self._tokenizer.bos_token is None:
                    self._tokenizer.bos_token = self._tokenizer.eos_token

            # Load the model
            device_map = "auto" if torch.cuda.is_available() else None
            torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

            self._model = model_class.from_pretrained(
                model_name,
                cache_dir=cache_dir,
                trust_remote_code=trust_remote_code,
                torch_dtype=torch_dtype,
                device_map=device_map,
                use_auth_token=use_auth_token
            )

            # Move model to device if not using device_map="auto"
            if device_map is None:
                self._model.to(device)

            # Resize token embeddings if needed
            if len(self._tokenizer) > self._model.config.vocab_size:
                self._model.resize_token_embeddings(len(self._tokenizer))

            self._model_loaded = True
            logger.info(f"Successfully loaded {model_name}")

        except Exception as e:
            error_msg = f"Failed to load model {model_name}: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
    
    def _move_inputs_to_device(self, inputs: Dict[str, torch.Tensor], device: str) -> Dict[str, torch.Tensor]:
        """Move input tensors to the specified device."""
        if device == "cpu":
            return inputs
        return {k: v.to(device) for k, v in inputs.items()}
    
    def generate(self, 
                prompt: str, 
                system_prompt: Optional[str] = None,
                files: Optional[List[Union[str, Path]]] = None,
                stream: bool = False,
                **kwargs) -> Union[str, Generator[str, None, None]]:
        """Generate text based on the prompt and optional files."""
        if not self._model_loaded:
            self.load_model()
            
        # Get device from config
        device = self.config_manager.get_param("device", "cpu")
            
        # Process files if provided
        if files:
            try:
                processed_files = []
                for file_path in files:
                    media_input = MediaFactory.from_source(file_path)
                    processed_files.append(media_input)
                
                # For vision models, we only support one image at a time currently
                if self._model_type in ["vision_seq2seq", "llava"]:
                    if len(processed_files) > 1:
                        raise ValueError("Vision models currently support only one image at a time")
                    if not any(isinstance(f, ImageInput) for f in processed_files):
                        raise ValueError("No valid image file found in the provided files")
                    image_file = next(f for f in processed_files if isinstance(f, ImageInput))
                    image = Image.open(image_file.source)
                else:
                    # For text models, we append file contents to the prompt
                    file_contents = []
                    for file in processed_files:
                        if file.media_type != "text":
                            logger.warning(f"Skipping non-text file {file.source} for text model")
                            continue
                        with open(file.source, 'r') as f:
                            file_contents.append("\n===== " + file.source + " =========\n" + f.read() + "\n")
                    if file_contents:
#                        prompt = prompt + "\n" + "\n".join(file_contents)
                        prompt = prompt + "\n\n===== JOINT FILES ======\n" + "\n".join(file_contents)
                        
            except Exception as e:
                error_msg = f"Error processing files: {str(e)}"
                logger.error(error_msg)
                raise ValueError(error_msg) from e

        try:
            # Get generation parameters from config manager
            params = {
                "max_length": self.config_manager.get_param(ModelParameter.MAX_TOKENS, 2048),
                "temperature": self.config_manager.get_param(ModelParameter.TEMPERATURE, 0.7),
                "top_p": self.config_manager.get_param(ModelParameter.TOP_P, 0.9),
                "top_k": kwargs.get('top_k', 50),
                "num_return_sequences": kwargs.get('num_return_sequences', 1),
                "do_sample": kwargs.get('do_sample', True)
            }
            
            # Prepare inputs based on model type
            if self._model_type in ["vision_seq2seq", "llava"]:
                inputs = self._processor(images=image, text=prompt, return_tensors="pt")
            else:
                inputs = self._tokenizer(prompt, return_tensors="pt", padding=True)
            
            # Move inputs to the correct device
            inputs = self._move_inputs_to_device(inputs, device)
            
            # Generate
            with torch.no_grad():
                outputs = self._model.generate(
                    **inputs,
                    **params,
                    pad_token_id=self._tokenizer.pad_token_id,
                    eos_token_id=self._tokenizer.eos_token_id
                )
            
            # Decode outputs
            if self._model_type in ["vision_seq2seq", "llava"]:
                generated_text = self._processor.batch_decode(outputs, skip_special_tokens=True)
            else:
                generated_text = self._tokenizer.batch_decode(outputs, skip_special_tokens=True)
            
            # Return first sequence if only one was requested
            return generated_text[0] if params["num_return_sequences"] == 1 else generated_text
            
        except Exception as e:
            error_msg = f"Generation failed: {str(e)}"
            logger.error(error_msg)
            raise GenerationError(error_msg) from e
    
    async def generate_async(self, prompt: str, system_prompt: Optional[str] = None,
                          files: Optional[List[Union[str, Path]]] = None,
                          stream: bool = False, **kwargs) -> str:
        """Generate text asynchronously."""
        # Run the synchronous generate method in a thread pool
        with ThreadPoolExecutor() as executor:
            return await asyncio.get_event_loop().run_in_executor(
                executor,
                self.generate,
                prompt,
                files,
                **kwargs
            )
    
    def get_capabilities(self) -> Dict[Union[str, ModelCapability], Any]:
        """Return capabilities of this implementation."""
        model = self.config_manager.get_param(ModelParameter.MODEL)
        is_vision_capable = any(vm in model for vm in VISION_CAPABLE_MODELS)
        
        return {
            ModelCapability.STREAMING: True,
            ModelCapability.MAX_TOKENS: None,  # Varies by model
            ModelCapability.SYSTEM_PROMPT: True,
            ModelCapability.ASYNC: True,
            ModelCapability.FUNCTION_CALLING: False,
            ModelCapability.VISION: is_vision_capable
        }
    
    @staticmethod
    def list_cached_models(cache_dir: Optional[str] = None) -> list:
        """List all models cached by this implementation."""
        if cache_dir is None:
            cache_dir = HuggingFaceProvider.DEFAULT_CACHE_DIR
            
        if cache_dir and '~' in cache_dir:
            cache_dir = os.path.expanduser(cache_dir)
            
        if not os.path.exists(cache_dir):
            return []
            
        try:
            from huggingface_hub import scan_cache_dir
            
            cache_info = scan_cache_dir(cache_dir)
            return [{
                "name": repo.repo_id,
                "size": repo.size_on_disk,
                "last_used": repo.last_accessed,
                "implementation": "transformers"
            } for repo in cache_info.repos]
        except ImportError:
            logger.warning("huggingface_hub not available for cache scanning")
            return []
    
    @staticmethod
    def clear_model_cache(model_name: Optional[str] = None, cache_dir: Optional[str] = None) -> None:
        """Clear model cache for this implementation."""
        if cache_dir is None:
            cache_dir = HuggingFaceProvider.DEFAULT_CACHE_DIR
            
        if cache_dir and '~' in cache_dir:
            cache_dir = os.path.expanduser(cache_dir)
            
        if not os.path.exists(cache_dir):
            return
            
        try:
            from huggingface_hub import delete_cache_folder
            
            if model_name:
                delete_cache_folder(repo_id=model_name, cache_dir=cache_dir)
            else:
                delete_cache_folder(cache_dir=cache_dir)
        except ImportError:
            logger.warning("huggingface_hub not available for cache clearing")

def torch_available() -> bool:
    """
    Check if PyTorch is available.
    
    Returns:
        bool: True if PyTorch is available
    """
    try:
        import torch
        return True
    except ImportError:
        return False

# Simple adapter class for tests
class HuggingFaceLLM:
    """
    Simple adapter around HuggingFaceProvider for test compatibility.
    """
    
    def __init__(self, model="llava-hf/llava-1.5-7b-hf", api_key=None):
        """
        Initialize a HuggingFace LLM instance.
        
        Args:
            model: The model to use
            api_key: Optional API key (will use environment variable if not provided)
        """
        config = {
            ModelParameter.MODEL: model,
        }
        
        if api_key:
            config[ModelParameter.API_KEY] = api_key
            
        self.provider = HuggingFaceProvider(config)
        
    def generate(self, prompt, image=None, images=None, **kwargs):
        """
        Generate a response using the provider.
        
        Args:
            prompt: The prompt to send
            image: Optional single image
            images: Optional list of images
            return_format: Format to return the response in
            **kwargs: Additional parameters
            
        Returns:
            The generated response
        """
        # Add images to kwargs if provided
        if image:
            kwargs["image"] = image
        if images:
            kwargs["images"] = images
            
        response = self.provider.generate(prompt, **kwargs)
        
        return response 