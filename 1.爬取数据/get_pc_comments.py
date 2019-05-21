from urllib import request         # 请求网页链接
import json                       # 解析json数据
import pandas as pd
import copy                       # 深拷贝
import traceback                  # 捕获异常
import time
import socket


socket.setdefaulttimeout(5)   # 5秒没有打开web页面，超时


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
id_file = root_path + 'params_id.json'
error_id_file = root_path + 'error_id.json'
logo_file = root_path + 'logo.txt'


# 获取链接的HTML
def open_url(url):
    req = request.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36')
    response = request.urlopen(url)
    html = response.read()
    return html


# 读取电脑id的json文件
def read_id_file():
    with open(id_file, "r") as f:
        id_dict = json.load(f)
    print('-----读取ID文件成功！-----')
    #print(json.dumps(dict, indent=1, ensure_ascii=False))
    return id_dict


# 保存评论
def save_comments(pro_id, key, pro_path):
    all_list = []
    try:
        stop_num = 0
        for i in range(0, 1000):
            #print(i*'-', '>')   # 打印进度
            try:
                url = 'https://sclub.jd.com/comment/productPageComments.action?productId='\
                      + pro_id + '&score=3&sortType=6&page=' + \
                    str(i) + '&pageSize=10'
                html = open_url(url)
                commJson = json.loads(html.decode('GBK'))
                comm_list = []   # 保存此款手机所有的评论
                if commJson['comments']:
                    for i in commJson['comments']:
                        comm_list.clear()
                        comm_list.append(i['nickname'])           # 评论用户名（不完整）
                        comm_list.append(i['id'])                 # 评论id
                        comm_list.append(i['creationTime'])       # 评论时间
                        comm_list.append(i['usefulVoteCount'])    # 此评论的点赞数
                        comm_list.append(i['score'])              # 分数（1-5表示星数）
                        comm_list.append(i['content'].strip())    # 评论内容
                        all_list.append(copy.deepcopy(comm_list))
                else:
                    if i < 80:
                        add_other_id(key, pro_id, error_id_file)  # 如果爬取页数过少
                    print('第', i, '页结束')
                    break
            except:
                stop_num = stop_num + 1
                if stop_num <= 5:   # 最多暂停3次
                    print('暂停1秒')
                    time.sleep(1)
                else:
                    add_other_id(key, pro_id, error_id_file)
                    write_logo(key, pro_id)
                    print('第', i, '页结束')
                    break
    except:
        add_other_id(key, pro_id, error_id_file)
        write_logo(key, pro_id)

    try:

        df = pd.DataFrame(
            columns=["用户名", "评论id", "评论时间", "点赞数", "商品分数", '内容'], data=all_list)
        df.to_csv(pro_path + '/' + key + '_' + pro_id + '_comments.csv',
                  encoding="GBK", index=False)
        df.to_csv('评论总和/' + key + '_' + pro_id + '_comments.csv',encoding="GBK", index=False)
    except:
        write_logo(key, pro_id)
    print(key, pro_id, '评论保存成功！')


# 捕获到错误则写进日志
def write_logo(key, pro_id):
    err = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    err = err + ' : ' + key + pro_id + '捕获错误'
    err = err + '\n' + traceback.format_exc()
    with open(logo_file, "a") as f:
        f.write(err + '\n')


# 信息保存主函数
def save_product_info():
    init_file()
    id_dict = read_id_file()
    for key in id_dict:        # key 品牌
        key_path = root_path + key + '/'
        #os.mkdir(key_path)
        num = 0
        for pro_id in id_dict[key]:
            pro_path = key_path + key + '_' + pro_id
            #os.mkdir(pro_path)
            save_comments(pro_id, key, pro_path)
            num = num + 1
        print('----------------', key, '共爬取', num, '款样式')


# 追加爬取id,用于再次爬取
def add_other_id(key, pro_id, path):
    with open(path, "r") as f:
        id_dict = json.load(f)
        newlist = []
        if key not in id_dict.keys():
            newlist.append(pro_id)
            id_dict[key] = newlist
        else:
            newlist = id_dict[key]
            newlist.append(pro_id)
            id_dict[key] = newlist
    with open(path, "w") as f:
        json.dump(id_dict, f, ensure_ascii=False)


# 清空各类日志文件
def init_file():
    with open(logo_file, "w") as f:
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        f.write(t + ' : 清空日志\n')
        print('清空logo.txt')
    with open(error_id_file, "w") as f:
        dict = {}
        json.dump(dict, f, ensure_ascii=False)
        print('清空error_id.json')


if __name__ == '__main__':

    # 保存数据
    save_product_info()
