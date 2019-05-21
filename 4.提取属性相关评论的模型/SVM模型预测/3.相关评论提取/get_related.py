import csv
import os


# 只返回 file_dir此目录下的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


# 将txt文件转成csv文件
def txt2csv(inputfile,outputfile):
    datacsv = open(outputfile, 'w', newline='', encoding='GBK')
    # newline参数解决python3baocuncsv时产生空行的问题
    csvwriter = csv.writer(datacsv, dialect=("excel"))
    txtfile = open(inputfile, 'r', encoding='utf-8')
    for line in txtfile.readlines():
        line.replace('\n', '')
        csvwriter.writerow([a for a in line.replace('\n', '').split(',')])
    datacsv.close()
    txtfile.close()


def get_related(path, save_path):
    logs = ''   # 相关评论的频率日志
    n = 0       # 电脑种类数
    frequnce100 = 0
    frequnce500 = 0
    frequnce1000 = 0
    frequnce3000 = 0
    frequnce5000 = 0
    frequnce_others = 0

    for name in file_name(path):
        save_name = name.replace('_comments.csv', '')
        n += 1
        logs += '第'+str(n) + '款' + '\n'
        logs += save_name + '\n'

        reader = csv.reader(open(path+name))
        column = [row for row in reader]
        content = [i[0] for i in column]
        label = [i[1] for i in column]
        lens = len(column)

        logs += '所有文本数：' + str(lens) + '\n'
        count = 0    # 记录相关评论数目
        result = ''  # 保存相关评论

        for k in range(0, lens):
            if label[k] == '1':
                result += content[k] + '\n'
                count += 1
        logs += '相关文本数量：' + str(count) + '\n'
        logs += '相关文本数量占比：' + str(float(count/lens)*100) + '%' + '\n\n'

        txt_name = 'temp.txt'
        csv_name = save_path + save_name + '_related.csv'
        f1 = open(txt_name, 'w', encoding='utf-8')
        f1.write(result)
        f1.close()
        txt2csv(txt_name, csv_name)

        # 统计数据频率
        if count <= 100:
            frequnce100 += 1
        elif 100 < count <= 500:
            frequnce500 += 1
        elif 500 < count <= 1000:
            frequnce1000 += 1
        elif 1000 < count <= 3000:
            frequnce3000 += 1
        elif 3000 < count <= 5000:
            frequnce5000 += 1
        else:
            frequnce_others += 1

    frequnce = '文本数量小于100的款式数：' + str(frequnce100) + '\n' \
               + '文本数量100~500的款式数：' + str(frequnce500) + '\n' \
               + '文本数量500~1000的款式数：' + str(frequnce1000) + '\n' \
               + '文本数量1000~3000的款式数：' + str(frequnce3000) + '\n' \
               + '文本数量3000~5000的款式数：' + str(frequnce5000) + '\n' \
               + '文本数量5000以上的款式数：' + str(frequnce_others) + '\n'
    log = open(path[11:-1]+'_frequnce.txt', 'w', encoding='utf-8')
    log.write(logs)
    log.write(frequnce)
    log.close()
    os.remove('temp.txt')  # 删除中间文件


if __name__ == '__main__':
    path = 'deploy_csv-cut/'
    save_path = 'related_csv-cut/'
    get_related(path, save_path)
    print('OK')

    path = 'deploy_csv-nocut/'
    save_path = 'related_csv-nocut/'
    get_related(path, save_path)
    print('OK')
