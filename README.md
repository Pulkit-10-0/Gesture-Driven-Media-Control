# Gesture-Driven Media Control System  

This project is a **touchless media control system** inspired by BMW cars' gesture-based volume control. It allows users to control system volume and Spotify playback using simple hand gestures, creating a seamless and futuristic interaction experience.  

---

## Features  
- **Volume Control**: Adjust system volume by rotating your hand.  
- **Track Navigation**: Switch tracks by pointing to specific zones on the screen.  
- **Real-Time Feedback**: Visual indicators for gestures and volume levels.  
- **Cooldown System**: Prevents accidental multiple track changes with a built-in delay.  

---

### Watch the Demo:
[![Watch the Demo](https://img.youtube.com/vi/E4N5C6S1yZA/0.jpg)](https://youtu.be/E4N5C6S1yZA)

---

## Tech Stack  
- **Programming Language**: Python  
- **Libraries/Tools**:  
  - OpenCV (for computer vision)  
  - MediaPipe (for hand tracking)  
  - NumPy (for mathematical calculations)  
  - osascript (to control macOS system volume and Spotify)  
- **Platform**: macOS  
- **Hardware**: Laptop/PC with a webcam  

---

## Inspiration  
This project is inspired by **BMW's gesture-based in-car volume controls**, reimagined for desktop use. The idea was to create an intuitive, touchless interface that integrates seamlessly into daily life.  

---

## How It Works  
1. **Hand Detection**: The system tracks your hand's position and orientation using MediaPipe.  
2. **Gesture Recognition**:  
   - **Rotate your hand**: Adjust system volume smoothly.  
   - **Point to zones**: Navigate to the previous or next track.  
3. **Real-Time Updates**: Visual feedback ensures accurate and responsive controls.  

---

## Setup  
1. Install required libraries:  
   `pip install opencv-python mediapipe numpy`  
2. Clone the repository and navigate to the project directory.  
3. Run the script:  
   `python gesture_control.py`  

---

## Key Learnings  
- Mastered gesture recognition using **MediaPipe** and **OpenCV**.  
- Integrated Python scripts with macOS commands for system volume and Spotify control.  
- Designed a touchless, user-centric interface inspired by real-world applications.  

---

## Future Enhancements  
- Cross-platform compatibility (Windows/Linux).  
- Support for additional media players.  
- Advanced gestures for finer controls.  

---

