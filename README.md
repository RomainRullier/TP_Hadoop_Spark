# Exo TP individuelle

### Etape 1 : Cloner le project

`git clone https://github.com/ArmandThomas/tp_indiv`

### Etape 2 : Lancer les dockers

`docker-compose up`

### Etape 3 : Créer le topic dans kafka

- Se connecter à votre kafka

`/bin/sh create_topic.sh`

### Etape 4 : importer les data dans le hdfs

- Se connecter à votre namenode

`/bin/sh import_data.sh`