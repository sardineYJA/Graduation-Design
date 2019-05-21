import pandas as pd
import os


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 统计每个文件的评论数量
def statistics_data(path, save_file):
    name = file_name(path)
    with open(save_file, 'w') as t:
        t.write('评论统计：共'+str(len(name))+'个文件\n')
    sum = 0
    for i in name:
        with open(path + i) as f:
            data = pd.read_csv(f)
            with open(save_file, 'a') as t:
                t.write(i + ' : ' + str(len(data)) + '\n')
            sum = sum+len(data)
    with open(save_file, 'a') as t:
        t.write('统计完成：共'+str(sum)+'条记录')
    print('统计完成')


if __name__ == '__main__':
    path = '评论总和-分句/'
    save_file = 'statistics-cut.txt'
    statistics_data(path, save_file)

    path = '评论总和-未分句/'
    save_file = 'statistics-nocut.txt'
    statistics_data(path, save_file)
