import cv2
import os
import sys

brush_size = 30
color = [255,0,0]
frames=[None,None]
mouse_pos = [0,0]
use_paint_dot_net = False#True
img_ext = "png"

def mouse_event(event, x, y, flags, param):
    global brush_size
    param["mouse_pos"][0] = x
    param["mouse_pos"][1] = y
    if flags&cv2.EVENT_FLAG_LBUTTON:
        cv2.circle(param["frames"][1],(x,y),param["brush_size"],param["color"],-1)
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0 and brush_size < 100:
            brush_size += 1
        elif flags < 0 and brush_size > 2:
            brush_size -= 1


def process_video(video_path):
    if not os.path.exists(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        return

    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    base_name = os.path.splitext(os.path.basename(video_path))[0]

    # Retrieve properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    # Define codec and VideoWriter
    vidout_filename = f"{base_name}_EDIT.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vidout = cv2.VideoWriter(vidout_filename, fourcc, fps, (frame_width, frame_height))
    cv2.namedWindow('Video Editor')
    frame_count = 0

    print(f"--- Processing: {video_path} ---")
    print("Controls: [Space] Next Frame | [Enter] Save Current Frame | [Q] Quit")

    while True:
        # 1. Capture the next frame
        ret, frames[1] = cap.read()
        if frames[1] is not None:
            frames[0] = frames[1].copy()
        if not ret:
            print("End of video reached.")
            break

        frame_count += 1
        saved_frame = False
        
        # 2. Stay on this specific frame until the user chooses to move on
        while True:
            frame_filename = f"{base_name}_{frame_count}.{img_ext}"
            if use_paint_dot_net and saved_frame:
                frames[1] = cv2.imread(frame_filename, cv2.IMREAD_COLOR)
                frames[0] = frames[1].copy()   
            
            


            cv2.setMouseCallback('Video Editor', mouse_event, {"frames":frames,"brush_size":brush_size,"color":color,"mouse_pos":mouse_pos})
            cv2.circle(frames[0],mouse_pos,brush_size,[0,0,0],-1)
            cv2.circle(frames[0],mouse_pos,brush_size-2,[255,255,255],-1)
            cv2.imshow("Video Editor", frames[0])
            frames[0] = frames[1].copy()

            # Wait for user input
            key = cv2.waitKey(1) & 0xFF

            if key == 32: # Space Bar: Advance to next frame
                break
            
            elif key == 13: # Enter Key: Save frame but STAY here
                if use_paint_dot_net:
                    cv2.imwrite(frame_filename, frames[1])
                    saved_frame = True
                    print(f"Saved: {frame_filename} (Standing by on frame {frame_count}...)")
                    os.system(f'"C:\\Program Files\\paint.net\\paintdotnet.exe" {frame_filename}')
                    # Note: We do NOT 'break' here, so the loop repeats for the same frame
            
            elif key == ord('q'): # Quit
                print("Exiting...")
                cap.release()
                cv2.destroyAllWindows()
                return
        vidout.write(frames[0])

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_video>")
    else:
        process_video(sys.argv[1])