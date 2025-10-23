from pypdf import PdfReader
import os
import sounddevice as sd
import soundfile as sf
import re
import pandas as pd 
from datetime import datetime as dt
import shutil

if not os.path.exists(r"Consorcios"):
    os.mkdir(r"Consorcios")
if not os.path.exists(r'Consorcios_Erro'):
    os.mkdir(r'Consorcios_Erro')

pasta_pdfs = r"Consorcios"
lista_pdfs = os.listdir(pasta_pdfs)

def play_sound(filename):
    data, samplerate = sf.read(filename)
    sd.play(data, samplerate)
    sd.wait()

def contrato_para_exel(index_contrato):
    parcelas = []
    transacao = []
    contabilizacao = []
    pagamento = []
    valor_a_pagar = []
    valor_pago = []
    percentual_fc = []
    valor_fc = []
    percentual_fr = []
    valor_fr = []
    percentual_tx = []
    valor_tx = []
    percentual_seguro = []
    valor_seguro = []
    percentual_multa_juros = []
    valor_multa_juros = []
    percentual_dif = []
    valor_dif = []
    grupo = []
    cota = []
    contrato = []

    # pdf que esta sendo trabalhado
    reader = PdfReader(os.path.join(pasta_pdfs, lista_pdfs[index_contrato]))
    
    # junta os textos das paginas em um so
    texto_paginas = "".join(page.extract_text() for page in reader.pages)
    # pega o cabecalho
    match = re.search(r"Conta Corrente\s*\n(.*?)\n", texto_paginas, re.DOTALL)
    if match:
        cabecalho = match.group(1).strip() 
        cabecalho = cabecalho.split(' ')

        index_valor = cabecalho.index('Valor')
        index_pagar = cabecalho.index('Pagar')
        index_pago = cabecalho.index('Pago')

        valor_a_pagar_cabeçalho = " ".join(cabecalho[index_valor:index_pagar+1])
        valor_pago_cabeçalho = " ".join(cabecalho[index_valor+3:index_pago+1])

        cabecalho = cabecalho[:index_valor] + [valor_a_pagar_cabeçalho] + [valor_pago_cabeçalho] + cabecalho[index_pago+1:]
        for i in cabecalho:
            if "%" in i:
                cabecalho.insert(cabecalho.index(i) + 1, f"Valor {i.replace('%','')}")
    
    match = re.search('Dados não disponíveis por solicitação do cliente', texto_paginas)
    if match:
        cabecalho = cabecalho[:2] + [cabecalho[2].removesuffix('Pagamento'), cabecalho[2].removeprefix('Contabilização')] + cabecalho[3:]
        print(cabecalho)
    # pega cada valor na tabela e coloca em uma string
    match = re.search(r"%Dif\s*(.*?)\s*\(\*\)", texto_paginas, re.DOTALL)
    if match:
        tabela_total = match.group(1).split('\n')

    # preenche a tabela
    for linha in tabela_total:
        linha = linha.split(' ')
        parcelas.append(linha[0])
        linha.pop(0)
        for valor in linha:
            pos_valor = linha.index(valor)
            check_data = re.search(r'\d{2}/\d{2}/\d{4}', valor)
            if check_data:
                data = check_data.group(0)
                if valor == data:
                    pass
                else:
                    linha[pos_valor] = valor.replace(data, "").strip() 
                    linha.insert(linha.index(valor.replace(data, '')) + 1, data)
            try:
                dt.strptime(valor, "%d/%m/%Y").date()
                index_data = pos_valor
                break
            except:
                pass
        transacao.append(re.sub(r"(\d{2}/\d{2}/\d{4})", "", " ".join(linha[0:index_data])))
        del linha[0:index_data]
        
        # retira as strings
        linha = [valor.replace('Parcela', '') for valor in linha if any(c.isdigit() or c == ',' or c == '-' for c in valor)]
        contabilizacao.append(linha[0])
        pagamento.append(linha[1])
        valor_a_pagar.append(linha[2])
        valor_pago.append(linha[3])
        percentual_fc.append(linha[4])
        percentual_fr.append(linha[5])
        percentual_tx.append(linha[6])
        percentual_seguro.append(linha[7])
        percentual_multa_juros.append(linha[8])
        percentual_dif.append(linha[9])

    # os totais das porcentagens
    for porcentagem in percentual_fc:
        valor_fc.append(str(float(porcentagem.replace(',', '.')) * float(valor_pago[percentual_fc.index(porcentagem)].replace(',', '.')) / 100).replace('.', ','))
    for porcentagem in percentual_fr:
        valor_fr.append(str(float(porcentagem.replace(',', '.')) * float(valor_pago[percentual_fr.index(porcentagem)].replace(',', '.')) / 100).replace('.', ','))
    for porcentagem in percentual_tx:
        valor_tx.append(str(float(porcentagem.replace(',', '.')) * float(valor_pago[percentual_tx.index(porcentagem)].replace(',', '.')) / 100).replace('.', ','))
    for porcentagem in percentual_seguro:
        valor_seguro.append(str(float(porcentagem.replace(',', '.')) * float(valor_pago[percentual_seguro.index(porcentagem)].replace(',', '.'))).replace('.', ','))
    for porcentagem in percentual_multa_juros:
        valor_multa_juros.append(str(float(porcentagem.replace(',', '.')) * float(valor_pago[percentual_multa_juros.index(porcentagem)].replace(',', '.'))).replace('.', ','))
    for porcentagem in percentual_dif:
        valor_dif.append(str(float(porcentagem.replace(',', '.')) * float(valor_pago[percentual_dif.index(porcentagem)].replace(',', '.'))).replace('.',','))

    # coleta o grupo, cota e contrato
    match = re.search(r"Grupo:\s*(\d+).*?Cota:\s*([\d-]+).*?Contrato:\s*(\d+)", texto_paginas)
    if match:
        for i in range(len(parcelas)):
            grupo.append(match.group(1))
            cota.append(match.group(2))
            contrato.append(match.group(3))

    dados = {
        "Grupo" : grupo,
        "Cota" : cota,
        "Contrato" : contrato,
        cabecalho[0] : parcelas,
        cabecalho[1] : transacao,
        cabecalho[2] : contabilizacao,
        cabecalho[3] : pagamento,
        cabecalho[4] : valor_a_pagar,
        cabecalho[5] : valor_pago,
        cabecalho[6] : percentual_fc,
        cabecalho[7] : valor_fc,
        cabecalho[8] : percentual_fr,
        cabecalho[9] : valor_fr,
        cabecalho[10] : percentual_tx,
        cabecalho[11] : valor_tx,
        cabecalho[12] : percentual_seguro,
        cabecalho[13] : valor_seguro,
        cabecalho[14] : percentual_multa_juros,
        cabecalho[15] : valor_multa_juros,
        cabecalho[16] : percentual_dif,
        cabecalho[17] : valor_dif
        }
    return pd.DataFrame(dados)

df_final = pd.DataFrame()
for i in range(len(lista_pdfs)):
    try:
        df_temp = contrato_para_exel(i)
        df_final = pd.concat([df_final, df_temp], ignore_index=True)
    except:
        shutil.move(fr'Consorcios\{lista_pdfs[i]}', r'Consorcios_Erro' )

df_final.to_excel(r'PLANILHAMENTO CONSORCIOS.xlsx')
play_sound('Pokémon Healed.flac')   