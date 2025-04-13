import torch
from torch import nn
from torch.quantization import quantize_dynamic
from torch.utils.data import DataLoader, Dataset
import logging

class AIOptimizer:
    """
    A class for optimizing AI models and workloads.
    """

    def __init__(self, model):
        self.model = model
        self.logger = logging.getLogger(__name__)

    def optimize_model(self):
        """
        Apply optimization techniques to the model, including:
        - Dynamic Quantization
        - Pruning
        """
        self.logger.info("\n--- Optimizing the Model ---")

        # Apply Dynamic Quantization
        self.logger.info("Applying Dynamic Quantization...")
        try:
            self.model = quantize_dynamic(
                self.model,  # Model to be quantized
                {nn.Linear},  # Layers to quantize (e.g., Linear layers)
                dtype=torch.qint8  # Data type for quantization
            )
            self.logger.info("Dynamic Quantization complete.")
        except Exception as e:
            self.logger.error(f"Dynamic Quantization failed: {e}")

        # Apply Pruning (e.g., prune 50% of weights in Linear layers)
        self.logger.info("Applying Pruning...")
        try:
            for module in self.model.modules():
                if isinstance(module, nn.Linear):
                    nn.utils.prune.l1_unstructured(module, name="weight", amount=0.5)
                    nn.utils.prune.remove(module, "weight")  # Remove pruning mask after pruning
            self.logger.info("Pruning complete.")
        except Exception as e:
            self.logger.error(f"Pruning failed: {e}")

        return self.model

    def optimize_workload(self, data, batch_size=32):
        """
        Optimize the workload for better performance by batching the data.
        """
        self.logger.info("\n--- Optimizing the Workload ---")
        try:
            # Split the data into batches for efficient processing
            batched_data = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]
            self.logger.info(f"Workload optimization complete. Total batches created: {len(batched_data)}")
            return batched_data
        except Exception as e:
            self.logger.error(f"Workload optimization failed: {e}")
            return None

    def apply_knowledge_distillation(self, teacher_model, student_model, data_loader, epochs=5, lr=0.001):
        """
        Apply Knowledge Distillation to train a smaller student model using the teacher model's predictions.
        """
        self.logger.info("\n--- Applying Knowledge Distillation ---")
        criterion = nn.KLDivLoss(reduction="batchmean")
        optimizer = torch.optim.Adam(student_model.parameters(), lr=lr)

        try:
            for epoch in range(epochs):
                self.logger.info(f"Epoch {epoch + 1}/{epochs}")
                for inputs, _ in data_loader:
                    teacher_outputs = teacher_model(inputs)
                    student_outputs = student_model(inputs)
                    loss = criterion(
                        torch.log_softmax(student_outputs, dim=1),
                        torch.softmax(teacher_outputs, dim=1)
                    )
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
            self.logger.info("Knowledge Distillation complete.")
        except Exception as e:
            self.logger.error(f"Knowledge Distillation failed: {e}")
        return student_model

    def apply_mixed_precision_training(self, model, data_loader, optimizer, criterion, epochs=5):
        """
        Apply Mixed-Precision Training using Automatic Mixed Precision (AMP).
        """
        self.logger.info("\n--- Applying Mixed-Precision Training ---")
        if not torch.cuda.is_available():
            self.logger.warning("Mixed-precision training skipped (no CUDA available).")
            return model

        scaler = torch.cuda.amp.GradScaler()
        model = model.cuda()

        try:
            for epoch in range(epochs):
                self.logger.info(f"Epoch {epoch + 1}/{epochs}")
                for inputs, labels in data_loader:
                    inputs, labels = inputs.cuda(), labels.cuda()

                    with torch.cuda.amp.autocast():
                        outputs = model(inputs)
                        loss = criterion(outputs, labels)

                    optimizer.zero_grad()
                    scaler.scale(loss).backward()
                    scaler.step(optimizer)
                    scaler.update()
            self.logger.info("Mixed-Precision Training complete.")
        except Exception as e:
            self.logger.error(f"Mixed-Precision Training failed: {e}")
        return model

    def save_model(self, path):
        """
        Save the optimized model to the specified path.
        """
        self.logger.info(f"Saving model to {path}...")
        try:
            torch.save(self.model.state_dict(), path)
            self.logger.info("Model saved successfully.")
        except Exception as e:
            self.logger.error(f"Failed to save model: {e}")

    def load_model(self, path):
        """
        Load a model from the specified path.
        """
        self.logger.info(f"Loading model from {path}...")
        try:
            self.model.load_state_dict(torch.load(path))
            self.logger.info("Model loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")