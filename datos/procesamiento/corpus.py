from typing import List
from datasets import Dataset
import itertools


class TaggedText:
    """Clase correspondiente a una fila de corpus
    Para usar al interior de la clase corpus"""
    def __init__(self,tokens:List[str],tags:List[str],id_number:int=None):
        """Inicializador de fila
        
        Argumentos
        
            tokens: list
                lista de strings
                
            tags: list
                lista de ints
        """
        if not len(tokens)==len(tags):
            raise ValueError("tokens y tags deben tener el mismo largo")
        self.tokens = tokens
        self.tags = tags
        self.id = id_number  # borrar?

    def __len__(self):
        return len(self.tokens)

    def __iter__(self):
        for i, tok in self.tokens:
            yield (tok,self.tags[i])


class Corpus:
    """Clase corpus de base"""
    def __init__(self,lista:List(TaggedText)=[],entidades_map:dict=None):
        self._lista = lista
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
        return [column.tags for column in self._lista]


    def to_HG_dataset(self) -> Dataset:
        """Returns a HuggingFace datasets.Dataset object"""
        if self._entidades is None:
            self.deducir_entidades()
        dataset_dict = {
            'id': list(range(len(self))),
           'tokens': self.tokens,
           'ner_tags': self.ner_tags
        }
        return Dataset.from_dict(dataset_dict)
