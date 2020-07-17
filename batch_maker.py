# coding:utf-8
import xlrd
import os
import cv2 as cv
import xml.etree.cElementTree as ET
import random
import shutil


def main():
    batch_size = 8
    ooo = listdir('../6.16_data/')
    random.shuffle(ooo)
    divide_img(ooo, batch_size)


def listdir(path):
    jpg_name = []
    xml_name = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.jpg':
            jpg_name.append(file)
        elif os.path.splitext(file)[1] == '.xml':
            xml_name.append(file)
    return jpg_name


def divide_img(img_list, batch_size):
    x = batch_size
    n = len(img_list)
    for k in range(n//x):
        if not os.path.exists('batch/{}'.format(k + 1)):
            os.makedirs('batch/{}'.format(k + 1))
        for i in range((k*x),(k*x+x)):
            shutil.copy('../6.16_data/' + img_list[i],'batch/{}'.format(k + 1))
            shutil.copy('../6.16_data/' + img_list[i][0:-4] + '.xml', 'batch/{}'.format(k + 1))


if __name__ == '__main__':
    main()
