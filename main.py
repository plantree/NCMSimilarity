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
from math import sqrt
import os
from selenium import webdriver
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
    url = 'http://music.163.com/#/user/home?id=' + id
    driver = webdriver.PhantomJS()
    driver.get(url)
    frame = driver.find_element_by_id('g_iframe')
    driver.switch_to.frame(frame)
    time.sleep(1)
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
        print('{} musics were collected. Your own habit data '
              'about music has been successfully created.'.format(len(songList)))
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

    similarity = dot(list1, list2) / (sqrt(dot(list1, list1)) * sqrt(dot(list2, list2)))
    return similarity * 100


if __name__ == '__main__':
    '''
    files = os.listdir('./data/')
    for file in files:
        if file.endswith('html'):
            parse_and_create('./data/' + file)

    habits = [x for x in os.listdir('./data/') if x.endswith('habit')]
    for i in range(len(habits) - 1):
        habit1 = habits[i]
        for j in range(i + 1, len(habits)):
            habit2 = habits[j]
            print(habit1.split('.')[0] + '-' + habit2.split('.')[0] + ':', compute_similarity('./data/' + habit1, './data/' + habit2))

    # print(compute_similarity('./data/wangpengyuan.habit', './data/zhangbeichen.habit'))
    #parse_web(14258676)
    '''
    while True:
        option = input('You want to create habit data or compute similarity?(1/2)')
        if option == '1':
            if not os.path.exists('data'):
                os.mkdir('data')
            id = input('Please input your id: ')
            if len(id) == 8:
                name = input('Please input your name: ')
                print('Waiting...')
                parse_web(id, name)
            else:
                print('id is not legal.')
        elif option == '2':
            files = os.listdir('data')
            if len(files) != 2:
                print('Error! Data directories must have two habit data.')
            else:
                file1 = 'data/' + files[0]
                file2 = 'data/' + files[1]
                print('{0}-{1}: {2}'.format(files[0].split('.')[0],
                                            files[1].split('.')[0],
                                            compute_similarity(file1, file2)))
        end = input('Continue?(y/n)')
        if end.lower() == 'n':
            break

