import time

def work_countdown(seconds):
    while seconds > 0:
        print(f'\rWork | Time remaining : {seconds // 60:02}:{seconds % 60:02}', end='', flush=True)
        time.sleep(1)
        seconds -= 1
    print("Work finished")
    return 1

def break_countdown(seconds):
    while seconds > 0:
        print(f'\rBreak | Time remaining : {seconds // 60:02}:{seconds % 60:02}', end='', flush=True)
        time.sleep(1)
        seconds -= 1
    print("Break finished")

def keep_going():
    decision = input('Start next Pomodoro? ').lower()
    while decision not in ('y', 'n'):
        print('Write y or n brochacho')
        decision = input('Start next Pomodoro? ').lower()
    return decision

cycle = 0

while True:
    cycle += work_countdown(300)
    print(f"Pomodoro {cycle} completed")
    if cycle == 4:
        print('Long break time!')
        break_countdown(10)
        cycle = 0
    else:
        print('Short break time!')
        break_countdown(3)
    answer = keep_going()
    if answer == 'n':
        break