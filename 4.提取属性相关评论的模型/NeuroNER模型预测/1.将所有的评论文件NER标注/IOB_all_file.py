import csv
import os
import jieba.posseg as pseg


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 所有的评论按相应格式写到一个txt文件中
def IOB_all_file(path, save_file):
    result = ''
    for name in file_name(path):
        t = name.split('_')   # 解析每个品牌，用于deploy.txt的分割界
        reader = csv.reader(open(path+name))
        column = [row for row in reader]
        content = [i[0] for i in column]
        lens = len(column)

        for k in range(0, lens):
            count = 0
            words = pseg.cut(content[k])  # 分词
            mark = 'rel'     # 为了让文本符合模型的读取格式，先将所有标注为rel或irr标签
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
        result += t[0] + '_' + t[1] + " " + "TAGSTART" + " " + "B-rel" +"\n"
        # 用标记将手机之间的预测数据分离开
        result += "\n"
        print(name, '--完成')

    print('开始写入')
    # 将所有的文件标注后保存到一个txt文本中
    f = open(save_file, 'w', encoding='utf-8')
    f.write(result)


if __name__ == '__main__':

    path = '评论总和-分句/'
    save_file = 'all_deploy-cut.txt'
    IOB_all_file(path, save_file)
    print('OK')

    path = '评论总和-未分句/'
    save_file = 'all_deploy-nocut.txt'
    IOB_all_file(path, save_file)
    print('OK')
