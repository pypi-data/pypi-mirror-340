import joblib
from .features import rf_features, svm_features, cnn_features
from .config import SUPPORTED_MODELS


class PasswordStrengthEvaluator:
    def __init__(self, model_type: str, model_path: str):
        self.model_type = model_type.lower()
        self.model = joblib.load(model_path)
        self.feature_fn = self._get_feature_function()

    def _get_feature_function(self):
        if self.model_type == 'rf':
            return rf_features.extract
        elif self.model_type == 'svm':
            return svm_features.extract
        elif self.model_type == 'cnn':
            return cnn_features.extract
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def predict(self, password: str) -> str:
        features = self.feature_fn(password)
        prediction = self.model.predict([features])[0]
        return prediction
