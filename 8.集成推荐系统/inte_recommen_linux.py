import os
import fasttext
import jieba
import pandas as pd


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 获取预测属性值
def get_predict(attrs, model_path, string):
    # str_list = ['我 要 一款 内存 大 运行 快 的 苹果 电脑']
    str_list = []
    result = ''
    for j in jieba.lcut(string):
        result = result + j + ' '
    result = result.strip()
    str_list.append(result)
    print(str_list)

    attrs_predict = []
    for attr in attrs:
        print(attr, '预测：')
        classifier = fasttext.load_model(
            model_path + attr + "_model.bin", label_prefix='__label__')
        lab = classifier.predict_proba(str_list, k=1)
        print(lab)     # [[('2', 0.976563)]]
        attrs_predict.append(lab[0][0][0])
    print(attrs_predict)
    return attrs_predict


# 获取推荐列表
def get_recommend(attrs_weights, string):
    # 绝对属性权重
    attrs_weights = get_attr_weights()

    # 预测用户需求文本
    attrs = ['System', 'CPU', 'RAM', 'ROM', 'Solid',
             'Screen', 'Time', 'Weight', "Price"]
    model_path = 'model-cut-Linux/'
    attrs_predict = get_predict(attrs, model_path, string)

    # 权值
    recom_weights = []
    for i in range(len(attrs)):
        recom_weights.append(attrs_weights[i] * int(attrs_predict[i]))
    print(recom_weights)

    # 计算与每个品牌的相似度
    df = pd.read_csv('absolute_attribute_trans_cut.csv', encoding='GBK')
    # print(df)
    # print(df.values)

    all_list = []
    for i in df.values:
        # print(i[0], end=' : ')
        distence = 0
        for j in range(len(attrs)):
            distence = distence + (recom_weights[j] - i[j + 1])**2
        # print(distence)
        all_list.append((i[0], distence))
    all_list.sort(key=lambda x: (x[1], x[0]))  # 根据距离排升序
    for i in all_list:
        print(i)

    # 推荐TopN
    n = 10
    return all_list[0:n]


# 获取需求文本
def get_demand_text():
    string = '我要一款内存大运行快的笔记本电脑'
    # string = ''
    return string


# 获取绝对属性权重
def get_attr_weights():
    attrs_weights = [0.3, 0.7, 0.4, 0.9, 0.8, 0.3, 0.2, 0.3, 0.5]
    # attrs_weights = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    return attrs_weights


if __name__ == '__main__':
    string = get_demand_text()
    if string.strip() == '':
        print('请输入需求文本')
    attrs_weights = get_attr_weights()
    recom_list = get_recommend(attrs_weights, string)
    print('OK')
