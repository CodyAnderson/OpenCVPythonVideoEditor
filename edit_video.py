import cv2
import os

def process_video(video_path):
    # Initialize video capture
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get the base filename without extension for saving frames
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_count = 0

    print("Controls: [Space] - Next Frame | [Enter] - Save Frame | [Q] - Quit")

    while True:
        ret, frame = cap.read()
        
        # If ret is False, we've reached the end of the video
        if not ret:
            print("End of video reached.")
            break

        frame_count += 1
        window_name = f"Video - Frame {frame_count}"
        
        while True:
            cv2.imshow("Frame Viewer", frame)
            
            # waitKey(0) pauses execution until a key is pressed
            key = cv2.waitKey(0) & 0xFF

            # If Space (32) is pressed, break inner loop to get next frame
            if key == 32:
                break
            
            # If Enter (13) is pressed, save the frame
            elif key == 13:
                filename = f"{base_name}_frame_{frame_count}.png"
                cv2.imwrite(filename, frame)
                print(f"Saved: {filename}")
            
            # If 'q' is pressed, exit the entire program
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

    cap.release()
    cv2.destroyAllWindows()

# Usage
process_video('your_video.mp4')