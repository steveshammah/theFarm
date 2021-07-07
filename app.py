from flask import Flask, render_template, url_for, request, redirect, session
from model import User, Admin


app = Flask(__name__)
app.secret_key = 'thesecretkey'


@app.route('/')
def home():
    try:
        user_email = session['email']
        if '@theFarm.co.ke' in user_email:
            return render_template('landing.html', employee_email=user_email)
        else:
            return render_template('landing.html', customer_email=user_email)
    except KeyError:
        return render_template('landing.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname, lname = request.form['username'].split(' ')[0], request.form['username'].split(' ')[1]
        email = request.form['email']
        phone = request.form['phone-number']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        residence = request.form['residence']
        customer = User(email)
        customer.sign_up(fname, lname, email, phone, residence, password, confirm_password)
        if customer.sign_up(fname, lname, email, phone, residence, password, confirm_password) == True:
            customer_details = customer.log_in(password)[1]
            session['email'] = email
            session['customer_id'] = customer_details[4]
            return render_template('customer.html', customer_details=customer_details)
        else:
            message = 'Passwords did not match'
            return render_template('signup.html', message=message)
    else:
        print('getting signup  template')
        return render_template('signup.html')


@app.route('/employee_login', methods=['POST', 'GET'])
def employee_login():
    if request.method == 'GET':
        session.pop('email', None)
        session.pop('employee_id', None)
        return render_template('employee-login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        print(f'Email: {email} & password: {password}')
        employee = User(email)
        Admin(employee).log_in(password)

        if Admin(employee).log_in(password)[0] == True:
            # SUCCESSFULL LOGIN
            employee_details = Admin(employee).log_in(password)[1]
            session['email'] = email
            session['employee_id'] = employee_details[0][2]
            print(session['employee_id'])
            # orders = Admin(email).orders_by_id(session['user_id'])
            return redirect('employee')
            # return render_template('employee.html', email=email, employee_details=employee_details[0], orders=orders)
        elif Admin(employee).log_in(password) == 'Wrong Password':
            message = 'Wrong password'
            return render_template('employee-login.html', message=message)
        elif Admin(employee).log_in(password) == 'Email Not Found':
            message = 'Email Not Found'
            return render_template('employee-login.html', message=message)
        else:
            return render_template('employee-login.html')


@app.route('/admin')
def admin():
    try:
        email = session['email']
        # employee_id = session['employee_id']
        admin = Admin('admin@theFarm.co.ke')
        employees = admin.employee_table()
        customers = admin.customers_table()
        orders = admin.orders_table()
        return render_template('admin.html', employees=employees, customers=customers, orders=orders, email=email)
    except KeyError:
        return redirect('employee_login')


@app.route('/management')
def management():
    return render_template('management.html')


@app.route('/new-employee', methods=['POST'])
def new_employee():
    fname, lname = request.form['employee-name'].split(' ')[0], request.form['employee-name'].split(' ')[1]
    phone = request.form['employee-phone']
    admin = request.form.get('rights')
    print(admin)
    if admin.upper() == 'sudo'.upper():
        rights = True
    else:
        rights = False
    user = User('admin@theFarm.coke')
    Admin(user).create_employee(fname, lname, phone, rights)
    return redirect(url_for('admin'))


@app.route('/employee')
def employee():
    try:
        email = session['email']
        employee_id = session['employee_id']
        my_details = Admin(email).my_details(employee_id)
        orders = Admin(email).orders_by_id(employee_id)
        return render_template('employee.html', employee_details=my_details[0], email=email, orders=orders)
    except KeyError:
        return redirect('employee_login')


@app.route('/login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'GET':
        session.pop('email', None)
        session.pop('customer_id', None)
        return render_template('customer-login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        print(f'Email: {email} & password: {password}')
        customer = User(email)
        if customer.log_in(password) == True:        # SUCCESSFUL LOGIN
            session['email'] = email
            print('successful login')
            # SESSION EMAIL SET
            return redirect('customer')
            # return render_template('customer.html', customer_details=customer_details)
        elif customer.log_in(password) == 'Wrong Password':
            message = 'Wrong password!'
            return render_template('customer-login.html', message=message)
        elif customer.log_in(password) == 'Email Not Found':
            message = 'Email Not Found!'
            return render_template('customer-login.html', message=message)
        else:
            return render_template('customer-login.html')


@app.route('/customer')
def customer():
    try:
        email = session['email']
        customer_details = User(email).user_details()[0]
        session['customer_id'] = customer_details[0]            # SESSION USER ID SET
        orders = Admin(email).orders_by_id(session['customer_id'])
        chicks = Admin(email).sort_orders('chicks', session['customer_id'])
        layers = Admin(email).sort_orders('layers', session['customer_id'])
        cocks = Admin(email).sort_orders('cocks', session['customer_id'])
        order_list = [chicks, layers, cocks]
        print('ORDER LIST: ', order_list)
        return render_template('customer.html', customer_details=customer_details, orders=orders, order_list=order_list)
    except KeyError:
        return render_template('customer-login.html')

    except IndexError:
        return render_template('customer.html', customer_details=customer_details)


@app.route('/order/<string:product_name>', methods=['POST', 'GET'])
def order(product_name):
    order_details = product_name
    count = request.form['count']
    print(order_details, count)
    customer_id = session['customer_id']
    admin = Admin('admin@theFarm.co.ke')
    admin.place_order(customer_id, order_details, count)
    email = session['email']
    customer_details = User(email).user_details()[0]
    session['customer_id'] = customer_details[0]  # SESSION USER ID SET
    orders = Admin(email).orders_by_id(session['customer_id'])
    message = 'ORDER HAS BEEN PLACED!'
    return render_template('customer.html', customer_details=customer_details, orders=orders, message=message)


if __name__ == '__main__':
    app.run(debug=True, port=7070)
