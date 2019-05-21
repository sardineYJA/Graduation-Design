import os
import fasttext


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 对9个属性训练，9个分类器
def train(attrs, path):
    for attr in attrs:
        print('开始训练---', attr)
        train_file = path + 'train-cut/' + attr + '_train.txt'
        model = path + 'model-cut/' + attr + '_model'
        fasttext.supervised(train_file, model, label_prefix='__label__')
        print('训练完成---', attr)


# 查看9个分类器效果
def precision(attrs, path):
    # 加载模型
    for attr in attrs:
        print(attr, '模型效果：')
        classifier = fasttext.load_model(
            path + "model-cut/" + attr + '_model.bin', label_prefix='__label__')
        # 测试准确率，召回率
        result = classifier.test(path + 'test-cut/' + attr + '_test.txt')
        # print(dir(result))
        print('准确率：', result.precision)
        # print('召回率：', result.recall)
        print('Number of examples:', result.nexamples)
        print('\n')


# 评论预测
def predict(attrs, path):
    str_list = ['我 要 一款 内存 大 运行 快 的 苹果 电脑']
    for attr in attrs:
        print(attr, '预测：')
        classifier = fasttext.load_model(
            path + 'model-cut/' + attr + "_model.bin", label_prefix='__label__')
        lab = classifier.predict_proba(str_list, k=1)
        print(lab)


if __name__ == '__main__':

    attrs = ['System', 'CPU', 'RAM', 'ROM', 'Price',
             'Screen', 'Solid', 'Time', "Weight"]

    # path = '等宽离散化标注/'
    path = '等频离散化标注/'
    # train(attrs, path)

    # precision(attrs, path)

    # predict(attrs, path)

    print('OK')
