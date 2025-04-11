import torch
from torch import nn
from torch.nn import CrossEntropyLoss
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torchvision import transforms

from tools.dataset import create_dataloaders


class ClassModel(nn.Module):
    def __init__(self):
        super(ClassModel, self).__init__()
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(4096, 1024),
            nn.ReLU(),
            nn.Linear(1024, 128),
        )

    def forward(self, x):
        x = self.classifier(x)
        return x


data_dir = ''
batch_size = 64
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = ClassModel().to(device)
# 数据预处理（增强版）
transform = transforms.Compose([
    transforms.Resize((160, 160)),
    transforms.Grayscale(),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])
train_loader, val_loader = create_dataloaders(data_dir, batch_size, transform)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
lr_scheduler = ReduceLROnPlateau(optimizer, 'min', factor=0.1, patience=4, min_lr=1e-9)
criterion = CrossEntropyLoss()
epochs = 100
for epoch in range(epochs):
    model.train()
    train_loss = 0


