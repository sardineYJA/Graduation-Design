import csv
import jieba.posseg as pseg


# 将其转换为GloVe工具处理的格式
def get_glove_data(csv_file, save_txt):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        row = [row for row in reader]
    content = [i[0] for i in row]  # 第一列为文本内容
    num = len(row)                 # 句子数目
    result = ''
    for k in range(num):
        words = pseg.cut(content[k])  # 结巴分词
        for w in words:
            result += str(w.word) + " "
    f = open(save_txt, 'w', encoding='utf-8')  # 将结果保存到另一个文档中
    f.write(result)
    f.close()
    print('分词完成！')


if __name__ == '__main__':
    csv_file = 'new_cut_train.csv'
    save_txt = 'glove-cut.txt'
    get_glove_data(csv_file, save_txt)
    print('运行成功')

    csv_file = 'new_nocut_train.csv'
    save_txt = 'glove-nocut.txt'
    get_glove_data(csv_file, save_txt)
    print('运行成功')
