import pandas as pd

if __name__ == "__main__":

    data = pd.read_csv('absolute_attribute_complete.csv', encoding='GBK')
    print('OK')
    # print(data)
    print(data.columns.values)       # 查看所有列值的名称

    print('-------------操作系统')
    # print(data.System.unique())
    print(data.System.value_counts())

    print('-------------CPU')
    # print(data.CPU.unique())
    # print(data.CPU.value_counts())
    print(data['CPU'].max(), data['CPU'].mean(), data['CPU'].min())

    print('-------------内存')
    print(data.RAM.unique())
    print(data.RAM.value_counts())
    # print(data['RAM'].max(), data['RAM'].mean(), data['RAM'].min())

    print('-------------硬盘')
    print(data.ROM.unique())
    print(data.ROM.value_counts())
    # print(data['ROM'].max(), data['ROM'].mean(), data['ROM'].min())

    print('-------------续航时间')
    # print(data.Time.unique())
    # print(data.Time.value_counts())
    print(data['Time'].max(), data['Time'].mean(), data['Time'].min())

    print('-------------固态硬盘')
    print(data.Solid.unique())
    print(data.Solid.value_counts())
    # print(data['Solid'].max(), data['Solid'].mean(), data['Solid'].min())

    print('-------------屏幕规格')
    # print(data.Screen.unique())
    # print(data.Screen.value_counts())
    print(data['Screen'].max(), data['Screen'].mean(), data['Screen'].min())

    print('-------------重量')
    # print(data.Weight.unique())
    # print(data.Weight.value_counts())
    print(data['Weight'].max(), data['Weight'].mean(), data['Weight'].min())

    print('-------------价格')
    # print(data.Price.unique())
    # print(data.Price.value_counts())
    print(data['Price'].max(), data['Price'].mean(), data['Price'].min())
