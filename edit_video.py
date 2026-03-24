import cv2
import os
import sys

def process_video(video_path):
    if not os.path.exists(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        return

    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_count = 0

    print(f"--- Processing: {video_path} ---")
    print("Controls: [Space] Next Frame | [Enter] Save Current Frame | [Q] Quit")

    while True:
        # 1. Capture the next frame
        ret, frame = cap.read()
        
        if not ret:
            print("End of video reached.")
            break

        frame_count += 1
        saved_frame = False
        
        # 2. Stay on this specific frame until the user chooses to move on
        while True:
            frame_filename = f"{base_name}_{frame_count}.png"
            if saved_frame:
                frame = cv2.imread(frame_filename, cv2.IMREAD_COLOR)
            cv2.imshow("Frame Viewer", frame)
            
            # Wait for user input
            key = cv2.waitKey(0) & 0xFF

            if key == 32: # Space Bar: Advance to next frame
                break
            
            elif key == 13: # Enter Key: Save frame but STAY here
                cv2.imwrite(frame_filename, frame)
                print(f"Saved: {frame_filename} (Standing by on frame {frame_count}...)")
                os.system(f'"C:\\Program%20Files\\paint.net\\paintdotnet.exe" {frame_filename}')
                # Note: We do NOT 'break' here, so the loop repeats for the same frame
            
            elif key == ord('q'): # Quit
                print("Exiting...")
                cap.release()
                cv2.destroyAllWindows()
                return

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_video>")
    else:
        process_video(sys.argv[1])