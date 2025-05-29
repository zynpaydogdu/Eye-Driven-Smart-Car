# Eye-Driven-Smart-Car 🚗👁️

Control a smart vehicle **using only your eye movements!**  
This project tracks your eye direction in real time and sends commands wirelessly to a Raspberry Pi to drive motors — no hands needed.

---

## What is it?

Eye-Driven-Smart-Car detects where you're looking (`right`, `left`, `forward`, `stop`) using a CNN model trained on eye images.  
It sends these commands over Wi-Fi to a Raspberry Pi, which drives motors accordingly and provides Turkish voice feedback.

---

## Key Features

- Real-time eye gaze classification with TensorFlow & OpenCV  
- TCP socket communication between PC (vision + model) and Raspberry Pi (motor control)  
- Motor control via Raspberry Pi GPIO pins  
- Turkish voice feedback with gTTS  
- Simple, modular Python scripts for training, tracking, and motor control  

---

## Quick Start

1. **Train your model** on your eye dataset:

    ```bash
    python train_model.py
    ```

2. **Run live eye tracking and send commands:**

    ```bash
    python live_tracking.py
    ```

3. **Start motor control server on Raspberry Pi:**

    ```bash
    python motor_server.py
    ```

---

## Dataset Structure

Prepare your images in `Data/` folder with four subfolders named:  
`right/`, `left/`, `forward/`, `stop/` — each containing relevant eye images.

---

## Notes

- Ensure PC and Raspberry Pi are on the same network.  
- Adjust Raspberry Pi IP/hostname in scripts as needed.  
- Install dependencies: `tensorflow`, `keras`, `opencv-python`, `gtts`, and `ffmpeg` (for audio).  
- Hardware GPIO pins must match your motor wiring.

---

## License & Contact

MIT License | Developed by Ayşe Z.  
Contact: aysez@example.com

---

Drive your car with your eyes — welcome to the future of hands-free control! 🚀
