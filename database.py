import mysql.connector
# import PrettyTable
# from data_download import get_yelp_food_dict, get_business_data

def create_connection():
    conn = mysql.connector.connect(user='root', database='petersguide', password='password', host='127.0.0.1', port=3307)
    


def del_table(table):
    conn = mysql.connector.connect(user='root', database='petersguide', password='password', host='127.0.0.1', port=3307)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE {};".format(table))

def create_food_places_table():
    conn = mysql.connector.connect(user='root', database='petersguide', password='password', host='127.0.0.1', port=3307)
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

def show_tables():
    conn = mysql.connector.connect(user='root', database='petersguide', password='password', host='127.0.0.1', port=3307)
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES;')


def insert_data(data):
    conn = mysql.connector.connect(user='root', database='petersguide', password='password', host='127.0.0.1', port=3307)
    cursor = conn.cursor()
    sql = """INSERT INTO food_places(name, location, image, rating, phone, latitude, longitude) VALUES(%s, %s, %s, %s, %s, %s, %s);"""
    cursor.execute(sql, data)               
    # cursor.execute("""INSERT INTO food_places(name, location, image, rating, phone, latitude, longitude) VALUES({name}, {location}, {image}, {rating}, {phone}, {latitude}, {longitude});""".format(
    #                         name=name, location=location, image=image, rating=rating, phone=phone,
    #                         latitude=latitude, longitude=longitude)
    #               )
    conn.commit()


def print_table(table):
    conn = mysql.connector.connect(user='root', database='petersguide', password='password', host='127.0.0.1', port=3307)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {};".format(table))
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

def insert_yelp_data(file):
    temp_dict = {}
    for line in open(file, 'a+'):
        if '->' not in line:
            if temp_dict != {}:
                data = [temp_dict['name'], temp_dict['location'], temp_dict['image'], 
                            temp_dict['rating'], temp_dict['phone'], temp_dict['latitude'], 
                            temp_dict['longitude']]
                insert_data(data)
            temp_dict = {}
            temp_dict['name'] = line.rstrip()
        else:
            category, value = line.split('-> ')
            temp_dict[category] = value.rstrip()
        
   
    


if __name__=='__main__':
    del_table('food_places')
    create_food_places_table()
    insert_yelp_data('yelp_data.txt')
    # show_tables()
    # print_table('food_places')
    

