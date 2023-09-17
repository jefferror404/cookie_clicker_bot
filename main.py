from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")
# --------Getting Upgrade item IDs------------
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]
print(f"The item id: {item_ids}")

game_on = True
timeout = time.time() + 5
five_min = time.time() + 60

while game_on:
    cookie.click()
    #every 5 seconds:
    if time.time() > timeout:

        #--------Getting Upgrade item Prices------------
        prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []
        for price in prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)
        print(f"The item price: {item_prices}")

        #-------Create a dictionary for Upgrade Item IDs and Prices-------
        upgrade = {}
        for n in range(len(item_prices)):
            upgrade[item_prices[n]] = item_ids[n]
        print(f"The upgrade dictionary: {upgrade}")

        #-----Find upgrades that we can afford-------------
        money = driver.find_element(By.ID,"money").text
        if "," in money:
            money = money.replace(",", "")
        money_count = int(money)

        affordable_upgrade = {}
        for cost, id in upgrade.items():
            if money_count > cost:
                affordable_upgrade[cost] = id

        print(f"The affordable upgrade dictionary: {affordable_upgrade}")

        #----Purchase the most expensive affordable item-----
        highest_price_upgrade = max(affordable_upgrade)
        to_buy_item_id = affordable_upgrade[highest_price_upgrade]
        print(f"To buy item is: {to_buy_item_id}")

        driver.find_element(By.ID, to_buy_item_id).click()

        #add 5 seconds until the next check
        timeout = time.time() + 5

    #Stop the bot after 5 minutes:
    if time.time() > five_min:
        cookie_per_second = driver.find_element(By.ID, "cps")
        print(f"The cookie per second: {cookie_per_second}")
        break

