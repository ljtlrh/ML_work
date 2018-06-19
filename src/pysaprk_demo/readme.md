环境搭建：http://blog.csdn.net/kokjuis/article/details/53537029
G:\spark\spark-2.1.1-bin-hadoop2.7\hadoop-2.7.3\etc\hadoop>hadoop-env.cmd

G:\spark\spark-2.1.1-bin-hadoop2.7\hadoop-2.7.3\etc\hadoop>hdfs namenode -format

启动：
cd G:\spark\spark-2.1.1-bin-hadoop2.7\hadoop-2.7.3\sbin
切换到 sbin目录 执行：start-dfs.cmd 
start-all.cmd

停止：
stop-all.cmd


查看hadoop管理页面：http://localhost:50070

cd G:\spark\spark-2.1.1-bin-hadoop2.7\hadoop-2.7.3\bin
hdfs命令上传整个文件夹： 

G:\spark\spark-2.1.1-bin-hadoop2.7\hadoop-2.7.3\bin>cd G:\spark\spark-2.1.1-bin-hadoop2.7\hadoop-2.7.3\bin

G:\spark\spark-2.1.1-bin-hadoop2.7\hadoop-2.7.3\bin>hadoop dfs -put G:\yan\recommend\data\ml-20m\ \train
DEPRECATED: Use of this script to execute hdfs command is deprecated.
Instead use the hdfs command for it.
put: `train': No such file or directory

G:\spark\spark-2.1.1-bin-hadoop2.7\hadoop-2.7.3\bin>hadoop dfs -mkdir -p /train
DEPRECATED: Use of this script to execute hdfs command is deprecated.
Instead use the hdfs command for it.

G:\spark\spark-2.1.1-bin-hadoop2.7\hadoop-2.7.3\bin>hadoop dfs -put G:\yan\recommend\data\ml-20m\ /train
DEPRECATED: Use of this script to execute hdfs command is deprecated.
Instead use the hdfs command for it.

G:\spark\spark-2.1.1-bin-hadoop2.7\hadoop-2.7.3\bin>hadoop dfs -mkdir -p /train/ml-100k
DEPRECATED: Use of this script to execute hdfs command is deprecated.
Instead use the hdfs command for it.

G:\spark\spark-2.1.1-bin-hadoop2.7\hadoop-2.7.3\bin>hadoop dfs -put G:\yan\recommend\data\ml-100k\ /train/ml-100k


