import configparser
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

config = configparser.ConfigParser()
config.read('config.ini')
path = config['chrome-driver']['path']
id = config['auth']['id']
passwd = config['auth']['passwd']
driver = webdriver.Chrome(
    service=Service(executable_path=r"{}".format(path))
)

url = r'https://kdt.fastcampus.co.kr'

driver.get(url)
driver.implicitly_wait(30)  # load


def login():
    driver.find_element(By.ID, 'user-email').send_keys(id)
    driver.find_element(By.ID, 'user-password').send_keys(passwd)
    driver.find_element(By.XPATH, '//*[@id="main"]/section/section/form/button').click()
    time.sleep(3)

login()
details_buttons = driver.find_elements(By.CSS_SELECTOR, '.sc-eb2000db-3')
for idx in range(len(details_buttons)):
    print('page 이동')
    driver.execute_script("arguments[0].click();", driver.find_elements(By.CSS_SELECTOR, '.sc-eb2000db-3')[idx])
    time.sleep(3)

    # part 아코디언 펼치기
    accordion_close_btns = driver.find_elements(
        By.CSS_SELECTOR,
        'div.common-accordion-menu:not(.common-accordion-menu--open) > .common-accordion-menu__header'
    )
    for btn in accordion_close_btns:
        driver.execute_script("arguments[0].click();", btn)

    # chapter 아코디언 펼치기
    accordion_close_btns = driver.find_elements(
        By.CSS_SELECTOR,
        'div.common-accordion-menu:not(.common-accordion-menu--open) > .common-accordion-menu__header'
    )
    for btn in accordion_close_btns:
        driver.execute_script("arguments[0].click();", btn)

    # bs4
    lecture_html = BeautifulSoup(driver.page_source, 'html.parser')
    # part로 나누기
    parts = lecture_html.select('div.classroom-sidebar-clip__chapter')
    for part in parts:
        part_title = part.select_one('p.classroom-sidebar-clip__chapter__title__text').text
        print(part_title)
        # part내 chapter로 나누기
        chapters = part.select('div.classroom-sidebar-clip__chapter__part')
        for chapter in chapters:
            chapter_title = chapter.select_one('p.classroom-sidebar-clip__chapter__part__title')
            print(chapter_title.text)
            semi_chapter_title = chapter.select('span.classroom-sidebar-clip__chapter__clip__title')
            semi_chapter_time = chapter.select('span.classroom-sidebar-clip__chapter__clip__time')

            for (c_title,c_time) in zip(semi_chapter_title, semi_chapter_time):
                print(f"{c_title.text} : {c_time.text}")

    print('뒤로 가기')
    driver.back()
    time.sleep(3)

time.sleep(60)  # main wait
