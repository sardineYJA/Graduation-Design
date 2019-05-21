import os
import json

root_path = '京东/'
id_file = root_path + 'params_id.json'


# 返回file_dir目录下所有目录的文件名
def dir_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return dirs


# 追加爬取id,用于再次爬取
def add_other_id(key, pro_id, path):
    with open(path, "r") as f:
        id_dict = json.load(f)
        newlist = []
        if key not in id_dict.keys():
            newlist.append(pro_id)
            id_dict[key] = newlist
        else:
            newlist = id_dict[key]
            newlist.append(pro_id)
            id_dict[key] = newlist
    with open(path, "w") as f:
        json.dump(id_dict, f, ensure_ascii=False)


# 解析文件夹名，得到key, id
def parse_dir(file_dir):
    dirs = dir_name(file_dir)
    for d in dirs:
        k = d.split("_")
        add_other_id(k[0], k[1], id_file)


if __name__ == '__main__':

    # 清空，并初始化 params_id.json
    with open(id_file, "w") as f:
        json.dump({}, f, ensure_ascii=False)

    key_dirs = dir_name(root_path)
    for key in key_dirs:
        parse_dir(root_path + key)
    print('OK')
