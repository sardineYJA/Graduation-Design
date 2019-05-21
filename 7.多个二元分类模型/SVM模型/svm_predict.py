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


# 预测
def predict(model_path, string, attrs, tfidf, cut):
    for attr in attrs:
        print(attr, end=':')
        model_file = model_path+attr+"_"+cut+'_'+tfidf+'.model'
        feature_file = model_path+attr+'_'+cut+'_'+tfidf+'.pkl'
        clf_model = joblib.load(model_file)
        if tfidf == 'tfidf':
            t = 1
        else:
            t = 0
        data_vec = covectorize(string, t, feature_file)
        predict_result = clf_model.predict(data_vec)
        print(predict_result)


# 完成打开文件后的准备工作
def comma_tokenizer(x): return jieba.cut(x, cut_all=True)


# 转换成词向量
def covectorize(data_words, tfidf, feature_file):
    if tfidf == 1:
        v = TfidfVectorizer(tokenizer=comma_tokenizer, decode_error="replace",
                            vocabulary=pickle.load(open(feature_file, "rb")))
    else:
        v = CountVectorizer(tokenizer=comma_tokenizer, decode_error="replace",
                            vocabulary=pickle.load(open(feature_file, "rb")))
    data_vec = v.fit_transform(data_words)    # ??????
    return data_vec


if __name__ == '__main__':
    attrs = ['System', 'CPU', 'RAM', 'ROM', 'Price',
             'Screen', 'Solid', 'Time', "Weight"]
    root_path = '等宽离散化标注/'
    model_path = root_path + 'model-cut/'
    string = ['我要一款运行内存大硬盘容量大的笔记本电脑']
    tfidf = 'tfidf'
    cut = 'cut'
    predict(model_path, string, attrs, tfidf, cut)
    print('OK')
