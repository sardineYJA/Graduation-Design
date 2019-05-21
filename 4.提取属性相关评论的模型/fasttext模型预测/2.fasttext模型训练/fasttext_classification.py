import os
import fasttext
import jieba


def train(path):
    fasttext.supervised(path + 'train.txt', path +
                        'model', label_prefix='__label__')
    print('训练完成')


def precision(path):
    # 加载模型
    classifier = fasttext.load_model(
        path + "model.bin", label_prefix='__label__')

    # 测试准确率，召回率
    result = classifier.test(path + 'test.txt')
    # print(type(result))
    # print(dir(result))
    print('准确率：', result.precision)
    print('召回率：', result.recall)
    print('f1_score:{0:0.3f}'.format(
        2 * result.recall * result.precision / (result.recall + result.precision)))
    print('Number of examples:', result.nexamples)


def test_predict(path):
    classifier = fasttext.load_model(
        path + "model.bin", label_prefix='__label__')

    # 输入格式要求
    str_list = [['视网膜 屏幕 很 养眼', '就是 贵 了 点'],
                ['电池 续航 能力 待 试用 之后 再 追评'],
                ['就是 贵 了 点'],
                ['最大 的 优点 是 方便 携带']]
    for string in str_list:
        lab = classifier.predict_proba(string, k=1)
        print(lab)

    str_list = ['视网膜 屏幕 很 养眼', '']
    lab = classifier.predict_proba(str_list, k=1)
    print(lab)
    print(type(lab))  # [[('rel', 0.617188)], [('rel', 0.84375)]]
    for i in lab:
        print(i)
        print(i[0][0])
        print(i[0][1])


if __name__ == '__main__':

    path = 'new_nocut_train/'
    # train(path)
    precision(path)
    # test_predict(path)

    path = 'new_cut_train/'
    # train(path)
    precision(path)
    # test_predict(path)

    print('OK')
