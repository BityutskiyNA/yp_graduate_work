# $ docker exec -it clickhouse-node1 bash
# $ clickhouse-client

CREATE DATABASE shard;

CREATE DATABASE replica;

CREATE TABLE shard.db (film_id String, user_id String, user_time Float, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/db', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY film_id;

CREATE TABLE replica.db (film_id String, user_id String, user_time Float, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/db', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY film_id;

CREATE TABLE default.db (film_id String, user_id String, user_time Float, event_time DateTime) ENGINE = Distributed('company_cluster', '', db, rand());

# exit
# exit

# создание таблиц на втором шарде:

# docker exec -it clickhouse-node3 bash
# clickhouse-client

CREATE DATABASE shard;

CREATE DATABASE replica;

CREATE TABLE shard.db (film_id String, user_id String, user_time Float, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/db', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY film_id;

CREATE TABLE replica.db (film_id String, user_id String, user_time Float, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/db', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY film_id;

CREATE TABLE default.db (film_id String, user_id String, user_time Float, event_time DateTime) ENGINE = Distributed('company_cluster', '', db, rand());
