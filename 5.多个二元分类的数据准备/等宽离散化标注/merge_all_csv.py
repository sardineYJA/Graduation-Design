import os
import pandas as pd


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


def merge_all_csv(file_dir, attr, save_path):
    all_files = file_name(file_dir)
    save_file = save_path + attr + '_all.csv'

    for name in all_files:
        attr_file = file_dir + name
        print(attr_file)
        # 文件路径有中文，使用read_csv()先使用open()函数
        data = pd.read_csv(open(attr_file, 'r', encoding='GBK'))
        data.to_csv(save_file, mode='a', index=False, encoding='GBK')


# 九个属性分别合并自己文件夹中的所有文件
if __name__ == '__main__':

    attrs = ['System', 'CPU', 'RAM', 'ROM', 'Price',
             'Screen', 'Solid', 'Time', "Weight"]

    save_path = 'merge_all-cut/'
    file_path = 'discrete_label-cut/'
    for attr in attrs:
        file_dir = file_path + attr + '_label/'
        print('合并', file_dir, '中')
        merge_all_csv(file_dir, attr, save_path)

    save_path = 'merge_all-nocut/'
    file_path = 'discrete_label-nocut/'
    for attr in attrs:
        file_dir = file_path + attr + '_label/'
        print('合并', file_dir, '中')
        merge_all_csv(file_dir, attr, save_path)

    print('OK')
