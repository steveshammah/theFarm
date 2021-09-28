from flask import Flask, render_template, url_for, request, redirect, session
from model import User, Admin


app = Flask(__name__)
app.secret_key = 'thesecretkey'


@app.route('/')
def home():
    try:
        user_email = session['email']
        admin = Admin('guest@theFarm.co.ke')
        feedbacks = admin.feedback_table()[::-1]
        if '@theFarm.co.ke' in user_email:
            return render_template('landing.html', employee_email=user_email, feedbacks=feedbacks)
        else:
            return render_template('landing.html', customer_email=user_email, feedbacks=feedbacks)
    except KeyError:
        return render_template('landing.html', feedbacks=feedbacks)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name, last_name = request.form['username'].split(' ')
        email = request.form['email']
        phone = request.form['phone-number']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        residence = request.form['residence']
        customer = User(email)
        print('Customer', customer)
        if customer.is_valid_email(email) == True:
            customer.sign_up(first_name, last_name, email, phone, residence, password, confirm_password)
            print('Creating User')
            if customer.sign_up(first_name, last_name, email, phone, residence, password, confirm_password) == True:

                customer_details = customer.log_in(password)
                # print(customer_details)
                session['email'] = email
                session['customer_id'] = customer_details[4]
                return render_template('customer.html', customer_details=customer_details)
            else:
                message = 'Passwords did not match'
                return render_template('signup.html', message=message)
        else:
            message = 'Email has already been used!!'
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
        # print(f'Email: {email} & password: {password}')
        employee = User(email)
        Admin(employee).log_in(password)
        # print(Admin(employee).log_in(password), 'STATUS')

        if Admin(employee).log_in(password)[0] == True:
            # SUCCESSFULL LOGIN
            employee_details = Admin(employee).log_in(password)
            # print('EMPLOYEE DETAILS: ', employee_details)
            session['email'] = email
            session['employee_id'] = employee_details[2]
            # print('USER ID IN SESSION', session['employee_id'])
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


# Make use of URL
@app.route('/management', methods=['GET', 'POST'])
def management():
    try:
        if request.method == 'POST':
            employee_id = session['employee_id']
            return render_template('management.html')
        else:
            admin_email = session['email']
            admin_id = session['employee_id']
            admin = Admin(admin_email)
            flock = admin.flock_table()
            brooders = admin.brooders_table()
            orders = admin.orders_table()
            feedbacks = admin.feedback_table()
            employees = admin.employee_table()
            customers = admin.customers_table()
            return render_template('management.html', flock=flock, brooders=brooders, orders=orders,
                                   feedbacks=feedbacks, employees=employees, customers=customers, admin=admin)
    except KeyError:
        redirect(url_for('employee_login'))


@app.route('/update/flock', methods=['POST'])
def admin_table_update():
    admin = Admin(session['email'])
    flock_quantity = request.form['flock-quantity']
    flock_price = request.form['flock-price']
    date_bought = request.form['date-bought']
    timestamp = admin.convert_to_timestamp(date_bought)
    print('Flock Details', flock_quantity, flock_price, timestamp)
    admin.update_flock_table(flock_quantity, flock_price, timestamp)
    return redirect(url_for('management'))


@app.route('/new-employee', methods=['POST'])
def new_employee():
    first_name, last_name = request.form['employee-name'].split(' ')
    phone = request.form['employee-phone']
    section = request.form['section']
    admin = request.form.get('rights')
    # print(admin)
    if admin.upper() == 'sudo'.upper():
        rights = True
    else:
        rights = False
    user = User('admin@theFarm.coke')
    Admin(user).create_employee(first_name, last_name, phone, rights, section)
    return redirect(url_for('admin'))


@app.route('/employee')
def employee():
    try:
        employee_email = session['email']
        employee_id = session['employee_id']
        # print('EMPLOYEE ID: ', employee_id)
        my_details = Admin(employee_email).my_details(employee_id)
        orders = Admin(employee_email).get_orders_by_id(employee_id)
        return render_template('employee.html', employee_details=my_details[0], email=employee_email, orders=orders)
    except KeyError:
        return redirect('employee_login')


#  Health Specialist
@app.route('/employee/health', methods=['POST', 'GET'])
def health():
    try:
        employee_id = session['employee_id']
        employee_email = session['email']
        username = session['username']
        if request.method == 'GET':
            return render_template('healthSpecialist.html', username=username, email=employee_email)
        else:
            pass
    except KeyError:
        redirect(url_for('employee_login'))


# Brooder Worker Section
@app.route('/employee/brooder', methods=['POST', 'GET'])
def brooder():
    try:
        employee_id = session['employee_id']
        employee_email = session['email']
        username = session['username']

        if request.method == 'GET':
            return render_template('brooderWorker.html', username=username, email=employee_email)
        else:
            pass
    except KeyError:
        redirect(url_for('employee_login'))


# CUSTOMER SECTION
@app.route('/login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'GET':
        session.pop('email', None)
        session.pop('customer_id', None)
        return render_template('customer-login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        # print(f'Email: {email} & password: {password}')
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


@app.route('/<string:username>/settings', methods=['POST', 'GET'])
def settings(username):
    user_email = session['email']
    user_data = Admin(user_email).user_details()
    return render_template('settings.html', user=user_data, username=username)


# Customer Profile
@app.route('/customer')
def customer():
    try:
        email = session['email']
        customer_details = User(email).user_details()[0]
        username = email.split('@')[0]
        session['customer_id'] = customer_details[0]            # set user ID in session
        session['username'] = username       # set user ID in session
        # print(customer_details)
        # print(session)
        orders = Admin(email).get_orders_by_id(session['customer_id'])      # Fetch user's orders
        # print('ORDERS', orders == True)

        # Check if user has orders and sort them
        if orders:
            chicks = Admin(email).sort_orders('chicks', session['customer_id'])
            layers = Admin(email).sort_orders('layers', session['customer_id'])
            cocks = Admin(email).sort_orders('cocks', session['customer_id'])
            order_list = [chicks, layers, cocks]
            # print('ORDER LIST: ', order_list)
            return render_template('customer.html', username=username, customer_details=customer_details, orders=orders, order_list=order_list)
        else:
            return render_template('customer.html', username=username, customer_details=customer_details, orders=orders)

    except KeyError:
        return render_template('customer-login.html')

    except IndexError:
        return render_template('customer.html', customer_details=customer_details)


# Place Order
@app.route('/orders/checkout', methods=['POST', 'GET'])
def place_order():
    order = []
    return redirect(url_for('my_orders'))


# User Orders Page
@app.route('/myorders', methods=['GET', 'POST'])
def my_orders():
    try:
        if request.method == 'GET':
            customer_email = session['email']
            username = session['username']
            customer_id = session['customer_id']
            customer = Admin(customer_email)
            orders = customer.get_orders_by_id(customer_id)
            print(orders)
            return render_template('customer-orders.html', orders=orders, username=username)
        else:
            pass
    except KeyError:
        return redirect('employee_login')


# User Feedback
@app.route('/feedback', methods=['POST'])
def feedback():
    customer_email = session['email']
    customer_id = session['customer_id']
    content = request.form['feedback-content']
    customer = Admin(customer_email)
    customer.save_feedback(customer_id, content)
    return redirect(url_for('customer'))


# Run app
if __name__ == '__main__':
    app.run(debug=True, port=7070)
