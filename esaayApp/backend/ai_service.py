from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from huggingface_hub import hf_hub_download
import os
from safetensors.torch import load_file

class AIService:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        print("AIService initialized")

    def load_model(self):
        """Load the fine-tuned GPT-2 model from Hugging Face"""
        try:
            print("Loading AI model...")
            
            # Load base GPT-2 model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
            self.model = AutoModelForCausalLM.from_pretrained("gpt2")
            
            print("Base model loaded, now loading fine-tuned weights...")
            
            # Download your fine-tuned weights
            repo_id = "sudhanbhandari0/Essay_College_test"
            weights_path = hf_hub_download(repo_id=repo_id, filename="checkpoint-85/model.safetensors")
            
            # Load your weights into the model
            state_dict = load_file(weights_path)
            
            # Apply the weights to the model
            missing_keys, unexpected_keys = self.model.load_state_dict(state_dict, strict=False)
            
            if missing_keys:
                print(f"Missing keys: {missing_keys}")
            if unexpected_keys:
                print(f"Unexpected keys: {unexpected_keys}")
            
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.is_loaded = True
            print("AI model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading AI model: {e}")
            return False

    def generate_feedback(self, essay_text):
        """Generate AI feedback for the given essay"""
        if not self.is_loaded:
            return "Error: AI model not loaded"
        
        try:
            # Prepare the input prompt
            prompt = f"Please provide feedback on this college essay, see gramar:\n\nEssay:\n{essay_text}\n\nFeedback:\n"
            
            # Tokenize the input
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=2048, truncation=True)
            
            # Generate feedback
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 500,  # Generate up to 200 more tokens
                    temperature=0.3,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode the generated text
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the feedback part (remove the original prompt)
            feedback = generated_text[len(prompt):].strip()
            
            return feedback
        except Exception as e:
            return f"Error generating feedback: {e}"

    