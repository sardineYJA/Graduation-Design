import csv
import jieba.posseg as pseg
import os
import random


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 分词并标注，用于 NeuroNER
def ner_label(file_path, attr, save_path):
    with open(file_path, 'r', encoding='GBK') as csvfile:
        reader = csv.reader(csvfile)
        row = [row for row in reader if len(row) != 0]
        random.shuffle(row)        # 打乱list中的顺序
    content = [i[0] for i in row]  # 第一列为文本内容
    label = [i[1] for i in row]    # 第二列为标签
    num = len(row)                 # 句子数目

    result = ''
    for k in range(0, num):
        count = 0
        words = pseg.cut(content[k])  # 结巴分词
        mark = label[k]
        for w in words:  # 按照词在句子中的位置进行标注
            count += 1
            if count == 1:
                marks = 'B-' + mark
                result += str(w.word) + " " + str(w.flag) + " " + marks + "\n"
            else:
                marks = 'I-' + mark
                result += str(w.word) + " " + str(w.flag) + " " + marks + "\n"
        result += "，" + " " + "wd" + " " + "O" + "\n"
        result += "\n"
    f = open(save_path + attr + '_IOB.txt', 'w', encoding='utf-8')
    f.write(result)
    f.close()


def IOB_all_file(file_dir, save_path):
    files = file_name(file_dir)
    for f in files:
        attr = f.split('_')[0]
        ner_label(file_dir + f, attr, save_path)
        print('完成对', file_dir + f, '的IOB标注')


if __name__ == '__main__':

    root_path = '等宽离散化标注/'
    file_dir = root_path + 'merge_all-cut/'
    save_path = root_path + 'IOB_label-cut/'
    IOB_all_file(file_dir, save_path)

    root_path = '等宽离散化标注/'
    file_dir = root_path + 'merge_all-nocut/'
    save_path = root_path + 'IOB_label-nocut/'
    IOB_all_file(file_dir, save_path)

    root_path = '等频离散化标注/'
    file_dir = root_path + 'merge_all-cut/'
    save_path = root_path + 'IOB_label-cut/'
    IOB_all_file(file_dir, save_path)

    root_path = '等频离散化标注/'
    file_dir = root_path + 'merge_all-nocut/'
    save_path = root_path + 'IOB_label-nocut/'
    IOB_all_file(file_dir, save_path)
    print('OK')
