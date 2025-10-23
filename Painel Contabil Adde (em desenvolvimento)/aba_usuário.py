import streamlit as st

def pag_usuario():
    st.title('Informações do usuário')

    st.write(f'**Nome**: {st.session_state.nome}')
    st.write(f'**Usuário**: {st.session_state.usuario}')
    st.write(f'**Senha**: {[len(st.session_state.usuario_senha[st.session_state.usuario]) * "*"][0]}')
    st.write(f'**Permissão**: {st.session_state.permissao}')

    if st.session_state.responsabilidades == None:
        st.write(f'**Responsabalidades:** Nenhuma atribuída')
    else:
        with st.expander('Responsabilidades'):
            for i in st.session_state.responsabilidades.split(','):
                st.write(f'- {i}')

    if st.button("Sair"):
        st.session_state.logado = False
        st.rerun()

