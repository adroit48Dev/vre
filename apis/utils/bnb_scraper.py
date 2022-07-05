from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
# StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as Bs
import json


def BnB_scraper(requestData):
    
    print("Getting scraper ready....")
    print("_______________________________________________________________________________________________________")

    location = requestData["location"]
    check_in = requestData["check_in"]
    check_out = requestData["check_out"]
    n_adults = requestData["n_adults"]
    n_child = requestData["n_child"]
    n_infants = requestData["n_infants"]
    n_pets = requestData["n_pets"]

    i_day = int(check_in.split("-")[-1])
    o_day = int(check_out.split("-")[-1])
    if o_day > i_day:
        n_days = o_day - i_day
    else:
        n_days = (31 - i_day) + o_day
    print("Please wait the scrapper is fetching data from AirBnB website...")

    print("_______________________________________________________________________________________________________")

    lnk = f"https://www.airbnb.com/s/{location}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_" \
          "trip_lengths%5B%5D=one_week&place_id=ChIJCzYy5IS16lQRQrfeQ5K5Oxw&date_picker_type=calendar&source=structured" \
          f"_search_input_header&search_type=filter_change&query=United%20States&checkin={check_in}&checkout={check_out}&" \
          f"adults={str(n_adults)}&children={str(n_child)}&infants={str(n_infants)}&pets={str(n_pets)}"

    data = []

    while True:

        options_seleniumWire = {
            'proxy': {
                'https': f'http://testuser881-rotate:sh881110@154.13.90.91:80'
            }
        }

        options = Options()

        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("detach", True)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("window-size=1280,800")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--incognito")
        # options.add_argument('--proxy-server=%s' % PROXY)

        s = Service(executable_path='./chromedriver_linux64/chromedriver')

        driver = webdriver.Chrome(service=s, options=options, seleniumwire_options=options_seleniumWire)

        try:
            driver.get(lnk)
        except WebDriverException:
            print("No internet... Please try again.")
            break

        time.sleep(10)

        # ac = ActionChains(driver)

        try:

            driver.execute_script("window.scrollTo(0, 2000)")

            main_div = driver.find_element(
                By.XPATH,
                '//*[@id="site-content"]/div[2]/div[4]/div/div/div/div/div/div/div/div/div/div')

            images = [img.get_attribute("src") for img in main_div.find_elements(By.TAG_NAME, 'img')]

            source = Bs(main_div.get_attribute('innerHTML'), 'html.parser')

            divs = source.find_all("div", class_="g1tup9az cb4nyux dir dir-ltr")

            i = 0

            for div in divs:

                li = [d.text for d in div.find_all('div')]

                try:
                    per_night = li[6].split("\xa0")
                    per_night = per_night[0]

                    if "originally" not in li[2]:
                        total = li[9].split(" ")[0]
                    else:
                        print(per_night, "per_night")
                        total = n_days * int(per_night.replace("$", "").replace(",", "").replace("£", "").replace("₹", ""))

                    data.append({"title": li[0], "beds": li[1], "per_night": per_night, "total": li[9].split(" ")[0],
                                    'thumbnail': images[i]})

                    i += 1

                except AttributeError:
                    print("AirBnB server is not responding... retrying...")
                    driver.quit()
                    print(
                        "_____________________________________________________________________________________________")

            if len(data) > 0:
                try:
                    nextt = driver.find_element(
                        By.XPATH, '//*[@id="site-content"]/div[2]/div[5]/div/div/div/div/div/nav/div/a[5]'
                    )
                    lnk = nextt.get_attribute('href')
                    break

                except NoSuchElementException:
                    break

            driver.quit()

        except (TimeoutException, NoSuchElementException):
            print("AirBnB is taking long to respond back... please wait...")
            driver.save_screenshot('screenie.png')
            driver.quit()
            print("_______________________________________________________________________________________________")

    return {'divs': data}


# if __name__ == '__main__':
#     div_data = BnB_scraper()
#     json_string = json.dumps(div_data)
#     with open('json_data.json', 'w') as outfile:
#         outfile.write(json_string)
