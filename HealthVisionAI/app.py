from flask import Flask, render_template, request, jsonify, Response
from chatbot import get_bot_response
import cv2
from fer import FER
from PIL import ImageFont, ImageDraw, Image
import numpy as np

app = Flask(__name__)
detector = FER(mtcnn=True)

# Emoji mapping
emoji_map = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "surprise": "😲",
    "neutral": "😐",
    "disgust": "🤢",
    "fear": "😨"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': 'Please type something.'})
    return jsonify({'response': get_bot_response(user_message)})

@app.route('/emotion')
def emotion():
    return render_template('emotion.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    camera = cv2.VideoCapture(0)
    font_path = "C:/Windows/Fonts/seguiemj.ttf"  # Font with emoji support

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Convert to RGB for PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)
        draw = ImageDraw.Draw(pil_img)
        font = ImageFont.truetype(font_path, 30)

        results = detector.detect_emotions(frame)
        for result in results:
            (x, y, w, h) = result["box"]
            emotions = result["emotions"]
            top_emotion = max(emotions, key=emotions.get)
            score = emotions[top_emotion]
            emoji = emoji_map.get(top_emotion, "❓")

            label = f"{emoji} {top_emotion} ({score:.2f})"
            draw.rectangle([x, y, x + w, y + h], outline=(255, 0, 255), width=3)
            draw.text((x, y - 30), label, font=font, fill=(255, 255, 255))

        # Convert back to OpenCV
        frame_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        ret, buffer = cv2.imencode('.jpg', frame_bgr)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    camera.release()

if __name__ == '__main__':
    app.run(debug=True)
