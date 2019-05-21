from urllib import request       # 请求网页链接
import re                        # 正则匹配
import json                      # 解析json数据
import time
import random


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


# 获取需要爬取的品牌
def get_brand():
    brand = {'联想': 11516, '戴尔': 5821, '华为': 8557, 'Apple': 14026, '小米': 18374,
             '惠普': 8740, 'ThinkPad': 11518, '华硕': 8551, '宏碁': 8354, '三星': 15127,
             '神舟': 15539, '微软': 17440, }
    return brand


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


# 获取各品牌的电脑id，返回字典
def get_id():
    brand = get_brand()                # 需要爬取的品牌
    pages = [1, 2, 3]                  # 默认只爬取第一页的商品15X4=60个
    sort = 'sort_totalsales15_desc'    # sort以评论数量或者销量排名进行爬取
    productIDs_dict = {}               # 保存各品牌的电脑id
    for key in brand:
        for i in pages:
            url = 'https://list.jd.com/list.html?cat=670,671,672'\
                  + '&ev=exbrand_' + str(brand[key]) + '&page=' \
                  + str(i) + '&sort=' + sort
            html = open_url(url)
            html = html.decode('utf-8')
            id_list = parse_html_id(html)
            time.sleep(2)               # 睡眠时间，单位秒

            if i == 1:
                productIDs_dict[key] = id_list
            else:
                productIDs_dict[key].extend(id_list)
        print(key, "---获取成功，款数目：", len(productIDs_dict[key]))
    return productIDs_dict


# 解析HTML，得到电脑id
def parse_html_id(html):
    id_list = []
    result = re.findall(
        'class="gl-i-wrap j-sku-item" data-sku="[0-9]{5,15}"', html)
    for a in result:
        id_list.append(a.split('"')[3])
    return id_list


# 保存电脑id到json文件中
def save_id_file(id_dict):
    with open(id_file, "w") as f:
        json.dump(id_dict, f, ensure_ascii=False)
    print("-----ID保存成功！-----")


if __name__ == '__main__':

    # 先获取要爬取的id
    id_dict = get_id()

    # 保存每个品牌的前n个，默认第一页60个
    #for key in id_dict:
        #random.shuffle(id_dict[key])      # 打乱顺序
        #id_dict[key] = id_dict[key][0:50]  # 只提取

    # 打印查看
    # for key in id_dict:
    #    print((key), '----爬取款数：', len(id_dict[key])

    # 保存到id.json文件中
    save_id_file(id_dict)
