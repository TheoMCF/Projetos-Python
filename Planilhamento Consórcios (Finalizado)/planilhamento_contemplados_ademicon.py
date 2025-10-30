import pdfplumber
import os
import pandas as pd

lista_paginas = []
path_consorcio = 'C:/Users/axoga/OneDrive/Desktop/Python/Projetos-Python/Planilhamento Consórcios (Finalizado)'

for arquivo in os.listdir(f'{path_consorcio}/Entrada'):
    if arquivo.endswith('.pdf'):
        nome_arquivo = arquivo

with pdfplumber.open(f"{path_consorcio}/Entrada/{nome_arquivo}") as pdf:
    for pagina in pdf.pages:
        texto = pagina.extract_text()
        lista_paginas.append(texto.split('\n'))

num_contrato = []
dt_contemplacao = []
tipo_contemplacao = []
credito = []
cred_corrigido = []
dt_pagamento = []
entrega_documento = []
valor_bem_entregue = []
liquido_a_pagar = []

# Checa se a página contém as informações desejadas
for pagina in lista_paginas:
    num_contrato.append(pagina[3].split(' ')[-1])
    for linha in pagina:
        if 'Dt.contemplação' in linha:
            linhas_infos = pagina[pagina.index(linha):pagina.index(linha)+2]
            for index, linha in enumerate(linhas_infos):
                linha = linha.split(' ')
                if index == 0:
                    dt_contemplacao.append(linha[0].split(':')[-1])
                    credito.append(linha[2])
                    if linha[linha.index('Pagamento:') + 1] != 'Valor':
                        dt_pagamento.append(linha[linha.index('Pagamento:') + 1])
                    else:
                        dt_pagamento.append(' ')
                    valor_bem_entregue.append(linha[linha.index('entregue:') + 1])
                if index == 1:
                    tipo_contemplacao.append(' '.join(linha[2:linha.index('Créd.')]))
                    cred_corrigido.append(linha[linha.index('corrig.:') + 1])
                    entrega_documento.append(linha[linha.index('docum.:') + 1])
                    liquido_a_pagar.append(linha[linha.index('pagar:') + 1])

for _ in range(len(num_contrato) - len(dt_contemplacao)):
    dt_contemplacao.append(' ')
    tipo_contemplacao.append(' ')
    credito.append(' ')
    cred_corrigido.append(' ')
    dt_pagamento.append(' ')
    entrega_documento.append(' ')
    valor_bem_entregue.append(' ')
    liquido_a_pagar.append(' ')
    
df_contemplados = pd.DataFrame({
    'Número Contrato': num_contrato,
    'Data Contemplação': dt_contemplacao,
    'Tipo de Contemplação': tipo_contemplacao,
    'Crédito': credito,
    'Crédito Corrigido': cred_corrigido,
    'Data Pagamento': dt_pagamento,
    'Entrega de Documentos': entrega_documento,
    'Valor Bem Entregue': valor_bem_entregue,
    'Líquido a Pagar': liquido_a_pagar
})

df_contemplados.to_excel('C:/Users/axoga/OneDrive/Desktop/Python/Projetos-Python/Planilhamento Consórcios (Finalizado)/Saída/CONSÓRCIOS CONTEMPLADOS.xlsx')