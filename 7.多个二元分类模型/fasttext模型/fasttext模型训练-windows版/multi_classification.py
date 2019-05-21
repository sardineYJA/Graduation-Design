import os
import fastText.FastText as ff


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 对9个属性训练，9个分类器
def train(attrs):
    for attr in attrs:
        print('开始训练---', attr)
        train_file ='train-cut/' + attr + '_train.txt'
        model ='model-cut/' + attr + '_model'
        classfier = ff.train_supervised(train_file)
        classfier.save_model(model)
        print('训练完成---', attr)


# 查看9个分类器效果
def precision(attrs):
    # 加载模型
    for attr in attrs:
        print(attr, '模型效果：')
        classifier = ff.load_model("model-cut/" + attr + '_model')
        result = classifier.test('test-cut/' + attr + '_test.txt')
        print('准确率：', result)
        # 准确率： (33417, 0.9593919262650746, 0.9593919262650746)


# 评论预测
def predict(attrs):
    str_list = ['我 要 一款 内存 大 运行 快 的 苹果 电脑']
    for attr in attrs:
        print(attr, '预测：')
        classifier = ff.load_model('model-cut/' + attr + "_model")
        lab = classifier.predict(str_list, k=1)
        print(lab)  # (['__label__2'], array([0.95485353]))


if __name__ == '__main__':
    attrs = ['System', 'CPU', 'RAM', 'ROM', 'Price',
             'Screen', 'Solid', 'Time', "Weight"]
    # train(attrs)
    precision(attrs)
    predict(attrs)
    print('OK')
