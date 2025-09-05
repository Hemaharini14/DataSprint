import cv2
import json
import numpy as np
from PIL import Image
from fer import FER

# ==============================
# Config
# ==============================
FRAME_SIZE = (128, 128)  # size of overlay

# ==============================
# Load single image
# ==============================
def load_model_image(path, size=FRAME_SIZE):
    img = Image.open(path).convert("RGBA")
    img = img.resize(size)
    return np.array(img)

# ==============================
# Overlay RGBA image on frame
# ==============================
def overlay_image(bg, overlay, x, y):
    h, w, _ = overlay.shape
    y1, y2 = max(0, y-h), min(bg.shape[0], y)
    x1, x2 = max(0, x-w//2), min(bg.shape[1], x+w//2)

    overlay_crop = overlay[-(y-y1):, -(x+w//2-x2):, :]
    oh, ow, _ = overlay_crop.shape
    roi = bg[y1:y1+oh, x1:x1+ow]

    if overlay_crop.shape[2] == 4:  # RGBA
        alpha = overlay_crop[:, :, 3:] / 255.0
        roi[:] = (1 - alpha) * roi + alpha * overlay_crop[:, :, :3]
    else:
        roi[:] = overlay_crop
    return bg

# ==============================
# Main
# ==============================
def main():
    # Initial model selection: "spider" or "rat"
    selected_model = "spider"
    model_paths = {
        "spider": "D:/ETherapy/etver4/spider_frames/spider.png",
        "rat": "D:/ETherapy/etver4/rat_frames/rat.png"
    }

    model_img = load_model_image(model_paths[selected_model])

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = FER(mtcnn=True)

    x_pos, y_pos = 100, 100
    dx, dy = 2, 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = frame.copy()  # prevent artifacts

        # Detect face and emotion
        results = detector.detect_emotions(frame)
        if results:
            (x, y, w, h) = results[0]["box"]
            emotions = results[0]["emotions"]
            dominant = max(emotions, key=emotions.get)

            # Save emotion JSON
            with open("D:/ETherapy/etver4/lib/pages/emotion.json", "w") as f:
                json.dump({"emotion": dominant, "confidence": emotions[dominant]}, f)

            # Draw box + label
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, dominant, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Make model follow head
            x_pos = x + w // 2
            y_pos = y - 30

        # Slight movement
        x_pos += dx
        y_pos += dy
        if x_pos < 0 or x_pos > frame.shape[1] - FRAME_SIZE[0]: dx *= -1
        if y_pos < 0 or y_pos > frame.shape[0] - FRAME_SIZE[1]: dy *= -1

        # Overlay model
        frame = overlay_image(frame, model_img, x_pos, y_pos)

        # Show
        cv2.imshow("Emotion + Model Overlay", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            selected_model = "spider"
            model_img = load_model_image(model_paths[selected_model])
        elif key == ord("r"):
            selected_model = "rat"
            model_img = load_model_image(model_paths[selected_model])

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
