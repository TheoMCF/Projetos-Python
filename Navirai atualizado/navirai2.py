from seleniumbase import SB
from datetime import datetime
import os
import shutil

class Navirai():
    def __init__(self, sb):
        self.sb = sb

    def login(self):
        # Inicia o navegador
        self.sb.open("https://navirai.oxy.elotech.com.br/iss/home")
        self.sb.maximize_window()
        self.sb.sleep(2)

        try:
            # Fecha aviso se tiver
            self.sb.click('//*[@id="btOk"]') 
        except:
            pass
        self.sb.sleep(2)
        
        # Botão da pagina de login
        self.sb.click(".btn.right.module-color")
        self.sb.sleep(3)
        
        # Desseleciona o cabecalho
        self.sb.uc_gui_press_key('esc')
        # Seleciona o campo do cpf e digita ele
        self.sb.uc_gui_press_key('tab')
        self.sb.uc_gui_write('42977908668')
        # Passa pro campo da senha e digita ela
        self.sb.uc_gui_press_key('tab')
        self.sb.uc_gui_write('123456')
        # Confirma
        self.sb.uc_gui_press_key('enter')
        self.sb.sleep(3)
        print()
    
    def selecionar_cnpj(self, cnpj):
        self.cnpj = cnpj
        self.sb.click('/html/body/app-root/div/app-theme1/app-main/div/elo-sidebar/aside/ul/div[2]/elo-sidebar-item/div/li/a')
        self.sb.sleep(3)
        self.sb.select_option_by_text("select#select-filter", "CNPJ/CPF")
        self.sb.sleep(1)
        self.sb.type('//*[@id="input-filter"]', f"{self.cnpj}")
        self.sb.sleep(1)
        
        try:
            self.sb.click('/html/body/app-root/div/app-theme1/app-main/roda-atalhos/div')
        except:
            pass

        self.sb.click('//*[@id="btnFilter"]')
        self.sb.sleep(1)
        self.sb.click('//*[@id="btnSelecionar-0"]')
        self.sb.sleep(3)
    
    def organizar_xmls(self, tipo, competencia, data_execucao):
        empresas_cnpj = {
            '31.675.485/0001-47': '169-NAVIRAI MATRIZ',
            '31.675.485/0002-28': '170-NAVIRAI FILIAL'
        }
        
        tipos_xml = {
            'Prestados': 'Saidas',
            'Tomados': 'Entradas'
        }
        
        dir_xmls = r'C:\Users\axoga\OneDrive\Desktop\Python\Projetos-Python\Navirai atualizado\downloaded_files'
        dir_destino = fr'C:\Users\axoga\OneDrive\Desktop\cerdil_xml\{tipos_xml[tipo]}\{empresas_cnpj[self.cnpj]}'
        
        if not os.path.exists(f'{dir_destino}\{competencia}'):
            os.mkdir(f'{dir_destino}\{competencia}')
        
        path_arquivo_novo = os.path.join(dir_xmls, f"{empresas_cnpj[self.cnpj]}_{data_execucao}.zip")

        arquivo_presente = False
        while not arquivo_presente: # Loop para esperar o download
            for arquivo in os.listdir(dir_xmls): # Roda na pasta de downloads
                if arquivo.endswith('.zip'):
                    os.rename(os.path.join(dir_xmls, arquivo), path_arquivo_novo) # Renomeia o arquivo baixado caso tenha .zip no nome
                    arquivo_presente = True

        shutil.move(path_arquivo_novo, f"{dir_destino}\{competencia}")
    
    def baixar_xmls(self, competencia, data_execucao):
        tipos_xml = ['Prestados', 'Tomados']

        self.sb.click('//*[@id="swipe"]/elo-sidebar/aside/ul/div[6]/elo-sidebar-item/div/li/a')
        self.sb.sleep(1)
        self.sb.click('//*[@id="swipe"]/elo-sidebar/aside/ul/div[6]/elo-sidebar-item/div/li/ul/elo-sidebar-item[9]/div/li/a')
        self.sb.sleep(2)
        
        for tipo in tipos_xml:
            self.sb.select_option_by_text('//*[@id="tipoServico"]', f"{tipo}")
            self.sb.sleep(1)
            self.sb.type('//*[@id="competencia"]', f"{competencia}")
            self.sb.sleep(1)
            self.sb.click('//*[@id="btnDownload"]')
            self.sb.sleep(5)
            self.organizar_xmls(tipo, competencia, data_execucao) 

lista_cnpjs = ['31.675.485/0001-47', '31.675.485/0002-28']

if __name__ == "__main__":
    dia = int(datetime.now().strftime("%d"))
    mes = int(datetime.now().strftime("%m"))
    ano = int(datetime.now().strftime("%Y"))
    
    data_execucao = f"{dia:02d}_{mes:02d}_{ano}"
    
    if dia < 15:
        mes -= 1

    # Adiciona zero a esquerda se o mes for menor que 10
    if mes <= 10:
        mes = f"0{mes}"

    competencia = f"{mes}{ano}"  

    with SB(uc=True, headless2=False, dark_mode=True, incognito=True) as sb:
        dir_download = fr'C:\Users\axoga\OneDrive\Desktop\Python\Projetos-Python\Navirai atualizado\downloaded_files'
        # Configurações de download para o Chrome
        chrome_options = {
            "download.default_directory": dir_download,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True
        }
                    
        # Iniciar o navegador com as opções definidas
        sb.driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": dir_download
        })

        n = Navirai(sb) 
        n.login()
        for cnpj in lista_cnpjs:
            n.selecionar_cnpj(cnpj)    
            n.baixar_xmls(competencia,data_execucao)

            