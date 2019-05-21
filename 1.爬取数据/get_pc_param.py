from urllib import request         # 请求网页链接
import re                          # 正则匹配
import os                          # 创建文件夹
from bs4 import BeautifulSoup      # 解析html
import json                        # 解析json数据
import csv
import traceback                   # 捕获异常
import time
import shutil
import socket


socket.setdefaulttimeout(10)   # 5秒没有打开web页面，超时
'''
京东笔记本电脑首页解析：page表示页数，sort表示笔记本电脑排名
以销量递减排名      https://list.jd.com/list.html?cat=670,671,672&page=1&sort=sort_totalsales15_desc
以评论数目递减排名  https://list.jd.com/list.html?cat=670,671,672&page=1&sort=sort_commentcount_desc
每件商品首页        https://item.jd.com/7632577.html

联想   &ev=exbrand_11516
ThinkPad &ev=exbrand_11518
戴尔   &ev=exbrand_5821
华硕   &ev=exbrand_8551
惠普   &ev=exbrand_8740
小米   &ev=exbrand_18374
华为   &ev=exbrand_8557
Apple  &ev=exbrand_14026
宏碁   &ev=exbrand_8354
三星   &ev=exbrand_15127
神舟   &ev=exbrand_15539
微软   &ev=exbrand_17440
外星人 &ev=exbrand_17193
'''

'''  
评论链接解析：
https://sclub.jd.com/comment/productPageComments.action
?productId=5225346   # 商品id
&score=1             # 0全部，5追评，4晒图，3好评，2中评，1差评
&sortType=6       
&page=0              # 页数从0开始
&pageSize=10         # 每页显示评论条数
&isShadowSku=0 
&fold=1
'''


root_path = '京东/'
id_file = root_path + 'id.json'
error_id_file = root_path + 'error_id.json'
logo_file = root_path + 'logo.txt'


# 获取链接的HTML
def open_url(url):
    req = request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.2; WOW64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/27.0.1453.94 Safari/537.36')
    response = request.urlopen(url)
    html = response.read()
    return html


# 读取电脑id的json文件
def read_id_file():
    with open(id_file, "r") as f:
        id_dict = json.load(f)
    print('读取ID文件成功！')
    #print(json.dumps(id_dict, indent=1, ensure_ascii=False))
    return id_dict


# 解析HTML，保存图片
def save_image(html, product_path):
    soup = BeautifulSoup(html, 'lxml')
    images = []  # 保存图片略缩图链接
    Images = []  # 保存图片高清图链接
    for i in soup.find_all(attrs={'class': 'lh'}):
        img = i.find_all('img')
        if (img):
            for j in img:
                images.append(j.attrs['src'])
    for i in images:  # 将略缩图修改成高清图
        Images.append(re.sub('n5/s54x54_jfs', 'n0/jfs', i))
    product_path += '/图片'
    os.mkdir(product_path)
    for url in Images:
        url = ' http:' + url
        imageName = product_path + '/' + url.split('/')[-1]
        with open(imageName, 'wb') as f:
            html = open_url(url)
            f.write(html)
    print('\t图片保存成功！')


# 获取商品价格
def get_price(id):
    # window 运行加上后面的
    url = 'http://p.3.cn/prices/mgets?skuIds=J_' + str(id) #+ '&pduid=pdtk'
    html = open_url(url)
    html = html.decode('utf-8')
    hjson = json.loads(html)
    return hjson[0]['p']


# 解析HTML，返回电脑配置参数的字典
def get_params(html):
    soup = BeautifulSoup(html, 'lxml')
    dic = {}  # 保存参数
    try:      # 如果提取标题出错，则跳过
        title = soup.find(attrs={'class': 'sku-name'})
        t = title.string.strip()    # 全称
        dic['名称'] = t
    except:
        dic = {}
    params = soup.find_all(attrs={'class': 'Ptable-item'})  # 笔记本规格参数
    for p in params:        # bs4.element.Tag类型
        for i, j in zip(p.find_all('dt'), p.find_all('dd')):
            dic[i.string] = j.string
    return dic


# 将参数保存到csv文件中
def save_params(params_dict, params_file):
    params_file = open(params_file, 'w', newline='', encoding='GBK')
    writer_file = csv.writer(params_file)
    for key in params_dict:
        writer_file.writerow([key, params_dict[key]])
    params_file.close()
    print('\t参数保存成功！')


# 捕获到错误则写进日志
def write_logo(key, pro_id):
    err = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    err = err + ' : ' + key + '_' + pro_id + ' : 捕获错误'
    err = err + '\n' + traceback.format_exc()
    with open(logo_file, "a") as f:
        f.write(err + '\n')


# 保存图片和参数
def save_img_and_params(key, pro_id, pro_path):
    try:
        url = 'https://item.jd.com/' + pro_id + '.html'
        html = open_url(url)
        #html = html.decode('utf-8')
        price = get_price(pro_id)
        params_dict = get_params(html)
        params_dict['价格'] = price
        if len(params_dict) > 5:
            save_image(html, pro_path)
            params_file = pro_path+'/'+key+'_'+pro_id+'_params.csv'
            save_params(params_dict, params_file)
            save_params(params_dict, "参数总和/"+key+'_'+pro_id+'_params.csv')
            return True
        else:
            print('\t参数没有解析到！')
            shutil.rmtree(root_path+key+'/'+key+'_'+pro_id)  # 删除文件夹
            add_other_id(key, pro_id, error_id_file)
            return False
    except:
        add_other_id(key, pro_id, error_id_file)
        write_logo(key, pro_id)
        shutil.rmtree(root_path + key + '/' + key + '_' + pro_id)  # 删除文件夹
        return False


# 追加爬取id,用于再次爬取
def add_other_id(key, pro_id, path):
    with open(path, "r") as f:
        id_dict = json.load(f)
        new_list = []
        if key not in id_dict.keys():
            new_list.append(pro_id)
            id_dict[key] = new_list
        else:
            new_list = id_dict[key]
            new_list.append(pro_id)
            id_dict[key] = new_list
    with open(path, "w") as f:
        json.dump(id_dict, f, ensure_ascii=False)


# 清空各类日志文件
def init_file():
    with open(logo_file, "w") as f:
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        f.write(t + ' : 清空日志\n')
        print('清空logo.txt')
    with open(error_id_file, "w") as f:
        dict_null = {}
        json.dump(dict_null, f, ensure_ascii=False)
        print('清空error_id.json')


# 信息保存主函数
def save_product_info():
    init_file()
    id_dict = read_id_file()
    for key in id_dict:
        key_path = root_path + key + '/'
        os.mkdir(key_path)      # 创建每个品牌的目录
        num = 0
        for pro_id in id_dict[key]:
            print(key, pro_id, '-->-->-->')
            pro_path = key_path + key + '_' + pro_id
            os.mkdir(pro_path)                                 # 创建每款目录
            if (save_img_and_params(key, pro_id, pro_path)):   # 获取图片以及参数
                num = num + 1
        print('----------------', key, '共成功爬取', num, '款样式')


if __name__ == '__main__':

    # 保存数据
    save_product_info()
    print('OK')
