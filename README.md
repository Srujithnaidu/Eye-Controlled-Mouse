# Eye Controlled Mouse 🎯

Control your computer mouse with just your **eyes** using **OpenCV**, **Mediapipe**, and **PyAutoGUI**.  
This project enables **hands-free interaction** by tracking eye movements and blinks to perform cursor actions.

---

## 🚀 Features
- 👀 **Cursor Movement** – Move your eyes/head to control the pointer  
- 👆 **Left Click** – Blink once  
- 👉 **Right Click** – Long blink (hold eye closed)  
- 🖱️ **Scrolling** – Move your left eye up/down  
- 🎚️ **Smoothing** – Reduces jitter by averaging recent eye positions  
- ⌨️ **Exit Anytime** – Press `ESC` to quit safely  

---

## 🛠️ Tech Stack
- **Python 3.10**  
- **OpenCV** – Webcam input & drawing  
- **Mediapipe** – Eye & face landmark detection  
- **PyAutoGUI** – Mouse control  
- **Keyboard** – Global key detection  

---

## 📦 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/<your-username>/Eye-Controlled-Mouse.git
   cd Eye-Controlled-Mouse
2. (Optional) Create a virtual environment
   ```bash
   # Windows
     python -m venv venv
     venv\Scripts\activate

   # Linux / Mac
     python3 -m venv venv
     source venv/bin/activate
   
3. Install dependencies
   ```bash
   pip install opencv-python mediapipe pyautogui keyboard

▶️ Usage
Run the project with:
   ```bash
   python eye_mouse.py
```

Controls:
Move your eyes/head → Cursor moves
Blink once → Left click
Long blink → Right click
Move left eye up/down → Scroll
Press ESC → Quit program

📂 Project Structure
  ```bash
  Eye-Controlled-Mouse/
  │── eye_mouse.py        # Main program
  │── requirements.txt    # Dependencies
  │── README.md           # Documentation
  │── .gitignore          # Ignore unnecessary files
  │── LICENSE             # MIT License
```

📌 Notes
Adjust calibration values (x_min, x_max, y_min, y_max) in the code if cursor feels misaligned.
Works best with good lighting and a stable webcam.
Tested on Windows 11 / Python 3.10.

📜 License
This project is licensed under the MIT License – you can freely use and modify it.


