import pdfplumber
import os
import pandas as pd

lista_paginas = []

for arquivo in os.listdir('Entrada'):
    if arquivo.endswith('.pdf'):
        nome_arquivo = arquivo

with pdfplumber.open(f"Entrada/{nome_arquivo}") as pdf:
    for pagina in pdf.pages:
        texto = pagina.extract_text()
        lista_paginas.append(texto.split('\n'))

print()