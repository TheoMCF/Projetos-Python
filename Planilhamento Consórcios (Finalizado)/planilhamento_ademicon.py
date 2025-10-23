import pdfplumber
import os
import pandas as pd
import sounddevice as sd
import soundfile as sf

def play_sound(filename):
    data, samplerate = sf.read(filename)
    sd.play(data, samplerate)
    sd.wait()

lista_paginas = []
conta_corrente = []
pendencia = []
cabecalho_conta_corrente = []
cabecalho_pendencia = []

for arquivo in os.listdir('Entrada'):
    if arquivo.endswith('.pdf'):
        nome_arquivo = arquivo

with pdfplumber.open(f"Entrada/{nome_arquivo}") as pdf:
    for pagina in pdf.pages:
        texto = pagina.extract_text()
        lista_paginas.append(texto.split('\n'))

# Pega as informações de cada página do PDF e separa em uma lista
for i, pagina in enumerate(lista_paginas):
    # Pega o número da página
    numero_pagina = int(pagina[0].split(' ')[-1])
    # Verifica se a página é ímpar, que é onde estão as informações das tabelas
    
    if numero_pagina %2 != 0:
        # Verifica o tipo de página
        try:
            comeco_lista = pagina.index('Conta Corrente')
            fim_lista = pagina.index('Consórcio v 004.026 - CNP')
            tipo_pagina = 'Conta Corrente'
        
        except:
            comeco_lista = pagina.index('Pendência') + 1
            for linha in pagina:
                if 'TOTAIS' in linha:
                    fim_lista = pagina.index(linha)
                    break
            tipo_pagina = 'Pendencia'

        lista_paginas[i] = pagina[comeco_lista:fim_lista]
        
        if tipo_pagina == 'Conta Corrente':

            # Se a lista estiver vazia, pega o cabeçalho, pois será a primeira página de conta corrente
            if not cabecalho_conta_corrente:   
                cabecalho_temp = lista_paginas[i][1].split(' ')
                cabecalho_conta_corrente.extend(cabecalho_temp[:6])
                cabecalho_temp = cabecalho_temp[6:]
                
                for i in range(2):
                    cabecalho_conta_corrente.append(cabecalho_temp[0] + cabecalho_temp[1])
                    cabecalho_temp = cabecalho_temp[2:]
                
                cabecalho_conta_corrente.append(cabecalho_temp[0] + ' ' + cabecalho_temp[1])
                cabecalho_temp = cabecalho_temp[2:]
                cabecalho_conta_corrente.extend(cabecalho_temp)
            
            if numero_pagina == 1:
                # Tira o cabeçalho da tabela
                conta_corrente.extend(lista_paginas[i - 1][2:])
            else:
                conta_corrente.extend(lista_paginas[i][2:])

        else:
            # Se a lista estiver vazia, pega o cabeçalho, pois será a primeira página de pendência
            if not cabecalho_pendencia:
                cabecalho_temp = lista_paginas[i][0].split(' ')
                cabecalho_pendencia.extend(cabecalho_temp[:5])
                cabecalho_temp = cabecalho_temp[5:]
                
                for _ in range(2):
                    cabecalho_pendencia.append(cabecalho_temp[0] + cabecalho_temp[1])
                    cabecalho_temp = cabecalho_temp[2:]
                
                cabecalho_pendencia.extend(cabecalho_temp[:2])
                cabecalho_temp = cabecalho_temp[2:]
                
                for _ in range(2):
                    cabecalho_pendencia.append(cabecalho_temp[0] + cabecalho_temp[1])
                    cabecalho_temp = cabecalho_temp[2:]

            pendencia.extend(lista_paginas[i][1:])
    
    else:
        try:  
            for linha in pagina:
                if 'Grupo:' in linha:
                    index1 = pagina.index(linha) + 1
                index2 = pagina.index('Pendência')
            conta_corrente.extend(lista_paginas[i][index1:index2])
            
            for linha in pagina:
                if 'TOTAIS:' in linha:
                    index3 = pagina.index(linha)
            pendencia.extend(lista_paginas[i][index2 + 2:index3])

            if not cabecalho_pendencia:
                cabecalho_temp = lista_paginas[i][index2 + 1].split(' ')
                cabecalho_pendencia.extend(cabecalho_temp[:5])
                cabecalho_temp = cabecalho_temp[5:]
                
                for _ in range(2):
                    cabecalho_pendencia.append(cabecalho_temp[0] + cabecalho_temp[1])
                    cabecalho_temp = cabecalho_temp[2:]
                
                cabecalho_pendencia.extend(cabecalho_temp[:2])
                cabecalho_temp = cabecalho_temp[2:]
                
                for _ in range(2):
                    cabecalho_pendencia.append(cabecalho_temp[0] + cabecalho_temp[1])
                    cabecalho_temp = cabecalho_temp[2:]

        except:
            pass
    
