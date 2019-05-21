# 切割格式化NER.txt，得到训练集为8：1：1
def split_NER_data(txt_file, save_dir):
    train_path = save_dir + 'train.txt'   # 训练集
    valid_path = save_dir + 'valid.txt'   # 验证集
    test_path = save_dir + 'test.txt'     # 测试集

    f1 = open(txt_file, 'r', encoding='utf-8')
    f2 = open(txt_file, 'r', encoding='utf-8')
    f_train = open(train_path, 'w', encoding='utf-8')
    f_valid = open(valid_path, 'w', encoding='utf-8')
    f_test = open(test_path, 'w', encoding='utf-8')

    # 文件总行数
    line_num = 0
    for _ in f1:
        line_num += 1
    print('行数：', line_num)
    train_num = int(line_num * 0.7)
    print('Train 行数：', train_num)
    valid_num = int(line_num * 0.1)
    print('Valid 行数：', valid_num)

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
    print('切割完成！')


if __name__ == '__main__':
    txt_file = 'NER-cut/NER-cut.txt'
    save_dir = 'NER-cut/'
    split_NER_data(txt_file, save_dir)
    print('运行成功')

    txt_file = 'NER-nocut/NER-nocut.txt'
    save_dir = 'NER-nocut/'
    split_NER_data(txt_file, save_dir)
    print('运行成功')
