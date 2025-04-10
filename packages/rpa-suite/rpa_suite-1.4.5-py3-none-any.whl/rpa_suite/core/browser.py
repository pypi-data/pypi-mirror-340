# default import
import os, requests

# imports
from rpa_suite.functions._printer import error_print, alert_print, success_print

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

class Browser():

    """
    WIP ...
    """

    driver: None
    port: int = None
    path_driver = None
    
    def __init__(self, port: int = 9393, close_all_chrome_on_this_port: bool = True):
        self.port = port
        self.path_driver = ChromeDriverManager().install()

        if close_all_chrome_on_this_port: self._close_all_chrome()
        ...

    def configure_browser(self) -> None:
        
        try:
            # Use the absolute path from comment
            
            options = Options()
            options.add_experimental_option("debuggerAddress",
                                         f"127.0.0.1:{str(self.port)}")
            
            # Additional configs  
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            
            # Verifica se o caminho do driver está correto
            if not os.path.exists(self.path_driver):
                raise FileNotFoundError(f'O caminho do driver não foi encontrado: {self.path_driver}')
            
            # Create driver with options and chromedriver path
            self.driver = webdriver.Chrome(
                #service=self.path_driver,
                options=options,
                keep_alive=True
            )

        except Exception as e:
            error_print(f'Erro durante a função: {self.configure_browser.__name__}! Error: {str(e)}.')

    def start_browser(self, close_chrome_on_this_port: bool = True, display_message: bool = False):
        
        try:
            if close_chrome_on_this_port: self.close_browser()

            # Inicia o Chrome com debugging port
            os.system(f'start chrome.exe --remote-debugging-port={str(self.port)} --user-data-dir="C:/temp/chrome_profile"')

            # Aguardar até que o Chrome esteja realmente aberto
            while True:
                try:
                    # Tenta conectar ao Chrome na porta de depuração
                    response = requests.get(f'http://127.0.0.1:{self.port}/json')
                    if response.status_code == 200:
                        break  # O Chrome está aberto
                except requests.ConnectionError:
                    sleep(1)  # Espera um segundo antes de tentar novamente
            
            # Inicializa o Chrome com as opções
            self.configure_browser()
            
            if display_message: success_print(f'Browser: Iniciado com sucesso!')
            
        except Exception as e:
            error_print(f'Erro ao iniciar navegador: {str(e)}.')


    def find_ele(self, value, by=By.XPATH, timeout=12, display_message=True):
        
        try:
            sleep(2)
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            ); return element
        
        except Exception as e:

            if display_message:
                error_print(f'Erro durante a função: {self.find_ele.__name__}! Error: {str(e)}.')
                return None
            else: return None

    # find elements (needs implementation)
    ...
    
    # navigate
    def get(self, url: str, display_message: bool = False):
        
        try:
            self.driver.get(url)
            if display_message: success_print(f'Browser: Navegando para: {url}')
            
        except Exception as e:
            error_print(f'Erro ao navegar para a URL: {url}. Error: {str(e)}.')


    def _close_all_chrome(self):

        try:
            os.system('taskkill /F /IM chrome.exe >nul 2>&1')
        except:
            pass


    def close_browser(self, display_message: bool = False):
        
        try:
            # Primeiro tenta fechar todas as janelas via Selenium
            try:
                self.driver.close()
            except:
                pass
                
            # Depois tenta encerrar a sessão
            try:
                self.driver.quit()
            except:
                pass
            
            # Aguarda um momento para o processo ser liberado
            sleep(1)
            
            # Força o fechamento do processo específico do Chrome
            os.system(f'taskkill /f /im chrome.exe /fi "commandline like *--remote-debugging-port={str(self.port)}*" >nul 2>&1')
            
            # Verifica se o processo foi realmente terminado
            check = os.system(f'tasklist /fi "imagename eq chrome.exe" /fi "commandline like *--remote-debugging-port={str(self.port)}*" >nul 2>&1')
            
            if check == 0:
                # Processo ainda existe, tenta método mais agressivo
                os.system(f'taskkill /f /im chrome.exe /fi "commandline like *--remote-debugging-port={str(self.port)}*" /t >nul 2>&1')
                if display_message: alert_print(f'Browser: Fechado via força!')
                
            else:
                if display_message: success_print(f'Browser: Fechado com sucesso!')
            
        except Exception as e:
            
            
            try:
                if display_message: alert_print(f'Erro ao fechar navegador: {str(e)}, Tentando meio mais forte!')

                # Último recurso - mata todos os processos do Chrome (use com cautela)
                os.system(f'taskkill /f /im chrome.exe /fi "commandline like *--remote-debugging-port={str(self.port)}*" /t >nul 2>&1')
                if display_message: alert_print(f'Browser: Fechado via força extrema!')
                
            except Exception as error_ultimate:
                if display_message: error_print(f'Falha crítica ao tentar fechar o navegador! Error: {str(error_ultimate)}!')
