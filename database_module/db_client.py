"""
Database client script
- Allows reading and writing to database defined in config.yml
"""

import yaml, socket
import pandas as pd
from sqlalchemy import create_engine

CONFIG_FILE_PATH = 'database_module/config/config.yml'


def main(): 
    engine = init_conn(CONFIG_FILE_PATH)
    # print(select_all('events', engine))
    # print(socket.gethostname())

    update([1, 2], [[3, 4], [30, 40], [32, 10]], engine)
    print(select_all('events', engine))
    pass

def update(ball_xy, players_xy, engine):
    if players_xy is None: 
        update_query = f"insert into events (src, ball) values ('{socket.gethostname()}', '{ball_xy}');"
    elif ball_xy is None: 
        update_query = f"insert into events (src, players) values ('{socket.gethostname()}', '{players_xy}');"
    else: 
        update_query = f"insert into events (src, ball, players) values ('{socket.gethostname()}', '{ball_xy}', '{players_xy}');"
    
    with engine.connect() as con:
        result = con.execute(update_query)
    print(result)


def init_conn(config):
    """
    Read local config file for database connection information and return connected database object
    """
    with open(config) as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)
    engine = create_engine(conf['URI']) # Using sqlalchemy
    return engine


def select_all(table_name, engine):
    """
    Returns dataframe of specified table
    """
    query = f'select * from {table_name}'
    result = pd.read_sql_query(query, engine) # Using pandas 
    return result


if __name__ == "__main__":
    main()