import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Qwen2_5_VLForConditionalGeneration, AutoProcessor, Qwen2AudioForConditionalGeneration, BitsAndBytesConfig
from typing import Optional, Union, List
import numpy as np
from PIL import Image
import soundfile as sf
import librosa
import os
import torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE
from qwen_vl_utils import process_vision_info

class QwenBaseModel:
    """Base class for all Qwen models."""
    
    def __init__(self, model_name: str, device: Optional[str] = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.uses_device_map = False
        self.default_max_new_tokens = 2048  # Default max new tokens for generation
        
    def load(self):
        """Load the model and tokenizer."""
        if self.model is None:
            # Check if we should use device_map
            if torch.cuda.is_available() and torch.cuda.get_device_properties(0).total_memory > 8 * 1024 * 1024 * 1024:  # 8GB
                # For models that might need device mapping
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    device_map="auto",
                    trust_remote_code=True
                )
                self.uses_device_map = True
            else:
                # For smaller models or when device mapping isn't needed
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    trust_remote_code=True
                ).to(self.device)
                self.uses_device_map = False
            
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
    def to(self, device: str):
        """Move the model to specified device."""
        self.device = device
        if self.model is not None and not self.uses_device_map:
            self.model = self.model.to(device)
            
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text based on the prompt."""
        if self.model is None or self.tokenizer is None:
            self.load()
            
        # Set default max_new_tokens if not provided
        if 'max_new_tokens' not in kwargs:
            kwargs['max_new_tokens'] = self.default_max_new_tokens
            
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs, **kwargs)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

class QwenTextModel(QwenBaseModel):
    """Model class for Qwen2.5-7B-Instruct."""
    
    def __init__(self, device: Optional[str] = None):
        super().__init__("Qwen/Qwen2.5-7B-Instruct", device)
        self.uses_device_map = True  # This model uses device mapping by default
        
    def load(self):
        """Load the model and tokenizer."""
        if self.model is None:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype="auto",
                device_map="auto",
                trust_remote_code=True
            )
            
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )

class QwenVLModel:
    """Model class for Qwen2.5-VL-7B-Instruct."""
    
    def __init__(self, device: Optional[str] = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = "Qwen/Qwen2.5-VL-7B-Instruct"
        self.model = None
        self.processor = None
        self.uses_device_map = True
        self.default_max_new_tokens = 2048  # Default max new tokens for generation
        
    def load(self):
        """Load the model and processor."""
        if self.model is None:
            self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                self.model_name,
                torch_dtype="auto",
                device_map="auto",
                trust_remote_code=True
            )
            
        if self.processor is None:
            self.processor = AutoProcessor.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
    def to(self, device: str):
        """Move the model to specified device."""
        self.device = device
        # Model uses device_map, so no need to move
            
    def generate_with_image(self, image: Union[str, Image.Image], prompt: str, **kwargs) -> str:
        """Generate text based on image and prompt."""
        if self.model is None or self.processor is None:
            self.load()
            
        # Set default max_new_tokens if not provided
        if 'max_new_tokens' not in kwargs:
            kwargs['max_new_tokens'] = self.default_max_new_tokens
            
        # Prepare image
        if isinstance(image, str):
            image = Image.open(image)
            
        # Prepare messages format
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image,
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ]
        
        # Prepare inputs
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.device)
        
        # Generate response
        generated_ids = self.model.generate(**inputs, **kwargs)
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]
        
        return output_text

class QwenCoderModel(QwenBaseModel):
    """Model class for Qwen2.5-Coder-7B-Instruct."""
    
    def __init__(self, device: Optional[str] = None):
        super().__init__("Qwen/Qwen2.5-Coder-7B-Instruct", device)
        
    def generate_code(self, prompt: str, **kwargs) -> str:
        """Generate code based on the prompt."""
        return self.generate(prompt, **kwargs)

class QwenAudioModel:
    """Model class for Qwen2-Audio-7B-Instruct."""
    
    def __init__(self, device: Optional[str] = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = "Qwen/Qwen2-Audio-7B-Instruct"
        self.model = None
        self.processor = None
        self.uses_device_map = True
        self.default_max_new_tokens = 2048  # Default max new tokens for generation
        
    def load(self):
        """Load the model and processor."""
        if self.model is None:
            # Configure 8-bit quantization
            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True,
                bnb_4bit_compute_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            
            self.model = Qwen2AudioForConditionalGeneration.from_pretrained(
                self.model_name,
                quantization_config=quantization_config,
                device_map={"": self.device},
                trust_remote_code=True
            )
            
        if self.processor is None:
            self.processor = AutoProcessor.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
    def to(self, device: str):
        """Move the model to specified device."""
        self.device = device
        # Model uses device_map, so no need to move
            
    def generate_with_audio(self, audio_path: str, prompt: str, **kwargs) -> str:
        """Generate text based on audio and prompt."""
        if self.model is None or self.processor is None:
            self.load()
            
        # Set default max_new_tokens if not provided
        if 'max_new_tokens' not in kwargs:
            kwargs['max_new_tokens'] = self.default_max_new_tokens
            
        # Read and resample audio file to match model's sampling rate
        audio, _ = librosa.load(audio_path, sr=self.processor.feature_extractor.sampling_rate)
        
        # Prepare conversation format
        conversation = [
            {'role': 'system', 'content': 'You are a helpful assistant.'}, 
            {"role": "user", "content": [
                {"type": "audio", "audio": audio},
                {"type": "text", "text": prompt},
            ]},
        ]
        
        # Prepare inputs
        text = self.processor.apply_chat_template(
            conversation, 
            add_generation_prompt=True, 
            tokenize=False
        )
        
        inputs = self.processor(
            text=text,
            audio=[audio],
            return_tensors="pt",
            padding=True
        )
        
        # Move all input tensors to the correct device
        inputs = {k: v.to(self.device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}
        
        # Generate response
        generate_ids = self.model.generate(
            **inputs,
            max_length=kwargs.get('max_new_tokens', self.default_max_new_tokens)
        )
        generate_ids = generate_ids[:, inputs['input_ids'].size(1):]
        
        output_text = self.processor.batch_decode(
            generate_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0]
        
        return output_text

class ZonosTTSModel(QwenBaseModel):
    """Model class for Zonos Text-to-Speech."""
    
    def __init__(self, device: Optional[str] = None):
        super().__init__("zonos-tts", device)
        self.tts_model = None
        self.device = device or DEFAULT_DEVICE
        
    def load(self):
        """Load the TTS model."""
        if self.tts_model is None:
            self.tts_model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=self.device)
            
    def generate_speech(self, text: str, output_path: str, speaker_reference: Optional[str] = None, **kwargs) -> str:
        """
        Generate speech from text and save to a file.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the audio file
            speaker_reference: Path to reference audio file for voice cloning
            **kwargs: Additional arguments for TTS generation
            
        Returns:
            Path to the generated audio file
        """
        if self.tts_model is None:
            self.load()
            
        # Generate speech
        if speaker_reference:
            if not os.path.exists(speaker_reference):
                raise FileNotFoundError(f"Speaker reference audio file not found: {speaker_reference}")
            # Load speaker reference audio
            wav, sampling_rate = torchaudio.load(speaker_reference)
            speaker = self.tts_model.make_speaker_embedding(wav, sampling_rate)
        else:
            speaker = None
            
        # Prepare conditioning
        cond_dict = make_cond_dict(
            text=text,
            speaker=speaker,
            language=kwargs.get('language', 'en-us')
        )
        conditioning = self.tts_model.prepare_conditioning(cond_dict)
        
        # Generate audio codes
        codes = self.tts_model.generate(conditioning)
        
        # Decode to waveform
        wavs = self.tts_model.autoencoder.decode(codes).cpu()
        
        # Save to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        torchaudio.save(output_path, wavs[0], self.tts_model.autoencoder.sampling_rate)
        
        return output_path 