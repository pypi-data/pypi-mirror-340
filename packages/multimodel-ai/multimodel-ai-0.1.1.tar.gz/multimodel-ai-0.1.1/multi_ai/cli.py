import argparse
import sys
import os
from typing import Optional
from .model_manager import ModelManager

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Multi-AI CLI - Manage and use multiple Qwen models")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List models command
    list_parser = subparsers.add_parser("list", help="List loaded models")
    
    # Load model command
    load_parser = subparsers.add_parser("load", help="Load a model")
    load_parser.add_argument("model_name", choices=["qwen-vl", "qwen-audio", "qwen-text", "zonos-tts"], 
                            help="Name of the model to load")
    
    # Unload model command
    unload_parser = subparsers.add_parser("unload", help="Unload a model")
    unload_parser.add_argument("model_name", choices=["qwen-vl", "qwen-audio", "qwen-text", "zonos-tts"], 
                              help="Name of the model to unload")
    
    # Generate text command
    generate_parser = subparsers.add_parser("generate", help="Generate text using a model")
    generate_parser.add_argument("model", choices=["qwen-vl", "qwen-audio", "qwen-text"], help="Model to use")
    generate_parser.add_argument("prompt", help="Prompt for text generation")
    generate_parser.add_argument("--image", help="Path to image file for vision models")
    generate_parser.add_argument("--audio", help="Path to audio file for audio models")
    generate_parser.add_argument("--max-tokens", type=int, help="Maximum number of tokens to generate")
    
    # TTS command
    tts_parser = subparsers.add_parser("tts", help="Generate speech from text")
    tts_parser.add_argument("text", help="Text to convert to speech")
    tts_parser.add_argument("--output", required=True, help="Path to save the audio file")
    tts_parser.add_argument("--speaker", help="Path to speaker reference audio for voice cloning")
    
    # Clear all models command
    clear_parser = subparsers.add_parser("clear", help="Clear all loaded models")
    
    return parser.parse_args()

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Initialize model manager
    manager = ModelManager()
    
    if args.command == "list":
        loaded_models = manager.list_loaded_models()
        if loaded_models:
            print("Loaded models:")
            for model in loaded_models:
                print(f"  - {model}")
        else:
            print("No models are currently loaded.")
            
    elif args.command == "load":
        try:
            model = manager.load_model(args.model_name)
            print(f"Model '{args.model_name}' loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            sys.exit(1)
            
    elif args.command == "unload":
        try:
            manager.unload_model(args.model_name)
            print(f"Model '{args.model_name}' unloaded successfully.")
        except Exception as e:
            print(f"Error unloading model: {e}")
            sys.exit(1)
            
    elif args.command == "generate":
        try:
            model = manager.load_model(args.model)
            
            # Prepare generation parameters
            gen_params = {}
            if hasattr(args, 'max_tokens') and args.max_tokens is not None:
                gen_params['max_new_tokens'] = args.max_tokens
            
            if args.model in ["qwen-vl"] and args.image:
                if not os.path.exists(args.image):
                    print(f"Error: Image file '{args.image}' not found.")
                    sys.exit(1)
                response = model.generate_with_image(args.image, args.prompt, **gen_params)
            elif args.model == "qwen-audio" and args.audio:
                if not os.path.exists(args.audio):
                    print(f"Error: Audio file '{args.audio}' not found.")
                    sys.exit(1)
                response = model.generate_with_audio(args.audio, args.prompt, **gen_params)
            elif args.model == "qwen-coder":
                response = model.generate_code(args.prompt, **gen_params)
            elif args.model == "zonos-tts":
                if not args.output:
                    print("Error: Output path is required for TTS generation.")
                    sys.exit(1)
                output_path = model.generate_speech(args.prompt, args.output, speaker_reference=args.speaker)
                print(f"\nSpeech generated and saved to: {output_path}")
                return
            else:
                response = model.generate(args.prompt, **gen_params)
                
            print("\nResponse:")
            print(response)
            
        except Exception as e:
            print(f"Error generating response: {e}")
            sys.exit(1)
            
    elif args.command == "tts":
        try:
            model = manager.load_model("zonos-tts")
            output_path = model.generate_speech(args.text, args.output, speaker_reference=args.speaker)
            print(f"\nSpeech generated and saved to: {output_path}")
        except Exception as e:
            print(f"Error generating speech: {e}")
            sys.exit(1)
            
    elif args.command == "clear":
        try:
            manager.clear_all_models()
            print("All models have been unloaded.")
        except Exception as e:
            print(f"Error clearing models: {e}")
            sys.exit(1)
            
    else:
        print("No command specified. Use --help for usage information.")
        sys.exit(1)

if __name__ == "__main__":
    main() 