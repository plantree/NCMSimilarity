#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 2017/12/22 11:00

@author: Lucifer
@site: plantree.me
@email: wpy1174555847@outlook.com
"""

from bs4 import BeautifulSoup


def parse_html(html):
    bsObj = BeautifulSoup(html, 'lxml')
    try:
        songs = bsObj.find('div', {'id': 'm-record'}).find_all('li')
    except AttributeError:
        print('Sorry! Something wrong.')
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
            if count == '':
                count = -1
            item = {'order': int(order), 'id': songId, 'name': songName, 'singer': singer, 'count': int(count)}
            songList.append(item)
    return songList


def dot(x, y):
    # compute two vector's dot mulitiple
    sum = 0
    if len(x) == len(y):
        for i in range(len(x)):
            sum += x[i] * y[i]
        return sum
    else:
        return