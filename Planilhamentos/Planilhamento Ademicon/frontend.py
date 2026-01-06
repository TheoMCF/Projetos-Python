import streamlit as st
from backend import planilhar, gerar_zip_dfs

def main():
    st.subheader('EXTRATO CERDIL')
    st.write(':grey[Planilhamento do PDF referente as notas de Extrato do Grupo Cerdil]')

    arquivos_pdfs = st.file_uploader('Selecione os Arquivos PDF (Recarregar a página irá limpar os arquivos selecionados)', type='pdf', accept_multiple_files=True)
    dfs = None
    
    if arquivos_pdfs:
        with st.container(horizontal=True):
            if st.button('Gerar Planilhamento', icon=':material/autoplay:', type='primary'):
                with st.spinner('Lendo os arquivos/notas ...'):
                    arquivos_pdfs = arquivos_pdfs[0]
                    dfs = planilhar(arquivos_pdfs)
                    zip = gerar_zip_dfs(dfs)

                st.download_button(
                    "Baixar ZIP",
                    data=zip,
                    file_name="CONSÓRCIOS.zip",
                    mime="application/zip",
                    icon=':material/download:'
                )
        if dfs:
            with st.expander('Conta corrente', expanded=True):
                st.dataframe(dfs[0])
            with st.expander('Pendências', expanded=True):
                st.dataframe(dfs[1])
            with st.expander('Contemplados', expanded=True):
                st.dataframe(dfs[2])
                        
                
main()