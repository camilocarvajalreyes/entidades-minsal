"""Funciones y métodos de generacion de texto desde dataset Minsal

Correr este código replica el código de Martin (Etiquetado_Dataset_Minsal.ipynb)"""
import pandas as pd
import numpy as np

from corpus import Corpus, TaggedText


def codigo_hfl(HLF):
    """Agregar descripción
    
    Argumentos
    ---
        HLF: pandas dataframe
        
    Retorna
    ---
        HLF_df: pandas dataframe
        describir
    """
    HLF_df = pd.DataFrame()

    HLF2 = HLF['CODIGO_HLF'].str.split(', ')
    HLF_list = []
    for i in range(len(HLF2)):
        HLF_list = HLF_list + HLF2[i] 
    try:
        HLF_list.remove('')
    except Exception:
        pass
    HLF_name = []
    for elem in HLF_list:
        HLF_name = HLF_name + HLF[HLF['CODIGO_HLF'].str.contains(elem)]['PRINCIPIO_ACTIVO'].values.tolist()
    
    HLF_df['CODIGO_MEDICAMENTO'] = HLF_list
    HLF_df['PRINCIPIO_ACTIVO'] = HLF_name
    return HLF_df


def split_rule(x):
    output = np.array([],dtype=object)
    for i in  range(len(x)):
        output = np.append(output,x[i].split())
    return output


def process_column(row:pd.Series,PA:pd.Series,FF:pd.Series) -> TaggedText:
    """
    Procesamiento de columnas propuesto por Martín para generar etiquetas
    
    Argumentos
    
        row: pandas Series
            fila de dataframe con prescripción y resumen
            
        PA: pandas Series
            fila de dataframe con principio activo

        FF: pandas Series
            fila de dataframe con forma fármaco
    
    Retorna

        output: TaggedText
            objeto de clase TaggedText con tokens y etiquetas NER
    
    """
    output_tokens, output_tags = [], []
    j = 0
    while j < len(row):
        if row[j] == 'cada' and row[j+1].isnumeric() :
            try:
                output_tokens.extend(row[j:j+3])
                output_tags.extend(['B-PERIODICITY','I-PERIODICITY','I-PERIODICITY'])
                j += 3
            except IndexError:
                output_tokens.append(row[j])
                output_tags.append('O')
                j += 1
        elif row[j] == 'durante' and row[j+1].isnumeric() :
            try:
                output_tokens.extend(row[j:j+3])
                output_tags.extend(['B-DURATION','I-DURATION','I-DURATION'])
                j += 3
            except IndexError:
                output_tokens.append(row[j])
                output_tags.append('O')
                j += 1
        elif row[j].lower() in PA or row[j].upper() in PA :
            output_tokens.append(row[j])
            output_tags.append('ACTVPRNCP')
            j+=1
        elif row[j].lower() in FF or row[j].upper() in FF :
            output_tokens.append(row[j])
            output_tags.append('ADMIN')
            j+=1
        else:
            output_tokens.append(row[j])
            output_tags.append('O')
            j += 1
    
    for i, token in enumerate(output_tokens):
        try:
            if token in ['+','CON','SOLUCIÓN']:
                output_tags[i+1] = output_tags[i]
            if output_tags[i] == 'ADMIN' and output_tags[i-1] == 'B-ADMIN':
                output_tags[i] = 'I-ADMIN'
            elif output_tags[i] == 'ADMIN':
                output_tags[i] = 'B-ADMIN'
            elif output_tags[i] == 'ACTVPRNCP' and output_tags[i-1] == 'B-ACTVPRNCP':
                output_tags[i] = 'I-ACTVPRNCP'
            elif output_tags[i] == 'ACTVPRNCP':
                output_tags[i] = 'B-ACTVPRNCP'
        except IndexError:
            pass

    """try:
        tt = TaggedText(output_tokens,output_tags)
    except ValueError:
        print(output_tokens)
        print(output_tags)"""
    
    return TaggedText(output_tokens,output_tags)

if __name__=="__main__":
    main_db = pd.read_csv('datos/DATA_HLF_MDS_2.csv',sep=',')

    code_db = pd.read_excel('datos/PRINCIPIOS_ACTIVOS_MDS.xlsx')
    HLF = code_db.loc[:,['PRINCIPIO_ACTIVO','CODIGO_HLF']]
    HLF_df = codigo_hfl(HLF)

    df = main_db.join(HLF_df.set_index('CODIGO_MEDICAMENTO'), on='CODIGO_MEDICAMENTO')

    #PARA DETECTAR LA POSICION DE ENTIDADES TIPO PRINCIPIO ACTIVO, FORMA FARMACO SE COMPARARAN LOS ELEMENTOS DEL CORPUS CON LAS LISTAS CORRESPONDIENTES.
    PA = np.unique(split_rule(df['PRINCIPIO_ACTIVO'].dropna().unique()))
    FF = np.unique(split_rule(df['FORMA_FARMA'].dropna().unique()))

    rows = (df['PRES_DENOMINACION'] + ' ' + df['RESUMEN']).dropna().unique()

    corpus = Corpus()

    for i in range(len(rows)):
        row = rows[i].split()
        tagged_seq = process_column(row,PA,FF)

        corpus.append(tagged_seq)

        if i > 100:
            # solo testeando :)
            break

    txt = corpus.to_numpy()
    np.savetxt('datos/minicorpus_recetas_V0.2.txt',txt,fmt="%s")
    print("Corpus recetas exitosamente guardado en corpus_recetas.txt")
