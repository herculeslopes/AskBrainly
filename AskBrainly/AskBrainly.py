import re, PyPDF2, bs4, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

# Open The Browser And Goes To Brainly
url = 'https://brainly.com.br'

print('Opening Chrome')
driver = webdriver.Chrome()
print('Entering brainly.com')
driver.get(url)

# TODO: Save All The Answers In A Text File
def saveAnswers():

    FileName = input('Nome Do Arquivo: ')

    with open(f'MinhasRespostas\{FileName}.txt', 'wt', encoding='utf-8') as AnswersFile:
        for index, answer in enumerate(AllAnswers):
            AnswersFile.write(f"Questão {index + 1}\n{'-'*50}\n{answer}\n{'-'*50}\n")


# Look For Answers In Brainly
def GetAnswer(question):

    driver.switch_to.window(driver.window_handles[0])

    inputBox = driver.find_element_by_css_selector('#hero-search')
    inputBox.clear()
    driver.execute_script("arguments[0].value = arguments[1]", inputBox, question)
    
    searchButton = driver.find_element_by_css_selector('#__next > div > div.section--lnnYy.section--KhXv2 > div > div.sg-flex.sg-flex--full-width.sg-flex--column > div > form > div > div > button')
    ActionChains(driver).move_to_element(searchButton).key_down(Keys.CONTROL).click(searchButton).key_up(Keys.CONTROL).perform()

    driver.switch_to.window(driver.window_handles[1])

    sleep(2)

    source = driver.page_source
    soup = bs4.BeautifulSoup(source, 'lxml')

    QuestionBox = soup.select('body > div.js-page-wrapper > div > div.sg-layout__container.js-main-container > div > div.js-react-search-results > div.sg-box.sg-box--light.sg-box--padding-m.sg-box--border-color-gray-secondary-lightest.sg-box--border.LayoutBox__box--1X9rF > div > div:nth-child(2)')
    EachQuestion = QuestionBox[0].find_all('div', class_='sg-content-box sg-content-box--spaced-top-large')

    VerifiedAnswers = QuestionBox[0].find_all('div', class_='sg-icon sg-icon--mint sg-icon--x32')

    print('\033[1;36mResultado Da Pesquisa\033[m\n')
    print(f'Total de Resultados Encontrados {len(EachQuestion)} ')
    print(f'Total de Resultados Verificados {len(VerifiedAnswers)}')
    print()

    link = driver.find_element_by_css_selector('body > div.js-page-wrapper > div > div.sg-layout__container.js-main-container > div > div.js-react-search-results > div.sg-box.sg-box--light.sg-box--padding-m.sg-box--border-color-gray-secondary-lightest.sg-box--border.LayoutBox__box--1X9rF > div > div:nth-child(2) > div:nth-child(1) > div.sg-content-box__content > a')
    link.click()

    sleep(2)

    AnswerPage = driver.page_source
    AnswerSoup = bs4.BeautifulSoup(AnswerPage, 'lxml')

    AnswerElement = AnswerSoup.find('div', class_='brn-qpage-next-answer-box__content')
    answer = AnswerElement.getText().strip()

    AllAnswers.append(answer)

    print('-'*50)
    print('Resposta Da Questão')
    print()
    print(f'\033[1;33m{answer}\033[m')
    print()
    
    driver.close()


# TODO: Check How Many Files Are In MyPDFs
AllFiles = os.listdir('MyPDFs')

PDFs = []

# Search For PDFs
for File in AllFiles:
    if File.endswith(('.pdf')):
        PDFs.append(File)

# Loop The Script
while True:

    os.system('cls')
    
    # TODO: Show All .pdf Files:
    print(f"\nExistem {len(PDFs)} arquivos .pdf No Diretório '\\MyPDFs': \n")

    print('-'*69)
    print('|\033[1;34m{:^6}\033[m|\033[1;34m{:60}\033[m|'.format('id', 'Nome Do Arquivo'))
    print('-'*69)
    for index, pdf in enumerate(PDFs):
        print('|\033[1;32m{:^6}\033[m|\033[1;32m{:60}\033[m|'.format(index, pdf))
    print('-'*69)

    pdfIndex = int(input('Index Do Arquivo A Ser Analizado: \033[1;32m'))

    # Get All Questions From a File
    QuestionRegex = re.compile(r'(\d+\s\.\s \s\(.*?\).*?\.)', re.DOTALL)  
    print(f'\033[m\nLendo PDF: {PDFs[pdfIndex]}')
    with open(f'MyPDFs\\{PDFs[pdfIndex]}', 'rb') as pdfFile:
        ReaderObject = PyPDF2.PdfFileReader(pdfFile)
        AllPages = []

        for pageIndex in range(ReaderObject.numPages):
            page = ReaderObject.getPage(pageIndex).extractText()
            AllPages.append(page)

        TextFile = '\n'.join(AllPages)
        AllQuestions = QuestionRegex.findall(TextFile)

    AllAnswers = []


    for index, Question in enumerate(AllQuestions):

        print('-'*50)
        print(f'\033[1;36mQuestão {index + 1}°\033[m')
        print('-'*50)
        print(f'\033[1;33m {Question}\033[m')
        print('-'*50)
        GetAnswer(Question)

    saveRes = input('Gostaria de Salvar As Respostar Em Um Arquivo De Texto? (S/N) ').lower().strip()

    if saveRes == 's':
        saveAnswers()

    res = input('Deseja Continuar? (S/N) ').lower().strip()

    if res == 'n':
        break

# Close Browser
driver.switch_to.window(driver.window_handles[0])
driver.close()
