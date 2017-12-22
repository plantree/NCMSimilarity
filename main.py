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


def parse_and_create(fileName):
    try:
        f = open(fileName, 'rb')
    except IOError:
        print('File is not found!')
        return
    else:
        html = f.read()
        bsObj = BeautifulSoup(html, 'lxml')
        try:
            songs = bsObj.find('div', {'id': 'm-record'}).find_all('li')
        except AttributeError:
            print('Sorry! The file is not deseired.')
            return
        else:
            songList = []
            for song in songs:
                order = song.find('span', {'class': 'num'}).get_text()[:-1]
                songInfo = song.find('span', {'class': 'txt'})
                songId = songInfo.find('a').attrs['href'].split('=')[1]
                songName = songInfo.find('b').get_text()
                index = songName.find('cover')
                if index != -1:
                    songName = songName.split('(')[0]
                songName = songName.strip()
                singer = songInfo.find('span', {'class': 'ar s-fc8'}).get_text()[2:]
                count = song.find('div', {'class': 'tops'}).get_text()[:-1]
                item = {'order': int(order), 'id': songId, 'name': songName, 'singer': singer, 'count': int(count)}
                songList.append(item)
            songList = json.dumps(songList)
            with open(fileName.replace('html', 'habit'), 'w') as fp:
                fp.write(songList)
    finally:
        f.close()


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
    print(list1, list1)
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
    print(compute_similarity('./data/wangpengyuan.habit', './data/zhangbeichen.habit'))