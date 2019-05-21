import csv
import os
import pandas as pd


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 读取所有参数文件
def read_params(path):
    attr = ['Number', 'System', 'CPU', 'RAM', 'ROM', 'Solid', 'Screen', 'Time', 'Weight' ,'Price']

    df = pd.DataFrame(columns=attr)
    for name in file_name(path):
        title = name.split('_')
        Number = title[0] + '_' + title[1]
        reader = csv.reader(open(path + name, encoding='GBK'))
        column = [row for row in reader]

        print('----------------', Number, '----------------')
        if title[0] == 'Apple':
            System = 'mac'
        else:
            System = 'windows'
        attr_list = [Number, System, '', '', '', '', '', '', '', '']  # 默认填充

        for col in column:
            if col[0] == 'CPU类型':
                attr_list[2] = attr_list[2] + col[1]
            if col[0] == 'CPU型号':
                attr_list[2] = attr_list[2] + col[1]
            if col[0] == 'CPU速度':
                attr_list[2] = attr_list[2] + col[1]
            if col[0] == '内存容量':
                attr_list[3] = attr_list[3] + col[1]
            if col[0] == '内存类型':
                attr_list[3] = attr_list[3] + col[1]
            if col[0] == '硬盘容量':
                attr_list[4] = col[1]
            if col[0] == '固态硬盘':
                attr_list[5] = col[1]
            if col[0] == '屏幕规格':
                attr_list[6] = col[1]
            if col[0] == '续航时间':
                attr_list[7] = col[1]
            if col[0] == '净重':
                attr_list[8] = col[1]
            if col[0] == '价格':
                attr_list[9] = col[1]

        df.loc[Number] = attr_list
        print(attr_list)

    df.to_csv('absolute_attribute.csv', index=False, encoding='GBK')


if __name__ == '__main__':
    path = '参数总和/'
    read_params(path)
    print('OK')
