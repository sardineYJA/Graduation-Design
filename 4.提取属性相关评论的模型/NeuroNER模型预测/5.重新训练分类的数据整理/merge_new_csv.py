import os
import pandas as pd
import csv
import random


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


def merge_new_csv(file_dir, new_file):
    all_files = file_name(file_dir)
    for name in all_files:
        file_path = file_dir + name
        data = pd.read_csv(file_path, encoding='GBK')
        data.to_csv(new_file, mode='a', index=False, encoding='GBK')
        print(name, '---完成')


# 打乱csv文件中数据的排序
def csv_unsort(csv_file, save_file):
    with open(csv_file, 'r', encoding='GBK') as csvfile:
        reader = csv.reader(csvfile)
        row = [row for row in reader if len(row) != 0]
        random.shuffle(row)  # 打乱list中的顺序
    content = [i[0] for i in row]  # 第一列为文本内容
    label = [i[1] for i in row]    # 第二列为标签
    num = len(row)                 # 句子数目

    f = open(save_file, 'a', encoding='GBK')
    for i in range(num):
        f.write(content[i]+','+label[i]+'\n')
    f.close()


if __name__ == '__main__':
    # new_file = 'new_cut_train.csv'
    # file_dir = 'deploy_csv-cut/'
    # merge_new_csv(file_dir, new_file)
    # file_dir = 'related_all_csv-cut/'
    # merge_new_csv(file_dir, new_file)

    # new_file = 'new_nocut_train.csv'
    # file_dir = 'deploy_csv-nocut/'
    # merge_new_csv(file_dir, new_file)
    # file_dir = 'related_all_csv-nocut/'
    # merge_new_csv(file_dir, new_file)

    # 打乱顺序
    csv_file = 'new_nocut_train.csv'
    save_file = 's.csv'
    csv_unsort(csv_file, save_file)
    print('OK')
