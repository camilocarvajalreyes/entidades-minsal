"""Script que ejecuta las predicciones para un modelo (solo HF por el momento)"""
import os
import sys
sys.path.append('../modelos')
from transformers import AutoModelForTokenClassification, AutoTokenizer
from auxfunctions import eval_text, map_entities

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

admin_ner_dict = {
    'O': 0,
    'B-CANT': 1,
    'I-CANT': 2,
    'B-UND':3,
    'I-UND':4,
    'B-VIA_ADMIN': 5,
    'I-VIA_ADMIN': 6
}


def cargar_modelo(admin=False,verbose=False):
    MODEL = 'ccarvajal/beto-prescripciones-medicas-ADMIN' if admin else 'ccarvajal/beto-prescripciones-medicas'
    folder = "bert-clinical-scratch-wl-es-NER-ADMIN" if admin else "bert-clinical-scratch-wl-es-NER-prescription"

    n_labels = len(admin_ner_dict) if admin else len(ner_dict)

    if os.path.isdir('../modelos/' + folder):
        folder = '../modelos/' + folder
        if verbose:
            print("Cargando modelo guardado localmente")
        tokenizer = AutoTokenizer.from_pretrained(folder)
        model = AutoModelForTokenClassification.from_pretrained(folder, num_labels=n_labels,ignore_mismatched_sizes=True)
    elif os.path.isdir('modelos/' + folder):
        folder = 'modelos/' + folder
        if verbose:
            print("Cargando modelo guardado localmente")
        tokenizer = AutoTokenizer.from_pretrained(folder)
        model = AutoModelForTokenClassification.from_pretrained(folder, num_labels=n_labels,ignore_mismatched_sizes=True)
    else:
        if verbose:
            print("Descargando modelo de repositorio HuggingFace")
        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        tokenizer.save_pretrained(folder)
        model_mini = AutoModelForTokenClassification.from_pretrained(MODEL, num_labels=n_labels,ignore_mismatched_sizes=True)
        model_mini.save_pretrained(folder)
    
    return tokenizer, model


tokenizer, model = cargar_modelo()
tokenizer_admin, model_admin = cargar_modelo(admin=True)


def get_admin(entidades:list,texto:str) -> str:
    """
    Retorna un substring correspondiente a aquellas entidades etiquetadas con admin y los indices donde esto ocurre
    """
    indices = [i for i, ent in enumerate(entidades) if ent == 'B-ADMIN' or ent == 'I-ADMIN']
    return ' '.join([token for i, token in enumerate(texto.split(' ')) if i in indices]), indices


def etiquetar(texto):
    entidades = map_entities(eval_text(texto,tokenizer,model),ner_dict)
    admin_text, indices = get_admin(entidades,texto)
    entidades_admin = map_entities(eval_text(admin_text,tokenizer_admin,model_admin),admin_ner_dict)
    for i, ent_admin in enumerate(entidades_admin):
        entidades[indices[i]] = ent_admin
    string_ent = '\t'.join(entidades)
    string_pre = '\t'.join(texto.split())
    print(string_ent)
    print(string_pre)
