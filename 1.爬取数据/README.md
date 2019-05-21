1. 运行 get_pc_id.py 获取下步需要爬取电脑信息的 id，并保存到id.json文件中

2. 运行 get_pc_param.py 根据 id.json 文件中的 id，爬取相应的电脑参数及图片
将出错的id保存到error_id.json,用于再次爬取,错误日志保存到logo.txt

3. 运行 get_id_from_dir.py 根据已经成功获取参数的id来进行获取评论，生成params_id.json
运行 get_pc_comments.py 根据 params_id.json 文件中的 id，爬取相应的电脑评论,错误日志保存到logo.txt
出错或者评论过少的id会保存到error_id.json 用于再次爬取

4.remove_same.py可以进行去重，也可对评论过少的进行删除

5. 运行 statistics_data.py 统计每款电脑获取评论的数目
