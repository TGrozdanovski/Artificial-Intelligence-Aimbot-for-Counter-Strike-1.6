import torch
import numpy as np
import cv2
import pygetwindow as window_manager
import mss
import time
import win32api
import win32con
from colorama import Fore, Style, init

init(autoreset=True)  # Enable automatic color reset in terminal

class ObjectDetector:
    def __init__(self, model_file):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'  # Check if CUDA is available
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_file)  # Load the YOLOv5 model
        self.classes = self.model.names  # Get class names from the model
        print(f'{Fore.GREEN}Device in use: {Fore.CYAN}{self.device}')  # Display the device in use
        self.print_signature()  # Show developer info

    def print_signature(self):
        print(f'{Fore.YELLOW}Developed by: {Fore.MAGENTA}T')  # Developer name
        print(f'{Fore.YELLOW}GitHub: {Fore.MAGENTA}https://github.com/TGrozdanovski')  # GitHub link

    def process_frame(self, frame):
        self.model.to(self.device)  # Move model to the selected device
        results = self.model([frame])  # Run inference on the frame
        labels, coordinates = results.xyxy[0][:, -1], results.xyxyn[0][:, :-1]  # Get labels and coordinates
        return labels, coordinates  # Return the results

    def draw_boxes(self, results, frame):
        labels, coordinates = results  # Unpack results
        frame_center_x, frame_center_y = frame.shape[1] // 2, frame.shape[0] // 2  # Get center of the frame
        closest_object = float('inf'), None  # Initialize closest object tracker

        for i in range(len(labels)):  # Loop through detected objects
            row = coordinates[i]  # Get the current object's coordinates
            if row[4] >= 0.2 and self.classes[int(labels[i])] == "enemy":  # Filter for confidence and class
                # Calculate the bounding box for the detected object
                x1, y1, x2, y2 = (
                    int(row[0] * frame.shape[1]),
                    int(row[1] * frame.shape[0]),
                    int(row[2] * frame.shape[1]),
                    int(row[3] * frame.shape[0]),
                )
                object_center = (x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2)  # Find the center of the object
                distance = np.sqrt((object_center[0] - frame_center_x) ** 2 + (object_center[1] - frame_center_y) ** 2)  # Calculate distance to center

                if distance < closest_object[0]:  # Check if this object is the closest
                    closest_object = distance, object_center

                # Draw a rectangle around the detected object
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, self.classes[int(labels[i])], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Label the object

        if closest_object[1]:  # If there is a closest object
            # Move the mouse cursor towards the closest detected object
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(speed * (closest_object[1][0] - frame_center_x)), int(speed * (closest_object[1][1] - frame_center_y - offset)), 0, 0)

        return frame  # Return the modified frame

    def find_window(self):
        game_window = window_manager.getWindowsWithTitle("Counter-Strike")  # Look for the game window
        if game_window:  # If found
            win = game_window[0]  # Get the first window
            return win.left, win.top, win.width, win.height  # Return window dimensions
        raise Exception("Game window not found")  # Raise error if not found

    def start_detection(self):
        with mss.mss() as screen:  # Use mss to capture the screen
            while True:  # Loop for continuous detection
                window_rect = self.find_window()  # Get the window's position and size
                screen_area = (window_rect[0], window_rect[1], window_rect[0] + window_rect[2], window_rect[1] + window_rect[3])  # Define the capture area

                start_time = time.perf_counter()  # Start timer for FPS calculation
                frame = np.array(screen.grab(screen_area))  # Capture the screen
                results = self.process_frame(frame)  # Process the captured frame
                frame = self.draw_boxes(results, frame)  # Draw bounding boxes on the frame
                end_time = time.perf_counter()  # End timer

                fps = 1 / np.round(end_time - start_time, 3)  # Calculate FPS
                cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Display FPS
                cv2.imshow('Detection', frame)  # Show the detection results

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if 'q' is pressed
                    break

# Configuration parameters
speed = 5  # Mouse movement speed
offset = 15  # Offset for mouse positioning
model_file_path = 'trained.pt'  # Path to the YOLOv5 model

detector = ObjectDetector(model_file_path)  # Create an instance of the detector
detector.start_detection()  # Start the detection process
