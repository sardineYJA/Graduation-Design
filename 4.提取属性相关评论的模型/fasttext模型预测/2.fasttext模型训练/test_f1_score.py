import os
import fasttext
import jieba
import csv


# 计算P,R,f1
def static_P_R_F1(model_file, predict_file):

    reader = csv.reader(open(predict_file, encoding='GBK'))
    column = [row for row in reader]
    content = [i[0] for i in column]
    manual_lab = [i[1] for i in column]

    # 分词
    string_list = []
    lens = len(column)
    for i in range(lens):
        result = ''
        for j in jieba.lcut(content[i]):
            result = result + j + ' '
        result = result.rstrip()    # 去掉尾空格
        string_list.append(result)

    labs = predict(model_file, string_list)

    TP = 0
    FP = 0
    FN = 0
    TN = 0
    for i in range(lens):
        if manual_lab[i] == 'rel' and labs[i][0][0] == 'rel':
            TP = TP + 1
        if manual_lab[i] == 'irr' and labs[i][0][0] == 'rel':
            FP = FP + 1
        if manual_lab[i] == 'rel' and labs[i][0][0] == 'irr':
            FN = FN + 1
        if manual_lab[i] == 'irr' and labs[i][0][0] == 'irr':
            TN = TN + 1
    print('TP=', TP, ' FP=', FP, ' FN=', FN, ' TN=', TN)
    P = TP / (TP + FP)
    R = TP / (TP + FN)
    print("precision: ", P)
    print("recall: ", R)
    print("f1_score: ", 2 * P * R / (P + R))

    print(model_file, ' --------------- 完成')


def predict(model_file, string_list):
    classifier = fasttext.load_model(
        model_file, label_prefix='__label__')
    labs = classifier.predict_proba(string_list, k=1)
    return labs


if __name__ == '__main__':

    model_file = 'new_cut_train/model.bin'
    predict_file = 'test_f1_score/new_cut_train.csv'
    static_P_R_F1(model_file, predict_file)
    print('OK')

    model_file = 'new_nocut_train/model.bin'
    predict_file = 'test_f1_score/new_nocut_train.csv'
    static_P_R_F1(model_file, predict_file)
    print('OK')
