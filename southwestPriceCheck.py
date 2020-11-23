from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from bs4 import BeautifulSoup as soup

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
        flightPrice = flightTimeSlot.find('div', {'class': 'fare-button fare-button_primary-yellow select-detail--fare'})
        flightPrice = flightPrice.text
        flightPrice = flightPrice[flightPrice.find('$'):]
        flightPriceResult = flightPrice.endswith('left')
        if flightPriceResult is True:
            flightPrice = flightPrice[:flightPrice.find(' ')]
            flightPrice = flightPrice[:-1]
        if int(flightPrice[1:]) < 140:
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


searchWebsiteItem = safariDriver.find_element_by_id("originationAirportCode")
searchWebsiteItem.send_keys("AUS")

searchWebsiteItem = safariDriver.find_element_by_id("destinationAirportCode")
searchWebsiteItem.send_keys("LAS")

searchWebsiteItem = safariDriver.find_element_by_id("departureDate")
searchWebsiteItem.send_keys("12/22")

searchWebsiteItem = safariDriver.find_element_by_id("returnDate")
searchWebsiteItem.send_keys("12/26")

searchWebsiteItem = safariDriver.find_element_by_id("form-mixin--submit-button")
searchWebsiteItem.click()
searchWebsiteItem.send_keys(Keys.RETURN)

WebDriverWait(safariDriver, 10).until(
    EC.element_to_be_clickable((By.ID, "air-booking-product-2")))

htmlWebScrap = safariDriver.page_source


htmlWebScrap= soup(htmlWebScrap, "lxml")


dep_arr_split = htmlWebScrap.find_all('span', {'class': 'transition-content price-matrix--details-area'})
dep = dep_arr_split[0]
arr = dep_arr_split[1]
departureFlightsSort = dep.find_all('li', {
    'class': 'air-booking-select-detail air-booking-select-detail_min-products air-booking-select-detail_min-duration-and-stops'})
returningFlightsSort = arr.find_all('li', {
    'class': 'air-booking-select-detail air-booking-select-detail_min-products air-booking-select-detail_min-duration-and-stops'})

findFlightPrices(departureFlightsSort, 'Flights that are Leaving\n\n', departureFlightsFound)
findFlightPrices(returningFlightsSort, 'Flights that are Returning\n\n', returnFlightsFound)
