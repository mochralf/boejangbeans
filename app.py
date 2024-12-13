from flask_session import Session
from flask import Flask, render_template, redirect, request, session, jsonify, url_for, flash
from datetime import datetime
import mysql.connector
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'kopi123' 

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "boejangbeans"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = []
        
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, nama, harga, stok, foto, typeCoffee FROM product")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', products=products)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    pid = request.form.get('product_id')  # Ensure you're sending the product ID from the frontend
    nama = request.form.get('product')
    harga = request.form.get('price')
    image = request.form.get('image')
    qty = request.form.get('jumlah')
    
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({'id': pid, 'name': nama, 'price': harga, 'image': image, 'quantity': qty})
    session.modified = True

    return redirect(url_for('trolley'))


@app.route('/remove_product', methods=['POST'])
def remove_product():
    try:
        data = request.get_json()
        pid = data.get('pid')

        if not pid:
            return jsonify({'success': False, 'message': 'Product ID tidak ditemukan'}), 400

        if 'cart' not in session:
            return jsonify({'success': False, 'message': 'Keranjang kosong'}), 400

        cart = session['cart']
        product_index = next((index for index, product in enumerate(cart) if product['id'] == pid), None)

        if product_index is not None:
            del cart[product_index]
            session.modified = True
            return jsonify({'success': True, 'message': 'Produk berhasil dihapus', 'cart': cart}), 200
        else:
            return jsonify({'success': False, 'message': 'Produk tidak ditemukan di keranjang'}), 400

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500



@app.route('/trolley')
def trolley():
    cart = session.get('cart', [])
    return render_template('trolley.html', cart=cart)

@app.route('/filter/', methods=['GET'])
def filter():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    product = []
    if request.args.get('typeCoffee'):
        query = request.args.get('typeCoffee')
        cursor.execute("SELECT id, nama, harga, stok, foto, typeCoffee FROM product WHERE typeCoffee = %s ORDER BY nama ASC", (query,))
        product = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('index.html', products=product)

@app.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    return render_template('checkout.html', cart=cart)

@app.route("/contact", methods=["POST"])
def contact():
    if request.method == "POST":
        nama = request.form["nama"]
        email = request.form["email"]
        no_hp = request.form["no_hp"]
        pesan = request.form["pesan"]

        # Connect to MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert data into the database
        sql = "INSERT INTO contact (nama, email, no_hp, pesan) VALUES (%s, %s, %s, %s)"
        values = (nama, email, no_hp, pesan)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

    return render_template("index.html")

# Berkaitan dengan Admin dan Dashboardnya !!!
admin_credentials = {
    'username': 'admin',
    'password': 'kopi123'
}

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Validasi username dan password dari admin_credentials
        if username == admin_credentials['username'] and password == admin_credentials['password']:
            # Login berhasil
            session["username"] = username
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Username atau password salah."
            return render_template("admin.html", error=error)

    return render_template("admin.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM contact")
    contacts = cursor.fetchall()

    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()

    cursor.execute("SELECT * FROM account")
    accounts = cursor.fetchall()


    cursor.close()
    connection.close()

    return render_template("admin_dashboard.html", contacts=contacts, products=products, accounts=accounts)


