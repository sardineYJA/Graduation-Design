1.deploy_csv-cut和deploy_csv-nocut中的数据是前面1-4步骤预测的数据包括rel和irr
2.related_all_csv-cut和related_all_csv-nocut中的数据是早期的数据只有rel（但是与步骤1预测用的模型一样），目的增加rel的样本数目
3.以上4个文件夹抽取多个文件合并(抽deploy34个，related17个)，得到两个新的训练数据：new_cut_train.csv和new_nocut_train.csv
4.手动修改一些标注，希望可以得到更好的数据去训练两个新的文本分类模型

merge_new_csv.py功能：
将 deploy_csv_cut     和 related_all_csv-cut     合并 new_cut_train.csv
将 deploy_csv_nocut 和 related_all_csv-nocut 合并 new_nocut_train.csv
并打乱 csv 文件中数据的排序