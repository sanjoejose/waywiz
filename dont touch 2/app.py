from flask import Flask, request, render_template, jsonify, redirect, url_for,session
import mysql.connector
import heapq

app = Flask(__name__)

# Define the graph
# g1 = {
#     100: [ ( 1136, 'right', 122), (250, 'straight',123), (200, 'up',200)],
#     101: [(1175, 'straight', 102)],
#     102: [(1032, 'right', 103), (1032, 'left', 104), (775, 'straight', 105), (1175, 'straight',101)],
#     103: [(1032, 'straight', 102), (200, 'up', 203)],
#     104: [(1032, 'straight', 102), (200, 'up',204)],
#     105: [(250, 'left', 120), (250,'right', 106),(775,'straight',102)],
#     106: [(880, 'straight', 107), (250, 'left', 105)],
#     107: [(523, 'straight', 108), (880, 'straight', 106)],
#     108: [(523, 'straight', 107), (1136, 'straight', 109), (1050, 'straight', 110)],
#     109: [(1136, 'right', 108), (250, 'straight', 110)],
#     110: [(250, 'straight', 109), (1050, 'left', 108), (200, 'up',210)],
#     120: [ (250, 'right', 105), (880, 'straight', 121)],
#     121: [ ( 880, 'straight', 120), (350, 'straight', 122)],
#     122: [ ( 350, 'straight', 121), (1136, 'straight', 123), (1136, 'straight', 100)],
#     123: [ ( 1136, 'left', 122), (250, 'straight',100)]
# }

g1 = {
    100: [(1325, 'straight', 103)],
    101: [(175, 'right', 105),(120, 'right', 148),(875, 'straight', 107)],
    102: [(525, 'right', 103),(525, 'left', 105),(50, 'up', 202)],
    103: [(1325, 'straight', 100),(525, 'left', 102),(525, 'straight', 104),(462, 'straight', 105)],
    104: [(525, 'straight', 103),(525, 'right', 105),(50, 'up', 204)],
    105: [(175, 'left', 101),(525, 'right', 102),(462, 'straight', 103),(525, 'left', 104),(325, 'right', 151),(325, 'right', 107),(700, 'left', 106)],
    106: [(700, 'right', 105),(850, 'left', 149),(875, 'straight', 151),(295, 'left', 148),(1225, 'straight', 107),(875, 'straight', 130)],
    107: [(875, 'straight', 101),(325, 'left', 105),(1225, 'straight', 106),(350, 'right', 129),(700, 'straight', 108),(612, 'left', 126)],
    108: [(700, 'straight', 107),(100, 'left', 152),(1397, 'straight', 109),(175, 'right', 126)],
    109: [(175, 'right', 185),(1397, 'straight', 108),(525, 'right', 110),(1400, 'straight', 111),(873, 'right', 152),(700, 'left', 113)],
    110: [(525, 'left', 109),(875, 'right', 111),(50, 'up', 210)],
    111: [(1400, 'left', 109),(875, 'left', 110),(175, 'right', 105),(700, 'right', 113)],
    113: [(700, 'right', 109),(700, 'left', 111)],
    126: [(612, 'right', 107),(175, 'left', 108)],
    129: [(350, 'left', 107),(120, 'right', 151)],
    130: [(875, 'straight', 106),(100, 'right', 150),(643, 'straight', 131),(120, 'left', 149)],
    131: [(643, 'left', 130),(785, 'right', 150),(525, 'left', 132),(700, 'right', 135),(1400, 'straight', 133)],
    132: [(525, 'right', 131),(787, 'left', 133),(50, 'up',232)],
    133: [(1400, 'straight', 131),(787, 'right', 132),(350, 'straight', 135)],
    135: [(700, 'left', 131),(350, 'straight', 133)],
    148: [(120, 'left', 101),(295, 'right', 106)],
    149: [(850, 'right', 106),(120, 'right', 130)],
    150: [(100, 'left', 130),(785, 'left', 131)],
    151: [(325, 'left', 105),(875, 'straight', 106),(120, 'left', 129)],
    152: [(100, 'right', 108),(873, 'left', 109)]
}

g2 = {
    200: [ (350, 'right', 236), (875, 'straight',235), (200, 'down',100)],
    202: [(50, 'up', 302)],
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

g3 = {
    300: [(162,'straight',301),(437,'right',303),(50,'straight',302)],
    301: [(162,'straight',300),(437,'left',319)],
    302: [(50,'straight',300)],
    303: [(437,'left',300),(437,'right',306)],
    304: [(50,'straight',306)],
    305: [(437,'right',307),(162,'straight',306)],
    306: [(437,'left',303),(50,'straight',304),(162,'straight',305)],
    307: [(437,'left',305),(730,'straight',309),(550,'left',318)],
    309: [(730,'straight',307),(20,'left',317),(262,'straight',311),(50,'right',318)],
    310: [(525,'right',313),(350,'left',312)],
    311: [(262,'straight',309),(225,'left',316),(700,'straight',312),(262,'right',317)],
    312: [(350,'right',310),(700,'straight',311),(1050,'straight',313),(350,'right',316)],
    313: [(525,'left',310),(1050,'straight',312),(30,'left',331),(262,'straight',314)],
    314: [(575,'left',315),(262,'right',331),(262,'straight',313)],
    315: [(575,'right',314)],
    316: [(225,'right',311),(350,'left',312)],
    317: [(20,'right',309),(262,'left',311)],
    318: [(550,'right',307),(50,'left',309)],
    319: [(437,'left',301),(612,'right',330),(962,'straight',321)],
    321: [(962,'straight',319),(502,'right',329),(522,'straight',322),(150,'left',330)],
    322: [(522,'straight',321),(30,'left',329),(437,'straight',323),(50,'right',328)],
    323: [(437,'straight',322),(962,'straight',324),(350,'left',332)],
    324: [(962,'straight',323),(525,'right',332),(30,'right',327),(262,'straight',325)],
    325: [(262,'straight',324),(252,'left',327)],
    327: [(30,'left',324),(252,'right',325)],
    328: [(50,'left',322)],
    329: [(502,'left',321),(30,'right',322)],
    330: [(612,'left',319),(150,'right',321)],
    331: [(262,'left',314),(30,'right',313)],
    332: [(350,'right',323),(525,'left',324)]
}

unified_graph = {**g1, **g2, **g3}
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

# Route to Get Staff Names and Locations
@app.route('/get-staff-locations', methods=['GET'])
def get_staff_locations():
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Query to get names and locations of staff
        cursor.execute("SELECT name, location FROM staff")
        staff = cursor.fetchall()
        conn.close()
        
        # Return the data as JSON
        return jsonify({'staff': staff})
    except Exception as e:
        return jsonify({'error': f'Error fetching staff locations: {str(e)}'})


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