from .rds import RDS
import pandas as pd
from typing import Optional

class SQLExecutionError(Exception): pass
class ConnectionError(Exception): pass

def query_rds(query: str, host: str, user: str, password: str, database: Optional[str] = None) -> pd.DataFrame:
    if not query:
        raise ValueError('Query must not be empty')

    try:
        rds_instance = RDS(host=host, user=user, password=password, database=database)
        return rds_instance.execute_query(query)
    except Exception as e:
        raise SQLExecutionError(f'Error executing query: {e}')
