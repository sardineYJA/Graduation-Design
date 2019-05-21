import pandas as pd 


# 切割数据train,dev,test
def split_data(csv_file, save_path, train_rate, dev_rate):
	all_data = pd.read_csv(csv_file, encoding='GBK', header=None)
	num = len(all_data)
	print(csv_file, '总行数：', num)
	train_num = int(num*train_rate)
	dev_num = int(num*(train_rate+dev_rate)) - train_num
	test_num = num - train_num - dev_num
	all_data[:train_num].to_csv(save_path+'train.csv', encoding="GBK", index=False, header=None)
	all_data[train_num:train_num+dev_num].to_csv(save_path+'dev.csv', encoding="GBK", index=False, header=None)
	all_data[train_num+dev_num:].to_csv(save_path+'test.csv', encoding="GBK", index=False, header=None)
	print("split data OK")
	print("train.csv：", train_num)
	print("dev.csv：", dev_num)
	print("test.csv：", test_num)


if __name__ == "__main__":
	csv_file = 'new_nocut_train.csv'
	save_path = 'split_nocut/'
	split_data(csv_file, save_path, 0.8, 0.1)
	print("OK")

	csv_file = 'new_cut_train.csv'
	save_path = 'split_cut/'
	split_data(csv_file, save_path, 0.8, 0.1)
	print("OK")
