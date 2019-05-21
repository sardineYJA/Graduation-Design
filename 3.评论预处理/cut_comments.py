import csv
import os
import pandas as pd
import re


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 将评论分句，去掉异常符号
def cut_comments(path):
    save_path = '评论总和-分句/'
    for name in file_name(path):
        save_file = open(save_path + name, 'a', encoding='GBK')
        try:
            with open(path + name) as f:
                data = pd.read_csv(f)
                comments = data['内容']
                for comment in comments:
                    comment = comment.replace(' ', '。')      # 空格替换成。分割
                    comment = comment.replace('&hellip', '')  # 去掉无用符合
                    clauses = re.split(
                        '\n|#|，|。|？|！|；|;|、|\?|!|·|）|（|\"|“|”|\000|,'
                        '|\'|\t|\v|\r|:|：|～|．', comment)
                    for string in clauses:
                        if string == '此用户未填写评价内容' or string == '此用户未及时填写评价内容，系统默认好评！':
                            continue
                        string = remove_unsign(string)
                        if len(string) < 2:  # 初步过滤不超过2个字的评论
                            continue
                        save_file.write(string + '\n')
        except:
            print(name, '---------出现分句失败')
    print('全部分句完成')


# 不分句只去掉异常符号
def nocut_comments(path):
    save_path = '评论总和-未分句/'
    for name in file_name(path):
        reader = csv.reader(open(path + name, encoding='GBK'))
        column = [row for row in reader]
        content = [i[5] for i in column if len(i) == 6]  # 第6列为商品评论
        f = open(save_path+name, 'a', encoding='GBK')
        for string in content[1:]:    # 去掉第一个"内容"
            if string == '此用户未填写评价内容' or string == '此用户未及时填写评价内容，系统默认好评！':
                continue
            string = remove_unsign(string)
            if len(string) < 5:   # 初步过滤不超过5个字的评论
                continue
            f.write(string+'\n')
        print(name, '----完成')


# 去掉句子中的异常符号
def remove_unsign(string):
    symbol = ['，', '。', '！', '、', '^', '_', '.', '？', '～', '~', '●',
              ',', '(', ')', '（', '）', '&', '*', ':', '：', '“', '”',
              ';', '#', '￣', '▽', '\n', '$', 'amp', '@', '/', '!', '；',
              '?', '-', '【', '】', 'hellip', 'rdquo', 'ldquo', ' ']
    for sym in symbol:
        string = string.replace(sym, '')
    return string


if __name__ == '__main__':
    path = '评论总和/'
    # nocut_comments(path)
    # cut_comments(path)
    print('OK')

