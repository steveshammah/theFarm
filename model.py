import mysql.connector
from datetime import datetime
import hashlib
from functools import reduce


DBCONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'admin',
    'database': 'theFarm'
}
# conn = mysql.connector.connect(**DBCONFIG)
# cursor = conn.cursor(buffered=True)
# conn.commit()
# cursor.close()
# conn.close()


class DbManager:
    def __init__(self, **DBCONFIG):
        self.config = DBCONFIG

    def __enter__(self):
        self.conn = mysql.connector.connect(**DBCONFIG, charset='utf8')
        self.cursor = self.conn.cursor(buffered=True)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


# CREATE SQL TABLES
def create_employees_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE employees (employee_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, first_name 
        VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL, email VARCHAR(200) NOT NULL, phone VARCHAR(100) NOT NULL, admin BOOL, 
        password VARCHAR(500) NOT NULL, status VARCHAR(20) NOT NULL, date DATETIME DEFAULT CURRENT_TIMESTAMP ); '''
        cursor.execute(SQL)


# Customers Table
def create_customers_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE customers (customer_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, first_name 
        VARCHAR(100) NOT NULL, last_name VARCHAR(100) NOT NULL, email VARCHAR(200) NOT NULL, 
        phone VARCHAR(100) NOT NULL, password VARCHAR(500) NOT NULL, residence VARCHAR(200), 
        status VARCHAR(20) NOT NULL, date DATETIME DEFAULT CURRENT_TIMESTAMP ); '''
        cursor.execute(SQL)


# Orders Table
def create_orders_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE orders (order_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
        customer_id INT, order_item VARCHAR(100) NOT NULL, date DATETIME DEFAULT CURRENT_TIMESTAMP, 
        status VARCHAR(100) NOT NULL, FOREIGN KEY(customer_id) REFERENCES customers(customer_id)); '''
        cursor.execute(SQL)


# Flock Table
def create_flock_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE `flock` (`flock_id` INT NOT NULL AUTO_INCREMENT,`quantity` INT NOT NULL,
        `price` INT NOT NULL,`date_bought` DATETIME DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (`flock_id`));'''
        cursor.execute(SQL)


# Brooder Table
def create_brooder_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE `brooder` (`brooder_id` int PRIMARY KEY NOT NULL,`quantity` int NOT NULL,
        `price` int NOT NULL,`date_bought` DATETIME DEFAULT CURRENT_TIMESTAMP);'''
        cursor.execute(SQL)


# Brooder Description
def create_brooder_description_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE `brooder description` (`brooder_id` int PRIMARY KEY NOT NULL,`flock_id` int NOT NULL,
        `last_flock_vaccinations` DATETIME DEFAULT CURRENT_TIMESTAMP,`last_cleaning` DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (`flock_id`) REFERENCES flock(`flock_id`));'''
        cursor.execute(SQL)


# Feeds Table
def create_feeds_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE feeds (
        feeds_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
        type VARCHAR(100) NOT NULL,
        quantity INT NOT NULL,
        date_bought DATETIME
         );'''
        cursor.execute(SQL)


# Feeds Usage Table
def create_feeds_usage_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE `feeds usage` (`usage_id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
        `brooder_id` int NOT NULL,`flock_id` int NOT NULL,
        `feeds_type` VARCHAR(100) NOT NULL,`feeds_quantity` INT NOT NULL,
        `date` DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (`brooder_id`) REFERENCES brooder(`brooder_id`),
        FOREIGN KEY (`flock_id`) REFERENCES flock(`flock_id`));'''
        cursor.execute(SQL)


# Medicine Table
def create_medicine_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE medicine (
        medicine_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
        medicine_details VARCHAR(300) NOT NULL,
        date_bought DATETIME,
        last_use_date DATETIME DEFAULT CURRENT_TIMESTAMP
         );'''
        cursor.execute(SQL)


# Health Stats Table
def create_health_stats_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE `health statistics` (`stats_id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
        `brooder_id` int NOT NULL,`flock_id` int NOT NULL,
        `feeds_type` VARCHAR(100) NOT NULL,
          `flock_mortality` INT NOT NULL,
        `health_status` VARCHAR(300) NOT NULL,
        `date` DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (`brooder_id`) REFERENCES brooder(`brooder_id`),
        FOREIGN KEY (`flock_id`) REFERENCES flock(`flock_id`));'''
        cursor.execute(SQL)


