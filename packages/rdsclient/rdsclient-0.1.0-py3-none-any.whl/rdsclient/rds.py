from functools import wraps
import logging
import traceback
import mysql.connector
import pandas as pd
from contextlib import contextmanager
from pyspark.sql import SparkSession
from typing import Optional, Tuple, Any

spark = SparkSession.builder.appName('RDS').getOrCreate()

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'Executing {func.__name__} with args: {args}, kwargs: {kwargs}')
        try:
            result = func(*args, **kwargs)
            logging.info(f'{func.__name__} executed successfully.')
            return result
        except Exception as e:
            logging.error(f'Error in {func.__name__}: {e}')
            logging.debug(traceback.format_exc())
            raise
    return wrapper

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class RDS(metaclass=SingletonMeta):
    def __init__(self, host: str, user: str, password: str, database: Optional[str] = None):
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('py4j').setLevel(logging.WARNING)

        if not hasattr(self, 'initialized'):
            self.host = host
            self.user = user
            self.password = password
            self.database = database
            self.connection = None
            self.cursor = None
            self.initialized = True

    @log
    def _create_connection(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            use_pure=True
        )
        self.cursor = self.connection.cursor()

    @log
    def _close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    @contextmanager
    @log
    def _mysql_cursor(self):
        self._create_connection()
        try:
            yield self.cursor
        finally:
            self._close_connection()

    @log
    def execute_query(self, query: str, params: Optional[Tuple[Any]] = None) -> pd.DataFrame:
        with self._mysql_cursor() as cursor:
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(rows, columns=columns)

    @log
    def execute_update(self, query: str, params: Optional[Tuple[Any]] = None) -> int:
        with self._mysql_cursor() as cursor:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.rowcount

    @log
    def query_to_spark_df(self, query: str, params: Optional[Tuple[Any]] = None):
        df = self.execute_query(query, params)
        return spark.createDataFrame(df)
