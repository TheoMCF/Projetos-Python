import streamlit as st
import os
import datetime

nomes_pastas = [] 

diretorio_projetos = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

filtro = ['Django','.git','.vscode','Portifólio', '.gitignore','venv','__pycache__','downloaded_files']

for pasta in os.listdir(diretorio_projetos):
    if pasta not in filtro:
        nomes_pastas.append(pasta)
        
nomes_pastas.insert(0, '')

st.set_page_config(
    page_title='Meus Projetos',
    page_icon='📁',
    layout='centered',
)

st.write("<h1 style='text-align: center;'>Meu portifólio</h1>", unsafe_allow_html=True)

abas = st.tabs(['Projetos','Informações do programador'])

with abas[0]:
    st.header("Projetos:")
    nome_projeto = st.selectbox('Selecione um projeto', nomes_pastas)

    if nome_projeto != '':
        dict_nome_cod = {}
        lista_codigos = []
        caminho_projeto = os.path.join(diretorio_projetos, nome_projeto)
        
        for arquivo in os.listdir(caminho_projeto):
            caminho_arquivo = os.path.join(caminho_projeto, arquivo)
            
            if arquivo.endswith('.py'):
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    texto = f.read()
                
                dict_nome_cod[arquivo] = texto
            
            elif os.path.isdir(caminho_arquivo):
                for arquivo in os.listdir(caminho_arquivo):
                    if arquivo.endswith('.py'):
                        caminho_arquivo = os.path.join(caminho_arquivo, arquivo)
                        with open(caminho_arquivo, "r", encoding="utf-8") as f:
                            texto = f.read()
                        
                        dict_nome_cod[arquivo] = texto
        
        for nome_arquivo, texto in dict_nome_cod.items():
            with st.expander(f'Ver código: {nome_arquivo}'):
                st.code(texto, language='python')            

    data_nascimento = datetime.date(2010, 9, 17)
    idade = (datetime.date.today() - data_nascimento).days // 365

with abas[1]:
    st.markdown('***Nome:*** Theo Marafon Cardoso Flor')
    st.markdown(f'***Data de Nascimento:*** {data_nascimento.strftime("%d/%m/%Y")}')
    st.markdown(f'***Idade:*** {idade} anos')
    st.markdown('***Cidade:*** Sobradinho - DF')
    st.markdown('***País:*** Brasil')
    st.markdown('***Email:*** theomarafonflor@gmail.com')
    st.markdown('***GitHub:*** https://github.com/TheoMCF/Projetos-Python')