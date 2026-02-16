import cv2
import pandas as pd
import easyocr
import os

# 1. SETUP
data = ["0.05"]
for it in data:
    fin_path = []
    fin_path.append(f"1200 {it}")

for item in fin_path:
    TRACKER_CSV = f"/mnt/main_storage/Physics_Work_Backup/csv_dist/{item}.csv"  
    VIDEO_FILE = f"/mnt/main_storage/Physics_Work_Backup/proc_vids/{item}_processed.mp4"
    print(VIDEO_FILE)
    print(TRACKER_CSV)
    
    SCREEN_ROI = [5, 101, 1221, 1471]

    # Initialize OCR
    reader = easyocr.Reader(["en"])

    # Load the Tracker data
    df = pd.read_csv(TRACKER_CSV, skiprows=1)

    cap = cv2.VideoCapture(VIDEO_FILE)
    results = []

    df.iloc[:, 2] = pd.to_numeric(df.iloc[:, 2], errors="coerce")
    df = df.dropna(subset=[df.columns[2]])

    print(f"Starting OCR on {len(df)} frames using column index 2...")
    for index, row in df.iterrows():
        frame_no = int(row.iloc[2])

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = cap.read()

        if not ret:
            print(f"Could not read frame {frame_no}")
            continue

        # Crop and OCR
        y1, y2, x1, x2 = SCREEN_ROI
        screen_crop = frame[y1:y2, x1:x2]

        ocr_result = reader.readtext(screen_crop, detail=0, allowlist="0123456789.G")

        mag_val = ocr_result[0] if ocr_result else "NaN"

        results.append(mag_val)

        if index % 10 == 0:
            print(f"Progress: {index}/{len(df)} frames processed. Current B: {mag_val}")

    df["Magnetic_Field_Raw"] = results

    df.to_csv(
        f"/mnt/main_storage/Physics_Work_Backup/csv_force/{item}_synced_physics_data.csv",
        index=False,
    )
    print(f"Done! Check {item}_synced_physics_data.csv")

cap.release()