cabecalho_conta_corrente.insert(7, '%F.Comum')
cabecalho_conta_corrente.insert(9, '%F.Reserva')
cabecalho_conta_corrente.insert(11, '%Taxa Adm.')
cabecalho_conta_corrente.insert(13, '%Seguros')
cabecalho_conta_corrente.insert(15, '%Multa')
cabecalho_conta_corrente.insert(17, '%Juros')
cabecalho_conta_corrente.insert(19, '%Total')

# Listas Conta Corrente
lancamento = []
cota = []
aviso = []
cod = []
vencimento = []
pagamento = []
f_comum = []
perc_f_comum = []
f_reserva = []
perc_f_reserva = []
taxa_adm = []
perc_taxa_adm = []
seguros = []
perc_seguros = []
multa = []
perc_multa = []
juros = []
perc_juros = []
total = []
perc_total = []

# Listas Pendência
ass = []
aviso_pendencia = []
historico = []
vencto = []
bem = []
vl_credito = []
vl_parcela = []
multa_pendencia = []
juros_pendencia = []
vl_seguro = []
perc_normal = []

for linha in conta_corrente:
    # Verifica se a linha tem as informações normais ou dos percentuais
    if conta_corrente.index(linha) %2 == 0:
        linha = linha.split(' ')
        lancamento.append(linha[0])
        cota.append(linha[1] + " "+ linha[2])
        aviso.append(linha[3])
        cod.append(linha[4])
        vencimento.append(linha[5])
        pagamento.append(linha[6])
        f_comum.append(linha[7])
        f_reserva.append(linha[8])
        taxa_adm.append(linha[9])
        seguros.append(linha[10])
        multa.append(linha[11]) 
        juros.append(linha[12])
        total.append(linha[13])

    else:
        linha = linha.split(' ')
        perc_f_comum.append(linha[1])
        perc_f_reserva.append(linha[2])
        perc_taxa_adm.append(linha[3])
        perc_seguros.append(linha[4])
        perc_multa.append(linha[5])
        perc_juros.append(linha[6])
        perc_total.append(linha[7])

for linha in pendencia:
    linha = linha.split(' ')
    ass.append(linha[0][:3])
    linha[0] = linha[0][3:]
    aviso_pendencia.append(linha[0])
    historico.append(linha[1] + linha[2])
    vencto.append(linha[3])
    bem.append(linha[4])
    vl_credito.append(linha[5])
    vl_parcela.append(linha[6])
    multa_pendencia.append(linha[7])
    juros_pendencia.append(linha[8])
    vl_seguro.append(linha[9])
    perc_normal.append(linha[10])

dados_df_conta_corrente = {
    cabecalho_conta_corrente[0] : lancamento,
    cabecalho_conta_corrente[1] : cota,
    cabecalho_conta_corrente[2] : aviso,
    cabecalho_conta_corrente[3] : cod,
    cabecalho_conta_corrente[4] : vencimento,
    cabecalho_conta_corrente[5] : pagamento,
    cabecalho_conta_corrente[6] : f_comum,
    cabecalho_conta_corrente[7] : perc_f_comum,
    cabecalho_conta_corrente[8] : f_reserva,
    cabecalho_conta_corrente[9] : perc_f_reserva,
    cabecalho_conta_corrente[10] : taxa_adm,
    cabecalho_conta_corrente[11] : perc_taxa_adm,
    cabecalho_conta_corrente[12] : seguros,
    cabecalho_conta_corrente[13] : perc_seguros,
    cabecalho_conta_corrente[14] : multa,
    cabecalho_conta_corrente[15] : perc_multa,
    cabecalho_conta_corrente[16] : juros,
    cabecalho_conta_corrente[17] : perc_juros,
    cabecalho_conta_corrente[18] : total,
    cabecalho_conta_corrente[19] : perc_total
}

dados_df_pendencia = {
    cabecalho_pendencia[0]: ass,
    cabecalho_pendencia[1]: aviso_pendencia,
    cabecalho_pendencia[2]: historico,
    cabecalho_pendencia[3]: vencto,
    cabecalho_pendencia[4]: bem,
    cabecalho_pendencia[5]: vl_credito,
    cabecalho_pendencia[6]: vl_parcela,
    cabecalho_pendencia[7]: multa_pendencia,
    cabecalho_pendencia[8]: juros_pendencia,
    cabecalho_pendencia[9]: vl_seguro,
    cabecalho_pendencia[10]: perc_normal
}

df_conta_corrente = pd.DataFrame(dados_df_conta_corrente)
df_pendencia = pd.DataFrame(dados_df_pendencia)

df_conta_corrente.to_excel('Saída/CONSORCIOS CONTA CORRENTE.xlsx')
df_pendencia.to_excel('Saída/CONSÓRCIOS PENDÊNCIA.xlsx')
play_sound('Pokémon Healed.flac')