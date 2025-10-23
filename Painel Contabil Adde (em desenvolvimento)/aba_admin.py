import streamlit as st
import time as t
from config import cn, cr

def pag_admin():
    # Painel Admin
    st.title('Painel de Administração')
    st.divider()

    # Declara as colunas principais
    col_prin_1, col_prin_2 = st.columns(2)
    with col_prin_1:
        st.subheader('**Usuários**')
        x = 0
        
        for i in st.session_state.lista_usuarios:
            with st.expander(f'Usuário: {i}'):
                col_expander1, col_expander2, col_expander3  = st.columns(3)
                
                with col_expander1:
                    st.write(f'**Nome**: {st.session_state.usuario_nome[i]}')
                    st.write(f'**Senha**: {st.session_state.usuario_senha[i]}')
                    st.write(f'**Permissão**: {st.session_state.usuario_permissao[i]}')
                    st.write(f'**Responsabilidades**: {st.session_state.usuario_responsabilidades[i].replace(",", ", ") if st.session_state.usuario_responsabilidades[i] else "Nenhuma atribuída"}')
        
                with col_expander2:
                    if st.button(f'Alterar Nome', key=f'alterar_nome_{x}'):
                        st.session_state.alterando_nome = True
                    if st.button(f'Alterar Senha', key=f'alterar_senha_{x}'):
                        st.session_state.alterando_senha = True
                    if st.button(f'Alterar Permissão', key=f'alterar_permissao_{x}'):
                        st.session_state.alterando_permissao = True
                
                with col_expander3:  
                    if st.button(f'Excluir Usuário', key=f'excluir_usuario_{x}'):
                        st.session_state.excluindo_usuario = True
                    if st.button('Alterar Responsabilidades', key=f'alterar_responsabilidades_{x}'):
                        st.session_state.alterando_responsabilidades = True
                
                if st.session_state.alterando_nome:
                    st.session_state.excluindo_usuario = False
                    st.session_state.alterando_senha = False
                    st.session_state.alterando_permissao = False
                    st.session_state.alterando_responsabilidades = False

                    novo_nome = st.text_input('Novo nome', key=f'nome_{x}')
                    confirmar_alteracao = st.button('Confirmar alteração', key=f'confirmar_nome_{x}')
                    
                    if novo_nome != "" and confirmar_alteracao:
                        if novo_nome in st.session_state.lista_nomes:
                            st.error('Nome indisponível')
                       
                        else:   
                            # Atualização dos dados
                            cr.execute("UPDATE info_usuarios SET Nome = ? WHERE Usuário = ?", (novo_nome, i))
                            cn.commit()
                            st.session_state.usuario_nome[i] = novo_nome
                            st.session_state.lista_nomes[st.session_state.lista_usuarios.index(i)] = novo_nome
                            st.success(f'Nome de usuário alterado para {novo_nome}')
                            t.sleep(3)
                            st.session_state.alterando_nome = False
                            st.rerun()
                    
                    elif st.button('Cancelar', key=f'cancelar{x}'):
                        st.success('Ação cancelada')
                        t.sleep(3)
                        st.session_state.alterando_nome = False
                        st.rerun()
                
                elif st.session_state.alterando_senha:
                    st.session_state.excluindo_usuario = False
                    st.session_state.alterando_nome = False
                    st.session_state.alterando_permissao = False
                    st.session_state.alterando_responsabilidades = False
                    

                    nova_senha = st.text_input('Nova senha', key=f'senha_{x}')
                    confirmar_alteracao = st.button('Confirmar alteração', key=f'confirmar_nome_{x}')

                    if nova_senha != "" and confirmar_alteracao: 
                        # Atualização dos dados
                        cr.execute("UPDATE info_usuarios SET Senha = ? WHERE Usuário = ?", (nova_senha, i))
                        cn.commit()
                        st.session_state.usuario_senha[i] = nova_senha
                        st.success(f'Senha alterada para {nova_senha}')
                        t.sleep(3)
                        st.session_state.alterando_senha = False
                        st.rerun()
                    elif st.button('Cancelar', key=f'cancelar{x}'):
                        st.success('Ação cancelada')
                        t.sleep(3)
                        st.session_state.alterando_senha = False
                        st.rerun()
                
                elif st.session_state.alterando_permissao:
                    st.session_state.excluindo_usuario = False
                    st.session_state.alterando_nome = False
                    st.session_state.alterando_senha = False
                    st.session_state.alterando_responsabilidades = False
                    

                    nova_permissao = st.selectbox('Nova permissão', ['Admin', 'Usuário'], key=f'permissao_{x}')
                    confirmar_alteracao = st.button('Confirmar alteração', key=f'confirmar_permissao_{x}')
                    if confirmar_alteracao:
                        # Atualização dos dados
                        cr.execute("UPDATE info_usuarios SET Permissão = ? WHERE Usuário = ?", (nova_permissao, i))
                        cn.commit()
                        st.session_state.usuario_permissao[i] = nova_permissao
                        st.success(f'Permissão alterada para {nova_permissao}')
                        t.sleep(3)
                        st.session_state.alterando_permissao = False
                        st.rerun()
                    elif st.button('Cancelar', key=f'cancelar{x}'):
                        st.success('Ação cancelada')
                        t.sleep(3)
                        st.session_state.alterando_permissao = False
                        st.rerun()
                
                elif st.session_state.excluindo_usuario:
                    st.session_state.alterando_nome = False
                    st.session_state.alterando_senha = False
                    st.session_state.alterando_permissao = False
                    st.session_state.alterando_responsabilidades = False
                    

                    # Deleta o usuário do banco de dados
                    st.warning(f'Você tem certeza que deseja excluir o usuário {i}? Esta ação não pode ser desfeita.')
                    if st.button('Confirmar', key=f'confirmar{x}'):
                        try:
                            cr.execute("DELETE FROM info_usuarios WHERE Usuário = ?", (i,))
                            cn.commit()
                            # Deleta todos os dados do usuário do session state
                            st.session_state.lista_usuarios.remove(i)
                            st.session_state.lista_nomes.remove(st.session_state.usuario_nome[i])
                            st.session_state.usuario_senha.pop(i, None)
                            st.session_state.usuario_nome.pop(i, None)
                            st.session_state.usuario_permissao.pop(i, None)
                            st.session_state.usuario_responsabilidades.pop(i, None)
                            st.success(f'Usuário {i} excluído com sucesso')
                            t.sleep(3)
                            st.rerun()
                        
                        except:
                            st.error('Erro ao excluir usuário. Tente novamente mais tarde.')
                            t.sleep(3)
                            st.session_state.excluindo_usuario = False
                            st.rerun()
                    
                    elif st.button('Cancelar', key=f'cancelar{x}'):
                        st.success('Ação cancelada')
                        t.sleep(3)
                        st.session_state.excluindo_usuario = False
                        st.rerun()
                    
                elif st.session_state.alterando_responsabilidades:
                    st.session_state.excluindo_usuario = False
                    st.session_state.alterando_nome = False
                    st.session_state.alterando_senha = False
                    st.session_state.alterando_permissao = False
                    

                    novas_responsabilidades = st.multiselect('Novas responsabilidades:', st.session_state.nomes_empresas, key=f'responsabilidades_{x}')
                    confirmar_alteracao = st.button('Confirmar alteração', key=f'confirmar_responsabilidades_{x}')
                    
                    if confirmar_alteracao:
                        # Atualização dos dados
                        cr.execute("UPDATE info_usuarios SET Responsabilidades = ? WHERE Usuário = ?", (','.join(novas_responsabilidades), i))
                        cn.commit()
                        st.session_state.usuario_responsabilidades[i] = ','.join(novas_responsabilidades)
                        st.success(f'Responsabilidades atualizadas para {i}')
                        t.sleep(3)
                        st.session_state.alterando_responsabilidades = False
                        st.rerun()  
                    
                    elif st.button('Cancelar', key=f'cancelar{x}'):
                        st.success('Ação cancelada')
                        t.sleep(3)
                        st.session_state.alterando_responsabilidades = False
                        st.rerun()
                
                x += 1
                    
    with col_prin_2:
        st.subheader('**Adicionar Usuário**')
        if st.button('Criar novo usuário'):
            st.session_state.criando_usuario = True
        if st.session_state.criando_usuario:
            nome = st.text_input('Nome')
            usuario = st.text_input('Usuário')
            senha = st.text_input('Senha')
            permissao = st.selectbox('Permissão', ['Admin', 'Usuário'])
            responsabilidades = st.multiselect('Responsabilidades:', st.session_state.nomes_empresas)
            if st.button('Adicionar usuário'):
                if usuario in st.session_state.lista_usuarios:
                    st.error('Usuário já existe')
                else:
                    cr.execute("INSERT INTO info_usuarios (Usuário, Nome, Senha, Permissão, Responsabilidades) VALUES (?, ?, ?, ?, ?)", (usuario, nome, senha, permissao, ','.join(responsabilidades)))
                    cn.commit()
                    # Atualiza as listas do session state
                    st.session_state.lista_usuarios.append(usuario)
                    st.session_state.lista_nomes.append(nome)
                    st.session_state.usuario_senha[usuario] = senha
                    st.session_state.usuario_nome[usuario] = nome
                    st.session_state.usuario_permissao[usuario] = permissao
                    st.session_state.usuario_responsabilidades[usuario] = ','.join(responsabilidades)

                    st.success(f'Usuário {usuario} adicionado com sucesso')
                    t.sleep(3)
                    st.session_state.criando_usuario = False
                    st.rerun()