from airflow.hooks.http_hook import HttpHook
from clickhouse_driver import Client


class ClickHouseHook(HttpHook):

    def __init__(self, clickhouse_conn_id):
        self.clickhouse_conn_id = clickhouse_conn_id

    def get_client(self, **kwargs):
        compression = False
        if 'compression' in kwargs:
            compression = kwargs.pop('compression')

        database = 'default'
        if 'database' in kwargs:
            database = kwargs.pop('database')

        secure = False
        if 'secure' in kwargs:
            secure = kwargs.pop('secure')

        verify = False
        if 'verify' in kwargs:
            verify = kwargs.pop('verify')

        conn = self.get_connection(self.clickhouse_conn_id)
        self.log.info({
            'host': conn.host,
            'port': conn.port,
            'user': conn.login,
            'password': conn.password,
            'database': database,
            'client_name': 'clickhouse_plugin',
            'compression': compression,
            'secure': secure,
            'verify': verify,
            'settings': kwargs,
        })
        client = Client(**{
            'host': conn.host,
            'port': conn.port,
            'user': conn.login,
            'password': conn.password,
            'database': database,
            'client_name': 'clickhouse_plugin',
            'compression': compression,
            'secure': secure,
            'verify': verify,
            'settings': kwargs,
        })
        return client

    def insert_into(self, database, table, columns, values, **kwargs):
        client = self.get_client(**kwargs)
        query_tmpl = 'INSERT INTO {database}.{table} VALUES'
        query = query_tmpl.format(**{
            'database': database,
            'table': table,
            'columns': ','.join(columns),
        })
        self.log.info(query)
        self.log.info([x for x in values])
        result = client.execute(query, values)
        return result
