import cv2
import os

def register_face():
    # Create dataset directory if not exists
    if not os.path.exists("dataset"):
        os.makedirs("dataset")

    name = input("Masukkan nama untuk pendaftaran: ").strip()
    if not name:
        print("Nama tidak boleh kosong!")
        return

    # Create folder for the user if using DeepFace standard structure (optional, but good for organization)
    # However, DeepFace.find can work with flat files too. 
    # Let's keep it simple: dataset/name.jpg
    
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
            img_path = os.path.join("dataset", f"{name}.jpg")
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
