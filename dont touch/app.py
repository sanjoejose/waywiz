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
    101: [(460, 'right', 105),(295, 'right', 148),(875, 'straight', 107)],
    102: [(1020, 'right', 103),(1020, 'left', 105),(50, 'up', 202)],
    103: [(1325, 'straight', 100),(1020, 'left', 102),(1020, 'straight', 104),(462, 'straight', 105)],
    104: [(1020, 'straight', 103),(1020, 'right', 105),(50, 'up', 204)],
    105: [(460, 'left', 101),(1020, 'right', 102),(462, 'straight', 103),(1020, 'left', 104),(450, 'right', 151),(975, 'right', 107),(975, 'left', 106)],
    106: [(975, 'right', 105),(850, 'left', 149),(875, 'straight', 151),(470, 'left', 148),(1400, 'straight', 107),(700, 'straight', 130)],
    107: [(875, 'straight', 101),(975, 'left', 105),(1400, 'straight', 106),(470, 'right', 129),(700, 'straight', 108),(850, 'left', 126)],
    108: [(700, 'straight', 107),(450, 'left', 152),(1050, 'straight', 109),(325, 'right', 126)],
    109: [(1050, 'straight', 108),(525, 'right', 110),(1400, 'straight', 111),(800, 'right', 152),(850, 'left', 113)],
    110: [(525, 'left', 109),(875, 'right', 111),(50, 'up', 210),(400, 'straight', 113)],
    111: [(1400, 'left', 109),(875, 'left', 110),(850, 'right', 113)],
    113: [(850, 'right', 109),(850, 'left', 111),(400, 'straight', 110)],
    126: [(850, 'right', 107),(325, 'left', 108)],
    129: [(470, 'left', 107),(325, 'right', 151)],
    130: [(700, 'straight', 106),(450, 'right', 150),(1050, 'straight', 131),(325, 'left', 149)],
    131: [(1050, 'left', 130),(800,'right', 150),(525, 'left', 132),(850, 'right', 135),(1400, 'straight', 133)],
    132: [(525, 'right', 131),(875, 'left', 133),(50, 'up',232),(400, 'straight', 135)],
    133: [(1400, 'straight', 131),(875, 'right', 132),(850, 'straight', 135)],
    135: [(850, 'left', 131),(850, 'straight', 133),(400, 'straight', 132)],
    148: [(295, 'left', 101),(470, 'right', 106)],
    149: [(850, 'right', 106),(325, 'right', 130)],
    150: [(450, 'left', 130),(800, 'left', 131)],
    151: [(450, 'left', 105),(875, 'straight', 106),(325, 'left', 129)],
    152: [(450, 'right', 108),(800, 'left', 109)]
}

g2 = {
    200: [ (625, 'right', 202), (525, 'right',203)],
    201: [ (625, 'right', 202), (460, 'left', 219)],
    202: [ (625, 'left', 201), (625, 'left', 200)],
    203: [ (525, 'right', 206), (985, 'left then right', 207), (525, 'left', 200), (985, 'left then right', 219)],
    204: [ (625, 'right', 206), (625, 'right', 205)],
    205: [ (460, 'right', 207), (625, 'left', 204)],
    206: [ (525, 'left', 203), (625, 'left', 204)],
    207: [ (350, 'straight', 208), (460, 'left', 205), (985, 'right then left', 203)],
    208: [ (525, 'straight', 209), (550, 'left', 218), (350, 'straight', 207)],
    209: [ (350, 'straight', 211), (210, 'left', 217), (375, 'right', 218), (525, 'straight', 208)],
    210: [ (625, 'left', 212), (625, 'right', 213),(50, 'down', 110),(50, 'up', 310)],
    211: [ (700, 'straight', 212), (550, 'left', 216), (550, 'right', 217), (350, 'straight', 209)],
    212: [ (1050, 'straight', 213), (550, 'right', 216), (625, 'right', 210), (700, 'straight', 211)],
    213: [ (450, 'left', 214), (800, 'straight', 215), (625, 'left', 210), (1050, 'straight', 212)],
    214: [ (550, 'left', 215), (450, 'right', 213)],
    215: [ (800, 'straight', 213), (550, 'right', 214)],
    216: [ (550, 'right', 211), (550, 'left', 212)],
    217: [ (210, 'right', 209), (550, 'left', 211)],
    218: [ (550, 'right', 208), (375, 'left', 209)],
    219: [ (985, 'right then left', 203), (350, 'straight', 220), (460, 'right', 201)],
    220: [ (725, 'right', 230), (525, 'straight', 221), (350, 'straight', 219)],
    221: [ (350, 'straight', 222), (375, 'left', 230), (210, 'right', 229), (525, 'straight', 220)],
    222: [ (700, 'straight', 223), (550, 'right', 228), (350, 'straight', 221)],
    223: [ (550, 'left', 228), (875, 'straight', 224), (625, 'left', 232), (700, 'straight', 222)],
    224: [ (210, 'right', 227), (350, 'straight', 225), (450, 'right', 232), (875, 'straight', 223)],
    225: [ (450, 'straight', 226), (440, 'left', 227), (350, 'straight', 224)],
    226: [ (450, 'straight', 225)],
    227: [ (210, 'left', 224), (440, 'right', 225)],
    228: [ (550, 'left', 222), (550, 'right', 223)],
    229: [ (210, 'left', 221)],
    230: [ (725, 'left', 220), (375, 'right', 221)],
    232: [ (625, 'right', 223), (450, 'left', 224)],
}

g3 = {
    300: [(162,'straight',301),(437,'right',303),(50,'straight',302)],
    301: [(162,'straight',300),(437,'left',319)],
    302: [(50,'straight',300),(50, 'down', 202)],
    303: [(437,'left',300),(437,'right',306)],
    304: [(50,'straight',306),(50, 'down', 204)],
    305: [(437,'right',307),(162,'straight',306)],
    306: [(437,'left',303),(50,'straight',304),(162,'straight',305)],
    307: [(437,'left',305),(730,'straight',309),(550,'left',318)],
    309: [(730,'straight',307),(20,'left',317),(262,'straight',311),(50,'right',318)],
    310: [(525,'right',313),(350,'left',312),(50, 'down', 210)],
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
    332: [(350,'right',323),(525,'left',324),(50, 'down', 232)]
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
    cursor.execute("SELECT name, availability FROM staff WHERE college_id like 'E%' ")
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