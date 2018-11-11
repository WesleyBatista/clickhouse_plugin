from airflow.plugins_manager import AirflowPlugin
from clickhouse_plugin.hooks.clickhouse_hook import ClickHouseHook
from clickhouse_plugin.operators.clickhouse_load_operator import (
     ClickHouseLoadCsvOperator)


class ClickHousePlugin(AirflowPlugin):
    name = "clickhouse_plugin"
    operators = [ClickHouseLoadCsvOperator]
    hooks = [ClickHouseHook]
