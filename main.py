#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 2017/12/20 14:42

@author: Lucifer
@site: plantree.me
@email: wpy1174555847@outlook.com
"""

from bs4 import BeautifulSoup
import json
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
from utils import *


def parse_and_create(fileName):
    try:
        f = open(fileName, 'rb')
    except IOError:
        print('File is not found!')
        return
    else:
        html = f.read()
        songList = parse_html(html)
        songList = json.dumps(songList)
        with open(fileName.replace('html', 'habit'), 'w') as fp:
            fp.write(songList)
    finally:
        f.close()


def parse_web(id, name):
    id = str(id)

    # login and get cookies (not necessarily)

    driver = webdriver.PhantomJS()
    '''
    driver.get('http://music.163.com/')
    frame = driver.find_element_by_id('g_iframe')
    driver.switch_to.frame(frame)
    login = driver.find_element_by_id('index-enter-default')
    login.click()
    time.sleep(1)
    driver.switch_to.default_content()
    mobile = driver.find_element_by_class_name('u-btn2')
    mobile.click()
    loginName = driver.find_element_by_class_name('j-phone')
    passwd = driver.find_element_by_class_name('j-pwd')
    actions = ActionChains(driver).click(loginName).send_keys('your telephone number')\
                .click(passwd).send_keys('your password').send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(3)
    myCookie = driver.get_cookies()
    '''

    url = 'http://music.163.com/#/user/home?id=' + id
    driver.get(url)
    frame = driver.find_element_by_id('g_iframe')
    driver.switch_to.frame(frame)
    time.sleep(3)
    allSongsBtn = driver.find_element_by_id('songsall')
    if allSongsBtn.text != '':
        allSongsBtn.click()
        time.sleep(1)
        moreBtn = driver.find_element_by_class_name('more').find_element_by_tag_name('a').click()
        time.sleep(1)
        allSongsBtn = driver.find_element_by_id('songsall').click()
        time.sleep(1)
        html = driver.page_source
        songList = parse_html(html)
        print('{} musics were collected.'.format(len(songList)))
        songList = json.dumps(songList)
        with open('data/' + name + '.habit', 'w') as fp:
            fp.write(songList)
    else:
        print('Sorry! Too less music.')


def compute_similarity(file1, file2):
    with open(file1, 'rb') as f1:
        data1 = json.loads(f1.read())
    with open(file2, 'rb') as f2:
        data2 = json.loads(f2.read())
    dict1 = {}
    dict2 = {}
    list1 = []
    list2 = []
    sets = set()

    # compute weight
    kind1 = len(data1) // 10
    for item in data1:
        if item['name'] not in dict1:
            dict1[item['name']] = (len(data1) - item['order']) // kind1 + 1
            sets.add(item['name'])
        else:
            dict1[item['name']] += (len(data1) - item['order']) // kind1 + 1

    kind2 = len(data2) // 10
    for item in data2:
        if item['name'] not in dict2:
            dict2[item['name']] = (len(data2) - item['order']) // kind2 + 1
            sets.add(item['name'])
        else:
            dict2[item['name']] += (len(data2) - item['order']) // kind2 + 1


    for item in sets:
        list1.append(int(dict1.get(item, 0)))
        list2.append(int(dict2.get(item, 0)))

    list1 = np.array(list1)
    list2 = np.array(list2)
    similarity = list1.dot(list2) / (np.sqrt(list1.dot(list1)) * np.sqrt(list2.dot(list2)))
    return similarity * 100


if __name__ == '__main__':
    '''
    files = os.listdir('./data/')
    for file in files:
        if file.endswith('html'):
            parse_and_create('./data/' + file)
    '''
    '''
    habits = [x for x in os.listdir('./data/') if x.endswith('habit')]
    for i in range(len(habits) - 1):
        habit1 = habits[i]
        for j in range(i + 1, len(habits)):
            habit2 = habits[j]
            print(habit1.split('.')[0] + '-' + habit2.split('.')[0] + ':', compute_similarity('./data/' + habit1, './data/' + habit2))
    '''
    # print(compute_similarity('./data/wangpengyuan.habit', './data/zhangbeichen.habit'))