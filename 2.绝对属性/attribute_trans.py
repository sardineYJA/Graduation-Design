import pandas as pd


def data_cut():
    data = pd.read_csv('absolute_attribute_complete.csv', encoding='GBK')

    # 标签化分三个1，2，3（其中标签不能为0，后续训练要求）

    # 等宽离散标签化
    cpu = pd.cut(data['CPU'], 3, labels=range(1, 4))
    time = pd.cut(data['Time'], 3, labels=range(1, 4))
    screen = pd.cut(data['Screen'], 3, labels=range(1, 4))
    weight = pd.cut(data['Weight'], 3, labels=range(1, 4))
    price = pd.cut(data['Price'], 3, labels=range(1, 4))

    # 查看等宽离散化的间距
    # cpu = pd.cut(data['CPU'], 3)
    # time = pd.cut(data['Time'], 3)
    # screen = pd.cut(data['Screen'], 3)
    # weight = pd.cut(data['Weight'], 3)
    # price = pd.cut(data['Price'], 3)
    # print('-------cpu')
    # print(cpu)
    # print('-------time')
    # print(time)
    # print('-------screen')
    # print(screen)
    # print('-------weight')
    # print(weight)
    # print('-------price')
    # print(price)

    data['CPU'] = cpu
    data['Time'] = time
    data['Screen'] = screen
    data['Weight'] = weight
    data['Price'] = price
    data.to_csv('absolute_attribute_trans_cut.csv', index=False, encoding='GBK')
    print('OK')


def data_qcut():
    data = pd.read_csv('absolute_attribute_complete.csv', encoding='GBK')
    # 等频离散标签化
    cpu = pd.qcut(data['CPU'], 3, labels=range(1, 4))
    time = pd.qcut(data['Time'], 3, labels=range(1, 4))
    screen = pd.qcut(data['Screen'], 3, labels=range(1, 4))
    weight = pd.qcut(data['Weight'], 3, labels=range(1, 4))
    price = pd.qcut(data['Price'], 3, labels=range(1, 4))

    # 查看等频离散化的间距
    # cpu = pd.qcut(data['CPU'], 3)
    # #time = pd.qcut(data['Time'], 3)
    # screen = pd.qcut(data['Screen'], 3)
    # weight = pd.qcut(data['Weight'], 3)
    # price = pd.qcut(data['Price'], 3)
    # print('-------cpu')
    # print(cpu)
    # print('-------time')
    # print(time)
    # print('-------screen')
    # print(screen)
    # print('-------weight')
    # print(weight)
    # print('-------price')
    # print(price)

    data['CPU'] = cpu
    data['Time'] = time
    data['Screen'] = screen
    data['Weight'] = weight
    data['Price'] = price
    data.to_csv('absolute_attribute_trans_qcut.csv', index=False, encoding='GBK')
    print('OK')


# （等宽，等频）离散化数据
# 系统，内存，硬盘，固态手动标签化
if __name__ == "__main__":
    # 等宽离散化
    data_cut()

    # 等频离散化
    data_qcut()
