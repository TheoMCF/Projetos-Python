import streamlit as st
import pandas as pd
import time as t
from config import cn, cr
import datetime

def pag_tabela(): # Visualizar tabela
    st.title("Tabela de Empresas")
    try:
        cr.execute("ALTER TABLE lev_empresas RENAME COLUMN saída TO Saída")
        cr.execute("ALTER TABLE lev_empresas RENAME COLUMN `Inicou na Adde` TO `Iniciou na Adde`")
        cr.execute("ALTER TABLE lev_empresas RENAME COLUMN `Ultimo a Escriturar` TO `Último a Escriturar`")
        cn.commit()
    except:
        pass
      
    # Obtém as responsabilidades do usuário
    responsabilidades = st.session_state.responsabilidades
    
    # Limpa e formata os nomes das empresas
    if responsabilidades:
        empresas_filtro = [empresa.strip().upper() for empresa in responsabilidades.split(",")]
    else:
        empresas_filtro = []

    # Query filtrada por empresas
    if empresas_filtro:
        # Cria string formatada para SQL
        empresas_str = ",".join([f"'{empresa}'" for empresa in empresas_filtro])
        
        # Query com filtro
        df_query = pd.read_sql_query(
            f"SELECT * FROM lev_empresas WHERE UPPER(Empresa) IN ({empresas_str})", 
            cn
        )
    else:
        # Se for admin, mostra tudo
        if st.session_state.permissao == "Admin":
            df_query = pd.read_sql_query("SELECT * FROM lev_empresas", cn)
        else:
            df_query = pd.DataFrame()  # DataFrame vazio

    # Formatação de datas
    colunas_formatar_data = ['Início das atividades', 'Cliente desde', 'Saída', 'Escriturada até']
    for coluna in colunas_formatar_data:
        cr.execute(f"SELECT `{coluna}` FROM lev_empresas")
        valores = [row[0] for row in cr.fetchall()]
        
        for valor_antigo in valores:
            if valor_antigo and '-' in str(valor_antigo):   
                novo_valor = valor_antigo.split(' ')[0].split('-')
                novo_valor.reverse()
                novo_valor = '/'.join(novo_valor)
                cr.execute(f"UPDATE lev_empresas SET `{coluna}` = ? WHERE `{coluna}` = ?", (novo_valor, valor_antigo))
                cn.commit()

    # Converte colunas para datetime
    df_query['Início das atividades'] = pd.to_datetime(df_query['Início das atividades'], dayfirst=True, errors='coerce').dt.date
    df_query['Cliente desde'] = pd.to_datetime(df_query['Cliente desde'], dayfirst=True, errors='coerce').dt.date
    df_query['Escriturada até'] = pd.to_datetime(df_query['Escriturada até'], dayfirst=True, errors='coerce').dt.date
    df_query['Saída'] = pd.to_datetime(df_query['Saída'], dayfirst=True, errors='coerce').dt.date

    # Exibe a tabela ou mensagem
    if df_query.empty:
        st.warning("Nenhuma empresa atribuída ao seu usuário.")
    else:
        df_editavel = st.data_editor(df_query, height=800, column_config={
            'Situação': st.column_config.SelectboxColumn('Situação', options=['Ativa', 'Inativa']),
            'Início das atividades': st.column_config.DateColumn("Início das atividades", format="DD/MM/YYYY"),
            'Cliente desde': st.column_config.DateColumn("Cliente desde", format="DD/MM/YYYY"),
            'Saída': st.column_config.DateColumn("Saída", format="DD/MM/YYYY"),
            'Escriturada até': st.column_config.DateColumn('Escriturada até', format="DD/MM/YYYY"),
            'Iniciou na Adde': st.column_config.SelectboxColumn('Iniciou na Adde', options=['SIM', 'NÃO']),
            'Regimento tributário': st.column_config.SelectboxColumn('Regimento tributário', options=['Simples Nacional', 'Lucro Presumido', 'Lucro Real'])
        })
    
    # cr.execute("SELECT * FROM lev_empresas")
    # linhas = cr.fetchall()
    # lista_linhas_db = [list(linha) for linha in linhas]

    def formatar_linhas_tupla(tupla):
        # # Transforma a tupla em lista
        tupla_df = list(tupla)
        # # Pega o codigo da tupla
        # index_tupla = tupla_df[0] - 1
        # print(index_tupla)
        # # Verifica se a tupla corresponde à linha da database
        # linha_correspondente_db = lista_linhas_db[index_tupla]
        # # Se a tupla não corresponder à linha da database, atualiza o nome do usuário
        # if tupla_df != linha_correspondente_db:
        #     tupla_df[11] = st.session_state.nome
        
        # Formata as datas   
        for i in tupla_df:
            if isinstance(i, datetime.date):
                data_formatada = i.strftime('%d/%m/%Y')
                tupla_df[tupla_df.index(i)] = data_formatada
            elif pd.isna(i):
                tupla_df[tupla_df.index(i)] = ""
                
        # Retorna a tupla formatada
        return tuple(tupla_df)

    c1, c2 = st.columns(2)
    
    with c1:
        if st.button('Atualizar dados'):
            st.rerun()

    with c2:
        confirmar = st.button('Confirmar alterações')
    
    
    if confirmar:
                
        cr.execute("DELETE FROM lev_empresas")  
        cn.commit()
        colunas_db = ", ".join(f'"{col}"' for col in df_editavel.columns)
        placeholders = ", ".join("?" for _ in df_editavel.columns)

        for _, row in df_editavel.iterrows():
            # valores = tuple(values)
            valores = formatar_linhas_tupla(tuple("" if pd.isna(v) else v for v in row))
            # st.write(valores)
            cr.execute(f'INSERT INTO lev_empresas ({colunas_db}) VALUES ({placeholders})', valores)
        
        cn.commit()
        st.success('Tabela atualizada com sucesso')
        t.sleep(3)