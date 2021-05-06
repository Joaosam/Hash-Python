from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from os import system
from sys import exit

class Webscraping:    
    def Iniciar(self):
        self.ticker = input("Qual ticker deseja consultar? ").upper()
        self.Main()

    def Main(self):
        self.Configurar_chrome()
        self.Iniciar_sistema()
        self.Validar_ticker()
        self.Validar_sistema()
        self.Baixar_planilhas()
        self.Encerrar_programa()

    def Configurar_chrome(self):
        # Instancio o Chrome
        self.chrome = webdriver.Chrome() 
        # Abro com tela maximizada       
        self.chrome.maximize_window()       

    def Iniciar_sistema(self):
        # Acesso o site http://www.b3.com.br/pt_br/          
        self.chrome.get("http://www.b3.com.br/pt_br/")
        # Acesso os elementos da página através do xpath
        self.chrome.find_element_by_xpath('//*[@id="sb-search-open"]/span').click()               
        self.chrome.find_element_by_xpath('//*[@id="query"]').send_keys(self.ticker + Keys.ENTER)
        try:
            wait(self.chrome, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-close-btn-container"]/button'))).click()
        except:
            pass                

    def Validar_ticker(self):
        # Valido se o elemento existe via xpath. Senão existir, limpo o console e chamo a função __init__()
        try:
            self.chrome.find_element_by_xpath('//*[@id="richSnippet"]/div[3]/div/div[2]/div[3]/a').click()            
        except NoSuchElementException:            
            sleep(2)
            self.chrome.close()
            clear = lambda: system("cls")
            clear()
            print("-" *40)
            print("\033[1;33m" + "         ##Ticker inválido!##    " + "\033[m")
            print("-" *40 + "\n")
            self.Iniciar()
            
    def Validar_sistema(self):
        try:
            # Altero o foco para o iframe bvmf_iframe, atribuindo isso a variável iframe 
            iframe = self.chrome.find_element_by_xpath('//*[@id="bvmf_iframe"]')
            self.chrome.switch_to_frame(iframe)
            # Aguardo até 10s para carregar o elemento selecionado pelo xpath                                
            wait(self.chrome, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_contentPlaceHolderConteudo_MenuEmpresasListadas1_tabMenuEmpresa_tabRelatoriosFinanceiros"]/span/span'))).click()
            sleep(1.5)
            # Crio uma exception caso apresente timeout ao não localizar o elemento acima           
        except TimeoutException:
            self.chrome.close()
            clear = lambda: system("cls")
            clear()
            print("-" *40)
            print("\033[1;31m" + "##Sistema indisponível. Tente novamente mais tarde!##   " + "\033[m")
            print("-" *40 + "\n")
            print("\nObrigado por usar nossos serviços!" + "\033[1m" + "\n\nJoaosam ©")
            sleep(2)
            exit()

    def Baixar_planilhas(self):
        # Altero para a janela principal        
        self.chrome.switch_to.default_content()
        # Desço a página até o fim        
        self.chrome.find_element_by_tag_name('HTML').send_keys(Keys.END)
        # Altero o foco para o iframe bvmf_iframe, atribuindo isso a variável iframe             
        iframe = self.chrome.find_element_by_xpath('//*[@id="bvmf_iframe"]')
        self.chrome.switch_to_frame(iframe) 
        sleep(1.5)
        # Download dos arquivos      
        wait(self.chrome, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_contentPlaceHolderConteudo_lkbDownload"]'))).click()
        # 31/12/2020 - Informe do Código de Governança - Versão 1.0       
        wait(self.chrome, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_contentPlaceHolderConteudo_rptDocumentosGovDownload_ctl00_lnkDownload"]'))).click()             
        sleep(2.5)        
        
    def Encerrar_programa(self):
        clear = lambda: system("cls")
        clear()
        print("-" *40)
        print("\033[1;32m" +"    ##Arquivo baixado com sucesso!## " + "\033[m")
        print("-" *40 + "\n")
        sleep(0.5)        
        self.chrome.close()        
        input("Pressione enter para sair!")
        sleep(0.5)
        print("\nObrigado por usar nossos serviços!" + "\033[1m" + "\n\nJoaosam ©")
        sleep(2)
        exit()            

start = Webscraping()
start.Iniciar()