import csv
import os
import jieba


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 评论进行标注，并且分割训练集，和测试集
def format_data(path):
    for name in file_name(path):
        train_result = ''
        test_result = ''

        reader = csv.reader(open(path + name, encoding='GBK'))
        column = [row for row in reader]
        content = [i[0] for i in column]
        labs = [i[1] for i in column]

        lens = len(column)
        for i in range(lens):
            if i < lens * 0.7:
                for j in jieba.lcut(content[i]):
                    train_result = train_result + j + ' '
                train_result += '     __label__' + labs[i] + '\n'
            else:
                for j in jieba.lcut(content[i]):
                    test_result = test_result + j + ' '
                test_result += '     __label__' + labs[i] + '\n'

        with open(path + 'train.txt', 'a', encoding='utf-8') as f:
            f.write(train_result)
        with open(path + 'test.txt', 'a', encoding='utf-8') as f:
            f.write(test_result)
        print(name, '----完成')


# 将csv文件切分：标签+tab+评论，8：1：1
def format_bert(file_name):
    train_result = ''
    test_result = ''
    dev_result = ''

    reader = csv.reader(open(file_name, encoding='GBK'))
    column = [row for row in reader]
    content = [i[0] for i in column]
    labs = [i[1] for i in column]

    lens = len(column)
    for i in range(lens):    # 8:1:1
        if i < lens * 0.8:
            train_result += labs[i] + '\t' + content[i] + '\n'
        elif lens * 0.9 > i > lens * 0.8:
            test_result += labs[i] + '\t' + content[i] + '\n'
        else:
            dev_result += labs[i] + '\t' + content[i] + '\n'

    with open('train.txt', 'a', encoding='utf-8') as f:
        f.write(train_result)
    with open('test.txt', 'a', encoding='utf-8') as f:
        f.write(test_result)
    with open('dev.txt', 'a', encoding='utf-8') as f:
        f.write(dev_result)
    print(file_name, '----完成')


if __name__ == '__main__':
    file_name = 'new_cut_train.csv'
    # format_bert(file_name)
    print('OK')
