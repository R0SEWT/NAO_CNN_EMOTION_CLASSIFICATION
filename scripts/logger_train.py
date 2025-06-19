
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

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            handlers=[
                logging.FileHandler(self.log_path),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger(model_name)
        self.csv_file = open(self.csv_path, mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["epoch", "train_loss", "val_loss", "train_acc", "val_acc"])

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
