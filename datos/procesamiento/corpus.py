from typing import List
from datasets import Dataset
import itertools
import numpy as np


class TaggedText:
    """Clase correspondiente a una fila de corpus
    Para usar al interior de la clase corpus"""
    def __init__(self,tokens:List[str],tags:List[str],id_number:int=None):
        """Inicializador de fila
        
        Argumentos
        
            tokens: list
                lista de strings
                
            tags: list
                lista de strings (nombres de entitdades)
        """
        if not len(tokens)==len(tags):
            raise ValueError("tokens y tags deben tener el mismo largo")
        self.tokens = tokens
        self.tags = tags
        self.id = id_number  # borrar?

    def __len__(self):
        return len(self.tokens)

    def __iter__(self):
        for i, tok in enumerate(self.tokens):
            yield (tok,self.tags[i])


class Corpus:
    """Clase corpus de base"""
    def __init__(self,lista=[],entidades_map:dict=None):
        self._lista = lista.copy()
        self._entidades = entidades_map
    
    def append(self,row:TaggedText):
        self._lista.append(row)

    # propiedades básicas
    def __len__(self):
        # largo del corpus
        return len(self._lista)

    @property
    def entidades(self):
        return self._entidades

    @entidades.setter
    def entidades(self, entidades_map:dict):
        """Propiedad entidades: diccionario de la forma
            { entidad (str) : indice (int) }
            en caso que se quiera colocar manualmente
        """
        self._entidades = entidades_map
    
    def deducir_entidades(self):
        ent_dict = {
            'O' : 0
        }
        ent = list(set(list(itertools.chain.from_iterable(self.ner_tags))))
        idx = 1
        for tag in ent:
            if not tag=='O':
                ent_dict[tag] = idx
                idx += 1
        self._entidades = ent_dict
    
    def __iter__(self):
        for row in self._lista:
            yield row
    
    @property
    def tokens(self) -> List[str]:
        return [row.tokens for row in self._lista]

    @property
    def ner_tags(self) -> List[str]:
        return [row.tags for row in self._lista]
    
    @property
    def ner_tag_ids(self) -> List[int]:
        if self._entidades is None:
            self.deducir_entidades()
        return [[self._entidades[tup[1]] for tup in row] for row in self._lista]

    def to_HF_dataset(self) -> Dataset:
        """Returns a HuggingFace datasets.Dataset object"""
        dataset_dict = {
            'id': list(range(len(self))),
           'tokens': self.tokens,
           'ner_tags': self.ner_tag_ids
        }
        return Dataset.from_dict(dataset_dict)

    def to_numpy(self) -> np.array:
        """Returns a numpy array"""
        # output = np.empty([len(self)*algo,2], dtype= object)
        output = []
        for row in self:
            for tup in row:
                output.append(np.array([tup[0],tup[1]], dtype = object))
            output.append(np.array(['', ''], dtype = object))
        
        return output
    
    def load_conll(self,path,verbose=True):
            """
            Lee un archivo en formato conll (limpiado sin -x-, por ahora) y agrega cada secuencia etiquetada al corpus
            """
            with open(path) as f:
                lines = f.readlines()
                tokens, entities, counter = [], [], 1
                for line in lines:
                    line = line.split()
                    if line:
                        try:
                            token = line[0]
                            entity = line[-1]
                        except ValueError as e:
                            if str(e) != "not enough values to unpack (expected 2, got 1)":
                                raise ValueError(e)
                            else:
                                token = ''
                                entity = line[-1]
                        tokens.append(token)
                        entities.append(entity)
                    else:
                        counter += 1
                        self.append(TaggedText(tokens,entities))
                        tokens, entities = [], []
                self.append(TaggedText(tokens,entities))
            if verbose:
                print("Agregadas {} secuencias de token-entidad al corpus".format(counter))
