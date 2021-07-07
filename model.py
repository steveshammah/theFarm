import mysql.connector
from datetime import datetime
import hashlib
from functools import reduce


DBCONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'admin',
    'database': 'chicksysDB'
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

#CREATE SQL TABLES
# def create_employees_table():
#     with DbManager(**DBCONFIG) as cursor:
#         SQL = '''create table employees (employee_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, fname VARCHAR(100) NOT NULL,
#         lname VARCHAR(100) NOT NULL, email VARCHAR(200) NOT NULL, phone VARCHAR(100) NOT NULL, admin BOOL, date DATETIME
#         DEFAULT CURRENT_TIMESTAMP ); '''
#         cursor.execute(SQL)
#
#
# def create_customers_table():
#     with DbManager(**DBCONFIG) as cursor:
#         SQL = '''create table customers (customer_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, fname VARCHAR(100) NOT NULL,
#         lname VARCHAR(100) NOT NULL, email VARCHAR(200) NOT NULL, phone VARCHAR(100) NOT NULL, residence VARCHAR(200),
#          date DATETIME DEFAULT CURRENT_TIMESTAMP ); '''
#         cursor.execute(SQL)
#
# def create_orders_table():
#     with DbManager(**DBCONFIG) as cursor:
#         SQL = '''create table orders (order_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
#         customer_id INT, order_item VARCHAR(100) NOT NULL,
#          date DATETIME DEFAULT CURRENT_TIMESTAMP,
#          FOREIGN KEY(customer_id) REFERENCES customers(customer_id)); '''
#         cursor.execute(SQL)
# create_customers_table()
# create_customers_table()
# create_orders_table()


# SHOW TABLES
# def test():
#     with DbManager(**DBCONFIG) as cursor:
#         call_to_db = '''SHOW TABLES'''
#         cursor.execute(call_to_db)
#         return cursor.fetchall()


# tables = test()
# print(datetime.now().year)
# for table in tables:
#     print(table[0])


class User:
    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return self.email

    def sign_up(self, fname, lname, email, phone, residence, password, confirm_password):
        if password == confirm_password:
            encrypt_pass = hashlib.sha256(password.encode()).hexdigest()
            with DbManager(**DBCONFIG) as cursor:
                sign_up_sql = '''INSERT INTO customers (fname, lname, email, phone, residence, password)
                VALUES (%s, %s, %s, %s, %s, %s)'''
                cursor.execute(sign_up_sql, (fname, lname, email, phone, residence, encrypt_pass))
                print('SIGN UP SUCCESS...')
                return True
        else:
            return False

    def log_in(self, password):
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


class Admin(User):
    def __init__(self, email):
        super().__init__(email)

    def create_employee(self, fname, lname, phone, rights):
        email = fname[0] + lname + '@theFarm.co.ke'
        password = hashlib.sha256('theFarm123'.encode()).hexdigest()
        with DbManager(**DBCONFIG) as cursor:
            admin_sql = '''INSERT INTO employees (fname, lname, email, phone, admin, password) 
            VALUES (%s, %s, %s, %s, %s, %s)'''
            cursor.execute(admin_sql, (fname, lname, email, phone, rights, password))
            return True

    def log_in(self, password):
        with DbManager(**DBCONFIG) as cursor:
            all_users_sql = '''SELECT email, password, admin, fname, lname, employee_id, phone FROM employees'''
            cursor.execute(all_users_sql)
            all_employee_details = cursor.fetchall()
            for employee_detail in all_employee_details:
                if str(self.email) in employee_detail:
                    if employee_detail[1] == hashlib.sha256(password.encode()).hexdigest():
                        return [True, self.my_details(employee_detail[5])]
                    else:
                        return 'Wrong Password'
            else:
                return 'Email Not Found'

    def my_details(self, user_id):
        with DbManager(**DBCONFIG) as cursor:
            my_details_sql = '''SELECT email, password, admin, fname, lname, phone FROM employees WHERE employee_id = %s'''
            cursor.execute(my_details_sql, (user_id,))
            return cursor.fetchall()

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

    def orders_by_id(self, customer_id):
        with DbManager(**DBCONFIG) as cursor:
            orders_by_sql = '''SELECT * FROM orders WHERE customer_id = %s'''
            cursor.execute(orders_by_sql, (customer_id, ))
            return cursor.fetchall()

    def sort_orders(self, product, customer_id):
        with DbManager(**DBCONFIG) as cursor:
            product_sql = '''SELECT sum(count) FROM orders WHERE order_item = %s and customer_id = %s'''
            cursor.execute(product_sql, (product, customer_id))
            return cursor.fetchall()

    def place_order(self, customer_id, order_details, count):
        with DbManager(**DBCONFIG) as cursor:
            order_details_sql = '''INSERT INTO orders (customer_id, order_item, count) VALUES(%s, %s, %s)'''
            cursor.execute(order_details_sql, (customer_id, order_details, count))



# user = User('admin@theFarm.co.ke')
# print(Admin(user).log_in('Sudo'))


