#!/usr/bin/env python3
import pw
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

workTimeUrl = "https://itriweb.itri.org.tw/itri_talk/index.aspx?tab=1"

browser = webdriver.Chrome()
browser.get(workTimeUrl)

browser.find_element_by_name('USER').send_keys(pw.user)
browser.find_element_by_name('PASSWORD').send_keys(pw.pw)
browser.find_element_by_name('Submit').send_keys(Keys.ENTER)


elem = browser.find_element_by_class_name('current_box')
print(elem.text)