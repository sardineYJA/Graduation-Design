
import os
import csv
import jieba


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


def get_glove(file_dir):
    all_files = file_name(file_dir)
    save_file = open('related_glove-nocut.txt', 'w', encoding='utf-8')
    num = 0
    for f in all_files:
        file_path = file_dir + f
        print('合并文件', file_path)
        reader = csv.reader(open(file_path, encoding='GBK'))
        column = [row for row in reader]
        conments = [col[0] for col in column]
        train_result = ''
        # 每句评论分词
        for content in conments:
            for j in jieba.lcut(content):
                train_result = train_result + j + ' '
        save_file.write(train_result)
        num = num + 1
    save_file.close()
    print('一共合并', num, '个文件')


# 九个属性分别合并自己文件夹中的所有文件
if __name__ == '__main__':

    file_dir = 'related_csv-nocut/'
    get_glove(file_dir)

    print('OK')
