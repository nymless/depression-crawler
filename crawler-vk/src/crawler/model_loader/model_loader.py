import os
import pickle
from pathlib import Path
from zipfile import ZipFile

import wget
from gensim.models.fasttext import FastTextKeyedVectors
from sklearn.svm import SVC


class ModelLoader:
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True, parents=True)

    def fetch_model(self, url: str, name: str) -> str:
        model_path = self.models_dir.joinpath(name)
        if any(item.is_file() for item in model_path.iterdir()):
            return str(model_path)

        model_path.mkdir(exist_ok=True, parents=True)
        zip_file = wget.download(url, out=str(model_path))
        model_path = model_path.joinpath(name)

        with ZipFile(zip_file, "r") as zp:
            zp.extractall(model_path)
        os.remove(zip_file)
        return str(model_path)

    def load_fasttext_model(self, model_path: str) -> FastTextKeyedVectors:
        return FastTextKeyedVectors.load(
            os.path.join(model_path, "model.model")
        )

    def load_classifier_model(self, model_path: str) -> SVC:
        return pickle.load(open(os.path.join(model_path, "model.pkl"), "rb"))
