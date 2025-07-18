# Hand Gesture Video Controller 🎥👋

A real-time hand gesture recognition system that allows you to control video playback and computer interactions using just your hand movements. Built with Python, OpenCV, and MediaPipe for seamless gesture detection and control.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **Real-time Hand Detection**: Uses MediaPipe for accurate hand landmark detection
- **Multiple Gesture Recognition**: Supports 10+ different hand gestures
- **Video Control**: Play/pause, fast forward, rewind, timeline navigation
- **Mouse Control**: Cursor movement and clicking
- **Zoom & Scroll**: Zoom in/out and scroll functionality
- **Visual Feedback**: Live gesture status and finger detection indicators
- **Optimized Performance**: Smooth 30+ FPS operation with gesture cooldown

## 🎯 Supported Gestures

| Gesture | Action | Description |
|---------|--------|-------------|
| 🖐️ **Open Palm** | Play Video | All fingers extended |
| ✊ **Closed Palm** | Stop/Pause Video | All fingers closed |
| 👆 **Index Finger** | Move Cursor | Point to move mouse cursor |
| ✌️ **Index + Middle** | Single Click | Two fingers up for clicking |
| 🤟 **Index + Middle + Ring** | Zoom In | Three fingers for zoom in |
| 🖐️ **All Four Fingers** | Zoom Out | Four fingers for zoom out |
| 👈 **Index Left** | Timeline Backward | Point left to rewind |
| 👉 **Index Right** | Timeline Forward | Point right to fast forward |
| 👍 **Thumb Up** | Scroll Up | Thumb pointing up |
| 👎 **Thumb Down** | Scroll Down | Thumb pointing down |
| 🤘 **Ring + Pinky** | Fast Forward | Heavy metal gesture |
| 🤙 **Index + Pinky** | Go Back | Shaka/call gesture |

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- Webcam/Camera
- Windows/macOS/Linux

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/hand-gesture-video-controller.git
cd hand-gesture-video-controller
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Required Dependencies

Create a `requirements.txt` file with:
```
opencv-python>=4.5.0
mediapipe>=0.8.0
pyautogui>=0.9.0
```

## 🎮 Usage

1. **Run the application**
```bash
python app.py
```

2. **Position your hand** in front of the camera (optimal distance: 1-3 feet)

3. **Start gesturing!** The application will display:
   - Live video feed with hand landmarks
   - FPS counter
   - Active gesture status
   - Finger detection indicators
   - Recent gesture history

4. **Controls**:
   - Press `q` to quit
   - Press `r` to reset controller state

## 🏗️ Project Structure

```
hand-gesture-video-controller/
├── app.py              # Main application with GUI and camera handling
├── controller.py       # Gesture recognition and control logic
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── venv/              # Virtual environment (created after setup)
```

## 🔧 Configuration

### Adjusting Detection Sensitivity

In `app.py`, you can modify MediaPipe settings:

```python
hands = mp_hands.Hands(
    min_detection_confidence=0.6,  # Lower = more sensitive
    min_tracking_confidence=0.6,   # Higher = more stable
    model_complexity=1             # 0=lite, 1=full
)
```

### Gesture Cooldown

In `controller.py`, adjust the gesture cooldown period:

```python
GESTURE_COOLDOWN = 0.3  # Seconds between gesture activations
```

### Camera Settings

Modify camera resolution in `app.py`:

```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

## 🧠 How It Works

1. **Hand Detection**: MediaPipe identifies hand landmarks in real-time
2. **Finger Analysis**: Each finger's position is analyzed to determine if it's up or down
3. **Gesture Recognition**: Combination of finger positions creates specific gestures
4. **Action Execution**: PyAutoGUI executes corresponding system actions
5. **Feedback Loop**: Visual feedback shows current gesture status

### Technical Details

- **Hand Landmarks**: 21 key points tracked per hand
- **Finger Detection**: Y-coordinate comparison with dynamic thresholds
- **Gesture Logic**: Boolean combinations of finger states
- **Smoothing**: Movement smoothing for stable cursor control
- **Cooldown System**: Prevents rapid gesture triggering

## 🎯 Use Cases

- **Accessible Computing**: Hands-free computer control
- **Presentation Control**: Navigate slides without touching keyboard
- **Video Streaming**: Control Netflix, YouTube, etc. from distance
- **Gaming**: Gesture-based game controls
- **Smart Home**: Integrate with home automation systems

## 🐛 Troubleshooting

### Common Issues

**Camera not detected:**
```bash
# Check available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"
```

**Poor gesture detection:**
- Ensure good lighting
- Keep hand 1-3 feet from camera
- Use plain background
- Check camera resolution

**Performance issues:**
- Lower camera resolution
- Reduce MediaPipe model complexity
- Close other applications using camera

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black app.py controller.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MediaPipe** by Google for hand tracking
- **OpenCV** for computer vision capabilities
- **PyAutoGUI** for system control automation

## 🔮 Future Enhancements

- [ ] Multi-hand gesture support
- [ ] Custom gesture training
- [ ] Voice command integration
- [ ] Mobile app version
- [ ] Gesture recording/playback
- [ ] Advanced gesture combinations
- [ ] Machine learning gesture improvement

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/hand-gesture-video-controller/issues) section
2. Create a new issue with detailed description
3. Include your Python version, OS, and error messages

## ⭐ Show Your Support

Give a ⭐ if this project helped you!

---

**Made with ❤️ by [Your Name]**
