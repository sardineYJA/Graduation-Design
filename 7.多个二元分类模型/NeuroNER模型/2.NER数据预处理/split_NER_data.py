
import os


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 切割格式化NER.txt，得到训练集为8：1：1
def split_NER_data(file_path, attr, save_path):
    train_name = 'train.txt'   # 训练集
    valid_name = 'valid.txt'   # 验证集
    test_name = 'test.txt'     # 测试集
    save_path = save_path + 'split_IOB_' + attr + '/'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    f1 = open(file_path, 'r', encoding='utf-8')
    f2 = open(file_path, 'r', encoding='utf-8')
    f_train = open(save_path + train_name, 'w', encoding='utf-8')
    f_valid = open(save_path + valid_name, 'w', encoding='utf-8')
    f_test = open(save_path + test_name, 'w', encoding='utf-8')

    # 文件总行数
    line_num = 0
    for _ in f1:
        line_num += 1
    print('行数：', line_num)
    train_num = int(line_num * 0.7)
    print('Train 行数：', train_num)
    valid_num = int(line_num * 0.1)
    print('Valid 行数：', valid_num)
    print('Test 行数：', line_num - train_num - valid_num)

    count_num = 0
    count_1 = 0
    for line_train in f2:
        count_num += 1
        if count_num <= train_num:
            f_train.write(line_train)
        else:
            line_sp = line_train.strip().split(' ')
            if len(line_sp) == 3:
                f_train.write(line_train)
            else:
                break
    for line_valid in f2:
        count_1 += 1
        if count_1 <= valid_num:
            f_valid.write(line_valid)
        else:
            line_sp = line_valid.strip().split(' ')
            if len(line_sp) == 3:
                f_valid.write(line_valid)
            else:
                break
    for line_test in f2:
        f_test.write(line_test)


def split_all(file_dir, save_path):
    files = file_name(file_dir)
    for f in files:
        attr = f.split('_')[0]
        split_NER_data(file_dir + f, attr, save_path)
        print(file_dir + f, '完成切割')


if __name__ == '__main__':
    root_path = '等宽离散化标注/'
    file_dir = root_path + 'IOB_label-cut/'
    save_path = root_path + 'split_IOB_label-cut/'
    split_all(file_dir, save_path)
    print('OK')

    root_path = '等宽离散化标注/'
    file_dir = root_path + 'IOB_label-nocut/'
    save_path = root_path + 'split_IOB_label-nocut/'
    split_all(file_dir, save_path)
    print('OK')

    root_path = '等频离散化标注/'
    file_dir = root_path + 'IOB_label-cut/'
    save_path = root_path + 'split_IOB_label-cut/'
    split_all(file_dir, save_path)
    print('OK')

    root_path = '等频离散化标注/'
    file_dir = root_path + 'IOB_label-nocut/'
    save_path = root_path + 'split_IOB_label-nocut/'
    split_all(file_dir, save_path)
    print('OK')

