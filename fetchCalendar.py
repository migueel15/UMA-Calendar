from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from os import path
import json
from dotenv import load_dotenv

# --------------------------------------------------------------------------- #

load_dotenv()

url = "https://informatica.cv.uma.es/"
databasePath = os.getenv("DATABASE_PATH") # Where to store calendar data.

user_mail = os.getenv("USER_MAIL")
user_passwd = os.getenv("USER_PASSWD")

# --------------------------------------------------------------------------- #

def startDriver():
    """Initialize driver setup for Firefox"""

    os.environ['MOZ_HEADLESS'] = '1'
    service = Service(log_path=path.devnull)

    return webdriver.Firefox(service=service)

def openUrl(url):
    """Open driver with url"""

    driver.get(url)
    
def login(uMail, uPasswd):
    """Append the values of uMail and uPasswd to the label and click of Log in.
    Then wait for page to load
    """

    loginButton = driver.find_element(By.TAG_NAME, "button")
    loginButton.click()

    email = driver.find_element(By.ID, "edit-name")
    passwd = driver.find_element(By.ID, "edit-pass")
    button = driver.find_element(By.ID,"submit_ok")

    email.send_keys(uMail)
    passwd.send_keys(uPasswd)
    button.click()
    WebDriverWait(driver,20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "current"))
    )
    
def clickCalAnchor():
    """Find calendar anchor.
    Returns href content
    """
    
    esteMes = driver.find_element(By.CLASS_NAME, "current")
    esteMes = esteMes.find_element(By.TAG_NAME, "a")

    linkCal = esteMes.get_attribute("href")
    driver.get(linkCal)

def getHtmlfromDriver():
    """Get html content and exit driver
    """

    html = driver.page_source
    driver.close()

    return html

def getGapDays(soup):
    """Get blank days before day 1"""
    
    mainCalendar = soup.find("div", {"class":"maincalendar"})
    firstWeek = mainCalendar.find("tr", {"data-region":"month-view-week"})
    firstWeekBlanks = firstWeek.find_all("td",{"class":"dayblank"})
    
    return firstWeekBlanks
    

def listaCal(html):
    """Parse html with soup and returns it"""

    soup = BeautifulSoup(html, "html.parser")

    return soup.find_all(
        "div", 
        {
            "class":"d-none d-md-block hidden-phone text-xs-center"
        }
    )
    
def saveTasks(lista): 
    """Save all tasks to table and return it"""
    soup = BeautifulSoup(html, "html.parser")
    tablaDias = []
    dia = 1
    for day in lista:
        tareasArray = []

        # Search for each task and append it to table
        tareasDelDia = day.find_all("span", {"class":"eventname"})
        for tarea in tareasDelDia:
            tareasArray.append(tarea.text)

        # Append day to json
        tablaDias.append({"dia":dia, "tareas":tareasArray})
        dia+=1

    return tablaDias

def saveTasksWithGaps(lista, html): 
    """Save all tasks to table and return it"""
    soup = BeautifulSoup(html, "html.parser")
    tablaDias = []
    for day in getGapDays(soup):
        tablaDias.append({"dia":"", "tareas":[]})
    dia = 1
    for day in lista:
        tareasArray = []

        # Search for each task and append it to table
        tareasDelDia = day.find_all("span", {"class":"eventname"})
        for tarea in tareasDelDia:
            tareasArray.append(tarea.text)

        # Append day to json
        tablaDias.append({"dia":dia, "tareas":tareasArray})
        dia+=1

    for day in range(7 - len(getGapDays(soup))):
        tablaDias.append({"dia":"", "tareas":[]})

    return tablaDias

def saveToFile(tablaDias, path):
    """Dumps json data from tablaDias to JSON file"""

    with open(path, "w")as f:
        jsonData = {}
        jsonData["calendario"] = tablaDias
        json.dump(jsonData,f)

# --------------------------------------------------------------------------- #

driver = startDriver()
openUrl(url)
login(user_mail,user_passwd)
clickCalAnchor()
html = getHtmlfromDriver()
listaDiasCalendario = listaCal(html)
tablaDias = saveTasks(listaDiasCalendario)
saveToFile(tablaDias, databasePath)

# --------------------------------------------------------------------------- #
