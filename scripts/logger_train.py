import os
import logging
import csv
from datetime import datetime

class TrainingLogger:
    def __init__(self, model_name="default", experiment="default", log_dir="logs/train"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.model_name = model_name

        self.base_dir = os.path.join(log_dir, model_name)
        os.makedirs(self.base_dir, exist_ok=True)

        self.log_path = os.path.join(self.base_dir, f"{timestamp}.log")
        self.csv_path = os.path.join(self.base_dir, f"{timestamp}.csv")
        self.params_path = os.path.join(self.base_dir, f"{timestamp}_params.txt")

        # 🔧 Logger único por instancia
        logger_name = f"{model_name}_{timestamp}"
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False  # Evita duplicados

        # 🧼 Limpia handlers previos si ya existen
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 📝 Configura handlers manualmente
        file_handler = logging.FileHandler(self.log_path)
        stream_handler = logging.StreamHandler()

        formatter = logging.Formatter("%(asctime)s - %(message)s")
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

        # 🧾 CSV init
        self.csv_file = open(self.csv_path, mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["epoch", "train_loss", "val_loss", "train_acc", "val_acc"])

        # 🧬 Guarda hiperparámetros si es dict
        if isinstance(experiment, dict):
            with open(self.params_path, 'w') as f:
                for k, v in experiment.items():
                    f.write(f"{k}: {v}\n")
            self.logger.info(f"📄 Trial parameters saved to {self.params_path}")

        self.logger.info(f"📁 Training log created for model: {model_name}")
        self.logger.info(f"📄 Logs will be saved to {self.log_path}")
        self.logger.info(f"📄 CSV will be saved to {self.csv_path}")

    def log_epoch(self, epoch, epochs, train_loss, val_loss, val_acc, start, duration):
        self.logger.info(f"Epoch {epoch+1}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f} | Time: {duration:.2f}s")
        self.csv_writer.writerow([epoch, epochs, train_loss, val_loss, val_acc, start, duration])
        self.csv_file.flush()

    def log_message(self, message):
        self.logger.info(message)

    def close(self):
        self.csv_file.close()
        self.logger.info("✅ Logging finalizado.")