# Sales Table
def create_sales_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE sales(
            sales_id INT PRIMARY KEY NOT NULL,
            order_id INT  NOT NULL,
            order_cost INT NOT NULL,
            date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(order_id) REFERENCES orders(order_id)
        );'''
        cursor.execute(SQL)


# Feedback Table
def create_feedback_table():
    with DbManager(**DBCONFIG) as cursor:
        SQL = '''CREATE TABLE feedback(
            feedback_id INT PRIMARY KEY NOT NULL,
            customer_id INT NOT NULL,
            feedback_details VARCHAR(250) NOT NULL,
            date DATETIME DEFAULT CURRENT_TIMESTAMP
        );'''
        cursor.execute(SQL)


# RUN CREATE TABLE QUERIES
def create_tables():
    try:
        create_employees_table()
        create_customers_table()
        create_orders_table()
        create_flock_table()
        create_brooder_table()
        create_brooder_description_table()
        create_feeds_table()
        create_feeds_usage_table()
        create_medicine_table()
        create_health_stats_table()
        create_sales_table()
        create_feedback_table()
        print('TABLE CREATED')
    except Exception as error:
        print('TABLE NOT CREATED')
        print(error)


# create_tables()


# SHOW TABLES
def show_tables():
    with DbManager(**DBCONFIG) as cursor:
        call_to_db = '''SHOW TABLES'''
        cursor.execute(call_to_db)
        tables = cursor.fetchall()
        for table in tables:
            print(table[0])
        print(f'Table count: {len(tables)}')
        return tables


# show_tables()




class User:
    def __init__(self, email: str):
        self.email = email

    def __repr__(self):
        return self.email

    def sign_up(self, first_name: str, last_name: str, email: str, phone: str, residence: str, password: str,
                confirm_password: str):
        if password == confirm_password:
            encrypt_pass = hashlib.sha256(password.encode()).hexdigest()
            status = 'active'
            with DbManager(**DBCONFIG) as cursor:
                sign_up_sql = '''INSERT INTO customers (first_name, last_name, email, phone, residence, password, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                cursor.execute(sign_up_sql, (first_name, last_name, email, phone, residence, encrypt_pass, status))
                print('SIGN UP SUCCESS...')
                return True
        else:
            return False

    def log_in(self, password: str):
        with DbManager(**DBCONFIG) as cursor:
            all_users_sql = '''SELECT email, password, customer_id FROM customers'''
            cursor.execute(all_users_sql)
            all_customers_details = cursor.fetchall()
            for customer_detail in all_customers_details:
                if str(self.email) in customer_detail:
                    if customer_detail[1] == hashlib.sha256(password.encode()).hexdigest():
                        return True
                    else:
                        return 'Wrong Password'
            else:
                return 'Email Not Found'

    def user_details(self):
        with DbManager(**DBCONFIG) as cursor:
            user_details = '''SELECT * FROM customers WHERE email = %s'''
            cursor.execute(user_details, (self.email, ))
            return cursor.fetchall()

    # Check if email exists in DB
    def verify_email(self, email: str):
        with DbManager(**DBCONFIG) as cursor:
            SQL = '''SELECT DISTINCT email FROM customers'''
            cursor.execute(SQL)
            emails = cursor.fetchall()
            for email in emails:
                if email in emails:
                    return False
                else:
                    return True

    # Check if user is active in the system
    def is_active(self, status: str):
        if status == 'active':
            return True
        else:
            return False


class Admin(User):
    def __init__(self, email: str):
        super().__init__(email)

    def create_employee(self, first_name, last_name, phone, rights, section):
        email = first_name[0] + last_name + '@theFarm.co.ke'
        password = hashlib.sha256('theFarm123'.encode()).hexdigest()
        status = 'active'
        with DbManager(**DBCONFIG) as cursor:
            admin_sql = '''INSERT INTO employees (first_name, last_name, email, phone, admin, password, status, section) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(admin_sql, (first_name, last_name, email, phone, rights, password, status, section))
            return True

    def delete_employee(self, employee_id: int):
        with DbManager(**DBCONFIG) as cursor:
            SQL = '''DELETE FROM employees WHERE employee_id = %s'''
            cursor.execute(SQL, employee_id)
            return True

    # Deactivate employee
    def disable_user(self, user_details: str, user_id: int, status: str):
        with DbManager(**DBCONFIG) as cursor:
            if user_details == 'employee':
                SQL = '''UPDATE employees SET status = %s WHERE employee_id = %s'''
            else:
                SQL = '''UPDATE customers SET status = %s WHERE customer_id = %s'''
        cursor.execute(SQL, status, user_id)

    def log_in(self, password: str):
        with DbManager(**DBCONFIG) as cursor:
            all_users_sql = '''SELECT email, password, employee_id, first_name, last_name, admin, phone 
            FROM employees'''
            cursor.execute(all_users_sql)
            all_employee_details = cursor.fetchall()
            for employee_detail in all_employee_details:
                if str(self.email) in employee_detail:
                    if employee_detail[1] == hashlib.sha256(password.encode()).hexdigest():
                        # print('SOME DATA FROM THE USER: ', employee_detail[2])
                        return [True, self.my_details(employee_detail[2]), employee_detail[2]]
                    else:
                        return 'Wrong Password'
            else:
                return 'Email Not Found'

    def my_details(self, user_id: int):
        # print('USER ID', user_id)
        with DbManager(**DBCONFIG) as cursor:
            my_details_sql = '''SELECT email, password, admin, first_name, last_name, phone, section FROM employees 
            WHERE employee_id = %s'''
            cursor.execute(my_details_sql, (user_id,))
            employee_data = cursor.fetchall()
            # print('EMPLOYEE DATA IN DB', employee_data)
            return employee_data


    def employee_table(self):
        with DbManager(**DBCONFIG) as cursor:
            employee_sql = '''SELECT * FROM employees'''
            cursor.execute(employee_sql)
            return cursor.fetchall()

    def customers_table(self):
        with DbManager(**DBCONFIG) as cursor:
            customers_sql = '''SELECT * FROM customers'''
            cursor.execute(customers_sql)
            return cursor.fetchall()

    def orders_table(self):
        with DbManager(**DBCONFIG) as cursor:
            orders_sql = '''SELECT * FROM orders'''
            cursor.execute(orders_sql)
            return cursor.fetchall()

    def orders_by_id(self, customer_id: int):
        with DbManager(**DBCONFIG) as cursor:
            orders_by_sql = '''SELECT * FROM orders WHERE customer_id = %s'''
            cursor.execute(orders_by_sql, (customer_id, ))
            return cursor.fetchall()

    def sort_orders(self, product: str, customer_id: int):
        with DbManager(**DBCONFIG) as cursor:
            product_sql = '''SELECT sum(count) FROM orders WHERE order_item = %s and customer_id = %s'''
            cursor.execute(product_sql, (product, customer_id))
            return cursor.fetchall()

    def place_order(self, customer_id: int, order_details: str, count: int):
        with DbManager(**DBCONFIG) as cursor:
            order_details_sql = '''INSERT INTO orders (customer_id, order_item, count) VALUES(%s, %s, %s)'''
            cursor.execute(order_details_sql, (customer_id, order_details, count))

    def flock_table(self):
        with DbManager(**DBCONFIG) as cursor:
            SQL = '''SELECT * FROM flock'''
            cursor.execute(SQL)
            flock_data = cursor.fetchall()
            return flock_data

    def update_flock_table(self, quantity, price, date):
        with DbManager(**DBCONFIG) as cursor:
            update_flock_sql = '''INSERT INTO flock (quantity, price, date_bought) VALUES(%s, %s, %s)'''
            cursor.execute(update_flock_sql, (quantity, price, date))
            return True

    def brooders_table(self):
        with DbManager(**DBCONFIG) as cursor:
            SQL = '''SELECT * FROM brooder'''
            cursor.execute(SQL)
            brooder_data = cursor.fetchall()
            return brooder_data

    def feedback_table(self):
        with DbManager(**DBCONFIG) as cursor:
            SQL = '''SELECT * FROM feedback'''
            cursor.execute(SQL)
            feedback_data = cursor.fetchall()
            return feedback_data

    def convert_to_timestamp(self, time):
        time_string = f'{time}T08::00::00.000000'
        timestamp = datetime.strptime(time_string, '%Y-%m-%dT%H::%M::%S.%f')
        return timestamp



user = User('admin@theFarm.co.ke')


