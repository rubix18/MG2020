import db_client as dbc   # import the db client library


CONFIG_FILE_PATH = 'config/config.yml'

def main(): 
    engine = dbc.init_conn(CONFIG_FILE_PATH)
    
    # dbc.update args: camera_location (string), ball_xy (1x2 list), players_xy (nx2 list of lists, where n is number of detected players), database_engine (object)
    # dbc.update('right corner', [1, 2], [[3, 4], [30, 40], [32, 10]], engine)
    # print(dbc.select_all('events', engine))

    dbc.ping_test(engine)

if __name__ == "__main__":
    main()