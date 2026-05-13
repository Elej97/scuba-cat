"""
Interactive Screen Overlay - El Hareketleriyle GIF Kontrolü
===========================================================
Gereksinimler:
    pip install opencv-python mediapipe Pillow numpy

Mantık:
    - Tek el görünürse → sadece kamera penceresi açık, GIF pencereleri yok
    - İki el görününce  → GIF pencereleri açılır ve oynamaya başlar
    - Eller ekrandan çekilince → GIF pencereleri kapanır

Çıkış: 'q' tuşu
"""

import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageSequence
import os
import sys
import time


GIF_PATH_1 = r"C:\Users\elifc\Desktop\AR\Nick Wilde Momo GIF.gif"
GIF_PATH_2 = r"C:\Users\elifc\Desktop\AR\Dance Cat GIF.gif"

GIF_WINDOW_W = 400
GIF_WINDOW_H = 300
CAM_WINDOW_W = 720
CAM_WINDOW_H = 540

# Pencere konumları
CAM_WIN_X,  CAM_WIN_Y  = 30,  30
GIF1_WIN_X, GIF1_WIN_Y = 780, 30
GIF2_WIN_X, GIF2_WIN_Y = 780, 370

FRAME_DELAY = 0.05   # GIF kare gecikmesi (saniye) → ~20 fps



def load_gif_frames(path: str, target_size: tuple) -> list:
    if not os.path.isfile(path):
        print(f"[UYARI] GIF bulunamadı: {path}")
        ph = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)
        cv2.putText(ph, "GIF bulunamadi", (20, target_size[1] // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (60, 60, 200), 2)
        return [ph]
    try:
        gif    = Image.open(path)
        frames = []
        for frame in ImageSequence.Iterator(gif):
            img = frame.convert("RGB").resize(target_size, Image.LANCZOS)
            arr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            frames.append(arr)
        print(f"[OK] {len(frames)} kare yuklendi: {os.path.basename(path)}")
        return frames
    except Exception as e:
        print(f"[HATA] GIF yuklenemedi ({path}): {e}")
        ph = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)
        cv2.putText(ph, "GIF yuklenemedi", (20, target_size[1] // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (60, 60, 200), 2)
        return [ph]



def draw_hands(frame: np.ndarray, results) -> None:
    mp_drawing = mp.solutions.drawing_utils
    mp_hands   = mp.solutions.hands
    if results.multi_hand_landmarks:
        for hand_lm in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_lm,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 180), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)
            )



def main():
    print("=" * 52)
    print("  Interactive Screen Overlay")
    print("  Iki el -> GIF pencereleri acilir")
    print("  Tek el -> Sadece kamera gorunur")
    print("  Cikis  -> 'q'")
    print("=" * 52)

    gif_size = (GIF_WINDOW_W, GIF_WINDOW_H)
    frames1  = load_gif_frames(GIF_PATH_1, gif_size)
    frames2  = load_gif_frames(GIF_PATH_2, gif_size)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[HATA] Kamera acilamadi!")
        sys.exit(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  CAM_WINDOW_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_WINDOW_H)

    mp_hands = mp.solutions.hands
    hands    = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6
    )

    # Sadece kamera penceresi baslangicta acik
    cv2.namedWindow("Kamera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Kamera", CAM_WINDOW_W, CAM_WINDOW_H)
    cv2.moveWindow("Kamera", CAM_WIN_X, CAM_WIN_Y)

    idx1, idx2       = 0, 0
    last_frame_time  = time.time()
    gif_windows_open = False

    print("[HAZIR] Kameranin onune gelin, sonra 2. elinizi getirin!\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame   = cv2.flip(frame, 1)
        rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        hand_count = len(results.multi_hand_landmarks) if results.multi_hand_landmarks else 0
        two_hands  = hand_count >= 2

        draw_hands(frame, results)
        cv2.imshow("Kamera", frame)

        now = time.time()

        if two_hands:
            # GIF pencereleri henuz yoksa olustur
            if not gif_windows_open:
                cv2.namedWindow("Nick Wilde Momo", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Nick Wilde Momo", GIF_WINDOW_W, GIF_WINDOW_H)
                cv2.moveWindow("Nick Wilde Momo", GIF1_WIN_X, GIF1_WIN_Y)

                cv2.namedWindow("Dance Cat", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Dance Cat", GIF_WINDOW_W, GIF_WINDOW_H)
                cv2.moveWindow("Dance Cat", GIF2_WIN_X, GIF2_WIN_Y)

                gif_windows_open = True
                print("[+] Iki el algilandi - GIF pencereleri acildi")

            # Kareyi ilerlet
            if now - last_frame_time >= FRAME_DELAY:
                last_frame_time = now
                idx1 = (idx1 + 1) % len(frames1)
                idx2 = (idx2 + 1) % len(frames2)

            cv2.imshow("Nick Wilde Momo", frames1[idx1])
            cv2.imshow("Dance Cat",       frames2[idx2])

        else:
            # Iki el yoksa GIF pencerelerini kapat
            if gif_windows_open:
                cv2.destroyWindow("Nick Wilde Momo")
                cv2.destroyWindow("Dance Cat")
                gif_windows_open = False
                idx1, idx2 = 0, 0
                print("[-] Eller cekildi - GIF pencereleri kapandi")

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("[CIKIS] Kapatiliyor...")
            break

    hands.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
