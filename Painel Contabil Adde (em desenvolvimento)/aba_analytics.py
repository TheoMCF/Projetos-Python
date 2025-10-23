import streamlit as st
import pandas as pd
from datetime import datetime as dt
from config import cr

def pag_analytics():
    st.title('Analytics')
    graficos, listagem = st.tabs(['Gráficos', 'Listagem de empresas'])

    cr.execute("SELECT `Escriturada até` FROM lev_empresas")
    status_escrituracao = [linha[0] for linha in cr.fetchall()]
    cr.execute("SELECT Código FROM lev_empresas")
    codigos = [linha[0] for linha in cr.fetchall()]
    cr.execute("SELECT CNPJ FROM lev_empresas")
    CNPJs = [linha[0] for linha in cr.fetchall()]

    # Dicionario relacionando as empresas e seus cnpjs
    nomes_e_cnpjs_dict = dict(zip(st.session_state.nomes_empresas, CNPJs))
    # Dicionario relacionando as empresas e seus codigos
    nomes_e_codigos_dict = dict(zip(st.session_state.nomes_empresas, codigos))
    # Dicionario relacionando as empresas e seus status
    nomes_e_status_dict = dict(zip(st.session_state.nomes_empresas, status_escrituracao))
    
    mes_escrituracao = dt.today().month - 1
    ano_escrituracao = dt.today().year
    if mes_escrituracao == 0:
        mes_escrituracao = 12
        ano_escrituracao -= 1
    
    with graficos: 
        # Pega os valores desejados, coloca em uma lista e retira-os da lista original
        sem_ocorrencias = status_escrituracao.count('')
        status_escrituracao[:] = [i for i in status_escrituracao if i != '']

        # Dataframe com as informações de quantidade de valores vazios, nao registrados...
        df_informacoes = pd.DataFrame({
            'Não registrados' : [sem_ocorrencias],
        })

        # Transforma "2025/02/01 00:00:00" em "[2025, 2]"
        for i in status_escrituracao:
            index_valor = status_escrituracao.index(i)
            i = i.split('/')[1:]
            i.reverse()
            status_escrituracao[index_valor] = i

        # Coloca as datas na ordem
        status_escrituracao = sorted(status_escrituracao)

        # Lista dos anos de escrituração
        lista_anos = list(dict.fromkeys(i[0] for i in status_escrituracao))
        for i in lista_anos:
            lista_anos[lista_anos.index(i)] = 'Escriturados em ' + i

        # Cria uma lista para cada coluna para armazenar seus dados
        valores_colunas = {ano: [] for ano in lista_anos}

        # Loop de armazenamento de dados
        for i in status_escrituracao:
            for ano in lista_anos:
                if f"Escriturados em {i[0]}" == ano:
                    valores_colunas[ano].append(f"{i[0]}-{i[1]}")

        # Pega o tamanho máximo da lista para corrigir o erro de arrays
        tamanho_maximo = max(len(values) for values in valores_colunas.values())

        # Preenche cada lista de coluna 
        for ano in valores_colunas:
            while len(valores_colunas[ano]) < tamanho_maximo:
                valores_colunas[ano].append(None)

        # Pega a quantidade de valores de cada coluna e faz um dict relacionando ano e quantidade de valores
        dict_valores_tabela = {}
        for key in valores_colunas:
            lista_valores = []
            for i in valores_colunas[key]:
                if i != None:
                    lista_valores.append(i)
            dict_valores_tabela[f'{key}'] = len(lista_valores)

        # Transforma os valores em listas para evitar o value error de valores escalares
        for i in dict_valores_tabela:
            if type(dict_valores_tabela[i]) != list:
                dict_valores_tabela[i] = [dict_valores_tabela[i]]

        # Transforma o dict em data frame
        df_valores_tabela = pd.DataFrame(dict_valores_tabela)
        if st.checkbox('Levar em conta escriturações vazias'):
            # Junta os 2 dataframes
            df_final = pd.concat([df_informacoes, df_valores_tabela], axis=1)

        else: 
            df_final = df_valores_tabela
            
        # Gráfico de barras com todas as informações
        st.bar_chart(df_final, x_label='Tipos Escrituração', y_label = 'Quantidade', stack=False)
    
    with listagem:
        st.header('Lista de empresas (por categoria)')
        tipo_listagem = st.selectbox('Tipo de listagem', [f'Escritradas até o mês anterior ({"0" + str(mes_escrituracao) if mes_escrituracao < 10 else mes_escrituracao }/{ano_escrituracao})', 'Por mês de escrituração', 'Por ano de escrituração'])
        def listagem_por_ano(ano_listagem):
            dict_mes_empresas = {
                    'Janeiro': [],
                    'Fevereiro': [],
                    'Março': [],
                    'Abril': [],
                    'Maio': [],
                    'Junho': [],
                    'Julho': [],
                    'Agosto': [],
                    'Setembro': [],
                    'Outubro': [],
                    'Novembro': [],
                    'Dezembro': []
                }
            for k, v in nomes_e_status_dict.items():
                if v.split('/')[-1] == ano_listagem:
                    if v != '':
                        if v.split('/')[1] == '01':
                            dict_mes_empresas['Janeiro'].append(k)
                        elif v.split('/')[1] == '02':
                            dict_mes_empresas['Fevereiro'].append(k)
                        elif v.split('/')[1] == '03':
                            dict_mes_empresas['Março'].append(k)
                        elif v.split('/')[1] == '04':
                            dict_mes_empresas['Abril'].append(k)
                        elif v.split('/')[1] == '05':
                            dict_mes_empresas['Maio'].append(k)
                        elif v.split('/')[1] == '06':
                            dict_mes_empresas['Junho'].append(k)
                        elif v.split('/')[1] == '07':
                            dict_mes_empresas['Julho'].append(k)
                        elif v.split('/')[1] == '08':
                            dict_mes_empresas['Agosto'].append(k)
                        elif v.split('/')[1] == '09':
                            dict_mes_empresas['Setembro'].append(k)
                        elif v.split('/')[1] == '10':
                            dict_mes_empresas['Outubro'].append(k)
                        elif v.split('/')[1] == '11':
                            dict_mes_empresas['Novembro'].append(k)    
                        elif v.split('/')[1] == '12':
                            dict_mes_empresas['Dezembro'].append(k)
            
            return dict_mes_empresas
        if tipo_listagem == 'Por mês de escrituração':
            ano_listagem = st.selectbox('Ano de listagem', [i.split(' ')[-1] for i in lista_anos])
        if st.button('Listar'):
            st.divider()
            
            if tipo_listagem == 'Por ano de escrituração':
                for col in df_final.columns:
                    with st.expander(col):
                        if col == 'Não registrados':
                            lista = [chave for chave, valor in nomes_e_status_dict.items() if valor == '']
                        
                        dict_anos_empresas = {}
                        for i in lista_anos:
                            dict_anos_empresas[i.replace('Escriturados em ', '')] = []
                        for k, v in nomes_e_status_dict.items():
                            v = v.split('/')[-1]
                            if v in dict_anos_empresas.keys() and v != '':
                                dict_anos_empresas[v].append(k)
                        colunas_excluidas = ['Não registrados','Sem escrituração','Sem movimento']

                        if col not in colunas_excluidas:
                            lista = dict_anos_empresas[col.replace('Escriturados em ', '')]
                        
                        lista_nomes = []
                        lista_codigos = []
                        lista_cnpj = []
                        
                        for i in lista:
                            lista_nomes.append(i)
                            lista_codigos.append(nomes_e_codigos_dict[i])
                            lista_cnpj.append(nomes_e_cnpjs_dict[i])
                        
                        st.dataframe(pd.DataFrame({
                            'Código' : lista_codigos,
                            'Nome' : lista_nomes,
                            'C.N.P.J.:' : lista_cnpj
                        }), 600, hide_index=True)
            
            elif tipo_listagem == 'Por mês de escrituração':
                dict_mes_empresas = listagem_por_ano(ano_listagem)
                        
                for mes, empresas in dict_mes_empresas.items():
                    with st.expander(mes):
                        dataframe_empresas = pd.DataFrame({
                            'Código' : [nomes_e_codigos_dict[i] for i in empresas],
                            'Nome' : empresas,
                            'C.N.P.J.:' : [nomes_e_cnpjs_dict[i] for i in empresas],
                            'Data' : [nomes_e_status_dict[i] for i in empresas]
                        })
                        if not dataframe_empresas.empty:
                            st.dataframe(dataframe_empresas, 600, hide_index=True)

            elif tipo_listagem == f'Escritradas até o mês anterior ({"0" + str(mes_escrituracao) if mes_escrituracao < 10 else mes_escrituracao }/{ano_escrituracao})':
                dict_ano_escrituracao = listagem_por_ano(ano_escrituracao)
                mes, empresa = list(dict_ano_escrituracao.items())[mes_escrituracao - 1]
                dataframe_empresas = pd.DataFrame({
                    'Código' : [nomes_e_codigos_dict[i] for i in empresa],
                    'Nome' : empresa,
                    'C.N.P.J.:' : [nomes_e_cnpjs_dict[i] for i in empresa],
                    'Data' : [nomes_e_status_dict[i] for i in empresa]
                })
                
                if dataframe_empresas.empty:
                    st.error('***Nenhuma empresa escriturada até o mês anterior.***')
                else:
                    st.dataframe(dataframe_empresas, 600, hide_index=True)
                    st.divider()
