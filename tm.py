# in development multiprocess scraping

import multiprocessing 
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

tagaliojimas = "2025"
#######################
# p1 car links # assign drivers for each process 
driver = webdriver.Chrome(options=chrome_options)
onePageCarLinks = []
# suitableCarLinks = []

elements = ""
# p2 car links
driver2 = webdriver.Chrome(options=chrome_options)
onePageCarLinks2 = []
# suitableCarLinks2 = []
elements2 = ""
#######################

pageNumbers = []
tempPageNumbers = [0]



autopliusLink = "https://autoplius.lt/skelbimai/naudoti-automobiliai?make_id_list=&engine_capacity_from=&engine_capacity_to=&power_from=&power_to=&kilometrage_from=&kilometrage_to=&has_damaged_id=&condition_type_id=&make_date_from=&make_date_to=&sell_price_from=&sell_price_to=1000&fuel_id%5B32%5D=32&co2_from=&co2_to=&euro_id=&fk_place_countries_id=1&fk_place_cities_id=1&qt=&number_of_doors_id=&gearbox_id=&steering_wheel_id=&is_partner=&technical_passport=1&older_not=&save_search=1&slist=2248902949&category_id=2&order_by=&order_direction=&page_nr="
source = ""






def getPageSource(pageNumber, notFirstlaunch):
    global driver
    if not notFirstlaunch:
        driver = solveCapcha(driver)
    driver.get(autopliusLink+pageNumber)
    print("getting "+pageNumber+" page source...")
    return driver
    
def getPageCarlinks(driverVar):
    driver = solveCapcha(driver)
    elements = driverVar.find_elements(By.XPATH, '//a[contains(@class, "announcement-item") and not(contains(@class, "is-sold"))]')
    return elements

    
def getPageNumbers(driver):
    driver = solveCapcha(driver)
    page_navigation_container = driver.find_element(By.CSS_SELECTOR, 'div.page-navigation-container')
    grandchildren = page_navigation_container.find_elements(By.XPATH, './/*[not(*) and number(text())]')
    for element in grandchildren:
        pageNumbers.append(element.text.strip())
    return pageNumbers
    
def solveCapcha(driverVar):
    driverState = driverVar
    captchaExist = True
    while captchaExist:
        try:
            error_element = driverVar.find_element(By.XPATH, '//div[@class="error" and contains(text(), "Jūs viršijote leistiną šio puslapio peržiūros limitą.")]')
            input("Captcha launched, open autoplius and enter it, then press enter")
            captchaExist = False
        except:
            captchaExist = False
            pass
    return driverState
        
        
# create separate function for each process
def getCarlinksFromPage(elementsVar):
    for element in elementsVar:
        onePageCarLinks.append(str(element.get_attribute('href')))
def getCarlinksFromPage2(elementsVar):
    for element in elementsVar:
        onePageCarLinks2.append(str(element.get_attribute('href')))
#########################          
def getSuitableCarLinks(suitableCarLinks):
    print("getting SuitableCarLinks, array length = "+str(len(onePageCarLinks)))
    for index, carlink in enumerate(onePageCarLinks):
            print("processing p1 : "+str(index)) 
            randomSleepTime()
            driver = solveCapcha(driver)
            driver.get(carlink)
            try:
                driver = solveCapcha(driver)
                page = driver.find_element(By.XPATH, '//div[contains(@class, "parameter-value") and contains(text(), "'+str(tagaliojimas)+'")]')
                if page:
                    suitableCarLinks.append(carlink)       
            except:
                pass
    return suitableCarLinks
            
def getSuitableCarLinks2(suitableCarLinks2):
    print("getting SuitableCarLinks, array length = "+str(len(onePageCarLinks2)))
    print(onePageCarLinks2)
    for index, carlink in enumerate(onePageCarLinks2):
            print("processing p2 : "+str(index)) 
            randomSleepTime()
            driver2 = solveCapcha(driver2)
            driver2.get(carlink)
            try:
                driver2 = solveCapcha(driver2)
                page = driver2.find_element(By.XPATH, '//div[contains(@class, "parameter-value") and contains(text(), "'+str(tagaliojimas)+'")]')
                if page:
                    
                    suitableCarLinks2.append(carlink)   
                    print(suitableCarLinks2)    
            except:
                pass
    return suitableCarLinks2
        
    
            
######################################################
            
def getLastPageNumber(driver, pageNumbers):
    tempPageNumbers = [0]
    print("getting last page number...")
    while tempPageNumbers[-1] != pageNumbers[-1]:
        
        tempPageNumbers = pageNumbers.copy()
        
        driver = solveCapcha(driver)
        driver.get(autopliusLink+str(pageNumbers[-1]))
        pageNumbers = getPageNumbers(driver)
        
    print("last page num is : "+str(pageNumbers[-1]))
    return pageNumbers[-1]




driver = getPageSource(str(1), "firstLaunch")
pageNumbers = getPageNumbers(driver)
lastPageNum = int(getLastPageNumber(driver, pageNumbers))

gapNumber = 0
# depending on process count, divide lastPageNum / processCount
if lastPageNum % 2 == 0:
    gapNumber = lastPageNum / 2
else:
    gapNumber = lastPageNum+1 / 2
    
gapNumber = int(gapNumber)
#delete this
gapNumber = 5
print("gap number = "+str(gapNumber))
    

def p1(suitableCarLinks):
    pageNum = 1
    while int(pageNum) != int(gapNumber):
        
        driver = getPageSource(str(pageNum))
        elements = getPageCarlinks(driver)
        getCarlinksFromPage(elements)
        print("p1 "+str(pageNum+1)+ " loop passed ...")
        pageNum += 1
    suitableCarLinks = getSuitableCarLinks(suitableCarLinks)
    suitableCarLinks.value = suitableCarLinks
        
    
    
def p2(suitableCarLinks2, result):
    pageNum2 = gapNumber
    while int(pageNum2) != int(lastPageNum):
        
        driver2 = getPageSource(str(pageNum2))
        elements2 = getPageCarlinks(driver2)
        getCarlinksFromPage2(elements2)
        print("p2 "+str(pageNum2+1)+ " loop passed ...")
        pageNum2 += 1
    result = getSuitableCarLinks2(suitableCarLinks2)
    
    

if __name__ == "__main__": 
    manager = multiprocessing.Manager()
    suitableCarLinks2 = []
    suitableCarLinks = []
    
    result = multiprocessing.Array('s', 10000) 
    listVal = multiprocessing.Value('s')
    
    process2 = multiprocessing.Process(target=p2, args=(suitableCarLinks2,result)) 
  
    # process1.start() 
    process2.start() 
  
    # process1.join() 
    process2.join() 
  
  
    print("Done!") 
    print(result)
    # print(suitableCarLinks)

    suitableCarLinks.extend(suitableCarLinks2)
    with open("automobiliai.html", 'w') as f:
            f.write('<html>\n<body>\n')
            for link in suitableCarLinks:
                f.write(f'<a href="{link}">{link}</a><br>\n')
            f.write('</body>\n</html>')
    




