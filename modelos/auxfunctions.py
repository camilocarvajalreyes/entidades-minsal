"""Funciones auxiliares para entrenamiento y evaluación"""
from scipy.special import softmax
import numpy as np
from seqeval.metrics import f1_score, precision_score, recall_score


def map_entities(y_pred,map_dict,return_type='list'):
    inv_map = {v: k for k, v in map_dict.items()}
    if return_type == 'list':
        return [inv_map[y] for y in y_pred]
    else:
        return np.array([inv_map[y] for y in y_pred])


def calculate_metrics(y_pred, y_true, verbose=True, ner_dict=None):
    """
    Calcula precision, recall y f1

    to do: mejorar descripción
    """
    if not isinstance(y_pred[0][0],str):
        if ner_dict is None:
            raise TypeError("O bien labels deben ser strings (nombres de NER tags) o bien se debe precisar diccionario entidad-id")
        y_pred = [map_entities(y,ner_dict) for y in y_pred]
        y_true = [map_entities(y,ner_dict) for y in y_true]
    # calcular scores
    f1 = f1_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, mode='strict')
    recall = recall_score(y_true, y_pred, mode='strict')

    if verbose:
        print("Resultados de evaluación")
        print(f'\t f1: {f1:.2f} | precision: {precision:.2f} | recall: {recall:.2f}')

    return precision, recall, f1


def tokenize_and_align_labels(examples,tokenizer):
    """
    Descripción: Agregar el roken especial [CLS] y [SEP] y la tokenización en subpalabras genera un desajuste entre input y etiquetas.
    Realineamos los tokens y las etiquetas del siguiente modo:
    - Mapear todos los tokens a sus palabras con el método word_ids
    - Asignar el label [-100] y tokens especiales [CLS] y [SEP] para que sean ignoradas por la función de pérdida de pytorch.
    - Solo etiquetamos el primer token de una palabra y asignamos -100 a los otros subtokens de la misma palabra.
    Fuente: https://huggingface.co/docs/transformers/tasks/token_classification
    """
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)

    labels = []
    for i, label in enumerate(examples[f"ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their respective word.
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:  # Set the special tokens to -100.
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:  # Only label the first token of a given word.
                label_ids.append(label[word_idx])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)

    tokenized_inputs["labels"] = labels

    return tokenized_inputs


def word_ids_method(text,tokenizer):
    """Método que asigna el primer token (subword) de una palabra como representante
        La etiqueta de este token será la etiqueta de la palabra
    Método integrado en tokenize_and_align_labels
    Fuente: https://huggingface.co/docs/transformers/tasks/token_classification

    Argumentos

        text: str o List[str]
            texto a tokenizar, si 
    """
    if not isinstance(text,list):
        text = text.split()
    n_words = len(text)

    tokenized_inputs = tokenizer([text], truncation=True, is_split_into_words=True)
    mask = []
    # for i in range(n_words):
    word_ids = tokenized_inputs.word_ids(batch_index=0)
    previous_word_idx = None
    for word_idx in word_ids:
        if word_idx is None:
            mask.append(0)
        elif word_idx != previous_word_idx:  # Only label the first token of a given word.
            mask.append(1)
        else:
            mask.append(0)
        previous_word_idx = word_idx
    
    return mask
    


def eval_text(text,tokenizer,model):
    """
    Toma un texto (lista de palabras o string), un tokenizador y modelo de HuggingFace
    Retorna el output del modelo (ids de entidades)
    """
    mask = word_ids_method(text,tokenizer)
    encoded_input = tokenizer(text,return_tensors='pt',is_split_into_words=isinstance(text,list))
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    result = np.argmax(scores,axis=1)

    return result[mask==np.array(1)]
