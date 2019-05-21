import csv


# 将txt文件转csv
def txt2csv(inputfile, outputfile):
    datacsv = open(outputfile, 'w', newline='', encoding='GBK')
    # newline参数解决python3保存csv时产生空行的问题
    csvwriter = csv.writer(datacsv, dialect=("excel"))
    txtfile = open(inputfile, 'r', encoding='utf-8')
    for line in txtfile.readlines():
        line.replace('\n', '')
        csvwriter.writerow([a for a in line.replace('\n', '').split(',')])
    datacsv.close()
    txtfile.close()


# 解析 000_deploy.txt 预测文件
def split_deploy(deploy_file, save_path):
    f = open(deploy_file, 'r', encoding='utf-8')
    result = ''  # 合并成一个csv文件
    word = ''    # 合并成一句话
    for line in f:
        line_sp = line.strip().split(' ')
        if len(line_sp) == 7:
            # 只输出预测标签
            if line_sp[5] != 'O':
                word += line_sp[0]
                deploy_tag = line_sp[6].replace('B-', '').replace('I-', '')
                if line_sp[4] == 'TAGSTART':  # 用标记将不同电脑之间的预测数据分离开
                    txt_name = 'temp/temp.txt'
                    csv_name = save_path + line_sp[0] + '_deploy.csv'
                    print('开始输出文件：' + line_sp[0])
                    f1 = open(txt_name, 'w', encoding='utf-8')
                    f1.write(result)
                    f1.close()
                    txt2csv(txt_name, csv_name)
                    word = ''
                    result = ''
            elif line_sp[5] == 'O':
                result += str(word) + ',' + deploy_tag + '\n'
                word = ''
    f.close()


if __name__ == '__main__':
    save_path = 'deploy_csv-cut/'
    split_deploy('000_deploy-cut.txt', save_path)
    print('完成对预测文本的重组！')

    save_path = 'deploy_csv-nocut/'
    split_deploy('000_deploy-nocut.txt', save_path)
    print('完成对预测文本的重组！')
