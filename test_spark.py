import os
from pyspark import SparkConf, SparkContext

'''
Launch the job:
./<SPARK_HOME>/bin/spark-submit --master local[2] <PATH_TO_FILE>/test_spark.py
'''

# Configure the environment
if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = '/home/ubuntu/spark-2.2.0-bin-hadoop2.7'

conf = SparkConf().setAppName('pubmed_open_access').setMaster('local[32]')
sc = SparkContext(conf=conf)

if __name__ == '__main__':
    ls = range(100)
    ls_rdd = sc.parallelize(ls, numSlices=1000)
    ls_out = ls_rdd.map(lambda x: x+1).collect()
    print 'output!: ', ls_out
