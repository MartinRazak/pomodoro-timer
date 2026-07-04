import tkinter as tk
import threading
from playsound import playsound

# --- Variables ---

time_left = 1500
is_running = False
timer_id: str | None = None
mode = "work"
sessions = 0
WORK_TIME = 1500
SHORT_BREAK = 600
LONG_BREAK = 900

# --- Logic functions ---

def play_sound(file):
    threading.Thread(
        target=lambda: playsound(file),
        daemon=True
    ).start()

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f'{minutes:02}:{seconds:02}'

def stop_timer():
    global is_running, timer_id

    is_running = False

    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

def start_timer():
    global is_running

    if not is_running:
        is_running = True
        update_timer()

def reset_timer():
    global is_running, time_left, mode, sessions

    stop_timer()
    mode = 'work'
    sessions = 0
    time_left = WORK_TIME
    label.config(text=format_time(time_left))
    mode_label.config(text=mode.upper())
    session_label.config(text=f"Sessions: {sessions}")
    pause_button.config(text="Pause")

def pause_resume_timer():
    global is_running

    if is_running:
        stop_timer()
        pause_button.config(text="Resume")
    else:
        start_timer()
        pause_button.config(text="Pause")

def update_timer():
    global time_left, mode, timer_id, sessions

    if not is_running:
        return

    if time_left <= 0:

        if mode == 'work':
            sessions += 1

            if sessions % 4 == 0:
                mode = 'break'
                time_left = LONG_BREAK
            else:
                mode = 'break'
                time_left = SHORT_BREAK

            play_sound("break_end.wav")
        else:
            mode = 'work'
            time_left = WORK_TIME
            play_sound("break_end.wav")
    else:
        time_left -= 1

    label.config(text=format_time(time_left))
    mode_label.config(text=mode.upper())
    session_label.config(text=f"Sessions: {sessions}")

    timer_id = root.after(1000, update_timer)

# --- User interface ---

root = tk.Tk()
root.title("Pomodoro Timer")
root.geometry("320x360")
root.configure(bg="#2b2b2b")  # dark background

main_frame = tk.Frame(root, bg="#2b2b2b")
main_frame.pack(expand=True)

# --- Timer (big focus) ---
label = tk.Label(
    main_frame,
    text=format_time(time_left),
    font=("Arial", 40, "bold"),
    fg="white",
    bg="#2b2b2b"
)
label.pack(pady=(30, 10))

# --- Mode ---
mode_label = tk.Label(
    main_frame,
    text=mode.upper(),
    font=("Arial", 14),
    fg="#aaaaaa",
    bg="#2b2b2b"
)
mode_label.pack()

# --- Sessions ---
session_label = tk.Label(
    main_frame,
    text="Sessions: 0",
    font=("Arial", 12),
    fg="#aaaaaa",
    bg="#2b2b2b"
)
session_label.pack(pady=(5, 20))

# --- Buttons ---
button_frame = tk.Frame(main_frame, bg="#2b2b2b")
button_frame.pack()

def style_button(btn):
    btn.configure(
        font=("Arial", 10, "bold"),
        bg="#444",
        fg="white",
        activebackground="#666",
        activeforeground="white",
        bd=0,
        padx=10,
        pady=5
    )

start_button = tk.Button(button_frame, text="Start", command=start_timer)
pause_button = tk.Button(button_frame, text="Pause", command=pause_resume_timer)
stop_button = tk.Button(button_frame, text="Stop", command=stop_timer)
reset_button = tk.Button(button_frame, text="Reset", command=reset_timer)

for i, btn in enumerate([start_button, pause_button, stop_button, reset_button]):
    style_button(btn)
    btn.grid(row=0, column=i, padx=5)

root.mainloop()