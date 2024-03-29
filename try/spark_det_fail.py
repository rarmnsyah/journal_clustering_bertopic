import pandas as pd 
import numpy as np
import sparknlp
import time
import pyspark.sql.functions as F

from sparknlp.base import DocumentAssembler, Pipeline
from sparknlp.annotator import (
    LanguageDetectorDL
)

DATASET = pd.read_excel('dataset/dataset_raw_deteksi_bahasa.xlsx')

spark = sparknlp.start()

# Step 1: Transforms raw texts to `document` annotation
document_assembler = (
    DocumentAssembler()
    .setInputCol("text")
    .setOutputCol("document")
)

# Step 2: Determines the language of the text
languageDetector = (
    LanguageDetectorDL.pretrained()
    .setInputCols("document")
    .setOutputCol("language") 
)

nlpPipeline = Pipeline(stages=[document_assembler, languageDetector])

# Create a dataframe from the sample texts in different languages
# data = spark.createDataFrame(np.expand_dims(DATASET.title[:5].values, 1)).toDF("text")
data = spark.createDataFrame([
    ["Spark NLP is an open-source text processing library for advanced natural language processing for the Python, Java and Scala programming languages."],
    ["Spark NLP est une bibliothèque de traitement de texte open source pour le traitement avancé du langage naturel pour les langages de programmation Python, Java et Scala."],
    ["Spark NLP ist eine Open-Source-Textverarbeitungsbibliothek für fortgeschrittene natürliche Sprachverarbeitung für die Programmiersprachen Python, Java und Scala."],
    ["Spark NLP es una biblioteca de procesamiento de texto de código abierto para el procesamiento avanzado de lenguaje natural para los lenguajes de programación Python, Java y Scala."],
    ["Spark NLP é uma biblioteca de processamento de texto de código aberto para processamento avançado de linguagem natural para as linguagens de programação Python, Java e Scala"]
]).toDF("text")

result = nlpPipeline.fit(data).transform(data)

result.select("text", "language.result").show(truncate=100)