import pandas as pd 
import pycld2 as cld2

DATASET = pd.read_excel('dataset/dataset_raw_deteksi_bahasa.xlsx')

pred_data_title = DATASET.title.apply(lambda x: cld2.detect(x, returnVectors=True))
pred_data_abstract = DATASET.abstract.apply(lambda x: cld2.detect(x, returnVectors=True))

DATASET_PRED = DATASET.copy()

def helper(pred):
    output = list(map(lambda x : x[3], pred[-1]))
    return '/'.join(output)

DATASET_PRED['title_pred_pycld2'] = list(map(helper, pred_data_title))
DATASET_PRED['abstract_pred_pycld2'] = list(map(helper, pred_data_abstract))
    
print(DATASET_PRED)

DATASET_PRED.to_excel('dataset/dataset_deteksi_bahasa_pycld2.xlsx')

