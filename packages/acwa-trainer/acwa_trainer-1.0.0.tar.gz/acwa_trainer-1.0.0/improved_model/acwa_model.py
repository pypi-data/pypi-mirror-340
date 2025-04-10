import torch.nn as nn
from acwa_trainer import ACWATrainer

class ACWAModel(nn.Module):
    def __init__(self, base_model, num_classes, alpha=0.02, beta=0.95, update_freq=50):
        super().__init__()
        self.base_model = base_model
        self.trainer = ACWATrainer(base_model, num_classes, alpha, beta, update_freq)

    def forward(self, x):
        return self.base_model(x)

    def train_step(self, inputs, labels, optimizer):
        return self.trainer.train_step(inputs, labels, optimizer)
