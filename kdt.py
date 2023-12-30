import configparser
import re
import time

from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def login(web, username, password):
    web.find_element(By.ID, 'user-email').send_keys(username)
    web.find_element(By.ID, 'user-password').send_keys(password)
    web.find_element(By.XPATH, '//*[@id="main"]/section/section/form/button').click()
    time.sleep(3)


def get_part_title(part_html):
    return part_html.select_one('p.classroom-sidebar-clip__chapter__title__text').text


# [(title, time), ...]
def get_semi_chapter_list(chapter_html):
    semi_chapter_title = chapter_html.select('span.classroom-sidebar-clip__chapter__clip__title')
    semi_chapter_time = chapter_html.select('span.classroom-sidebar-clip__chapter__clip__time')
    ret = []
    for (c_title, c_time) in zip(semi_chapter_title, semi_chapter_time):
        ret.append((c_title.text, c_time.text))
    return ret


def retrieve_chapter_info(part_title, chapters_html, lecture_exel):
    for idx, chapter in enumerate(chapters_html):
        chapter_block = chapter.select_one('p.classroom-sidebar-clip__chapter__part__title')
        chapter_title = chapter_block.text if chapter_block else part_title
        semi_chapter_list = get_semi_chapter_list(chapter)
        for (s_title, s_time) in semi_chapter_list:
            lecture_exel.append([part_title, chapter_title, s_title, s_time])


def spread_accordion(web):
    accordion_close_elements = web.find_elements(
        By.CSS_SELECTOR,
        'div.common-accordion-menu:not(.common-accordion-menu--open) > .common-accordion-menu__header'
    )
    for element in accordion_close_elements:
        web.execute_script("arguments[0].click();", element)


def get_lecture_title(web, idx):
    title = web.find_elements(By.CSS_SELECTOR, 'h3.sc-d01c8748-5')[idx].text
    return title.split(':')[-1].strip()


def short_title(title):
    bracket_pattern = r'\([^)]*\)'  # 괄호 제거
    str_pattern = r'[^A-Za-z0-9가-힣]'  # 한글/숫자/영어 추출
    t = re.sub(pattern=bracket_pattern, repl='', string=title)
    t = re.sub(pattern=str_pattern, repl='', string=t)
    return t.strip()[0:20]


def retrieve_lecture_info(lecture_html, lecture_ws):
    lecture_ws.append(['대주제(Part)', '중주제(Chapter)', '소주제(Clip)', '강의 시간'])

    # part로 나누기
    parts = lecture_html.select('div.classroom-sidebar-clip__chapter')
    for part in parts:
        part_title = get_part_title(part)
        print(part_title)
        # part내 chapter로 나누기
        chapters = part.select('div.classroom-sidebar-clip__chapter__part')
        if chapters:
            retrieve_chapter_info(part_title, chapters, lecture_ws)
        else:
            retrieve_chapter_info(part_title, part, lecture_ws)


def get_lecture_len(web):
    return int(web.find_element(By.CSS_SELECTOR, 'em.sc-66c26572-1').text)


def remove_default_sheet(lecture_wb):
    lecture_wb.remove(lecture_wb['Sheet'])


def travel_lecture(web, filename='schedule_t.xlsx'):
    lecture_len = get_lecture_len(web)
    print(f"총 강좌수 : {lecture_len} 개")
    lecture_wb = Workbook()
    for idx in range(lecture_len):
        lecture_title = get_lecture_title(web, idx)
        print(f"강좌 {idx} - {lecture_title}")
        lecture_ws = lecture_wb.create_sheet(short_title(lecture_title))

        # 강좌 클릭
        web.execute_script("arguments[0].click();", web.find_elements(By.CSS_SELECTOR, '.sc-d01c8748-3')[idx])
        time.sleep(2)

        # part 아코디언 펼치기
        spread_accordion(web)
        time.sleep(1)
        # chapter 아코디언 펼치기
        spread_accordion(web)
        time.sleep(1)

        # 강좌 정보 획득
        retrieve_lecture_info(BeautifulSoup(web.page_source, 'html.parser'), lecture_ws)

        # 뒤로가기
        web.back()
        time.sleep(2)
    remove_default_sheet(lecture_wb)
    lecture_wb.save(filename)


def start_crawling(filename='schedule_t.xlsx'):
    config = configparser.ConfigParser()
    config.read('config.ini')
    user_id = config['auth']['id']
    user_pw = config['auth']['passwd']
    driver = webdriver.Chrome(
        # service=Service(executable_path=r"{}".format(path))
    )
    url = r'https://kdt.fastcampus.co.kr'

    driver.get(url)
    driver.implicitly_wait(30)  # load

    login(driver, user_id, user_pw)

    travel_lecture(driver, filename)


if __name__ == '__main__':
    start_crawling()
