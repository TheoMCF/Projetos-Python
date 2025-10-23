from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import qrcode
import pyautogui
import time as t
import threading

# Lista os arquivos.pdf na pasta 'pdfs'
lista_pdfs = os.listdir(r'C:\Users\axoga\Downloads\Python\Projetos-Python\Pdf to QRCODE\pdfs')
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
index_lista = 0

def fazer_login():
    t.sleep(5)
    pyautogui.click(pyautogui.locateCenterOnScreen('Pdf to QRCODE\email.png', confidence=0.6))
    t.sleep(3)
    pyautogui.click(pyautogui.locateCenterOnScreen(r'Pdf to QRCODE\avancado.png', confidence=0.6))
    t.sleep(3)
    pyautogui.click(pyautogui.locateCenterOnScreen(r'Pdf to QRCODE\acessar_permissoes.png', confidence=0.6))
    t.sleep(3)
    pyautogui.press('tab' for i in range(1,8))
    t.sleep(1)
    pyautogui.press('enter')
    t.sleep(5)
    while True: 
        if pyautogui.locateCenterOnScreen(r'Pdf to QRCODE\autenticacao.png', confidence=0.6):
            pyautogui.hotkey('ctrl', 'w')
            break
def upload_para_drive(caminho_do_arquivo):
    global nome_pdf
    # Define o nome a partir da última barra, retirando também o .pdf
    nome_pdf = (caminho_do_arquivo.split("/")[-1]).replace(".pdf", "")
    
    #Setup
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile("Pdf to QRCODE\client_secrets.json")
    thread = threading.Thread(target=fazer_login)
    thread.start()
    gauth.LocalWebserverAuth()
    thread.join()
    drive = GoogleDrive(gauth)

    #Cria o arquivo                 
    arquivo_drive = drive.CreateFile({
        'title': nome_pdf
    })
    
    #Dá conteúdo ao arquivo
    arquivo_drive.SetContentFile(caminho_do_arquivo)

    #Faz o upload do arquivo
    arquivo_drive.Upload()
  
    # Adiciona permissão para todos
    arquivo_drive.InsertPermission({
    'type': 'anyone',
    'value': 'anyone',
    'role': 'reader'
    })
    
    global link_pdf
    link_pdf = arquivo_drive['alternateLink']

for i in range(1, len(lista_pdfs) + 1):

    upload_para_drive(fr"C:/Users/axoga/Downloads/Python/Projetos-Python/Pdf to QRCODE/pdfs/{lista_pdfs[index_lista]}")

    # Faz um qrcode com o link do pdf
    qr = qrcode.make(link_pdf)
    qr_path = os.path.join("Pdf to QRCODE", "qrcodes", f"{nome_pdf.replace(' ', '-').replace('-','_')}.png")
    qr.save(qr_path)
    # Passa para o próximo nome na lista de pdfs
    index_lista += 1