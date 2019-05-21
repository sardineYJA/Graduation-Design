# -*- coding: utf-8 -*-
from sklearn import datasets
import random
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy
from sklearn.externals import joblib   # 保存模型
import os
import csv
import pickle


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 保存所有预测
def save_all_predict(file_path, model_file, save_path, feature_path):
    clf_model = joblib.load(model_file)
    for name in file_name(file_path):
        print(name)
        reader = csv.reader(open(file_path + name, encoding='GBK'))
        column = [row for row in reader]
        content = [i[0] for i in column]

        tfidf = 0    # TF-IDF或者Count(使用的是count.model所以是0)
        data_vec = covectorize(content, tfidf, feature_path)
        predict_result = clf_model.predict(data_vec)

        result = ''
        for i in range(len(content)):
            result = result + content[i] + ',' + predict_result[i] + '\n'
        f = open(save_path + name, 'w', encoding='GBK')
        f.write(result)
        f.close


# 完成打开文件后的准备工作
def comma_tokenizer(x): return jieba.cut(x, cut_all=True)


# 转换成词向量
def covectorize(data_words, tfidf, feature_path):
    if tfidf == 1:
        feature_file = feature_path + 'tfidf.pkl'
        v = TfidfVectorizer(tokenizer=comma_tokenizer, decode_error="replace",
                            vocabulary=pickle.load(open(feature_file, "rb")))
    else:
        feature_file = feature_path + 'count.pkl'
        v = CountVectorizer(tokenizer=comma_tokenizer, decode_error="replace",
                            vocabulary=pickle.load(open(feature_file, "rb")))
    data_vec = v.transform(data_words)
    return data_vec


if __name__ == '__main__':
    # file_path = '评论总和-分句/'
    # model_file = 'train_cut_model/cut_count.model'
    # save_path = 'deploy_csv-cut/'
    # feature_path = 'train_cut_model/'
    # save_all_predict(file_path, model_file, save_path, feature_path)
    # print('OK')

    file_path = '评论总和-未分句/'
    model_file = 'train_nocut_model/nocut_count.model'
    save_path = 'deploy_csv-nocut/'
    feature_path = 'train_nocut_model/'
    save_all_predict(file_path, model_file, save_path, feature_path)
    print('OK')
