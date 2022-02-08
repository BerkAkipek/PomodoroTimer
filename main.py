from tkinter import *
import math
from pygame import mixer
# ---------------------------- CONSTANTS ------------------------------- #
# Colors From: https://colorhunt.co/
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
TIMER = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global REPS
    window.after_cancel(TIMER)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    check_mark.config(text="")
    REPS = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global REPS
    REPS += 1
    study_time = WORK_MIN * 60
    short_break = SHORT_BREAK_MIN * 60
    long_break = LONG_BREAK_MIN * 60
    if REPS % 8 == 0:
        count_down(long_break)
        timer_label.config(fg=RED, text="Break")
    elif REPS % 2 == 0:
        count_down(short_break)
        timer_label.config(fg=PINK, text="Break")
    else:
        count_down(study_time)
        timer_label.config(fg=GREEN, text="Work")

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global TIMER
    count_minutes = math.floor(count / 60)
    count_seconds = count % 60
    if count_seconds < 10:
        count_seconds = f"0{count_seconds}"
    canvas.itemconfig(timer_text, text=f"{count_minutes}:{count_seconds}")
    if count > 0:
        TIMER = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(REPS/2)
        for _ in range(work_sessions):
            marks += " + "
            mixer.music.play()
        check_mark.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))
canvas.grid(column=1, row=1)

mixer.init()
mixer.music.load("Censor Beep Sound Effect.mp3")

timer_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 30, "bold"))
timer_label.grid(column=1, row=0)

start_button = Button(text="Start", bg="white", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", bg="white", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_mark = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 18, "bold"))
check_mark.grid(column=1, row=3)

window.mainloop()
