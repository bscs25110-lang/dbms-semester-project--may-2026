from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="shopify_db"
)

# HOME PAGE (Dashboard)
@app.route('/')
def home():
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    return render_template('home.html', products=total_products, customers=total_customers)

# VIEW PRODUCTS + SEARCH
@app.route('/products')
def products():
    search = request.args.get('search')
    cursor = conn.cursor()

    if search:
        query = "SELECT * FROM products WHERE name LIKE %s"
        cursor.execute(query, (f"%{search}%",))
    else:
        cursor.execute("SELECT * FROM products")

    data = cursor.fetchall()
    return render_template('products.html', products=data)

# ADD PRODUCT
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
        conn.commit()

        return redirect('/products')

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)

