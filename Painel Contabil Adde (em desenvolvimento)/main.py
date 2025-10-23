import streamlit as st
from aba_tabela import pag_tabela as vis_tab
from aba_usuário import pag_usuario as usu_tab
from aba_admin import pag_admin as adm_tab
from aba_analytics import pag_analytics as ana_tab
from config import cr

cr.execute("SELECT Senha FROM info_usuarios")
lista_senhas = [linha[0] for linha in cr.fetchall()]

cr.execute("SELECT Permissão FROM info_usuarios")
lista_permissoes = [linha[0] for linha in cr.fetchall()]

cr.execute("SELECT Responsabilidades FROM info_usuarios")
lista_responsabilidades = [linha[0] for linha in cr.fetchall()]

# Guarda as informações não locais no session state

# Informações de ações em andamento
if "alterando_nome" not in st.session_state:
    st.session_state.alterando_nome = False
if "alterando_senha" not in st.session_state:
    st.session_state.alterando_senha = False
if "alterando_permissao" not in st.session_state:
    st.session_state.alterando_permissao = False
if "alterando_responsabilidades" not in st.session_state:
    st.session_state.alterando_responsabilidades = False
if "excluindo_usuario" not in st.session_state:
    st.session_state.excluindo_usuario = False
if "criando_usuario" not in st.session_state:
    st.session_state.criando_usuario = False

# Informações do usuário	
if "logado" not in st.session_state:
    st.session_state.logado = False
if "nome" not in st.session_state:
    st.session_state.nome = ''
if "usuario" not in st.session_state:
    st.session_state.usuario = ''
if "permissao" not in st.session_state:
    st.session_state.permissao = ''
if "responsabilidades" not in st.session_state:
    st.session_state.responsabilidades = []

# Listas Session State
if "lista_usuarios" not in st.session_state:
    cr.execute("SELECT Usuário FROM info_usuarios")
    st.session_state.lista_usuarios = [linha[0] for linha in cr.fetchall()]
if "nomes_empresas" not in st.session_state:
    cr.execute("SELECT Empresa FROM lev_empresas")
    st.session_state.nomes_empresas = [linha[0] for linha in cr.fetchall()]
if "lista_nomes" not in st.session_state:
    cr.execute("SELECT Nome FROM info_usuarios")
    st.session_state.lista_nomes = [linha[0] for linha in cr.fetchall()]

# Dicts Sessions State
if "usuario_senha" not in st.session_state:
    st.session_state.usuario_senha = dict(zip(st.session_state.lista_usuarios, lista_senhas))
if "usuario_nome" not in st.session_state:
    st.session_state.usuario_nome = dict(zip(st.session_state.lista_usuarios, st.session_state.lista_nomes))
if "usuario_permissao" not in st.session_state:
    st.session_state.usuario_permissao = dict(zip(st.session_state.lista_usuarios, lista_permissoes))
if "usuario_responsabilidades" not in st.session_state:
    st.session_state.usuario_responsabilidades = dict(zip(st.session_state.lista_usuarios, lista_responsabilidades))

if not st.session_state.logado:    
    st.set_page_config(page_title="Login", layout="centered", initial_sidebar_state="collapsed")
else:
    st.set_page_config(page_title="Painel Contabil Adde", layout="wide", initial_sidebar_state="expanded")

def login():
    st.write(st.session_state)
    st.title("Login")
    with st.container(border=True):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if usuario in st.session_state.usuario_senha and st.session_state.usuario_senha[usuario] == senha:
                st.session_state.logado = True
                st.session_state.nome = st.session_state.usuario_nome[usuario]
                st.session_state.usuario = usuario
                st.session_state.permissao = st.session_state.usuario_permissao[usuario]
                st.session_state.responsabilidades = st.session_state.usuario_responsabilidades[usuario]
                st.success(f"Bem-vindo, {st.session_state.nome}!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
if not st.session_state.logado:
    login()
    
else:
    paginas = [
        st.Page(vis_tab, title="Visualizar Tabela"),
        st.Page(usu_tab, title="Informações do Usuário"),
        st.Page(ana_tab, title="Analytics")
    ]
    if st.session_state.permissao == 'Admin':
        paginas.append(st.Page(adm_tab, title="Administração"))

    pagina_selecionada = st.navigation(paginas)
    pagina_selecionada.run()