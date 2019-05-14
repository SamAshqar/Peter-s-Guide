import mysql.connector
import json
# import PrettyTable
# from data_download import get_yelp_food_dict, get_business_data

def create_connection():
    user, database, password, host, port = _get_sql_details()
    conn = mysql.connector.connect(user=user, database=database, password=password, host=host, port=port)

def del_table(table):
    user, database, password, host, port = _get_sql_details()
    conn = mysql.connector.connect(user=user, database=database, password=password, host=host, port=port)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE {};".format(table))

def create_food_places_table():
    user, database, password, host, port = _get_sql_details()
    conn = mysql.connector.connect(user=user, database=database, password=password, host=host, port=port)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS food_places(
                        id INTEGER AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        location VARCHAR(255) NOT NULL,
                        image VARCHAR(255), 
                        rating DECIMAL(2, 1),
                        phone VARCHAR(255),
                        latitude DECIMAL(8, 5) NOT NULL,
                        longitude DECIMAL(8, 5) NOT NULL);"""
                    )
    cursor.close()
    conn.close()

def create_hours_table():
    user, database, password, host, port = _get_sql_details()
    conn = mysql.connector.connect(user=user, database=database, password=password, host=host, port=port)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS hours(
                        id INTEGER AUTO_INCREMENT PRIMARY KEY,
                        start TIME NOT NULL, 
                        end TIME NOT NULL, 
                        day VARCHAR(255) NOT NULL, 
                        bussiness_id INTEGER,
                        FOREIGN KEY (bussiness_id) REFERENCES food_places(id));"""
                    )
    cursor.close()
    conn.close()


                   

def show_tables():
    user, database, password, host, port = _get_sql_details()
    conn = mysql.connector.connect(user=user, database=database, password=password, host=host, port=port)
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES;')


def insert_data(data):
    user, database, password, host, port = _get_sql_details()
    conn = mysql.connector.connect(user=user, database=database, password=password, host=host, port=port)
    cursor = conn.cursor()
    sql = """INSERT INTO food_places(name, location, image, rating, phone, latitude, longitude) VALUES(%s, %s, %s, %s, %s, %s, %s);"""
    cursor.execute(sql, data)               
    conn.commit()


def insert_yelp_data(file):
    temp_bus_dict = {}
    temp_hours_dict = {}
    for line in open(file):
        if '->' not in line:
            if temp_bus_dict != {}:
                data = [temp_bus_dict['name'], temp_bus_dict['location'], temp_bus_dict['image'], 
                            temp_bus_dict['rating'], temp_bus_dict['phone'], temp_bus_dict['latitude'], 
                            temp_bus_dict['longitude']]
                insert_data(data)

                # insert hours into database
                j = json.loads('')

                for each in j['open']:
                    print (each['day'])

            temp_bus_dict = {}
            temp_bus_dict['name'] = line.rstrip()
        else:
            category, value = line.split('-> ')
            if category == 'hours':
                # temp_hours_dict[category] = 
                pass
            else:
                temp_bus_dict[category] = value.rstrip()




def print_table(table):
    user, database, password, host, port = _get_sql_details()
    conn = mysql.connector.connect(user=user, database=database, password=password, host=host, port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {};".format(table))
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def _get_sql_details():
    f = open('sql_conn_details.txt', 'r')
    sql_details = []
    for line in f:
        k, v = line.split(': ')
        v = v.rstrip()
        if k == 'port':
            v = int(v)
        sql_details.append(v)
    return sql_details

if __name__=='__main__':
    # del_table('food_places')
    # create_food_places_table()
    # insert_yelp_data('yelp_data.txt')
    # show_tables()
    print_table('food_places')
    

