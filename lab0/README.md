# 0. Laboratorijska Vježba

## 1. Zadatak
Naredbom `docker build -t kubia app.js` u ovom direktoriju gradimo docker image koji će se zvati `kubia

Naredbom `docker docker run --name kubia-container -p 8080:8080 -d kubia` pokrećemo kontejner koji će se zvati `kubia-container` i koji će biti dostupan na portu 8080.


## 2. Zadatak
Naredbom `docker-compose up -d` u ovom direktoriju pokrećemo kafka cluster.

Naredba za listanje topic-a:
```docker exec <container_name> kafka-topics --bootstrap-server <container_name>:9092 --list
```

Kreiranje topic-a:
```docker exec <container_name> kafka-topics --bootstrap-server <container_name>:9092 --create --topic <topic_name>
```
Dodati zastavicu `--partitions <number_of_partitions>` za kreiranje topic-a sa određenim brojem particija.

Brisanje topic-a:
```docker exec <container_name> kafka-topics --bootstrap-server <container_name>:9092 --delete --topic <topic_name>
```

Slanje poruka na topic:
```docker exec --interactive --tty <container_name> kafka-console-producer --bootstrap-server <container_name>:9092 --topic <topic_name>
```
Dodati zastavicu `--property "parse.key=true" --property "key.separator=:"` za slanje poruka sa ključem.


Čitanje poruka sa topic-a:
```docker exec --interactive --tty <container_name> kafka-console-consumer --bootstrap-server <container_name>:9092 --topic <topic_name> --from-beginning
```