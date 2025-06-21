import os
import shutil
import random
from pathlib import Path


# TODO: Ajustar el script

def sample_dataset(src_dir, dst_dir, num_per_class=10):
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)

    for split in ['train', 'val']:
        src_split = src_dir / split
        dst_split = dst_dir / split

        if not src_split.exists():
            print(f"Ruta no encontrada: {src_split}")
            continue

        dst_split.mkdir(parents=True, exist_ok=True)

        for class_dir in src_split.iterdir():
            if class_dir.is_dir():
                images = list(class_dir.glob("*.*"))
                if not images:
                    print(f"No hay imágenes en {class_dir}")
                    continue

                sampled = random.sample(images, min(num_per_class, len(images)))
                dst_class_dir = dst_split / class_dir.name
                dst_class_dir.mkdir(parents=True, exist_ok=True)

                for img_path in sampled:
                    shutil.copy(img_path, dst_class_dir / img_path.name)

                print(f"{split}/{class_dir.name}: {len(sampled)} imágenes copiadas.")

if __name__ == "__main__":

    num_obs = 500
    percent_val = 0.2
    n_clases = 7
    num_per_class = int(num_obs / (n_clases * (1 + percent_val)))  

    src_dir = "data/kers2013"
    out_dir = f"{src_dir}_sample_{num_obs}_val{int(percent_val * 100)}"

    sample_dataset(
        src_dir=src_dir,
        dst_dir=out_dir,
        num_per_class=num_per_class
    )
