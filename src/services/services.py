"""Lightweight ML service that manages Hugging Face pipelines.

This small manager caches pipelines by (task, model) so demo runs avoid
re-loading models repeatedly. The implementation is intentionally
minimal for portfolio clarity.
"""

import logging
from transformers import pipeline
from src.models import HFInferenceResult

logger = logging.getLogger("uvicorn")


class ModelManager:
    _instance = None
    _pipelines = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance

    def load_model(self, task: str, model_name: str):
        """Lazy loader for HF pipelines."""
        key = f"{task}_{model_name}"
        if key not in self._pipelines:
            logger.info(f"Loading HF Model: {model_name} for task: {task}...")
            try:
                # device=-1 for CPU, device=0 for GPU
                self._pipelines[key] = pipeline(task, model=model_name, device=-1)
                logger.info(f"Model {model_name} loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load model {model_name}: {str(e)}")
                raise RuntimeError(f"Model loading failed: {e}")
        return self._pipelines[key]

    async def predict_sentiment(self, text: str) -> HFInferenceResult:
        # Runs sentiment analysis on input text.
        # Truncates text to avoid excessively long inputs for demo purposes.
        model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        pipe = self.load_model("sentiment-analysis", model_name)

        # Truncation for standard BERT limitations
        safe_text = text[:1500]

        try:
            result = pipe(safe_text)[0]  # e.g. [{'label': 'positive', 'score': 0.9}]
            return HFInferenceResult(
                label=result["label"], score=result["score"], model_name=model_name
            )
        except Exception as e:
            logger.error(f"Inference error: {e}")
            raise


ml_service = ModelManager()
