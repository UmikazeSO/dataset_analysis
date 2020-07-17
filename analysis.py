# coding:utf-8
import xlrd
import os
import xlwt
import pandas as pd
import xml.etree.cElementTree as ET
import numpy as np


def listdir(path):
    jpg_name = []
    xml_name = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.jpg':
            jpg_name.append(file)
        elif os.path.splitext(file)[1] == '.xml':
            xml_name.append(file)
    return xml_name


def main():
    col_num, row_mark, booksheet, array = read_xlsx('analysis.xlsx')
    for i in range(len(col_num)):
        xml_name = listdir('batch/' + str(int(i + 1)))
        for j in range(len(xml_name)):
            xml_file = xml_name[j]
            process_xml(i, xml_file, row_mark, booksheet, array)
    write_xlsx(array, 'results.xlsx')
    return array


def process_xml(i, xml_name, row_mark, booksheet, array):
    tree = ET.parse(os.path.join('../6.16_data', xml_name))
    root = tree.getroot()
    childnodes = root.getchildren()
    if len(childnodes) == 0:
        print("error in {}".format(xml_name))
    else:
        for child in childnodes:
            if child.tag == 'object':
                object_children = child.getchildren()
                mark = object_children[0].text
                for marks in range(len(row_mark)):
                    if mark == row_mark[marks]:
                        num = row_mark.index(mark)
                        #a = i + 1
                        #b = num + 3
                        #ori = booksheet.cell(a, b)
                        #booksheet.write(a, b, ori + 1)
                        array[i, num] = array[i, num] + 1


def read_xlsx(xlsx_name):
    # 读取xlsx的数据
    workbook = xlrd.open_workbook(xlsx_name)
    booksheet = workbook.sheet_by_name('Sheet1')
    # 读第一列和第一行数据，文件夹和标注代号,储存为字符串
    col_0 = booksheet.col_values(0, 1)
    col_num = [str(int(x)) for x in col_0]
    row_0 = booksheet.row_values(0, 1)
    row_mark = [str(int(x)) for x in row_0]
    print(col_num, row_mark)
    array = np.zeros((len(col_num), len(row_mark)))

    return col_num, row_mark, booksheet, array


def write_xlsx(array, xlsx_name):
    data = pd.DataFrame(array)
    writer = pd.ExcelWriter(xlsx_name)
    data.to_excel(writer, 'Sheet2', float_format='%.5f')
    writer.save()

    writer.close()


if __name__ == '__main__':
    main()
