# Seminario 
Seminario Especialización en ciencia de datos

## Objetivos: Aplicar lo aprendido en el Seminario.

## Metodologia:
* Levantar un ambiente productivo con docker
* Generar un script que busque el precio de Etherium
* Publicar el precio de Etherium en kafka con el topico crypto
* Realizar un ETL a los datos de ese topico de kafka utilizando pyspark
* Almacenarlos datos del etl en una base de datos postgres
* Visualizar los datos con superset

Paso 1:

Clonar el repositorio con el siguiente comando


```
git clone https://github.com/dgarzond/seminario.git
```

Luego se inicializa el docker con el siguiente comando:

```
./control-env.sh start
```

Paso 2:

Para correr el script que busca el precio de ETH con una api publica de coingecko, la misma busca el precio cada 30 segundos, ejecturar el siguiente comando.

```
docker exec -it worker1 bash

cd /app/

python eth_prices.py
```

En la terminal se observará como se empezan a escribir los siguientes campos.

![](./images/eth_prices.jpg)

El script anterior busca los precios de ETH con la api y luego lo transfiere a kafka. Para ver como se estan transfiriendo los datos kafka correr el siguiente comando.

```
docker run --rm --network=wksp_default edenhill/kafkacat:1.6.0 -q \
    -b kafka:9092 \
    -C -t crypto -p0 \
    -f 'Partition: %p | Offset: %o | Timestamp: %T | Value: %s\n' 
```

En la terminal se observará como se están guardando los campos en kafka:

![](./images/kafka.jpg)

Paso 3:

Para capturar los datos streameados en kafka y trasladarlos a una base de datos de Postgres, se ejecuta los siguientes comandos.

```
#1
docker exec -it worker1 bash
#2
 cd /app/
#3
spark-submit \
master 'spark://master:7077' \
packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 \
jars /app/postgresql-42.1.4.jar \
total-executor-cores 1 \
etl_stream_eth.py
```

Si se ejecuta los siguientes comandos se puede observar como se van guardando los campos en la base de datos:

```
#1
 ./control-env.sh psql
 #Esto nos abrira un debian donde podemos ejectura posgres en la terminal. 
#2
 select * from crypto order by 1 desc;
```
Con este comando se visualizara la tabla de postgres donde se guardan los datos:
![](./images/postgres.jpg)

Paso 4: 

Abrir superset, y visualizar el dashboard en el navegador con la siguiente url: http://localhost:8088/superset/dashboard/1/. En el dashboard se podrá observar un line chart con el precio de eth en los ultimos 7 minutos.

![](./images/superset.jpg)


