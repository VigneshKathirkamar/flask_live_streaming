from distutils.log import debug
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)


def generate_frame():
    camera = cv2.VideoCapture(0)
    while True:
        ret, img = camera.read()
        if not ret:
            break
        else:
            success, buffer = cv2.imencode('.jpg',img)
            img = buffer.tobytes()
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n'+ img +b'\r\n')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
