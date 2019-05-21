# -*- coding: utf-8 -*-
from sklearn import svm
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
import numpy
from sklearn.externals import joblib   # 保存模型
import pickle                          # 保存TF-IDF模型
import csv
import os


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 分词
def comma_tokenizer(x): return jieba.cut(x, cut_all=True)


# 得到准确率和召回率
def evaluate(actual, pred):
    m_precision = metrics.precision_score(actual, pred, average='macro')
    m_recall = metrics.recall_score(actual, pred, average='macro')
    print('precision:{0:.3f}'.format(m_precision))
    print('recall:{0:0.3f}'.format(m_recall))
    print('f1_score:{0:0.3f}'.format(2 * m_recall *
                                     m_precision / (m_recall + m_precision)))
    print('\n')


# 创建svm分类器
def train_clf(train_data, train_tags, model_file):
    clf = svm.SVC(C=10.0, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3,
                  gamma='auto', kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True,
                  tol=0.001, verbose=False)
    clf.fit(train_data, numpy.asarray(train_tags))  # list转array

    joblib.dump(clf, model_file)
    print('模型保存成功')
    return clf


# 转换成词向量
def covectorize(train_words, test_words, tfidf, feature_path):
    if tfidf == 1:
        v = TfidfVectorizer(tokenizer=comma_tokenizer, binary=False,
                            decode_error='replace', stop_words='english')
        feature_file = feature_path + 'tfidf.pkl'
    else:
        v = CountVectorizer(tokenizer=comma_tokenizer, binary=False,
                            decode_error='replace', stop_words='english')
        feature_file = feature_path + 'count.pkl'
    train_data = v.fit_transform(train_words)
    # (0, 309)	1     0表示行号，309表示次分词的序号，1表示出现次数
    # (0, 326)	1
    # (1, 100)	1
    # (1, 103)	1
    test_data = v.transform(test_words)
    with open(feature_file, 'wb') as fw:
        pickle.dump(v.vocabulary_, fw)
        print('保存特征成功')
    return train_data, test_data


# 训练模型函数，train_file为训练文件，model_file为模型保存文件，tfidf转换词向量方式
def train_model(train_file, model_file, tfidf, feature_path):
    reader = csv.reader(open(train_file, encoding='GBK'))
    column = [row for row in reader]
    contents = [i[0] for i in column]
    labs = [i[1] for i in column]

    # 切分数据集
    train_num = int(len(contents) * 0.7)
    train_words = contents[:train_num]
    test_words = contents[train_num:]
    train_tags = labs[:train_num]
    test_tags = labs[train_num:]

    # 转换成词向量
    train_data, test_data = covectorize(
        train_words, test_words, tfidf, feature_path)
    # print(test_data)
    # print(type(test_data)) #<class 'scipy.sparse.csr.csr_matrix'>

    clf = train_clf(train_data, train_tags, model_file)  # 训练模型

    re = clf.predict(test_data)  # 得到预测标签
    # print(re)                  # [0 1 0 0 ..... 1 0 1 0]
    evaluate(numpy.asarray(test_tags), re)  # 准确率，召回率


# ############################# # 分别训练模型
def train1(root_path):
    # 分句，TF-IDF+SVM模型训练
    train_path = 'merge_all-cut/'
    model_path = 'model-cut/'
    for name in file_name(root_path + train_path):
        train_file = root_path + train_path + name
        attr = name.split('_')[0]
        print('分句：', attr, 'TF-IDF')
        model_file = root_path + model_path + attr + '_cut_tfidf.model'
        tfidf = 1
        feature_path = root_path + model_path + attr + '_cut_'
        train_model(train_file, model_file, tfidf, feature_path)


def train2(root_path):
    # 分句，Count+SVM模型训练
    train_path = 'merge_all-cut/'
    model_path = 'model-cut/'
    for name in file_name(root_path + train_path):
        train_file = root_path + train_path + name
        attr = name.split('_')[0]
        print('分句：', attr, 'Count')
        model_file = root_path + model_path + attr + '_cut_count.model'
        tfidf = 0
        feature_path = root_path + model_path + attr + '_cut_'
        train_model(train_file, model_file, tfidf, feature_path)


def train3(root_path):
    # 未分句，TF-IDF+SVM模型训练
    train_path = 'merge_all-nocut/'
    model_path = 'model-nocut/'
    for name in file_name(root_path + train_path):
        train_file = root_path + train_path + name
        attr = name.split('_')[0]
        print('未分句：', attr, 'TF-IDF')
        model_file = root_path + model_path + attr + '_nocut_tfidf.model'
        tfidf = 1
        feature_path = root_path + model_path + attr + '_nocut_'
        train_model(train_file, model_file, tfidf, feature_path)


def train4(root_path):
    # 未分句，Count+SVM模型训练
    train_path = 'merge_all-nocut/'
    model_path = 'model-nocut/'
    for name in file_name(root_path + train_path):
        train_file = root_path + train_path + name
        attr = name.split('_')[0]
        print('未分句：', attr, 'Count')
        model_file = root_path + model_path + attr + '_nocut_count.model'
        tfidf = 0
        feature_path = root_path + model_path + attr + '_nocut_'
        train_model(train_file, model_file, tfidf, feature_path)


if __name__ == '__main__':
    root_path = '等宽离散化标注/'
    train1(root_path)
    train2(root_path)
    train3(root_path)
    train4(root_path)
    print('OK')

    root_path = '等频离散化标注/'
    train1(root_path)
    train2(root_path)
    train3(root_path)
    train4(root_path)
    print('OK')
