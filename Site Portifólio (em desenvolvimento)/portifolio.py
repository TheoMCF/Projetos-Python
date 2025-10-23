import streamlit as st
import os
import datetime
from streamlit_modal import Modal

nomes_pastas = os.listdir("C:/Users/axoga/OneDrive/Desktop/Python/Projetos-Python")
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_pai = os.path.dirname(diretorio_atual)
dicionario_codigos = {}

filtro = []

for nome_pasta in nomes_pastas:
    if "." not in nome_pasta and nome_pasta != '__pycache__':
        filtro.append(nome_pasta)
        
nomes_pastas[:] = filtro
for nome_da_pasta in nomes_pastas:
    if 'Site Portifólio' in nome_da_pasta:
        nomes_pastas.remove(nome_da_pasta)
nomes_pastas.insert(0, '')

for nome_pasta in nomes_pastas:
    if nome_pasta != '':
        arquivos_nas_pastas = os.listdir(fr'{diretorio_pai}\{nome_pasta}')
        for arquivo in arquivos_nas_pastas:
            if arquivo.endswith('.py'):
                dicionario_codigos[nome_pasta] = arquivo

st.set_page_config(
    page_title='Meus Projetos',
    page_icon='📁',
    layout='centered',
)

st.write("<h1 style='text-align: center;'>Meu portifólio</h1>", unsafe_allow_html=True)

abas = st.tabs(['Projetos','Informações do programador'])

with abas[0]:
    col1, col2 = st.columns(2, vertical_alignment='center')
    with col1:
        st.subheader("Projetos:")
    with col2:
        nome_projeto = st.selectbox('Selecione um projeto', nomes_pastas)

    if nome_projeto != '':
        with st.expander("Ver código"):
            caminho_arquivo = fr"C:\Users\axoga\OneDrive\Desktop\Python\Projetos-Python\{nome_projeto}/{dicionario_codigos[nome_projeto]}"
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                texto = f.read()
            st.code(texto, language='python')            

    data_nascimento = datetime.date(2010, 9, 17)
    idade = (datetime.date.today() - data_nascimento).days // 365

with abas[1]:
    st.markdown('***Nome:*** Theo Marafon Cardoso Flor')
    st.markdown(f'***Data de Nascimento:*** {str(data_nascimento).replace("-", "/")}')
    st.markdown(f'***Idade:*** {idade} anos')
    st.markdown('***Cidade:*** Sobradinho - DF')
    st.markdown('***País:*** Brasil')
    st.markdown('***Email:*** theomarafonflor@gmail.com')
    st.markdown('***GitHub:*** https://github.com/TheoMCF/Projetos-Python')