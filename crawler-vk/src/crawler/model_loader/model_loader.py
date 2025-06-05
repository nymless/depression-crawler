import os
import pickle
from pathlib import Path
from zipfile import ZipFile

import gdown
import wget
from gensim.models.fasttext import FastTextKeyedVectors
from sklearn.svm import SVC


class ModelLoader:
    def __init__(self, vectorizer_model_path, classifier_model_path):
        self.vectorizer_model_path = Path(vectorizer_model_path)
        self.vectorizer_model_path.mkdir(exist_ok=True, parents=True)
        
        self.classifier_model_path = Path(classifier_model_path)
        self.classifier_model_path.mkdir(exist_ok=True, parents=True)

    def fetch_vectorizer_model(self, url: str) -> str:
        model_path = self.vectorizer_model_path
        
        if any(item.is_file() for item in model_path.iterdir()):
            return str(model_path)

        zip_file = wget.download(url, out=str(model_path))

        with ZipFile(zip_file, "r") as zp:
            zp.extractall(model_path)
        os.remove(zip_file)
        return str(model_path)

    def load_vectorizer_model(self, model_path: str) -> FastTextKeyedVectors:
        return FastTextKeyedVectors.load(
            os.path.join(model_path, "model.model")
        )

    def fetch_classifier_model(self, url: str) -> str:
        model_path = self.classifier_model_path
        
        if any(item.is_file() for item in model_path.iterdir()):
            return str(model_path)
        
        zip_file = gdown.download(url, model_path)
        with ZipFile(zip_file, "r") as zp:
            zp.extractall(model_path)
        os.remove(zip_file)
        return str(model_path)
        
    
    def load_classifier_model(self, model_path: str) -> SVC:
        return pickle.load(open(os.path.join(model_path, "model.pkl"), "rb"))
