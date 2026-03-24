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
    print(os.path.splitext(os.path.basename(video_path)))

    # Retrieve properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    # Define codec and VideoWriter
    vidout_filename = f"{base_name}_EDIT.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vidout = cv2.VideoWriter(vidout_filename, fourcc, fps, (frame_width, frame_height))
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
            key = cv2.waitKey(1) & 0xFF

            if key == 32: # Space Bar: Advance to next frame
                break
            
            elif key == 13: # Enter Key: Save frame but STAY here
                cv2.imwrite(frame_filename, frame)
                saved_frame = True
                print(f"Saved: {frame_filename} (Standing by on frame {frame_count}...)")
                os.system(f'"C:\\Program Files\\paint.net\\paintdotnet.exe" {frame_filename}')
                # Note: We do NOT 'break' here, so the loop repeats for the same frame
            
            elif key == ord('q'): # Quit
                print("Exiting...")
                cap.release()
                cv2.destroyAllWindows()
                return
        vidout.write(frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_video>")
    else:
        process_video(sys.argv[1])