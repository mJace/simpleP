#!/usr/bin/env python3


import csv
import logging
import os
import sys
import time
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

path = os.path.dirname(os.path.abspath(__file__))
timeStr = time.strftime('%Y_%m_%d')
logFile = path + '/yohoDaemon.log'
csvFile = path + '/yoho' + timeStr + '.csv'

LoginUrl = 'http://yohoweb.itri.org.tw/main.aspx'
UserName = ''
UserPass = ''


def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1:
        return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1:
        return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b:
        return ""
    return value[adjusted_pos_a:pos_b]


def daemonLog(exctype, value, tb):
    logging.error('\tDaemon Error')
    logging.error('Type         : %s', exctype)
    logging.error('Value        : %s', value)
    logging.error('TrackBack    : %r', tb)


if __name__ == "__main__":
    fmt = '%(asctime)s[%(levelname)s] %(funcName)s():%(lineno)i: %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=fmt,
                        filename=logFile,
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s[%(levelname)s] %(funcName)s():%(lineno)i: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    sys.excepthook = daemonLog
    logging.debug('start~')

    with open(csvFile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Date', 'Power', 'Water'])
        while True:
            now = datetime.datetime.now()
            today5pm = now.replace(hour=17, minute=0, second=0, microsecond=0)
            today10pm = now.replace(hour=22, minute=0, second=0, microsecond=0)
            logging.debug('check time')
            if today5pm < now < today10pm:
                logging.debug('start browser')
                Browser = webdriver.Chrome()
                Browser.get(LoginUrl)
                Browser.find_element_by_name('USER').send_keys(UserName)
                Browser.find_element_by_name('PASSWORD').send_keys(UserPass)
                Browser.find_element_by_name('Submit').send_keys(Keys.ENTER)

                while True:
                    now = datetime.datetime.now()
                    if today5pm < now < today10pm:
                        waterTotal = 0
                        powerTotal = 0
                        soup = BeautifulSoup(Browser.page_source, "html.parser")

                        waterImg1 = soup.findAll("img", {"id": "waterNum_1"})
                        if waterImg1:
                            waterSrc1 = waterImg1[0].get('src')
                            waterNum1 = int(between(waterSrc1, '/', '.png'))
                            waterTotal = waterNum1

                            # logging.debug('waterNum1:%s', waterNum1)
                            logging.debug('waterTotal : %s', waterTotal)
                        else:
                            logging.debug('No water img1')
                            waterNum1 = 0

                        waterImg2 = soup.findAll("img", {"id": "waterNum_2"})
                        if waterImg2:
                            waterSrc2 = waterImg2[0].get('src')
                            waterNum2 = int(between(waterSrc2, '/', '.png'))
                            waterTotal = waterNum1 * 10 + waterNum2

                            # logging.debug('waterNum2:%s', waterNum2)
                            logging.debug('waterTotal : %s', waterTotal)
                        else:
                            waterNum2 = 0
                            logging.debug('No water img2')

                        waterImg3 = soup.findAll("img", {"id": "waterNum_3"})
                        if waterImg3:
                            waterSrc3 = waterImg3[0].get('src')
                            waterNum3 = int(between(waterSrc3, '/', '.png'))
                            waterTotal = waterNum1 * 100 + waterNum2*10 + waterNum3

                            # logging.debug('waterNum2:%s', waterNum2)
                            logging.debug('waterTotal : %s', waterTotal)
                        else:
                            waterNum3 = 0
                            logging.debug('No water img3')

                        powerImg1 = soup.findAll("img", {"id": "powerNum_1"})
                        if powerImg1:
                            powerSrc1 = powerImg1[0].get('src')
                            powerNum1 = int(between(powerSrc1, '/', '.png'))
                            powerTotal = powerNum1

                            # logging.debug('powerNum1:%s', powerNum1)
                            logging.debug('powerTotal : %s', powerTotal)
                        else:
                            logging.debug('No power img1')
                            powerNum1 = 0

                        powerImg2 = soup.findAll("img", {"id": "powerNum_2"})
                        if powerImg2:
                            powerSrc2 = powerImg2[0].get('src')
                            powerNum2 = int(between(powerSrc2, '/', '.png'))
                            powerTotal = powerNum1 * 10 + powerNum2

                            # logging.debug('powerNum2:%s', powerNum2)
                            logging.debug('powerTotal : %s', powerTotal)
                        else:
                            powerNum2 = 0
                            logging.debug('No power img2')

                        powerImg3 = soup.findAll("img", {"id": "powerNum_3"})
                        if powerImg3:
                            powerSrc3 = powerImg3[0].get('src')
                            powerNum3 = int(between(powerSrc3, '/', '.png'))
                            powerTotal = powerNum1 * 100 + powerNum2*10 + powerNum3

                            # logging.debug('powerNum3:%s', powerNum3)
                            logging.debug('powerTotal : %s', powerTotal)
                        else:
                            powerNum3 = 0
                            logging.debug('No power img3')

                        timeStamp = time.strftime('%m/%d-%H:%M')
                        writer.writerow([timeStamp, powerTotal, waterTotal])
                        Browser.refresh()

                    else:
                        break
                    logging.debug('wait 5 mins for next round')
                    time.sleep(300)

            elif now > today10pm:
                break
            else:
                logging.debug('sleep 5 mins')
                time.sleep(300)

    Browser.close()