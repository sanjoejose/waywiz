from flask import Flask, request, render_template, jsonify, redirect, url_for,session
import mysql.connector
import heapq

app = Flask(__name__)

# Define the graph
g1 = {
    100: [ ( 1136, 'right', 122), (250, 'straight',123), (200, 'up',200)],
    101: [(1175, 'straight', 102)],
    102: [(1032, 'right', 103), (1032, 'left', 104), (775, 'straight', 105), (1175, 'straight',101)],
    103: [(1032, 'straight', 102), (200, 'up', 203)],
    104: [(1032, 'straight', 102), (200, 'up',204)],
    105: [(250, 'left', 120), (250,'right', 106),(775,'straight',102)],
    106: [(880, 'straight', 107), (250, 'left', 105)],
    107: [(523, 'straight', 108), (880, 'straight', 106)],
    108: [(523, 'straight', 107), (1136, 'straight', 109), (1050, 'straight', 110)],
    109: [(1136, 'right', 108), (250, 'straight', 110)],
    110: [(250, 'straight', 109), (1050, 'left', 108), (200, 'up',210)],
    120: [ (250, 'right', 105), (880, 'straight', 121)],
    121: [ ( 880, 'straight', 120), (350, 'straight', 122)],
    122: [ ( 350, 'straight', 121), (1136, 'straight', 123), (1136, 'straight', 100)],
    123: [ ( 1136, 'left', 122), (250, 'straight',100)]
}

g2 = {
    200: [ (350, 'right', 236), (875, 'straight',235), (200, 'down',100)],
    236: [ (700,'straight',237),(350,'straight',200)],
    237: [ (700,'straight',236)],
    235: [ (875,'straight',200),(523,'straight',234)],
    234: [ (523,'straight',235),(150,'straight',233)],
    233: [ (150,'straight',234),(1400,'straight',232)],
    232: [ (625,'straight',204),(1400,'straight',233),(1050,'straight',226)],
    204: [ (625,'straight',232),(200, 'down',104)],
    226: [(625,'straight',203),(1050,'straight',232),(1050,'straight',227)],
    203: [ (625,'straight',226), (200, 'down',103)],
    227: [ (150,'straight',228),(1050,'straight',226)],
    228: [(150,'straight',227),(529,'straight',229)],
    229: [(875,'straight',210),(529,'straight',228)],
    210: [(875,'straight',229),(1050,'straight',230),(200,'down',110)],
    230: [(1050,'straight',210)]
}

unified_graph = {**g1, **g2}
# Shortest path function
def shortest_path(graph, start, end):
    queue = [(0, start, [], [])]
    visited = set()
    
    while queue:
        (cost, node, path, directions) = heapq.heappop(queue)
        
        if node in visited:
            continue
        visited.add(node)
        
        path = path + [node]
        
        if node == end:
            return cost, path, directions
        
        for distance, direction, next_node in graph.get(node, []):
            if next_node not in visited:
                heapq.heappush(queue, (cost + distance, next_node, path, directions + [direction]))
    
    return float("inf"), [], []
print(shortest_path(unified_graph,107,235))

# API endpoint
@app.route('/shortest-path', methods=['POST']) 
def get_shortest_path():
    data = request.json
    start = int(data.get('start'))
    end = int(data.get('end'))
    total_distance, path_taken, directions_taken = shortest_path(unified_graph, start, end)
    
    return jsonify({
        'distance': total_distance,
        'path': path_taken,
        'directions': directions_taken
    })
# MySQL Database Connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='waywiz@123456',
        database='campus_navigation'
    )
    return conn

# Route for Home Page
@app.route('/')
def home():
    return render_template('land.html')  # Your main HTML page  # Home page with Login and Availability Status options

# Route for Login Page
@app.route('/staff-login', methods=['GET', 'POST'])
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
@app.route('/availability_status', methods=['GET', 'POST'])
def availability_status():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Get selected staff name from the form
        selected_name = request.form['staff_name']
        cursor.execute("SELECT name, room, location, availability FROM staff WHERE name = %s", (selected_name,))
        selected_staff = cursor.fetchone()
    else:
        selected_staff = None

    # Fetch all staff names and availability for the dropdown
    cursor.execute("SELECT name, availability FROM staff")
    staff_data = cursor.fetchall()

    conn.close()

    # Pass data to the template
    return render_template(
        'availability_status.html',
        staff_data=staff_data,
        selected_staff=selected_staff
    )


@app.route('/update_availability', methods=['POST'])
def update_availability():
    data = request.get_json()
    college_id = data.get('college_id')
    availability = data.get('availability')

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # First, update the availability in the database
    cursor.execute(
        "UPDATE staff SET availability = %s WHERE college_id = %s",
        (availability, college_id)
    )

    # If availability is set to 0, update the location with the room value
    if availability == 0:
        cursor.execute(
            "UPDATE staff SET location = room WHERE college_id = %s",
            (college_id,)
        )

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Availability updated successfully!"})


# Route for Updating Location
@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.get_json()
    college_id = data.get('college_id')
    location = data.get('location')

    # Update location in the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE staff SET location = %s WHERE college_id = %s",
        (location, college_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Location updated successfully!"})



@app.route('/select')
def select():
    return render_template('sam.html')

@app.route('/staff-login')
def staff_login():
    return render_template('login.html')

@app.route('/path-finder')
def path_finder():
    return render_template('path.html')


if __name__ == '__main__':
    app.run(debug=True)
