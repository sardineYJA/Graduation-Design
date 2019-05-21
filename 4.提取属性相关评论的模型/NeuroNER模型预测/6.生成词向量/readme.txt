jieba_cut.py 将文件 new_cut_train.csv 和 new_nocut_train.csv 的句子分词保存到 glove-cut.txt 和glove-nocut.txt
在ubuntu环境（使用shell命令）中使用 GloVe-master 工具将 glove.txt 生成词向量文件 
命令：sh demo.sh
CORPUS=**.txt      　　 #　目标文件
VECTOR_SIZE=100　　＃　维度大小
VOCAB_FILE=**.txt　　＃　结果文件

得到词向量文件：vectors-cut.txt 和 vectors-nocut