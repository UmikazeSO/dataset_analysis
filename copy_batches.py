# coding:utf-8
import xlrd
import os
import xlwt
import shutil
import numpy as np

def read_xlsx(xlsx_name):
    # open xlsx
    workbook = xlrd.open_workbook(xlsx_name)
    booksheet = workbook.sheet_by_name('sheet1')
    # reading column and transforming
    col_0 = booksheet.col_values(0, 1)
    col_0 = col_0[2:-1]
    col_num = [str(int(x)) for x in col_0]
    print(len(col_num))
    for batches in col_num:
        shutil.copytree('batch/' + batches, 'balanced/' + batches)

    return col_num


if __name__ == '__main__':
    read_xlsx("batch统计表.xlsx")