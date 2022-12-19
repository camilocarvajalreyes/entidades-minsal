"""Script que ejecuta las predicciones para un modelo (solo HF por el momento)"""
import os
import sys
sys.path.append('../modelos')
from transformers import AutoModelForTokenClassification, AutoTokenizer
from auxfunctions import eval_text, map_entities
import pandas as pd

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
        model = AutoModelForTokenClassification.from_pretrained(MODEL, num_labels=n_labels,ignore_mismatched_sizes=True)
        model.save_pretrained(folder)
    
    return tokenizer, model


tokenizer, model = cargar_modelo()
tokenizer_admin, model_admin = cargar_modelo(admin=True)


def get_admin(entidades:list,texto:str) -> str:
    """
    Retorna un substring correspondiente a aquellas entidades etiquetadas con admin y los indices donde esto ocurre
    """
    indices = [i for i, ent in enumerate(entidades) if ent == 'B-ADMIN' or ent == 'I-ADMIN']
    return ' '.join([token for i, token in enumerate(texto.split(' ')) if i in indices]), indices


def render_pandas(ents,text_list):
    data = {'ACTIVE_PRINCIPLE':'','FORMA_FARMA':'','CANT-ADMIN':'','UND-ADMIN':'','VIA-ADMIN':'','PERIODICITY':'','DURATION':''}

    for i, ent in enumerate(ents):
        if '-ACTIVE_PRINCIPLE' in ent:
            data['ACTIVE_PRINCIPLE'] += ' ' + text_list[i]
        elif '-FORMA_FARMA' in ent:
            data['FORMA_FARMA'] += ' ' + text_list[i]
        elif '-CANT' in ent:
            data['CANT-ADMIN'] += ' ' + text_list[i]
        elif '-UND' in ent:
            data['UND-ADMIN'] += ' ' + text_list[i]
        elif '-VIA_ADMIN' in ent:
            data['VIA-ADMIN'] += ' ' + text_list[i]
        elif '-PERIODICITY' in ent:
            data['PERIODICITY'] += ' ' + text_list[i]
        elif '-DURATION' in ent:
            data['DURATION'] += ' ' + text_list[i]

    # df = pd.DataFrame([dict(zip(ents,text_list))])
    df = pd.DataFrame([data])
    # df = df.style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
    # df = df.set_properties(**{'text-align': 'center'}).hide_index()
    # df = df.style.hide(axis='index')
    return df.style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])]).hide(axis='index')


def etiquetar(texto,pandas=True):
    entidades = map_entities(eval_text(texto,tokenizer,model),ner_dict)
    admin_text, indices = get_admin(entidades,texto)
    entidades_admin = map_entities(eval_text(admin_text,tokenizer_admin,model_admin),admin_ner_dict)
    for i, ent_admin in enumerate(entidades_admin):
        entidades[indices[i]] = ent_admin
    if pandas:
        return render_pandas(entidades,texto.split())
    else:
        string_ent = '\t'.join(entidades)
        string_pre = '\t'.join(texto.split())
        print(string_ent)
        print(string_pre)
