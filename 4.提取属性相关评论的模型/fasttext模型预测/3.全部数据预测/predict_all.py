import os
import fasttext
import jieba
import csv


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 保存所有预测
def save_all_predict(file_path, model_path, save_path):
    for name in file_name(file_path):
        print(name)
        reader = csv.reader(open(file_path + name, encoding='GBK'))
        column = [row for row in reader]
        content = [i[0] for i in column]

        string_list = []
        lens = len(column)
        for i in range(lens):
            result = ''

            for j in jieba.lcut(content[i]):
                result = result + j + ' '
            result = result.rstrip()    # 去掉尾空格
            string_list.append(result)

        # 检查是否有过短异常符号或空格打印索引
        for i in range(len(string_list)):
            if len(string_list[i]) < 2:
                print(i)

        labs = predict(model_path, string_list)
        # 解析预测结果，并写进文件
        result = ''
        for i in range(lens):
            result = result + content[i] + ',' + labs[i][0][0] + \
                ',' + str(labs[i][0][1]) + '\n'
        # print(result)
        f = open(save_path + name, 'w', encoding='GBK')
        f.write(result)
        f.close

        print(name, ' --------------- 完成')


def predict(model_path, string_list):
    classifier = fasttext.load_model(
        model_path + "model.bin", label_prefix='__label__')
    labs = classifier.predict_proba(string_list, k=1)
    return labs


if __name__ == '__main__':

    # file_path = '评论总和-分句/'
    # model_path = 'new_cut_train/'
    # save_path = 'deploy_csv-cut/'
    # save_all_predict(file_path, model_path, save_path)
    # print('OK')

    file_path = '评论总和-未分句/'
    model_path = 'new_nocut_train/'
    save_path = 'deploy_csv-nocut/'
    save_all_predict(file_path, model_path, save_path)
    print('OK')
