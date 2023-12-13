from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def option():
    return render_template('option.html')

currentDateTime = datetime.now()
connect = sqlite3.connect('database.db')
connect.execute(
    'CREATE TABLE IF NOT EXISTS customers (name TEXT, \
email TEXT, city TEXT, BookingDate TIMESTAMP, phone TEXT)')
@app.route('/capture', methods=['GET', 'POST'])
def capture():
    if request.method == 'POST':
        # Extract form data
        customer_name = request.form['name']
        email = request.form['email']
        city = request.form['city']
        currentDateTime = request.form['currentDateTime']
        telephone = request.form['phone']

        # Connect to the database
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()

            # Execute the SQL query
            cursor.execute("""
                INSERT INTO customers (name, email, city, BookingDate, phone) 
                VALUES (?, ?, ?, ?, ?)
            """, (customer_name, email, city, currentDateTime, telephone))

            # Commit the transaction
            users.commit()

        # Render the 'option' template upon successful POST request
        return render_template("option.html")
    else:
        # Render the 'capture' template for GET request
        return render_template('capture.html')


@app.route('/customers')
def customers():
    # Connect to the database
    connect = sqlite3.connect('database.db')

    cursor = connect.cursor()

    # Execute the SQL statement
    cursor.execute('SELECT * FROM customers')

    # Fetch all the data
    data = cursor.fetchall()

    # Render the 'customers' template with the data
    return render_template("customers.html", data=data)

if __name__ == '__main__':
    # Create the table if it doesn't exist
    with sqlite3.connect('database.db') as connect:
        app.run(debug=True)
