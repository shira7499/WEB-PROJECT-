from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'your_secret_key'

TWILIO_ACCOUNT_SID = 'ACefaacb760e211db2cc815166552534f5'
TWILIO_AUTH_TOKEN = '2211175f0ad0c199a9a40a9150cbc330' 
TWILIO_WHATSAPP_FROM = 'whatsapp:+14155238886'

# פונקציה לשליחת הודעת WhatsApp
def send_whatsapp_message(to, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    if not to.startswith('+'):
        to = '+972' + to.lstrip('0')  # הוספת הקידומת הבינלאומית לישראל אם לא קיימת
    message = client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_FROM,
        to=f'whatsapp:{to}'
    )
    return message.sid

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu_page():
    return render_template('menu.html')

@app.route('/blog')
def blog_page():
    return render_template('blog.html')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('add_dish'))
            elif user['role'] == 'customer':
                return redirect(url_for('customer_dashboard'))
            elif user['role'] == 'operator':
                return redirect(url_for('operator_dashboard'))
            else:
                return render_template('login.html', error='Invalid role')
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
        
    msg = ""
    if request.method == 'POST':
        try:
            dish_name = request.form['dish_name']
            description = request.form['description']
            price = request.form['price']
            
            with get_db_connection() as con:
                cur = con.cursor()
                cur.execute("INSERT INTO dishes (name, description, price) VALUES (?, ?, ?)", 
                            (dish_name, description, price))
                con.commit()
                
                msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = f"Error in insert operation: {e}"
        finally:
            return render_template("result.html", msg=msg)
    
    return render_template('add_dish.html')

def insert_order(customer_name, phone_number, delivery_address, order_details):
    conn = get_db_connection()
    conn.execute("INSERT INTO orders (customer_name, phone_number, delivery_address, order_details, status) VALUES (?, ?, ?, ?, 'open')",
                 (customer_name, phone_number, delivery_address, order_details))
    order_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute("INSERT INTO open_orders (order_id) VALUES (?)", (order_id,))
    conn.commit()
    conn.close()

@app.route('/customer_dashboard', methods=['GET', 'POST'])
def customer_dashboard():
    if 'username' not in session or session['role'] != 'customer':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    dishes = conn.execute('SELECT * FROM dishes').fetchall()
    conn.close()

    message = None
    summary = None
    total_price = 0

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        phone_number = request.form['phone_number']
        delivery_address = request.form['delivery_address']

        summary = {}
        order_details = ""
        for dish in dishes:
            quantity_str = request.form.get(f'quantity_{dish["id"]}', '0')
            try:
                quantity = int(quantity_str)
            except ValueError:
                quantity = 0
            if quantity > 0:
                summary[dish["name"]] = quantity
                total_price += dish['price'] * quantity
                order_details += f"{dish['name']}: {quantity}, "

        if summary:
            insert_order(customer_name, phone_number, delivery_address, order_details)
            message = "Order placed successfully"
        else:
            message = "Please select at least one item"

    return render_template('customer_dashboard.html', menu_items=dishes, summary=summary, total_price=total_price, message=message)

@app.route('/operator_dashboard', methods=['GET', 'POST'])
def operator_dashboard():
    if 'username' not in session or session['role'] != 'operator':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        order_id = request.form['order_id']
        conn.execute('UPDATE orders SET status = "closed" WHERE id = ?', (order_id,))
        conn.commit()
        conn.execute('DELETE FROM open_orders WHERE order_id = ?', (order_id,))
        conn.commit()
        # שליחת הודעת WhatsApp על הכנת המנה למספר שהוזן בעת ההזמנה
        customer_phone = conn.execute('SELECT phone_number FROM orders WHERE id = ?', (order_id,)).fetchone()['phone_number']
        message_sid = send_whatsapp_message(customer_phone, f"Order {order_id} is ready for delivery.")
        print(f"WhatsApp message SID: {message_sid}")
    
    open_orders = conn.execute('''
        SELECT orders.id, orders.customer_name, orders.phone_number, orders.delivery_address, orders.order_details, orders.status
        FROM orders
        JOIN open_orders ON orders.id = open_orders.order_id
        WHERE orders.status = "open"
    ''').fetchall()
    conn.close()
    
    return render_template('operator_dashboard.html', open_orders=open_orders)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session or session['role'] != 'customer':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        order_id = request.form['order_id']
        rating = request.form['rating']
        comment = request.form['comment']
        image = request.files['image']
        
        # TODO: Handle feedback saving logic
        
        return redirect(url_for('thank_you'))  
    
    return render_template('feedback.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
