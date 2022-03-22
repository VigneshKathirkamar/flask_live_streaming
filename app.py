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
            text = "Place your face within the box"
            frame_shape = img.shape
            #origin order is (x,y)
            org = (int(0.05*frame_shape[1]),int(0.05*frame_shape[0]))
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (0,0,255)
            thickness = 1
            img = cv2.rectangle(img, (int(0.25*frame_shape[1]), int(0.10*frame_shape[0])), (int(0.75*frame_shape[1]), int(0.90*frame_shape[0])), (255,0,0), 2)
            img = cv2.putText(img,text,org,font,fontScale,color,thickness,cv2.LINE_AA)
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
