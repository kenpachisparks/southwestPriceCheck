'''
To Setup Install Python3 then

sudo pip3 install selenium
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py
sudo pip3 install bs4
pip install lxml
To Run:
python3 southwestPriceCheck.py

'''



from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from bs4 import BeautifulSoup as soup

departureAirportCode = "AUS"
returningAirportCode = "LAS"
leavingDate = "5/10"
returningDate = "5/13"

departureFlightsFound = []
returnFlightsFound = []

def findFlightPrices(flightPathList, flightDirectionMessage, flightsArray):
    flightListLenght = len(flightPathList)
    flightListCount = 0
    flightCount = 0
    while flightListCount < flightListLenght:
        flightTimeSlot = flightPathList[flightListCount]
        flightTimes = flightTimeSlot.findAll('div', {
            'class': 'air-operations-time-status air-operations-time-status_booking-primary select-detail--time'})
        departureTimeText = flightTimes[0].text
        arrivalTimeText = flightTimes[1].text
        flitghtNumbers = flightTimeSlot.find('div', {'class': 'flyout-trigger flight-numbers--trigger'})
        flitghtNumbers = flitghtNumbers.text
        flitghtNumbers = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*®. ,]', '', flitghtNumbers)
        flightDuration = flightTimeSlot.find('div', {'class': 'select-detail--flight-duration'})
        flightDuration = flightDuration.text
        durationStops = flightTimeSlot.find('div', {'class': 'select-detail--number-of-stops'})
        durationStops = durationStops.text
        if 'Nonstop' in durationStops:
            durationStops = durationStops[:7]
        else:
            durationStops = durationStops[:2]
        flightDuration = flightDuration + '\nTotal Stop(s): ' + durationStops
        flightPrice = flightTimeSlot.find('span', {'class': 'currency currency_dollars currency-box'})
        flightPrice = flightPrice.text
        flightPrice = flightPrice[flightPrice.find('$'):]
        flightPriceResult = flightPrice.endswith('left')
        if flightPriceResult is True:
            flightPrice = flightPrice[:flightPrice.find(' ')]
            flightPrice = flightPrice[:-1]

###----------------------------- Change the number on the right of < to the last price that was paid
        if int(flightPrice[1:]) < 240:
            flightsArray.append(('Flight Plan: ' + str(
                flightCount) + '\n' + departureTimeText + '\n' + arrivalTimeText + '\nDuration: ' + flightDuration + '\nPrice: ' + flightPrice + '\nFlight Number(s): ' + flitghtNumbers))

            flightListCount = flightListCount + 1
            flightCount = flightCount + 1
        else:
            flightListCount = flightListCount + 1

    flightListCount = 0
    flightListLenght = len(flightsArray)
    print(flightDirectionMessage)
    while flightListCount < flightListLenght:
        print(flightsArray[flightListCount])
        print('\n')
        flightListCount = flightListCount + 1


safariDriver = webdriver.Safari(port=0, executable_path="/usr/bin/safaridriver", quiet=False)


safariDriver.get("https://www.southwest.com/air/booking/index.html?clk=GSUBNAV-AIR-BOOK")
WebDriverWait(safariDriver, 10).until(
    EC.element_to_be_clickable((By.ID, "form-mixin--submit-button")))


searchWebsiteItem = safariDriver.find_element("id", "originationAirportCode")
searchWebsiteItem.send_keys(departureAirportCode)
searchWebsiteItem.send_keys(Keys.RETURN)

time.sleep(1)

searchWebsiteItem = safariDriver.find_element("id", "departureDate")
searchWebsiteItem.clear()
searchWebsiteItem.send_keys(leavingDate)
searchWebsiteItem.send_keys(Keys.TAB)
searchWebsiteItem.send_keys(Keys.TAB)
searchWebsiteItem.send_keys(Keys.TAB)

searchWebsiteItem = safariDriver.find_element("id", "destinationAirportCode")
searchWebsiteItem.send_keys(returningAirportCode)

searchWebsiteItem.send_keys(Keys.TAB)

time.sleep(1)

searchWebsiteItem = safariDriver.find_element("id", "returnDate")
searchWebsiteItem.clear()
searchWebsiteItem.send_keys(returningDate)

time.sleep(1)

searchWebsiteItem = safariDriver.find_element("id", "originationAirportCode")
searchWebsiteItem.send_keys(departureAirportCode)
searchWebsiteItem.send_keys(Keys.RETURN)

time.sleep(1)

searchWebsiteItem = safariDriver.find_element("id", "form-mixin--submit-button")
searchWebsiteItem.click()

WebDriverWait(safariDriver, 10).until(
    EC.element_to_be_clickable((By.ID, "air-booking-product-2")))

htmlWebScrap = safariDriver.page_source


htmlWebScrap= soup(htmlWebScrap, "lxml")


flightDirectionSplit = htmlWebScrap.find_all('span', {'class': 'transition-content price-matrix--details-area'})
departureSection = flightDirectionSplit[0]
returnSection = flightDirectionSplit[1]
departureFlightsSort = departureSection.find_all('li', {
    'class': 'air-booking-select-detail'})
returningFlightsSort = returnSection.find_all('li', {
    'class': 'air-booking-select-details'})

findFlightPrices(departureFlightsSort, 'Flights that are Leaving\n\n', departureFlightsFound)
findFlightPrices(returningFlightsSort, 'Flights that are Returning\n\n', returnFlightsFound)
