from __future__ import print_function
from airflow.operators import LivySparkBatchOperator
from airflow.models import DAG
from datetime import datetime, timedelta
import os

"""
Pre-run Steps:

1. Open the Airflow WebServer
2. Navigate to Admin -> Connections
3. Add a new connection
    1. Set the Conn Id as "livy_http_conn"
    2. Set the Conn Type as "http"
    3. Set the host
    4. Set the port (default for livy is 8998)
    5. Save
4. Add the SPARK_HOME for your machine
5. Remove jars parameter
"""

DAG_ID = "spark_livy_batch_operator_scala"

HTTP_CONN_ID = "livy_http_conn"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
    }

dag = DAG(DAG_ID, default_args=default_args, schedule_interval=None, start_date=(datetime.now() - timedelta(minutes=1)))
SPARK_HOME="/opt/spark"
import json
config_parameters = {
  "proxyUser": "spark", # Remove if you want to run as local user
  "args": ["10"],
  "jars": ["random-0.0.1.jar", "impatient-1.0.jar"], # This is for demonstation only. Remove to run this example
  "driverMemory": "1g",
  "conf": {"spark.yarn.maxAppAttempts": "1", "spark.network.timeout": "1500s"}
}
APPLICATION_JAR = SPARK_HOME + "/examples/jars/spark-examples_2.11-2.4.4.jar"
java_class = "org.apache.spark.examples.SparkPi"
SESSION_CONFIG = json.loads(config_parameters)
application_file = "local:" + APPLICATION_JAR

dummy = LivySparkBatchOperator(
    task_id=java_class.rsplit(".", 1)[1],
    application_file=application_file,
    class_name=java_class,
    http_conn_id="livy_http_conn",
    session_config=SESSION_CONFIG,
    poll_interval=3,
    provide_context=True,
    dag=dag)
