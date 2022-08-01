# Seminario 
Seminario Especialización en ciencia de datos

## Objetivos: Aplicar lo aprendido en el Seminario.

## Metodologia:
* Levantar un ambiente productivo con docker
* Generar un script que busque el precio de Etherium
* Publicar el precio de Etherium en kafka con un topico crypto
* Realizar un ETL a los datos de ese topico de kafka utilizando pyspark
* Almacenarlos datos del etl en una base de datos postgres
* Visualizar los datos con superset

Paso 1:

Clonar el repositorio con el siguiente comando


```
git clone https://github.com/dgarzond/seminario.git
```

Luego vamos a inicializar el docker con el siguiente comando:
```
./control-env.sh start
```

Paso 2:

Para hacer correr el script que busca el precio de ETH con una api publica de coingecko, la misma busca el precio cada 30 segundos.

```
docker exec -it worker1 bash

cd /app/

python eth_prices.py
```
En la terminal se observara que se empezaran a escribir los siguientes campos

![](/images/eth-prices.png)

Este script busca los precios de ETH y luego se lo transfiere a kafka. Para ver como se estan transfiriendo los datos kafka correr los siguiente

```
docker run --rm --network=wksp_default edenhill/kafkacat:1.6.0 -q \
    -b kafka:9092 \
    -C -t crypto -p0 \
    -f 'Partition: %p | Offset: %o | Timestamp: %T | Value: %s\n' 
```

Paso 3:

Para capturar los datos streameados en kafka y trasladarlos a una base de datos de posgres, se ejecuta el siguiente comando 

```
docker exec -it worker1 bash 

 cd /app/
 
spark-submit \
master 'spark://master:7077' \
packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 \
jars /app/postgresql-42.1.4.jar \
total-executor-cores 1 \
etl_stream_eth.py
```

Paso 4: 

Abrir superset, y visualizar el dashboard en el navegador con la siguiente url: http://localhost:8088/superset/dashboard/1/