# Berkaitan dengan Akun !!!
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Ambil hash password dan salt dari database
        sql = "SELECT password_hash, salt FROM account WHERE username = %s"
        cursor.execute(sql, (username,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            password_hash, salt = user
            salted_password = password + salt  # Gabungkan password input dengan salt
            if check_password_hash(password_hash, salted_password):  # Verifikasi password
                session["username"] = username
                return redirect(url_for("admin_dashboard"))
            else:
                error = "Password salah."
        else:
            error = "Username tidak ditemukan."
        
        return render_template("login.html", error=error)

    return render_template("login.html")

@app.route("/logged/", methods=["POST"] )
def logged():
    # Get log in info from log in form
    user = request.form["username"].lower()
    pwd = request.form["password"]
    #pwd = str(sha1(request.form["password"].encode('utf-8')).hexdigest())
    # Make sure form input is not blank and re-render log in page if blank
    if user == "" or pwd == "":
        return render_template ( "login.html" )
    # Find out if info in form matches a record in user database
    query = "SELECT * FROM account WHERE username = :user AND password_hash = :pwd"
    rows = mysql.connection.cursor ( query, user=user, pwd=pwd )

    # If username and password match a record in database, set session variables
    if len(rows) == 1:
        session['user'] = user
        session['time'] = datetime.now( )
        session['uid'] = rows[0]["id"]
    # Redirect to Home Page
    if 'user' in session:
        return redirect ( "/" )
    # If username is not in the database return the log in page
    return render_template ( "login.html", msg="Wrong username or password." )



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Generate a unique salt
        salt = os.urandom(16).hex()  # Generates a 32-character hexadecimal string
        salted_password = password + salt  # Combine password and salt

        # Hash the salted password
        password_hash = generate_password_hash(salted_password)

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        try:
            sql = """
                INSERT INTO account (fname, lname, username, email, password_hash, salt)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (fname, lname, username, email, password_hash, salt)
            cursor.execute(sql, values)
            connection.commit()
            success_message = "Pendaftaran berhasil! Silakan login."
            return render_template("login.html", success_message=success_message)
        except mysql.connector.Error as err:
            error_message = f"Terjadi kesalahan: {err}"
            return render_template("register.html", error_message=error_message)
        finally:
            cursor.close()
            connection.close()
    return render_template("register.html")

@app.route('/resetpasswd')
def resetpasswd():
    return render_template('respasswd.html')




# Berkaitan dengan CRUD !!!
@app.route("/add_contact", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        nama = request.form["nama"]
        email = request.form["email"]
        no_hp = request.form["no_hp"]
        pesan = request.form["pesan"]

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        sql = "INSERT INTO contact (nama, email, no_hp, pesan) VALUES (%s, %s, %s, %s)"
        values = (nama, email, no_hp, pesan)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    return render_template("add_contact.html")

@app.route("/update_contact/<int:id>", methods=["GET", "POST"])
def update_contact(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    if request.method == "POST":
        nama = request.form["nama"]
        email = request.form["email"]
        no_hp = request.form["no_hp"]
        pesan = request.form["pesan"]

        sql = "UPDATE contact SET nama = %s, email = %s, no_hp = %s, pesan = %s WHERE id = %s"
        values = (nama, email, no_hp, pesan, id)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    cursor.execute("SELECT * FROM contact WHERE id = %s", (id,))
    contact = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("update_contact.html", contact=contact)

@app.route("/delete/<int:id>")
def delete_contact(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM contact WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("admin_dashboard"))

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        nama = request.form["nama"]
        harga = request.form["harga"]
        stok = request.form["stok"]
        foto = request.form["foto"]
        typeCoffee = request.form["typecoffee"]

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        sql = "INSERT INTO product (nama, harga, stok, foto, typeCoffee) VALUES (%s, %s, %s, %s, %s)"
        values = (nama, harga, stok, foto, typeCoffee)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    return render_template("add_product.html")

@app.route("/update_product/<int:id>", methods=["GET", "POST"])
def update_product(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    if request.method == "POST":
        nama = request.form["nama"]
        harga = request.form["harga"]
        stok = request.form["stok"]
        foto = request.form["foto"]
        typeCoffee = request.form["typeCoffee"]

        sql = "UPDATE product SET nama = %s, harga = %s, stok = %s, foto = %s, typeCoffee = %s WHERE id = %s"
        values = (nama, harga, stok, foto, typeCoffee, id)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    cursor.execute("SELECT * FROM product WHERE id = %s", (id,))
    product = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("update_product.html", product=product)

@app.route("/delete_product/<int:id>")
def delete_product(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM product WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("admin_dashboard"))

@app.route("/add_account", methods=["GET", "POST"])
def add_account():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        sql = "INSERT INTO account (fname, lname, username, email, password_hash) VALUES (%s, %s, %s, %s, %s)"
        values = (fname, lname, username, email, password_hash)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    return render_template("add_account.html")

@app.route("/delete_account/<int:id>")
def delete_account(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM account WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("admin_dashboard"))

@app.route('/Rafli Profile')
def rafli():
    return render_template('rafli.html')

@app.route('/Nagita Profile')
def nagita():
    return render_template('nagita.html')

@app.route('/Azzam Profile')
def azzam():
    return render_template('azzam.html')

@app.route('/Faqih Profile')
def faqih():
    return render_template('faqih.html')

@app.route('/menu')
def menu():
    coffee_types = [
        {'name': 'All', 'url': '/'},
        {'name': 'Kopi Gahar', 'url': '/filter/?typeCoffee=Strong'},
        {'name': 'Kopi Selingan', 'url': '/filter/?typeCoffee=Medium'},
        {'name': 'Kopi Hening', 'url': '/filter/?typeCoffee=Low'}
    ]
    return render_template('menu.html', coffee_types=coffee_types)




if __name__ == "__main__":
    app.run()