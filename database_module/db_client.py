import yaml, socket
import pandas as pd
from sqlalchemy import create_engine


def main():
    with open('database_module/config/config.yml') as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)

    # Using sqlalchemy and pandas 
    engine = create_engine(conf['URI'])
    query = 'select * from people'
    result = pd.read_sql_query(query, engine) 
    print(result)
    
    print(socket.gethostname())



if __name__ == "__main__":
    main()