from typing import List
from datasets import Dataset


class TaggedText:
    """Clase correspondiente a una columna de corpus
    Para usar al interior de la clase corpus"""
    def __init__(self,tokens:List[str],tags:List[int],id_number:int=None):
        """Inicializador de columna
        
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

    # propiedades básicas
    def __len__(self):
        # largo del corpus
        return len(self._lista)

    @property
    def entidades(self):
        return self._entidades

    @entidades.setter
    def entitdades(self, entidades_map:dict):
        """Propiedad entidades: diccionario de la forma
            { indice (int) : entidad (str) }
        """
        self._entidades = entidades_map
    
    def __iter__(self):
        for column in self._lista:
            yield column
    
    @property
    def tokens(self) -> List[str]:
        return [column.tokens for column in self._lista]
    
    @property
    def ner_tags(self) -> List[int]:
        return [column.tags for column in self._lista]


    def to_HG_dataset(self) -> Dataset:
        """Returns a HuggingFace datasets.Dataset object"""
        dataset_dict = {
            'id': list(range(len(self))),
           'tokens': self.tokens,
           'ner_tags': self.ner_tags
        }
        return Dataset.from_dict(dataset_dict)
