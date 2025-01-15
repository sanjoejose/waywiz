from flask import Flask, request, render_template, jsonify, redirect, url_for
import mysql.connector

# Initialize Flask app
app = Flask(__name__)

# MySQL Database Connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='4321@Wiz',
        database='campus_navigation'
    )
    return conn

# Route for Home Page
@app.route('/')
def home():
    return render_template('index.html')  # Home page with Login and Availability Status options

# Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        college_id = request.form['college_id']
        password = request.form['password']

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM staff WHERE college_id = %s", (college_id,))
        user = cursor.fetchone()
        conn.close()

        # Check if user exists and if passwords match
        if user and user['password_hash'] == password:
            # Render the success page with user details
            return render_template('login_success.html', user=user)
        else:
            return "Invalid credentials or user not found."

    return render_template('login.html')  # Show the login form

# Route for Availability Status Page
@app.route('/availability_status')
def availability_status():
    # Fetch staff names and their availability
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, availability FROM staff")
    staff_data = cursor.fetchall()
    conn.close()

    # Pass staff data to the template
    return render_template('availability_status.html', staff_data=staff_data)

# Route for Updating Availability
@app.route('/update_availability', methods=['POST'])
def update_availability():
    data = request.get_json()
    college_id = data.get('college_id')
    availability = data.get('availability')

    # Update availability in the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE staff SET availability = %s WHERE college_id = %s",
        (availability, college_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Availability updated successfully!"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

