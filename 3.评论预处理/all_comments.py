import os
import pandas as pd


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)
        # print(dirs)     # 打印root目录下的文件夹
        # print(files)    # 打印root目录下的所有文件名
        return files


# 只提取评论，至于点赞数，时间等属性暂时先不理
def all_comments(path):
    names = file_name(path)
    for name in names:
        with open(path + name) as f:
            data = pd.read_csv(f)
            data['内容'].to_csv('评论总和/'+name, encoding='GBK', index=False)
        print(name, ' 提取成功')


if __name__ == '__main__':
    path = 'all_comments/'
    all_comments(path)
    print('OK')
