from cassandra.cluster import Cluster

CASSANDRA_KEYSPACE = "sensor"
CASSANDRA_TABLE = "gait_data"

def create_table():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {CASSANDRA_KEYSPACE}
        WITH REPLICATION = {{ 'class' : 'SimpleStrategy', 'replication_factor' : 1 }};
    """)
    session.execute(f"""
        CREATE TABLE IF NOT EXISTS {CASSANDRA_KEYSPACE}.{CASSANDRA_TABLE} (
            timestamp FLOAT,
            data LIST<FLOAT>,
            PRIMARY KEY (timestamp)
        );
    """)
    session.shutdown()
    cluster.shutdown()

if __name__ == "__main__":
    create_table()
