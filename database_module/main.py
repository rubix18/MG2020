import db_client as dbc   # import the db client library


CONFIG_FILE_PATH = 'database_module/config/config.yml'

def main(): 
    engine = dbc.init_conn(CONFIG_FILE_PATH)
    dbc.update([1, 2], [[3, 4], [30, 40], [32, 10]], engine)
    print(dbc.select_all('events', engine))

if __name__ == "__main__":
    main()