# clickhouse-plugin for Airflow

## Install
First we need to get the dependencies installed with:
```
pip3 install -r requirements.txt
```
Next step is to add the `$AIRFLOW_HOME/plugins` to the **PYTHONPATH**.
```
export PYTHONPATH="$PYTHONPATH:$AIRFLOW_HOME/plugins"
```
> this also works: `PYTHONPATH=$AIRFLOW_HOME/plugins airflow webserver`
 Put the files from this repository on the Airflow Plugins directory
 ```
cp -rf ~/devel/clickhouse_plugin/ $AIRFLOW_HOME/plugins
```

## Getting started

Using the `clickhouse-client` CLI _(or whatever)_ create a table like this:
```sql
CREATE TABLE test (x Int32) ENGINE = Memory
```


Once we have a table, here comes an example of DAG loading data using the operator:

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from clickhouse_plugin.operators.clickhouse_load_operator import (
    ClickHouseLoadCsvOperator)

DAG_ID = 'testing_clickhouse_plugin'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 11, 9),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'provide_context': True,
}

dag = DAG(DAG_ID, **{
    'default_args': default_args,
    'schedule_interval': '@daily',
    'catchup': False,
})


with dag:
    ClickHouseLoadCsvOperator(**{
        'task_id': 'load_csv',
        'clickhouse_conn_id': 'clickhouse_localhost',
        'filepath': '/path/to/some/sample.csv',
        'database': 'default',
        'table': 'test',
        'schema': {
            'x': lambda x: int(float(x))
        },
    })


```

`sample.csv`
```
x
1
2
3
4
```

Setup the `clickhouse_conn_id` on **`Airflow > Admin > Connections`** creating a **HTTP** connection, filling the following fields:
 - **Host**: localhost
 - **Port**: 9000
 - **Login**: default
 - **Password**: <xxxxxx> _(set a password on ClickHouse's users.xml)_

