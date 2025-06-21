import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from scripts.models.cnn import get_mobilenet_model, get_vgg19_model, CustomCNN
import time
import argparse

from scripts.logger_train import TrainingLogger

import sys
import os
from pathlib import Path


def train(model, dataloader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    for inputs, labels in dataloader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * inputs.size(0)

        # TODO: anadir train acc

    return running_loss / len(dataloader.dataset)

def evaluate(model, dataloader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            running_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels.data)
    acc = correct.double() / len(dataloader.dataset)
    return running_loss / len(dataloader.dataset), acc.item()

def main(model_name='mobilenet', batch_size=32, epochs=10, lr=0.001, data_path="./data/kers2013_sample_500_val20/"):

    logger = TrainingLogger(model_name=model_name)  # dispositivo, tiempo


    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1) if model_name == 'custom' else transforms.Lambda(lambda x: x),
        transforms.Resize((48, 48) if model_name == 'custom' else (224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)) if model_name == 'custom' else transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])


    train_path = data_path + "train"
    val_path = data_path + "val"

    train_dataset = datasets.ImageFolder(train_path, transform=transform)
    val_dataset = datasets.ImageFolder(val_path, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    if model_name == 'mobilenet':
        model = get_mobilenet_model()
    elif model_name == 'vgg19':
        model = get_vgg19_model()
    else:
        model = CustomCNN()

    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    for epoch in range(epochs):
        
        start = time.time()
        train_loss = train(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)

        # add train acc
        duration = time.time() - start
        logger.log_epoch(epoch, epochs, train_loss, val_loss, val_acc, start, duration)
        print(f"Epoch {epoch+1}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f} | Time: {duration:.2f}s")

    save_path =data_path+"../models/"
    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    torch.save(model.state_dict(), f"{save_path}{model_name}_final.pt")
    logger.log_message("Entrenamiento completo. Guardando modelo final...")
    logger.close()
    return val_acc


if __name__ == '__main__':
    sys.path.append(str(Path(__file__).resolve().parents[2]))  #root project
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='mobilenet', help='mobilenet, vgg19, custom')
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--lr', type=float, default=0.001)
    parser.add_argument('--data', type=str, default='./data/kers2013_sample_500_val20/', help='revisa data')
    args = parser.parse_args()
    main(args.model, args.batch_size, args.epochs, args.lr, args.data)


#use  PYTHONPATH=. python scripts/train/train_cnn.py --model mobilenet --epochs 20
