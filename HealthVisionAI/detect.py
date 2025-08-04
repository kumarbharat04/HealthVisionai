import cv2
from fer import FER

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize FER detector (with MTCNN for better accuracy)
detector = FER(mtcnn=True)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Detect emotions in the frame
    results = detector.detect_emotions(frame)

    for result in results:
        (x, y, w, h) = result["box"]
        emotions = result["emotions"]
        top_emotion = max(emotions, key=emotions.get)
        score = emotions[top_emotion]

        # Draw rectangle and emotion label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
        cv2.putText(frame, f"{top_emotion} ({score:.2f})", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Display the frame with results
    cv2.imshow("Emotion Detector - Press 'q' to Quit", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
