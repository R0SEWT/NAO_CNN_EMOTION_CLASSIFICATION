import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from scripts.models.cnn import get_mobilenet_model, get_vgg19_model, CustomCNN
import time
import os


def evaluate(model, dataloader, device):
    model.eval()
    correct = 0
    total = 0
    start_time = time.time()
    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels.data)
            total += labels.size(0)
    end_time = time.time()
    accuracy = correct.double() / total
    avg_time = (end_time - start_time) / total
    return accuracy.item(), avg_time


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    dataset = datasets.ImageFolder('./data/fer2013/test', transform=transform)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=False)

    models_info = {
        'mobilenet': get_mobilenet_model(),
        'vgg19': get_vgg19_model(),
        'custom': CustomCNN()
    }

    for name, model in models_info.items():
        model_path = f'./models/{name}_final.pt'
        if not os.path.exists(model_path):
            print(f"Modelo no encontrado: {model_path}")
            continue

        model.load_state_dict(torch.load(model_path, map_location=device))
        model.to(device)

        acc, avg_time = evaluate(model, dataloader, device)
        print(f"{name.upper()} -> Accuracy: {acc:.4f} | Tiempo promedio de inferencia: {avg_time:.4f}s")


if __name__ == '__main__':
    main()
