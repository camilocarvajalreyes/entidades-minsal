"""Script que ejecuta las predicciones para un modelo (solo HF por el momento)"""
import sys
sys.path.append('../modelos')
from transformers import AutoModelForTokenClassification, AutoTokenizer
from auxfunctions import eval_text, map_entities

MODEL = "bert-clinical-scratch-wl-es-NER-prescription-mini"

model = AutoModelForTokenClassification.from_pretrained('../modelos/'+MODEL)
tokenizer = AutoTokenizer.from_pretrained('../modelos/'+MODEL)

ner_dict = {'O': 0,
            'B-ACTIVE_PRINCIPLE': 1,
            'I-ACTIVE_PRINCIPLE': 2,
            'B-FORMA_FARMA':3,
            'I-FORMA_FARMA':4,
            'B-ADMIN': 5,
            'I-ADMIN': 6,
            'B-PERIODICITY': 7,
            'I-PERIODICITY': 8,
            'B-DURATION': 9,
            'I-DURATION': 10
            }
