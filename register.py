import cv2
import os
from database import init_db, add_user
import config

def register_face():
    # Ensure DB is initialized
    init_db()

    name = input("Masukkan nama untuk pendaftaran: ").strip()
    if not name:
        print("Nama tidak boleh kosong!")
        return

    # Add user to database
    if add_user(name):
        print(f"Pendaftaran user {name} ke database berhasil.")
    else:
        print(f"Pendaftaran user {name} ke database gagal atau user sudah ada.")

    cap = cv2.VideoCapture(0)
    print(f"Menyiapkan kamera untuk {name}...")
    print("Tekan 's' untuk mengambil foto, 'q' untuk batal.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal mengakses kamera.")
            break

        cv2.imshow("Pendaftaran Wajah - Tekan 's' untuk Simpan", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            img_path = os.path.join(config.DATASET_DIR, f"{name}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"Berhasil menyimpan wajah untuk {name} di {img_path}")
            break
        elif key == ord('q'):
            print("Pendaftaran dibatalkan.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    register_face()
