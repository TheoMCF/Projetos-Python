from seleniumbase import SB
import getpass
import datetime as dt
import calendar 
import os
import shutil

class CAMPO_GRANDE:
    def __init__(self, sb) -> None:

        self.url = 'https://nfse.pmcg.ms.gov.br/NotaFiscal/index.php'
        self.user = getpass.getuser()
        self.download_dir = rf'C:\Users\{self.user}\Downloads'

        self.sb = sb
    
    def get(self):
        print('Acessando o site')  
        self.sb.activate_cdp_mode(self.url)
        self.sb.cdp.sleep(5)
        self.sb.cdp.maximize()
    
    def acesso_sistema(self, cnpj, senha):
        print('Acessando o sistema')
        # acessar iframe da pagina principal
        # Muda o contexto para o iframe
        # iframe = self.sb.cdp.find_element('principal', by='id')
        self.sb.switch_to_frame('//*[@id="principal"]')

        # clicar para acessar o sistema
        self.sb.click('//*[@id="coluna1"]/div/div[2]/ul/li[2]/a')
       
        # login
        self.sb.send_keys('//*[@id="rLogin"]', cnpj)
        # self.sb.find_element('rLogin', by='id').send_keys(cnpj)
        # senha
        self.sb.send_keys('//*[@id="rSenha"]', senha)
        # self.sb.find_element('rSenha', by='id').send_keys(senha)

        self.sb.cdp.sleep(2)

        # clicar para acessar sistema
        self.sb.click('//*[@id="btnEntrar"]')

        self.sb.sleep(4)
    def exportar_notas_fiscais(self, dataInicio, dataFinal):
        # clicar no aleatorio da pagina
        # self.sb.click('/html/body/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/div[1]/ul/li/a')
        self.sb.click('/html/body/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/div[1]/ul/li/a')

        print('Acessar o menu de exportar notas fiscais')
        self.sb.get('https://nfse.pmcg.ms.gov.br/NotaFiscal/exportarNotas.php')
        self.sb.refresh()
        self.sb.sleep(1)

        self.sb.go_back()
        self.sb.sleep(1)
        print('Acessar o menu de exportar notas fiscais')
        self.sb.get('https://nfse.pmcg.ms.gov.br/NotaFiscal/exportarNotas.php')
        self.sb.refresh()
        self.sb.sleep(1)

        self.sb.switch_to_default_content()
        self.sb.sleep(10)        
        # clicar em intervalo de datas
        try:
            self.sb.click('/html/body/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[4]/span/form/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/input')
        except:
            pass
        self.sb.sleep(1)

        # inserir a data do periodo de exportacao das notas
        self.sb.clear('//*[@id="rDataInicioEN"]')
        self.sb.send_keys('//*[@id="rDataInicioEN"]', dataInicio)

        self.sb.sleep(1)

        self.sb.clear('//*[@id="rDataFimEN"]')
        self.sb.send_keys('//*[@id="rDataFimEN"]', dataFinal)

        self.sb.sleep(2)

        # clicar no botao de gerar xml
        self.sb.click('//*[@id="btnGerarXML"]')

        self.sb.sleep(10)
        print('Feito Download do XML')

    def mover_arquivo(self, codDominio, competencia, dataInicial, dataFinal):
        pasta_servidor = r'G:\Drives compartilhados\000 - Fiscal\cerdil_xml'
        # pasta_servidor = r'G:\Meu Drive\000 - Fiscal\cerdil_xml'
        print('Verificando pasta download')
        for arquivo in os.listdir(self.download_dir):
            
            if '.xml' in arquivo:
                # Temporário V V V V
                if not os.path.exists(fr'{pasta_servidor}\Saidas\{codDominio}'):
                    os.mkdir(fr'{pasta_servidor}\Saidas\{codDominio}')
                # Temporário ^ ^ ^ ^ 
                if not os.path.exists(fr'{pasta_servidor}\Saidas\{codDominio}\{competencia}'):
                    os.mkdir(fr'{pasta_servidor}\Saidas\{codDominio}\{competencia}')
                shutil.move(fr'{self.download_dir}\{arquivo}', fr'{pasta_servidor}\Saidas\{codDominio}\{competencia}')
                print('Arquivo movido com sucesso')
                try:
                    os.rename(fr'{pasta_servidor}\Saidas\{codDominio}\{competencia}\{arquivo}', fr'{pasta_servidor}\Saidas\{codDominio}\{competencia}\{codDominio}_{dataInicial.replace("/", "_")}_{dataFinal.replace("/", "_")}.xml')
                except:
                    print('Arquivo ja possui na pasta! Removendo arquivo')
                    os.remove(fr'{pasta_servidor}\Saidas\{codDominio}\{competencia}\{arquivo}')
                break

if __name__ == '__main__':
    hoje = dt.date.today()
    dia = hoje.day
    mes = hoje.month
    ano = hoje.year

    dias_no_mes = calendar.monthrange(ano, mes)[1]
    
    dict_calendario = {
        'primeira_quinzena': [('01', '05'), ('06', '10'), ('11', '15')],
        'segunda_quinzena': [('16', '20'), ('21', '25')]  
    }

    dict_calendario['segunda_quinzena'].append(('26', dias_no_mes))
    
    
    if dia > 3:
        quinzena_execuçao = 'primeira_quinzena'
    else:
        quinzena_execuçao = 'segunda_quinzena'
        mes -= 1
    
    if mes < 10:
        mes = f'0{mes}'

    datas_execuçao = dict_calendario[quinzena_execuçao]
    competencia = f'{mes}{ano}'
    
    empresas = [
            ('161-CERDIL CAMPO GRANDE', '03.304.188/0011-21', 'GGKT121'),
            ('226-D2M TECNOLOGIA', '45.019.459/0001-75', '4AF13AF1'),
            ('367-SIM MEDICINA FILIAL', '38.395.178/0002-32', '606DE82D')
        ]
    
    for empresa in empresas:
        cnpj = empresa[1]
        senha = empresa[-1]
        codEmpresa = empresa[0]
    
        for index, _ in enumerate(datas_execuçao):
            dataInicial = f'{datas_execuçao[index][0]}/{mes}/{ano}'
            dataFinal = f'{datas_execuçao[index][1]}/{mes}/{ano}'
            
            user = getpass.getuser()
            download_dir = rf'C:\Users\{user}\Downloads'
            with SB(uc=True, incognito=True) as sb:

                chrome_options = {
                    "download.default_directory": download_dir,
                    "download.prompt_for_download": False,
                    "safebrowsing.enabled": True
                }

                sb.driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                    "behavior": "allow",
                    "downloadPath": download_dir
                        })
                
                campo_grande = CAMPO_GRANDE(sb)
                campo_grande.get()
                campo_grande.acesso_sistema('03.304.188/0011-21', 'GGKT121')

                campo_grande.exportar_notas_fiscais(dataInicial, dataFinal)
                print('Movendo arquivo')
                campo_grande.mover_arquivo(codEmpresa, competencia, dataInicial, dataFinal)
                campo_grande.sb.quit()
                print()