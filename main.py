import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import CHROME_PATH, username, password, url


if __name__ == '__main__':
    _head_less = False
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")
    if _head_less:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path=CHROME_PATH, options=options)
    driver.get('https://www.linkedin.com/login/en?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

    try:
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_class_name("btn__primary--large.from__button--floating.mercado-button--primary").click()
        driver.get(url)
        time.sleep(2)
        driver.maximize_window()  # Maximize Window
        driver.find_element_by_class_name("msg-overlay-bubble-header").click()  # Minimize Chat
    except Exception as e:
        print("Login Exception: " + str(e))
        driver.quit()
        exit()

    btn_s = []
    check = True

    while check:
        try:
            webdriver.ActionChains(driver).send_keys(Keys.END).perform()  # Scroll Page Down
            time.sleep(2)
            btn_s = driver.find_elements(By.XPATH, "//button[text()='Connect']")  # Find all Connect buttons
        except Exception as e:
            print('Error, not found Connect button!')
        print('New Connect on page: ' + str(len(btn_s)))
        actions = ActionChains(driver)

        for btn in btn_s:

            try:
                actions.move_to_element(btn).perform()  # Move to Connect button
                btn.click()
                time.sleep(1)
                driver.find_element_by_xpath("//span[text()='Done']").click()
                print('Sent a request to connect!')
            except Exception as e:
                print("Error 'Click Connect'.")

            try:
                driver.find_element_by_xpath("//span[text()='Got it']").click()
                print("Reached the invitation limit!!!")
                check = False
                driver.quit()
                break
            except Exception as e:
                pass

        try:
            time.sleep(2)
            driver.find_element(By.XPATH, "//span[text()='Next']").click()
            time.sleep(2)
        except Exception as e:
            print("Not found 'next' button")
