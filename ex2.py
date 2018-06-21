import pw
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

workTimeUrl = "https://itriap8.itri.org.tw/perabs/Attend/Program/RecFill.aspx"

browser = webdriver.Chrome()
browser.get(workTimeUrl)

browser.find_element_by_name('USER').send_keys(pw.user)
browser.find_element_by_name('PASSWORD').send_keys(pw.pw)
browser.find_element_by_name('Submit').send_keys(Keys.ENTER)

browser.find_element_by_id('EndTime20').send_keys('2000')

elem = browser.find_element_by_id('btn_Save')
elem.click()