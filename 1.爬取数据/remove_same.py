import os
import pandas as pd
import json
import shutil
import csv

# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 查重，匹配每款评论的前10条评论
def find_same(path):
    init_file()
    names = file_name(path)
    all = {}          # 用于保存每个评论文件的前10条评论
    for i in names:
        with open(path + i) as f:
            data = pd.read_csv(f)
            all[i] = data['评论id'].head(10)
            # 判断评论文件是否一致根据前10个评论的id

    for i in names:
        for j in names:
            if i == j:
                continue
            else:
                # 找出评论一致的电脑id,保存到json文件
                if compare_ndarray(all[i].values, all[j].values):
                    print(i, '-------', j)
                    id1 = i.split('_')[1]
                    id2 = j.split('_')[1]
                    if id_is_deal(id1) and id_is_deal(id2):
                        pass
                    else:
                        if id_is_deal(id1):
                            save_same_id(id1, id2)
                            write_id(id2)

                        elif id_is_deal(id2):
                            save_same_id(id2, id1)
                            write_id(id1)
                        else:
                            save_same_id(id1, id2)
                            write_id(id1)
                            write_id(id2)
    print('查重完成')


# 判断两个数组是否完全一致
def compare_ndarray(a_ndarray, b_ndarray):
    for i in range(10):
        try:
            if a_ndarray[i] != b_ndarray[i]:
                return False
        except:
            return False
    return True


# 相同评论的id保存到json文件中，用于删除
def save_same_id(key, id):
    with open('same_comments_id.json', "r") as f:
        id_dict = json.load(f)
        newlist = []
        if key not in id_dict.keys():
            newlist.append(id)
            id_dict[key] = newlist
        else:
            newlist = id_dict[key]
            newlist.append(id)
            id_dict[key] = newlist
    with open('same_comments_id.json', "w") as f:
        json.dump(id_dict, f, ensure_ascii=False)


# 判断此id是否已经经过相同评论的检查
def id_is_deal(id):
    with open('has_check_id.txt', 'r') as f:
        for eachline in f:
            if eachline.strip() == id:
                return True
    return False


# 检查过评论的id写进txt
def write_id(id):
    with open('has_check_id.txt', 'a') as f:
            f.write(id+'\n')


# 初始化文件
def init_file():
    with open("same_comments_id.json", "w") as f:
        dict = {}
        json.dump(dict, f, ensure_ascii=False)
    with open('has_check_id.txt', 'w') as f:
        print()


# 删除相同评论的品牌，包括评论，图片，参数
def delete_same():
    with open('same_comments_id.json', "r") as f:
        id_dict = json.load(f)
    num = 0
    for key in id_dict:
        for pid in id_dict[key]:
            for i in file_name('评论总和/'):
                t = i.split('_')
                if pid == t[1]:
                    # 删除文件
                    shutil.rmtree('京东/'+t[0]+'/'+t[0]+'_'+t[1])
                    os.remove('评论总和/'+t[0]+'_'+t[1]+'_comments.csv')
                    os.remove('参数总和/'+t[0]+'_'+t[1]+'_params.csv')
                    num = num + 1
                    print('成功删除', t[0] + '_' + t[1])
    print('删除成功,共', num, '个')


# 删除评论过少的品牌
def delete_too_little(path):
    names = file_name(path)
    num = 0
    for name in names:
        with open(path+name, 'r', encoding='GBK') as f:
            data = pd.read_csv(f)
            if len(data) < 400:
                t = name.split('_')
                shutil.rmtree('京东/'+t[0]+'/'+t[0]+'_'+t[1])
                os.remove('评论总和/'+t[0]+'_'+t[1]+'_comments.csv')
                os.remove('参数总和/'+t[0]+'_'+t[1]+'_params.csv')
                print('成功删除', t[0]+'_'+t[1])
                num = num + 1
    print('一共删除', num, '款')


if __name__ == '__main__':

    # 查重
    path = '评论总和44/'

    # 获取相同评论的id号
    # find_same(path)

    # 删除评论，参数，图片
    # delete_same()

    # 删除评论过少的
    # delete_too_little(path)
    # 注意如果读取此文件夹中文件，不可对文件夹中的文件进行删除


