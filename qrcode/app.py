from flask import Flask, render_template, Response, jsonify
import cv2
from pyzbar.pyzbar import decode

app = Flask(__name__)

# Initialize the camera
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()  # Read the frame
        if not success:
            break
        else:
            # Encode the frame as a JPEG to display on the webpage
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/scan_qr_code')
def scan_qr_code():
    # QR Code scanning logic
    success, frame = camera.read()
    qr_data = None
    if success:
        # Decode QR code from the frame
        decoded_objects = decode(frame)
        if decoded_objects:
            # Extract the first decoded QR code's data
            qr_data = decoded_objects[0].data.decode('utf-8')

    # Return the result as JSON
    return jsonify({'qr_data': qr_data})

if __name__ == "__main__":
    app.run(debug=True)
