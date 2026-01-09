🖐️ Real-Time ASL Recognition Using CNN and MediaPipe
📌 Project Overview

This project is a Real-Time American Sign Language (ASL) Recognition System developed using Computer Vision and Deep Learning.
The system captures hand gestures through a webcam, recognizes ASL alphabets using a CNN-based model, converts them into text, and finally produces speech output.

This project mainly focuses on helping deaf and mute people communicate easily with normal users.

🎯 Problem Statement

Communication between deaf-mute people and normal people is difficult because most people do not understand sign language.
There is a need for a real-time, low-cost, and automated system that can recognize sign language and convert it into text and speech.

🛠️ Technologies Used

Python

OpenCV

MediaPipe

TensorFlow / Keras

NumPy

Windows Text-to-Speech (SAPI)

⚙️ System Working

Webcam captures live hand gesture.

MediaPipe detects hand landmarks.

Extracted features are passed to a CNN model.

CNN classifies the gesture into an ASL alphabet.

Predicted letters are combined to form words.

Text is converted into speech output.

🧠 CNN Usage in This Project

A Convolutional Neural Network (CNN) is used for gesture classification.

The CNN model is trained using collected hand gesture samples.

The trained model is saved as asl_model.h5.

During real-time execution, the model predicts ASL alphabets from live input.

📂 Project Structure
ASL_Project/
│
├── data/                 # Dataset of hand gestures
├── train_model.py        # CNN model training file
├── main.py               # Real-time detection and prediction
├── asl_model.h5          # Trained CNN model
├── requirements.txt      # Required libraries
└── README.md             # Project documentation

▶️ How to Run the Project

Clone the repository

git clone <your-github-repo-link>


Install required libraries

pip install -r requirements.txt


Train the model (optional if model already exists)

python train_model.py


Run the real-time recognition system

python main.py

✅ Features

Real-time ASL alphabet and some symbols(love you, happy, sad) recognition

CNN-based gesture classification

No special hardware required

Text and speech output

User-friendly and low cost

📈 Future Enhancements

sentence-level recognition

Support for multiple sign languages

Mobile application integration

Improved accuracy with larger datasets

🏁 Conclusion

This project successfully demonstrates how CNN and computer vision can be used to recognize ASL gestures in real time.
It provides an effective solution to bridge the communication gap between deaf-mute people and normal users and can be extended further for real-world applications.


👤 Author

Nandan Rathod,
Final Year CSE Student
