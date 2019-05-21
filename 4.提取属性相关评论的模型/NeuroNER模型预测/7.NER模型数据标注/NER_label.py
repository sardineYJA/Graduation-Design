import csv
import jieba.posseg as pseg
import os


# 分词并标注，用于 NeuroNER
def ner_label(csv_file, save_txt):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        row = [row for row in reader]
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
    f = open(save_txt, 'w', encoding='utf-8')
    f.write(result)
    f.close()
    print('分词并标注完成！')


# 格式NER.txt文件
def format_NER_file(temp_file, save_txt):
    # 每1000行增加分隔符 -DOCSTART- -X- -X- O
    f1 = open(temp_file, 'r', encoding='utf-8')
    f2 = open('NER_2.txt', 'w', encoding='utf-8')
    line_num = 0
    for line in f1:
        line_num += 1
        f2.write(line)
        if line_num >= 1000:
            line_sp = line.strip().split(' ')
            if len(line_sp) == 3:
                if line_sp[2] == 'O':
                    f2.write("\n")
                    f2.write('-DOCSTART- -X- -X- O')
                    f2.write('\n')
                    line_num = 0
            else:
                f2.write('-DOCSTART- -X- -X- O')
                f2.write('\n')
                line_num = 0
    f1.close()
    f2.close()
    print('成功添加分隔符！')

    # 检查是否存在两个连续空行
    f_r = open('NER_2.txt', 'r', encoding='utf-8')
    f_w = open(save_txt, 'w', encoding='utf-8')
    previous_token_label = 'O'
    count = 0
    for line in f_r:
        count += 1
        if line.find('-DOCSTART-') != -1:
            f_w.write(line)
            continue

        line_sp = line.strip().split(' ')
        if len(line_sp) <= 2 and previous_token_label == "O":
            f_w.write(line)
        elif len(line_sp) == 3:
            f_w.write(line)
            if line_sp[2] != "O":
                previous_token_label = line_sp[2][:2]
            else:
                previous_token_label = "O"
        else:
            print(len(line_sp))
            print("%d error %s" % (count, line))
    f_r.close()
    f_w.close()
    print("完成去掉多余的空行操作！")

    # 删除中间文件
    os.remove(temp_file)
    os.remove('NER_2.txt')


if __name__ == '__main__':
    csv_file = 'new_cut_train.csv'
    temp_file = 'temp.txt'
    save_txt = 'NER-cut.txt'
    ner_label(csv_file, temp_file)
    format_NER_file(temp_file, save_txt)
    print('运行成功')

    csv_file = 'new_nocut_train.csv '
    temp_file = 'temp.txt'
    save_txt = 'NER-nocut.txt'
    ner_label(csv_file, temp_file)
    format_NER_file(temp_file, save_txt)
    print('运行成功')
