import csv
import os
import jieba
import random


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 对每个csv文件生成fasttext训练数据，并分割训练集，和测试集
def split_csv(path):
    for name in file_name(path):
        print(name)
        train_result = ''
        test_result = ''
        attr = name.split('_')[0]

        reader = csv.reader(open(path + name, encoding='GBK'))
        column = [row for row in reader]
        random.shuffle(column)   # 打乱list中的顺序
        content = [i[0] for i in column]  # 评论
        label = [i[1] for i in column]    # 标签

        # train占70%，test占30%
        lens = len(column)
        for i in range(lens):
            if i < lens * 0.7:
                for j in jieba.lcut(content[i]):
                    train_result = train_result + j + ' '
                train_result += '     __label__' + label[i] + '\n'
            else:
                for j in jieba.lcut(content[i]):
                    test_result = test_result + j + ' '
                test_result += '     __label__' + label[i] + '\n'

        with open('train/' + attr + '_train.txt', 'a', encoding='utf-8') as f:
            f.write(train_result)
        with open('test/' + attr + '_test.txt', 'a', encoding='utf-8') as f:
            f.write(test_result)
        print(name, '------切割完成')


if __name__ == '__main__':
    # path = '等宽离散化标注/merge_all-cut/'
    # path = '等宽离散化标注/merge_all-nocut/'
    # path = '等频离散化标注/merge_all-cut/'
    path = '等频离散化标注/merge_all-nocut/'
    split_csv(path)
    print('OK')
