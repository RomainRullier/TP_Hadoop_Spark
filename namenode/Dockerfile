FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

MAINTAINER Ivan Ermilov <ivan.s.ermilov@gmail.com>

HEALTHCHECK CMD curl -f http://localhost:9870/ || exit 1

ENV HDFS_CONF_dfs_namenode_name_dir=file:///hadoop/dfs/name
RUN mkdir -p /hadoop/dfs/name
VOLUME /hadoop/dfs/name

COPY ./run.sh /run.sh
RUN chmod a+x /run.sh

COPY ./import_data.sh /import_data.sh
RUN chmod a+x /import_data.sh

COPY shared shared

EXPOSE 9870

CMD ["/run.sh"]