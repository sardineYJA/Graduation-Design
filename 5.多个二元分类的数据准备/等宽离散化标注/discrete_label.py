import pandas as pd
import csv
import os


# 根据attr_value值标注file_name文件
def label_file(file_name, attr, attr_value):
    file_path = '../related_csv-nocut/' + file_name + '_related.csv'
    save_path = 'discrete_label-nocut/' + attr + '_label/'
    save_file = save_path + file_name + '_' + attr + '_label.csv'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    reader = csv.reader(open(file_path, encoding='GBK'))
    column = [row for row in reader]
    f = open(save_file, 'w', encoding='GBK')
    attr_value = str(attr_value.tolist())
    for col in column:
        f.write(col[0] + ',' + str(attr_value) + '\n')
    f.close


def discrete_label(attr_csv):
    data = pd.read_csv(attr_csv, encoding='GBK', index_col='Number')
    for n in range(214):    # 共214款
        file_name = data.iloc[n].name
        for attr in data.iloc[n].index:
            print(file_name, '进行属性', attr, '的标注')
            label_file(file_name, attr, data.iloc[n][attr])
            print('......................完成！')


if __name__ == '__main__':
    attr_csv = 'absolute_attribute_trans_cut.csv'
    discrete_label(attr_csv)
    print('OK')
