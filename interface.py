import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import sounddevice as sd
import scipy.io.wavfile as wav
import subprocess
from PIL import Image, ImageTk
import time
import os
import requests
import threading
import subprocess

pt1="projectfolder/path_config1.txt" 

def start_recording():
    # Define the recording parameters
    sample_rate = 16000  # Sample rate (Hz)
    duration = 10  # Duration of recording (seconds)
    RECORDING_TIME_LIMIT=duration
    CHANNELS = 1

    progress_dialog = tk.Toplevel(window)
    progress_dialog.title("Recording Progress")

    progress_label = ttk.Label(progress_dialog, text="Recording in progress...")
    progress_label.pack(pady=10)

    stopwatch_label = ttk.Label(progress_dialog, text="00:00")
    stopwatch_label.pack()

    progress_bar = ttk.Progressbar(progress_dialog, length=300, mode="determinate", maximum=RECORDING_TIME_LIMIT)
    progress_bar.pack(pady=10)

    
    audio_data = []

    def recording_thread():
        nonlocal audio_data

        # Start recording audio
        audio_data = sd.rec(int(RECORDING_TIME_LIMIT * sample_rate), samplerate=sample_rate, channels=CHANNELS)
        sd.wait()

    def update_progress():
        start_time = time.time()
        elapsed_time = 0

        while elapsed_time < RECORDING_TIME_LIMIT:
            current_time = time.time()
            elapsed_time = current_time - start_time
            progress_bar["value"] = elapsed_time
            progress_dialog.update()

            # Update the stopwatch label
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            stopwatch_label["text"] = f"{minutes:02d}:{seconds:02d}"

        messagebox.showinfo("Message", "Recording stopped.")
        progress_dialog.destroy()
        file_pathaud= filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Audio files", "*.mp3")])
        if file_pathaud:
            wav.write(file_pathaud, sample_rate, audio_data)
            print(f"Recording saved to: {file_pathaud}")
        with open("C:/Users/AKASH V A/Documents/projectfolder/path_config1.txt" , "w") as file:
            file.write(file_pathaud)

    # Start the recording and progress update threads
    recording_thread = threading.Thread(target=recording_thread)
    progress_thread = threading.Thread(target=update_progress)
    progress_thread.start()
    recording_thread.start()
   


    

   
pt2="/projectfolder/path_config2.txt"


def start_video_recording():
    # Define the video recording parameters
    video_width = 640  # Width of the video frame
    video_height = 480  # Height of the video frame
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Video files", "*.mp4")])
    
    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_file, fourcc, 20.0, (video_width, video_height))
    
    # Start video recording
    print("Video recording started...")
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if ret:
            video_writer.write(frame)
            cv2.imshow('Video Recording', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Stop recording on 'q' key press
                break
    
    # Release resources
    video_capture.release()
    video_writer.release()
    cv2.destroyAllWindows()
    
    print(f"Video recording saved to: {output_file}")
    file_pathvid=output_file
    with open(pt2, "w") as file:
        file.write(file_pathvid)

    


def upload_audio():
    file_pathaud = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*")])
    with open(pt1, "w") as file:
        file.write(file_pathaud)
    # Perform necessary operations with the audio file

def upload_video():
    file_pathvid = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    with open(pt2, "w") as file:
        file.write(file_pathvid)


def execute_code():
    # Replace "your_replicate_api_token" with your actual Replicate API token
    os.environ["REPLICATE_API_TOKEN"] = "r8_0YQ7tU73hy58WoAmFv1L5GbH53gWNQS27lSxj"

    notebook_path = "C:/Users/AKASH V A/Documents/projectfolder/versionproject.ipynb" # provide path here
       # Check if the file exists
    # Check if the file exists
    if not os.path.isfile(notebook_path):
        messagebox.showerror("Error", "Notebook file not found.")
        return

    # Execute the IPython Notebook
    try:
        subprocess.run(["jupyter", "nbconvert", "--execute", "--inplace", notebook_path], check=True)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    
    messagebox.showinfo("Message","Conversion completed. ")



def play_video():
    root = tk.Tk()
    root.withdraw()

    file_path = "C:/Users/AKASH V A/Documents/result.mp4"

    if file_path:
        try:
            # Use the default media player to open the video
            subprocess.run(['start', '', file_path], shell=True)
        except FileNotFoundError:
            print("Error: No default media player found.")
        except Exception as e:
            print("Error:", e)



# Create the main window
window = tk.Tk()
window.title(" EXPRESSIVE SPEECH TRANSLATOR")
window.geometry("700x400")  # Set the window size
window.resizable(False, False)  # Disable resizing the window

# Load the soundwave image
image = Image.open("C:/Users/AKASH V A/Documents/soundwave.jpg")
background_image = ImageTk.PhotoImage(image)

# Create a label with the soundwave image as the background
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


# Create style for buttons
button_style = ttk.Style()
button_style.configure("Custom.TButton", font=("Times New Roman", 16, "bold"), width=16, background="#000000", foreground='#000000')


# Create buttons
audio_button = ttk.Button(window, text="Record Audio", command=start_recording, style="Custom.TButton")
audio_button.pack(pady=10)

audio_button = ttk.Button(window, text="Upload Audio", command=upload_audio, style="Custom.TButton")
audio_button.pack(pady=10)

video_button = ttk.Button(window, text="Record Video", command=start_video_recording, style="Custom.TButton")
video_button.pack(pady=10)

audio_button = ttk.Button(window, text="Upload Video", command=upload_video, style="Custom.TButton")
audio_button.pack(pady=10)

code_button = ttk.Button(window, text="Execute Code", command=execute_code, style="Custom.TButton")
code_button.pack(pady=10)

play_button = ttk.Button(window, text="Play Video", command=play_video, style="Custom.TButton")
play_button.pack(pady=10)


# Start the main loop
window.mainloop()
