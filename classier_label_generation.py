# coding:utf-8
import xlrd
import os
import cv2 as cv
import xml.etree.cElementTree as ET
global k
k = 0


def listdir(path):
    jpg_name = []
    xml_name = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.jpg':
            jpg_name.append(file)
        elif os.path.splitext(file)[1] == '.xml':
            xml_name.append(file)
    return jpg_name

def main():

    #读取xlsx的数据
    workbook = xlrd.open_workbook('classification_20.xlsx')
    booksheet = workbook.sheet_by_name('Sheet2')
    # 读两列数据，标签和标注码
    col_0 = booksheet.col_values(0, 1)
    col_ori = [str(int(x)) for x in col_0]
    col_3 = booksheet.col_values(2, 1)
    col_tar = [str(int(x)) for x in col_3]
    print(col_ori, col_tar)
    #读取结束

    filename_list = listdir('samples/')
    generation(col_ori,col_tar,filename_list)

def generation(ori, tar, files):
    for id in range(len(files)):
        process_xml(files[id], ori, tar)


def read_image(img_name):

    path = os.path.join('samples',img_name)
    im = cv.imread(path)
    cv.imshow('asdas',im)
    cv.waitKey(0)

def get_BBox(node):
    return [int(node[0].text),int(node[1].text),int(node[2].text),int(node[3].text)]

def process_xml(img_name, ori, tar):
    im = cv.imread(os.path.join('samples',img_name))
    xml_name = img_name[0:-4] + '.xml'
    tree = ET.parse(os.path.join('samples',xml_name))
    root = tree.getroot()
    childnodes = root.getchildren()
    if len(childnodes) == 0:
        print("error in {}".format(xml_name))
    else:
        k = 0
        for child in childnodes:
            if child.tag == 'object':
                object_children = child.getchildren()
                id = 0
                if object_children[0].text == '0000' or object_children[0].text=='0001' or object_children[0].text == '0002':
                    if not os.path.exists('CNN_datasets/{}'.format('4')):
                        os.makedirs('CNN_datasets/{}'.format('4'))
                    BBox = get_BBox(object_children[4].getchildren())
                    cropper = im[BBox[1]:BBox[3], BBox[0]:BBox[2]]
                    print(img_name[0:-4], ' ', ori[id], ':', BBox)
                    cv.imwrite('CNN_datasets/{}/{}_{}_{}.jpg'.format('4', img_name[0:-4], ori[id], k), cropper)
                    k = k + 1
                else:
                    if object_children[0].text in ori:

                        id = ori.index(object_children[0].text)
                        if not os.path.exists('CNN_datasets/{}'.format(tar[id])):
                            os.makedirs('CNN_datasets/{}'.format(tar[id]))

                        BBox = get_BBox(object_children[4].getchildren())
                        cropper = im[BBox[1]:BBox[3],BBox[0]:BBox[2]]
                        print(img_name[0:-4], ' ',ori[id],':',BBox)
                        cv.imwrite('CNN_datasets/{}/{}_{}_{}.jpg'.format(tar[id],img_name[0:-4], ori[id],k), cropper)
                        k = k + 1
                    else:
                        if not os.path.exists('CNN_datasets/{}'.format('error')):
                            os.makedirs('CNN_datasets/{}'.format('error'))
                        BBox = get_BBox(object_children[4].getchildren())
                        cropper = im[BBox[1]:BBox[3], BBox[0]:BBox[2]]
                        print(img_name[0:-4], ' ', ori[id], ':', BBox)
                        cv.imwrite('CNN_datasets/{}/{}_{}_{}.jpg'.format('error', img_name[0:-4],object_children[0].text, k), cropper)
                        k = k + 1


if __name__=='__main__':
    main()
