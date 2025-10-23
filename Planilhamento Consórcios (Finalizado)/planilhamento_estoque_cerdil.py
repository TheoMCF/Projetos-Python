import streamlit as st
import pdfplumber
import pandas as pd
import io
import re

colunas = ['Nota', 'Fornecedor','Operação', 'Data Emissão', 'Data Entrada', 
           'Total Nota', 'Codigo Item', 'Descrição Item', 'Quantidade', 'Unidade', 'Valor Item']

def pdf_para_df(bytes_pdf):
    df_informacoes = pd.DataFrame(columns=colunas)

    with pdfplumber.open(io.BytesIO(bytes_pdf)) as pdf_file:
        for page in pdf_file.pages:
            texto = page.extract_text()
            notas = [[linha.split(" ") for linha in nota.split("\n")] 
                     for nota in texto.split("Nota fiscal: ")[1:]]
            
            for nota in notas:
                num_nota = []
                fornecedor = []
                operacao = []
                data_emissao = []
                data_entrada = []
                total_nota = []
                codigos_produtos = []
                descricao_produtos = []
                quantidades = []
                unidades = []
                valores_produtos = []

                tem_produtos = False

                for index_linha, linha in enumerate(nota):
                    if index_linha == 0:
                        num_nota.append(linha[0])
                        data_emissao.append(linha[linha.index('Emissao:') + 1] if 'Emissao:' in linha else '')
                    
                    elif index_linha == 1:
                        fornecedor.append(" ".join(linha[linha.index('Fornecedor:')+1:linha.index('Entrada:')]) if 'Fornecedor:' in linha and 'Entrada:' in linha else '')
                        data_entrada.append(linha[linha.index('Entrada:') + 1] if 'Entrada:' in linha else '')
                        total_nota.append(linha[linha.index('nota:') + 1] if 'nota:' in linha else '')
                    
                    elif index_linha == 4 and 'Operação:' in linha and 'O' in linha:
                        operacao.append(" ".join(linha[linha.index('Operação:')+1:linha.index('O')]))

                    if linha[0] == 'Se':
                        tem_produtos = True
                        inicio_produtos = index_linha + 1
                        break

                if tem_produtos:
                    linhas_produtos = []
                    for linha in nota[inicio_produtos:]:
                        if linha and re.match(r"^\d+$", str(linha[0])) and len(linha) >= 6:
                            linhas_produtos.append(linha)
                    
                    for produto in linhas_produtos:
                        codigo = re.findall(r'\d+', produto[1])[0]                       
                        partes_texto = [re.sub(r'^\d+', '', produto[1])]

                        for parte in produto[2:]:
                            if not re.search(r'\d', parte):
                                partes_texto.append(parte)
                                
                        descricao = ' '.join(partes_texto).strip()

                        codigo = re.findall(r'\d+', produto[1])[0]

                        partes_texto = [re.sub(r'^\d+', '', produto[1])]
                        for parte in produto[2:]:
                            if not re.search(r'\d', parte):
                                partes_texto.append(parte)
                        descricao = ' '.join(partes_texto).strip()

                        qtd_un = next((x for x in produto if re.search(r'\d+[.,]\d+[A-Za-z]+', x)), None)
                        if qtd_un:
                            qtd = re.findall(r'[\d,.]+', qtd_un)[0]
                            un = re.findall(r'[A-Za-z]+', qtd_un)[0]
                        else:
                            qtd = un = ''

                        valor_tokens = [x for x in produto if re.fullmatch(r'\d+[,\.]\d+', x)]
                        valor = valor_tokens[-1] if valor_tokens else '0,00'

                        
                        codigos_produtos.append(codigo)
                        descricao_produtos.append(descricao)
                        quantidades.append(qtd)
                        unidades.append(un)
                        valores_produtos.append(valor)

                        
                if codigos_produtos:  
                    df_temp = pd.DataFrame({
                        'Nota': num_nota * len(codigos_produtos),
                        'Fornecedor': fornecedor * len(codigos_produtos),
                        'Operação': operacao * len(codigos_produtos),
                        'Data Emissão': data_emissao * len(codigos_produtos),
                        'Data Entrada': data_entrada * len(codigos_produtos),
                        'Total Nota': total_nota * len(codigos_produtos),
                        'Codigo Item': codigos_produtos,
                        'Descrição Item': descricao_produtos,
                        'Quantidade': quantidades,
                        'Unidade': unidades,
                        'Valor Item': valores_produtos
                    })
                    df_informacoes = pd.concat([df_informacoes, df_temp], ignore_index=True)
    
    return df_informacoes


col1, col2 = st.columns(2)
with col1:
    pdfs = st.file_uploader("Faça o upload dos PDFs", type=["pdf"], accept_multiple_files=True)
with col2:
    empresa = st.selectbox('Selecione a empresa', [' ', 'Corumbá', 'RM Cassems', 'RM Diagnóstico', 'RM Gattas', 'Sede', 'Shopping', 'Sim CG', 'BEST', 'Cassems Naviraí'])

st.divider()

if pdfs and empresa != ' ':
    
        st.write('Clique aqui para gerar o Excel')
    
        if st.button('Gerar'):
            df_final = pd.DataFrame(columns=colunas)
            for pdf in pdfs:
                df = pdf_para_df(pdf.getvalue())
                df_final = pd.concat([df_final, df], ignore_index=True)
            bytes_df_final = io.BytesIO()
            with pd.ExcelWriter(bytes_df_final, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, index=False, sheet_name=f'Planilhamento {empresa}')

            st.download_button(
            label="Baixar Excel",
            data=bytes_df_final,
            file_name=f"Planilhamento {empresa}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
