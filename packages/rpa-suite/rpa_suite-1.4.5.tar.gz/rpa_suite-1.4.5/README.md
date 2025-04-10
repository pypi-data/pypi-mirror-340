![RPA Suite](https://raw.githubusercontent.com/CamiloCCarvalho/rpa_suite/db6977ef087b1d8c6d1053c6e0bafab6b690ac61/logo-rpa-suite.svg)

<h1 align="left">
    RPA Suite
</h1>
<br>

![PyPI Latest Release](https://img.shields.io/pypi/v/rpa-suite.svg)
![PyPI Downloads](https://img.shields.io/pypi/dm/rpa-suite.svg?label=PyPI%20downloads)

---

## O que é?

**RPA Suite:** um conjunto abrangente de ferramentas projetadas para simplificar e otimizar o desenvolvimento de projetos de automação RPA com Python. Embora nossa suíte seja um conjunto de Ferramentas de RPA especializado, sua versatilidade a torna igualmente útil para uma ampla gama de projetos de desenvolvimento. Esta desenvolvendo com Selenium, Botcity ou Playwright? Experimente a RPA Suite e descubra como podemos facilitar seu projeto, ou qualquer projeto de Robôs de Software.

## Sumário do conteudo

- [Destaque](#destaque)
- [Objetivo](#objetivo)
- [Instalação](#instalação)
- [Exemplo](#exemplo)
- [Dependências](#dependências)
- [Estrutura do módulo](#estrutura-do-módulo)
- [Versão do projeto](#versão-do-projeto)
- [Mais Sobre](#mais-sobre)

## Destaque

**Versátil**: Além da Automação de Processos e criação de BOT em RPA, mas também para uso geral podendo  ser aplicadas em outros modelos de projeto, *além do RPA*.

**Simples**: Construímos as ferramentas de maneira mais direta e assertiva possível, utilizando apenas bibliotecas conhecidas no mercado para garantir o melhor desempenho possível.

## Objetivo

Nosso objetivo é se tornar a Biblioteca Python para RPA referência. Tornando o desenvolvimento de RPAs mais produtivo, oferecendo uma gama de funções para tal:

- Envio de emails (já configurado e personalizavel)
- Validação de emails (limpeza e tratamento)
- Busca por palavras, strings ou substrings (patterns) em textos.
- Criação e deleção de pasta/arquivo temporário com um comando
- Console com mensagens de melhor visualização com cores definidas para alerta, erro, informativo e sucesso.
- E muito mais

## Instalação

Para **instalar** o projeto, utilize o comando:

```python
>>> python -m pip install rpa-suite
```

ou no conda:

```python
conda install -c conda-forge rpa-suite
```

Após instalação basta fazer a importação do modulo e instanciar o Objeto ``suite``:

```python
from rpa_suite import suite as rpa
```

Feito isso já estará pronto para o uso:

```python
# function send mail by SMTP 
rpa.send_mail(...)
```

> [!NOTE]
>
> Para **desinstalar** o projeto, utilize o comando abaixo.
> **Obs.:** como usamos algumas libs no projeto, lembre-se de desinstar elas caso necessário.

```python
>>> python -m pip uninstall rpa-suite
```

> [!IMPORTANT]
>
> Opcionalmente você pode querer desinstalar as libs que foram inclusas no projeto, sendo assim:

```python
>>> python -m pip uninstall loguru mail_validator colorama
```

## Exemplo

Do módulo principal, importe a suite. Ela retorna uma instância do Objeto de classe Rpa_suite, onde possui variáveis apontando para todas funções dos submódulos:

    from rpa_suite import suite as rpa

    # Usando a função de envio de email por SMTP default
    rpa.send_email(my_email, my_pass, mail_to, subject, message_body)

    # Usando submódulo clock para aguardar 30 (seg) e então executar uma função
    time = 30
    rpa.wait_for_exec(time, my_function, param1, param2)

## Dependências

No setup do nosso projeto já estão inclusas as dependências, só será necessário instalar nossa **Lib**, mas segue a lista das libs usadas:

- colorama
- loguru
- email-validator
- colorlog
- pillow
- pyautogui
- typing

  opcionalmente para automação de navegador:

  - selenium
  - webdriver_manager

[!IMPORTANT]
No caso da função de screenshot é necessario ter as libs 'pyautogui' 'pillow' e 'pyscreeze' instalados, geralmente a instalação de pyautogui já instala as demais dependências deste caso.

## Estrutura do módulo

O módulo principal do rpa-suite é dividido em categorias. Cada categoria contém módulos com funções destinadas a cada tipo de tarefa

! Divisao e nomes de funções precisam ser atualizadas nesta sessão de Estrutura do módulo !

- **rpa_suite**
  - **clock**
    - **waiter** - Função capaz de aguardar para executar a função do argumento, ou executar a função do argumento para aguardar posteriormente
    - **exec_at** - Função capaz de executar a função do argumento no horario especificado "xx:yy" parecido com scheduler, porem com a vantagem de ter o horario como variavel dentro do escopo de código podendo gerar variações pela propria natureza da aplicação
  - **date**
    - **date** - Funções capazes de extrair dia/mes/ano e hora/min/seg, facilitando a necessidade de formatar o resultado de datetime, a função ja devolve os valores em trio formatados em string
  - **email**
    - **sender_smtp** - Funções para envio de email SMPT com configuração simples já default porem personalizavel
  - **file**
    - **counter** - Funções para contagem de arquivos
    - **temp_dir** - Funções para diretórios temporários
    - **screen_shot** -  Função para criar diretório e arquivo de print com nome do diretório, arquivo e delay personalizáveis
    - **file_flag** -  Funções para criar e deletar arquivo utilizado como flag de execução, tendo path e nome do arquivo já automatico porem personalizavel para se adequar ao seu projeto
  - **log**
    - **logger_uru** - Instanciador de stream e handlefile que cria na pasta raiz do arquivo chamador pasta de log e seta o stream para as funções de log
    - **functions_logger_uru** - Funções de log parecida com os prints personalizados, setadas e personalizadas para todos log levels usado pelo ´logger_uru´, já escreve no arquivo setado além de gerar o print no terminal
    - **printer** - Funções de print personalizados (alerta, erro, sucesso, informativo)
  - **regex**
    - **pattern_in_text** - Função para otimizar o uso mais comum de regex buscando padrões em um texto
  - **validate**
    - **mail_validator** - Função para validar lista de emails, devolvendo a lista com emails validos a partir da lista original
    - **string_validator** - Função que valida presença de letras, palavras, e textos e possibilita contar as ocorrencias em uma string

## Release

Versão: **Beta 1.4.5**

Lançamento: *20/02/2024*

Última atualização: *10/04/2025*

Status: Em desenvolvimento.

### Notas da atualização: 1.4.5

- Mudança dos submodulos para Objetos, agora Rpa_suite é um Objeto de Suite que compoe diversos sub-objetos separados pelas mesmas categorias anteriormente ja definidas
- Reformulada a arquitetura do projeto para melhor coeção e menos subpastas e arquivos, agora a estrutura é mais simples e de melhor manutenção contendo apenas uma pasta core para o nucleo de nossos modulos, e uma pasta utils com ferramentas utilitarias que vamos adicionar varias novidades
- Adicionado setor utils com funcionalidade de tornar o diretorio atual em um importavel relativo para o python
- Adicionado Automação de Navegadores! Sim estamos devendo esta feature a bastante tempo, porem estamos com a primeira versão disponivel, em breve teremos mais recursos e disponibilidade para outros navegadores, atualmente suporte apenas para *Chrome.*
- Mantemos o alerta! **get_dma** atualizada e **renomeada** para **get_dmy** para manter o padrão em ingles
- Função *send_email* atualizada para simplificar seu uso e funcionalidade em uma maior variedade de maquinas
- Melhoria nas descrições das funções e adicionado docstring (documentação explicativa) de todos Objetos e respectivas funções
- Sub-modulos agora como são Objetos internos do Objeto principal Suite pode ser acessado de duas formas, ex1: " from rpa_suite import rpa ; rpa.modulo.function() " ou então ex2: "from rpa_suite.core.Submodulo import NomeModulo ; meu_obj = NomeModulo() ; meu_obj.function()",
- Funções de regex e busca em textos foi simplificada e em breve estaremos adicionando funcionalidades mais interessantes.
- Correção e melhoria do Submodulo de Log. Tinhamos dois formatos de Log com duas bibliotecas e decidimos optar apenas pela Loguru para podermos dedicar mais atenção e fornecer recursos de Log mais completos, agora possui funcionalidade para indicar o caminho da pasta, nome da pasta, e também nome do arquivo, realizando stream tanto para o console (terminal) como também para o arquivo com todos levels já configurados e personalizados para ter distinção e facilitar o reconhecimento visual do que esta acontecendo no seu projeto.

## Mais Sobre

Para mais informações, visite nosso projeto no Github ou PyPi:
`<br>`
`<a href='https://github.com/CamiloCCarvalho/rpa_suite' target='_blank'>`
    Ver no GitHub.
`</a>`
`<br>`
`<a href='https://pypi.org/project/rpa-suite/' target='_blank'>`
    Ver projeto publicado no PyPI.
`</a>`

<hr>
