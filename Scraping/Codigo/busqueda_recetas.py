"""
Este script tiene como objetivo buscar nuevas recestas en base a los ingredientes
que hemos sido capaces de extraer.
Para ello buscará en la pagina supercook las recetas que tengan los ingredientes 
del video.
Esta pagina web permite buscar recetas en base as los ingredientes disponibles.

"""
__author__ = 'ro-otgo'

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

GECKO_DRIVER = r"Scraping\Codigo\web_driver\geckodriver.exe"
driver = None

def add_ingredients(ingredients:list):
    driver.get("https://www.supercook.com/")
    if driver.caps.get("moz:headless", False):
        # https://stackoverflow.com/a/74301253
        print("Firefox is headless")
    else:
        driver.maximize_window()
    driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]/p").click()

    for ingredient in ingredients:
        try:
            driver.find_element(By.CSS_SELECTOR, ".row > #search").send_keys(ingredient)
            driver.find_element(By.CSS_SELECTOR, ".row > #search").send_keys(Keys.ENTER)
            WebDriverWait(driver, timeout=3)
            # Esto solo sale si no existe el ingrediente
            try:
                dialog = driver.find_element(By.CSS_SELECTOR, 'html.wf-nunito-n7-active.wf-nunito-n6-active.wf-nunito-n3-active.wf-nunito-n4-active.wf-active body.mat.desktop.no-touch.platform-mat.q-responsive-modal div.modal.fullscreen.row.items-end.justify-center.with-backdrop div.modal-backdrop.absolute-full')
                if dialog:
                    action = webdriver.common.action_chains.ActionChains(driver)
                    action.click()
                    action.perform()
            except Exception as e:
                print (e)
            # driver.find_element(By.CSS_SELECTOR, ".row > #search").clear()
            for i in range(len(ingredient)):
                driver.find_element(By.CSS_SELECTOR, ".row > #search").send_keys(Keys.BACKSPACE)
            # Esto solo sale si no existe el ingrediente
            # pop_up_dialog = driver.find_element(By.CSS_SELECTOR, ".q-btn-inner > div")
            pop_up_dialog = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[3]/button/div[2]")
            if pop_up_dialog:
                pop_up_dialog.click()
                driver.find_element(By.CSS_SELECTOR, ".row > #search").clear()
        except Exception as e:
            print(e)

def clear_window():
    try:
        dialog = driver.find_element(By.CSS_SELECTOR, 'div.modal:nth-child(18) > div:nth-child(1)')
        if dialog:
            action = webdriver.common.action_chains.ActionChains(driver)
            action.click()
            action.perform()
    except Exception as e:
        print (e)
    time.sleep(3)
    try:
        dialog = driver.find_element(By.CSS_SELECTOR, "html.wf-nunito-n3-active.wf-nunito-n6-active.wf-nunito-n7-active.wf-nunito-n4-active.wf-active body.mat.desktop.no-touch.platform-mat.q-responsive-modal div.modal.fullscreen.row.items-end.justify-center.with-backdrop div.modal-backdrop.absolute-full")
        if dialog:
            action = webdriver.common.action_chains.ActionChains(driver)
            action.click()
            action.perform()
    except Exception as e:
        print (e)
    time.sleep(3)
    try:
        pop_up_dialog = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[3]/button/div[2]")
        if pop_up_dialog:
            pop_up_dialog.click()
    except Exception as e:
        print (e)
    try:
        dialog = driver.find_element(By.XPATH,"button.q-btn:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
        if pop_up_dialog:
            pop_up_dialog.click()
    except Exception as e:
        print (e)

def search_recipe():
    clear_window()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "a.w-button").click()
    # Ir a la receta
    time.sleep(5)
    try:
        driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .product-list-item .q-icon").click()
    except Exception as e:
        print (e)
        try:
            driver.find_element(By.CSS_SELECTOR, "div.section-block:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > i:nth-child(3)").click()
        except Exception as e:
            print (e)
            try:
                driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div[2]/main/section/div/div[4]/div[1]/div/div[2]/div[1]/i').click()
            except Exception as e:
                print (e)
  

def read_ingredients_list(file_path: str) -> list:
    with open(file_path,'r+',encoding='utf-8') as file:
        data = file.readlines()
        data[:] = [l.strip() for l in data]
        return data

def create_driver(headless=False):
    service = Service(executable_path=GECKO_DRIVER)
    options =  webdriver.FirefoxOptions()
    options.headless = headless
    driver = webdriver.Firefox(service=service, options= options)
    return driver

if __name__ == '__main__':
    ingredients = read_ingredients_list(os.path.join('.',r'ETL\Datos\ingredients\processed\spacy\postres\video__1TzqLW456I.txt'))
    driver = create_driver()
    add_ingredients(ingredients)
    search_recipe()
    