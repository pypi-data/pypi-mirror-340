import json
import os

# llm_script.py
import sys
from typing import Any, Dict, Tuple

import numpy as np
import requests
from transformers import pipeline

from .base import AIProvider

# Paths for ONNX
MODEL_PATH_ONNX = os.path.join(os.path.dirname(__file__), "distilgpt2.onnx")
TOKENIZER_PATH = os.path.join(os.path.dirname(__file__), "tokenizer.json")
MODEL_URL = (
    "https://github.com/quantum-ernest/cmscribe/main/distilgpt2.onnx"  # Replace with your repo
)
TOKENIZER_URL = "https://raw.githubusercontent.com/yourusername/cmscribe/main/tokenizer.json"

# Check for PyTorch
try:
    import torch
    from transformers import GPT2LMHeadModel, GPT2Tokenizer

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

if not HAS_TORCH:
    import onnxruntime as ort
    from tokenizers import Tokenizer


class HuggingFaceProvider(AIProvider):
    """HuggingFace provider for commit message generation."""

    def get_default_model(self) -> str:
        return "distilgpt2"

    def validate_config(self) -> bool:
        if not HAS_TORCH and not os.path.exists(MODEL_PATH_ONNX):
            raise ValueError("PyTorch not available and ONNX model not found")
        return True

    def _download_file(self, url: str, path: str) -> None:
        """Download a file from a URL."""
        print(f"Downloading {os.path.basename(path)} from {url}...", file=sys.stderr)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded to {path}", file=sys.stderr)

    def _ensure_onnx_files(self) -> None:
        """Ensure ONNX model and tokenizer files exist."""
        if not os.path.exists(MODEL_PATH_ONNX):
            try:
                self._download_file(MODEL_URL, MODEL_PATH_ONNX)
            except requests.RequestException:
                raise FileNotFoundError(
                    "Failed to download distilgpt2.onnx. Ensure MODEL_URL is correct or manually place it at cmscribe/distilgpt2.onnx."
                )
        if not os.path.exists(TOKENIZER_PATH):
            try:
                self._download_file(TOKENIZER_URL, TOKENIZER_PATH)
            except requests.RequestException:
                raise FileNotFoundError(
                    "Failed to download tokenizer.json. Ensure TOKENIZER_URL is correct or manually place it at cmscribe/tokenizer.json."
                )

    def _load_pytorch_model(self) -> Tuple["GPT2LMHeadModel", "GPT2Tokenizer"]:
        """Load PyTorch model and tokenizer."""
        tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
        model = GPT2LMHeadModel.from_pretrained("distilgpt2")
        return model, tokenizer

    def _load_onnx_model(self) -> Tuple[ort.InferenceSession, Tokenizer]:
        """Load ONNX model and tokenizer."""
        self._ensure_onnx_files()
        session = ort.InferenceSession(MODEL_PATH_ONNX)
        tokenizer = Tokenizer.from_file(TOKENIZER_PATH)
        return session, tokenizer

    def generate_commit_message(self, diff_content: str) -> str:
        """Generate a commit message using either PyTorch or ONNX model."""
        self.validate_config()

        if HAS_TORCH:
            model, tokenizer = self._load_pytorch_model()
            inputs = tokenizer(self.format_prompt(diff_content), return_tensors="pt")
            outputs = model.generate(
                **inputs,
                max_new_tokens=self.max_tokens,
                do_sample=True,
                temperature=self.temperature,
            )
            msg = tokenizer.decode(outputs[0], skip_special_tokens=True)[
                len(self.format_prompt(diff_content)) :
            ].strip()
        else:
            session, tokenizer = self._load_onnx_model()
            inputs = tokenizer.encode(self.format_prompt(diff_content))
            input_ids = inputs["input_ids"]
            attention_mask = inputs["attention_mask"]

            for _ in range(self.max_tokens):
                outputs = session.run(
                    None, {"input_ids": input_ids, "attention_mask": attention_mask}
                )
                logits = outputs[0][:, -1, :]
                next_token_id = np.argmax(logits, axis=-1)
                input_ids = np.concatenate([input_ids, next_token_id[:, None]], axis=1)
                attention_mask = np.concatenate(
                    [attention_mask, np.ones_like(next_token_id[:, None])], axis=1
                )
                if next_token_id[0] == tokenizer.token_to_id("<|endoftext|>"):
                    break
            msg = tokenizer.decode(input_ids[0])[len(self.format_prompt(diff_content)) :].strip()

        return msg
