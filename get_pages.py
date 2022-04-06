from selenium import webdriver
import io
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pathlib
import time


options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")


url = 'https://www.tripadvisor.ru/Attractions-g187070-Activities-c36-t132-France.html'
driver = webdriver.Chrome("driver/chromedriver.exe", options=options)
driver.get(url)
output = 'Pages'

more_info = None
winery_num = 1
page = 1
resume = True
while resume:
    try:
        WebDriverWait(driver, 20).until(
            ec.visibility_of_element_located((By.XPATH, './/div[contains(@class, "_3LwzvfhX")]')))
    except TimeoutException:
        print('Cannot locate producers table')
        continue

    time.sleep(20)
    wineries = driver.find_elements_by_class_name('_1SVhvMXu')
    for winery in wineries:
        ActionChains(driver).key_down(Keys.CONTROL).click(winery).key_up(Keys.CONTROL).perform()
        driver.switch_to.window(driver.window_handles[1])

        try:
            WebDriverWait(driver, 20).until(
                ec.visibility_of_element_located((By.XPATH, './/div[contains(@class, "delineation accessible_red_3")]')))
        except TimeoutException:
            print('Cannot locate vine card')
            continue
        time.sleep(0.1)

        try:
            more_info = driver.find_element_by_class_name('_3HOBzctX')
            # ActionChains(driver).key_down(Keys.CONTROL).click(more_info).key_up(Keys.CONTROL).perform()
            more_info.click()
        except NoSuchElementException:
            print("No element found")

        time.sleep(0.1)


        with io.open(output + '/' + str(winery_num) + ".html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
            f.close()
        print('Saved vine {}'.format(str(winery_num)))
        time.sleep(0.5)

        winery_num += 1
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    try:
        current_button = driver.find_elements_by_xpath(
            './/a[contains(@class, "ui_button nav next primary ")]'.format(page)).pop()
        driver.execute_script("arguments[0].scrollIntoView();", current_button)
        driver.implicitly_wait(2)
        ActionChains(driver).click(current_button).perform()
        print('Next page button clicked')
    except IndexError:
        resume = False


print('Done')
driver.quit()
