from flask import Flask, render_template, Response, jsonify
from camera import *  # Ensure this is your actual camera module

app = Flask(__name__)

headings = ("Name", "Album", "Artist")
df1 = music_rec()  # Assuming this is a function that initializes your DataFrame
df1 = df1.head(15)

@app.route('/')
def index():
    print(df1.to_json(orient='records'))
    return jsonify(df1.to_json(orient='records'))  # Adjusting to return JSON for API

def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')

# Vercel expects the app to be callable
if __name__ == '__main__':
    app.run()
