import re
import string
from typing import List

import nltk
from natasha import Doc, MorphVocab, NewsEmbedding, NewsMorphTagger, Segmenter
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)


class TextProcessor:
    def __init__(self):
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.stop_words = stopwords.words("russian")
        self.punctuation = list(string.punctuation + "«»—…")

    def clean_text(self, text: str) -> str:
        def replace_vk_mentions(text):
            return re.sub(r"\[.*?\|(.*?)\]", "<NAME>", text)

        def replace_url(text):
            return re.sub(r"http\S+|www\.\S+", "<URL>", text)

        def replace_tangut(text):
            result = []
            inside_tangut = False

            for ch in text:
                if self._is_tangut(ch):
                    if not inside_tangut:
                        result.append("<UNK>")
                        inside_tangut = True
                else:
                    result.append(ch)
                    inside_tangut = False
            return "".join(result)

        text = text.lower()
        text = replace_vk_mentions(text)
        text = replace_url(text)
        text = replace_tangut(text)
        return text

    def tokenize_text(self, text: str) -> List[str]:
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)

        lemmatized_tokens = []
        for token in doc.tokens:
            if token.text not in self.punctuation:
                token.lemmatize(self.morph_vocab)
                # Delete stop words except pronouns
                if (
                    token.lemma not in self.stop_words or token.pos == "PRON"
                ) and token.lemma is not None:
                    lemmatized_tokens.append(token.lemma)
        return lemmatized_tokens

    def _is_tangut(self, ch):
        code_point = ord(ch)
        return (
            (0x17000 <= code_point <= 0x187FF)
            or (0x18800 <= code_point <= 0x18AFF)
            or (0x18D00 <= code_point <= 0x18D8F)
        )
