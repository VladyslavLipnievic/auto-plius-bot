# working autoplius crawler - 1 process to handle all
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import random
import time, copy
chrome_options = Options()
chrome_options.add_argument("--headless")  

def randomSleepTime():
    random_sleep_time = random.uniform(0.7, 1.2)
    time.sleep(random_sleep_time)

tagaliojimas = "2026"
onePageCarLinks = []
suitableCarLinks = []
pageNumbers = []
tempPageNumbers = [0]



autopliusLink = "https://autoplius.lt/skelbimai/naudoti-automobiliai?category_id=2&fk_place_countries_id=1&fuel_id%5B32%5D=32&sell_price_to=1000&steering_wheel_id=10922&qt=&page_nr="
source = ""
driver = webdriver.Chrome(options=chrome_options)

elements = ""

def getPageSource(pageNumber):
    solveCapcha()
    driver.get(autopliusLink+pageNumber)
    print("getting "+pageNumber+" page source...")
    return driver
    
def getPageCarlinks(driver):
    solveCapcha()
    elements = driver.find_elements(By.XPATH, '//a[contains(@class, "announcement-item") and not(contains(@class, "is-sold"))]')
    return elements

    
def getPageNumbers(driver):
    solveCapcha()
    page_navigation_container = driver.find_element(By.CSS_SELECTOR, 'div.page-navigation-container')
    grandchildren = page_navigation_container.find_elements(By.XPATH, './/*[not(*) and number(text())]')
    for element in grandchildren:
        pageNumbers.append(element.text.strip())
    return pageNumbers
    
def solveCapcha():
    captchaExist = True
    while captchaExist:
        try:
            error_element = driver.find_element(By.XPATH, '//div[@class="error" and contains(text(), "Jūs viršijote leistiną šio puslapio peržiūros limitą.")]')
            input("Captcha launched, open autoplius and enter it, then press enter")
            captchaExist = False
        except:
            captchaExist = False
            pass
        
        

def getCarlinksFromPage(elements):
    for element in elements:
        onePageCarLinks.append(str(element.get_attribute('href')))
    print("getting "+str(pageNum)+" page car links...") 
       
        
def getSuitableCarLinks():
    print("getting SuitableCarLinks, array length = "+str(len(onePageCarLinks)))
    for index, carlink in enumerate(onePageCarLinks):
            print("processing : "+str(index)) 
            randomSleepTime()
            solveCapcha()
            driver.get(carlink)
            try:
                solveCapcha()
                page = driver.find_element(By.XPATH, '//div[contains(@class, "parameter-value") and contains(text(), "'+str(tagaliojimas)+'")]')
                if page:
                    suitableCarLinks.append(carlink)       
            except:
                pass
            
def getLastPageNumber(driver, pageNumbers):
    tempPageNumbers = [0]
    print("getting last page number...")
    while tempPageNumbers[-1] != pageNumbers[-1]:
        
        tempPageNumbers = pageNumbers.copy()
        
        solveCapcha()
        driver.get(autopliusLink+str(pageNumbers[-1]))
        pageNumbers = getPageNumbers(driver)
        
    print("last page num is : "+str(pageNumbers[-1]))
    return pageNumbers[-1]



pageNum = 0
lastPageNum = 1111
    
while int(pageNum) != int(lastPageNum+1):
    
    
    if int(pageNum) == 0:
        driver = getPageSource(str(pageNum+1))
        elements = getPageCarlinks(driver)
        getCarlinksFromPage(elements)
        pageNumbers = getPageNumbers(driver)
        lastPageNum = int(getLastPageNumber(driver, pageNumbers))

       
    elif int(pageNum) > 1:
        driver = getPageSource(str(pageNum))
        elements = getPageCarlinks(driver)
        getCarlinksFromPage(elements)
        
            
    print(str(pageNum+1)+ " loop passed ...")
    pageNum += 1
getSuitableCarLinks()
        
    
    
    


with open("automobiliai.html", 'w') as f:
            f.write('<html>\n<body>\n')
            for link in suitableCarLinks:
                f.write(f'<a href="{link}">{link}</a><br>\n')
            f.write('</body>\n</html>')

