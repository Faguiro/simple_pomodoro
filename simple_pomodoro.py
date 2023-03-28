import pygame
import time
import threading
import PySimpleGUI as sg

pygame.mixer.init()

def play_sound(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def pomodoro_work(window, i):
    print("Pomodoro Work session starts now!")
    window['cicle'].update(value="Ciclo: "+str(i+1))
    for i in range(1500, 0, -1):
        mins, secs = divmod(i, 60)
        time_left = f'{mins:02d}:{secs:02d}'
        window['timer'].update(value=time_left)
        window['step'].update(value="Sessão de trabalho")
        time.sleep(1)  # 1 second
        if i % 60 == 0:
            play_sound("sounds/start_sound.mp3")
    play_sound("sounds/break_sound.mp3")
    print("Pomodoro Work session breaked. Time for a break!")

def pomodoro_break(window, i):
    print("Time for a break!")
    for i in range(300, 0, -1):
        mins, secs = divmod(i, 60)
        time_left = f'{mins:02d}:{secs:02d}'
        window['timer'].update(value=time_left)
        window['step'].update(value="Pausa")
        time.sleep(1)  # 1 second
        if i % 60 == 0:
            play_sound("sounds/break_sound.mp3")
    print("Break breaked. Time for another Pomodoro Work session!")

def pomodoro(window):
    num_pomodoros = 4
    for i in range(num_pomodoros):
        pomodoro_work(window, i)
        
        if i != num_pomodoros - 1:
            play_sound("sounds/break_sound.mp3")
            pomodoro_break(window, i)
    window['timer'].update(value='00:00')
    window['step'].update(value="Pausa longa (20 minutos)")
    play_sound("sounds/Wooden.mp3")
    #pomodoro_work(window, i)
    #time.sleep(1200) # pausa de 20 minutos
    print("Pomodoro session completed. Time for a long break!")

def run_pomodoro(window):
    thread = threading.Thread(target=pomodoro, args=(window,))
    thread.start()

layout = [
    [sg.Text(''), sg.Text('00:00', key='timer', font=('Helvetica', 50))],
    [sg.Text(''), sg.Text('', key='step', font=('Helvetica', 12))],
    [sg.Text(''), sg.Text('', key='cicle', font=('Helvetica', 14))],
    [sg.Button('Iniciar Pomodoro')],
    [sg.Button('Sair')]
]

window = sg.Window('Pomodoro Timer', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Sair':
        break
    if event == 'Iniciar Pomodoro':
        run_pomodoro(window)

window.close()
