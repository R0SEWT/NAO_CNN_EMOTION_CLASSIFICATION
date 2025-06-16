import os
import pandas as pd
import numpy as np
import cv2
from tqdm import tqdm

# FER2013 tiene 7 emociones en total
EMOTIONS = {
    0: "angry",
    1: "disgust",
    2: "fear",
    3: "happy",
    4: "sad",
    5: "surprise",
    6: "neutral"
}


def save_image(img_array, path):
    img = np.reshape(img_array, (48, 48))
    cv2.imwrite(path, img)


def preprocess_fer2013(csv_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for split in ['train', 'val', 'test']:
        for label in EMOTIONS.values():
            os.makedirs(os.path.join(output_dir, split, label), exist_ok=True)

    df = pd.read_csv(csv_path)
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        label = EMOTIONS[int(row['emotion'])]
        pixels = np.fromstring(row['pixels'], dtype=int, sep=' ')
        usage = row['Usage']
        if 'Training' in usage:
            split = 'train'
        elif 'PublicTest' in usage:
            split = 'val'
        else:
            split = 'test'

        filename = os.path.join(output_dir, split, label, f"img_{idx}.png")
        save_image(pixels, filename)


if __name__ == '__main__':
    csv_path = './data/fer2013/fer2013.csv'
    output_dir = './data/fer2013/'
    preprocess_fer2013(csv_path, output_dir)
    print("Preprocesamiento terminado.")

