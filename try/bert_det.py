import pandas as pd

# Use a pipeline as a high-level helper
from transformers import pipeline


pipe = pipeline("text-classification", model="jb2k/bert-base-multilingual-cased-language-detection")

label = ['Arabic', 'Basque', 'Breton', 'Catalan', 'Chinese_China', 'Chinese_Hongkong', 'Chinese_Taiwan', 'Chuvash', 'Czech', 'Dhivehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'French', 'Frisian', 'Georgian', 'German', 'Greek', 'Hakha_Chin', 'Indonesian', 'Interlingua', 'Italian', 'Japanese', 'Kabyle', 'Kinyarwanda', 'Kyrgyz', 'Latvian', 'Maltese', 'Mongolian', 'Persian', 'Polish', 'Portuguese', 'Romanian', 'Romansh_Sursilvan', 'Russian', 'Sakha', 'Slovenian', 'Spanish', 'Swedish', 'Tamil', 'Tatar', 'Turkish', 'Ukranian', 'Welsh']


# def helper2(text):
#     return [text]

dataset = pd.read_csv('../dataset/sample_text_2k.csv')
abstract = list(dataset.desc)
abstract_pred = pipe(abstract, truncation=True)

for i in range(len(dataset)):
    print(label[int(abstract_pred[i]['label'].split('_')[-1])])

# print(title_pred, abstract_pred)
