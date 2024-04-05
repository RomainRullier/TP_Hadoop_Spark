hdfs dfs -mkdir -p /data/
hdfs dfs -put ./shared/dataset_sismique_villes.csv /data/dataset_sismique_villes.csv
hdfs dfs -ls /data