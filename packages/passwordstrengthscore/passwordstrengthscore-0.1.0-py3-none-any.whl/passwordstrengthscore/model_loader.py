import joblib
import hashlib
from .exceptions import ModelTamperError

class ModelLoader:
    def __init__(self, model_paths: dict, expected_hashes: dict):
        """
        model_paths: {"model1": "path/to/model1.pkl", ...}
        expected_hashes: {"model1": "sha256_hash", ...}
        """
        self.models = {}
        for name, path in model_paths.items():
            self._verify_model(path, expected_hashes[name])
            self.models[name] = joblib.load(path)
            
    def _verify_model(self, path: str, expected_hash: str):
        """Check model integrity"""
        with open(path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            
        if file_hash != expected_hash:
            raise ModelTamperError(f"Model {path} has been tampered with")