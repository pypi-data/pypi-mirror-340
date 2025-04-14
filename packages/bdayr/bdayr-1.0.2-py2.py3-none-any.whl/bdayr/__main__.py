from ics import Calendar
from datetime import datetime
import json
import os
def PrAllEv(calendar):
    for event in calendar.events:
        event_name = event.name
        event_start = event.begin
        formatted_date = event_start.strftime('%m/%d')
        print(f"{event_name} @ {formatted_date}")

def EvByNme(calendar):
    opt2 = input("Enter exact name: ")
    for event in calendar.events:
        name = event.name
        if name == opt2:
            event_start = event.begin
            date = event_start.strftime('%m/%d')
            print(f"{name} @ {date}")

def main():
    home = os.path.expanduser("~")
    with open(f"{home}/.config/rcal/config.json", "r") as f:
        config = json.load(f)
    with open(config["calpath"], 'r') as file:
        calendar = Calendar(file.read())

    options = {1: EvByNme, 2: PrAllEv}

    print("You can: ")
    print("Get Event by Name (1)")
    print("Get All Events (2)")

    try:
        opt = int(input(">.. "))
        if opt in options:
            options[opt](calendar)
        else:
            print("Invalid option")
    except ValueError:
        print("That ain't a valid number.")

if __name__ == "__main__":
    main()