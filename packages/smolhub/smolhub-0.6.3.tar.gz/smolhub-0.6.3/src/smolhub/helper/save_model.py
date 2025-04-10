from pathlib import Path
import torch
#Saves the trained model

class SaveModel:
    def __init__(self, model, savepath, tokenizer):
        self.model = model
        self.path = Path.cwd() / savepath  # Corrected to use Path.cwd() for proper path handling
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.tokenizer = tokenizer
        
    def save(self):
        torch.save(self.model.state_dict(), self.path)
        torch.save(self.tokenizer, self.path)
        