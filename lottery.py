import time
import os
import random
from datetime import datetime, timedelta

USERS_FILE = "users.txt"
LOG_FILE = "lottery_log.txt"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        for user in users:
            f.write(user + "\n")

def log_event(message, include_timestamp=True):
    with open(LOG_FILE, "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if include_timestamp:
            log.write(f"[{timestamp}] {message}\n")
        else:
            log.write(f"{message}\n")

def is_valid_username(username):
    return username.isalnum() and username != ""

def registration_loop(duration_minutes, users, start_label="Registration"):
    print(f"\n=== {start_label} Phase ({duration_minutes} minutes) ===")
    end_time = datetime.now() + timedelta(seconds=duration_minutes)
    next_reminder = datetime.now() + timedelta(seconds=10)
    next_autosave = datetime.now() + timedelta(minutes=5)

    while datetime.now() < end_time:
        now = datetime.now()

        if now >= next_reminder:
            remaining = end_time - now
            print(f"[Reminder] {remaining.seconds} seconds remaining...")
            next_reminder += timedelta(seconds=10)

        if now >= next_autosave:
            save_users(users)
            print("[Autosave] Progress saved.")
            next_autosave += timedelta(minutes=5)

        try:
            username = input("Enter your username: ").strip()

            if not is_valid_username(username):
                print("Invalid username! Only letters and numbers allowed.")
                continue

            if username in users:
                print("Username already registered.")
                continue

            users.append(username)
            save_users(users)
            log_event(f"User registered: {username} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"User '{username}' registered! Total: {len(users)}")

        except KeyboardInterrupt:
            print("\n[Interrupted] Saving progress and exiting...")
            save_users(users)
            log_event("Program interrupted by user.")
            exit()

    return users


def declare_winner(users):
    winner = random.choice(users)
    print("\n=== Lottery Draw Completed! ===")
    print(f"Total Participants: {len(users)}")
    print(f"*** Winner: {winner} ***")

    with open(LOG_FILE, "a") as f:
        f.write("\n=== LOTTERY RESULT ===\n")
        f.write(f"Total Participants: {len(users)}\n")
        f.write("Participants:\n")
        for user in users:
            f.write(f" - {user}\n")
        f.write(f"Winner: {winner}\n")

    return winner




print("=== Welcome to the Terminal Lottery System ===")
users = load_users()

log_event("Lottery system started.")
users = registration_loop(10, users, "Initial Registration")

if len(users) < 5:
    print("\n[Notice] Less than 5 users. Extending registration by 30 minutes...")
    log_event("Extension activated due to low registrations.")
    users = registration_loop(30, users, "Extended Registration")

if len(users) == 0:
    print("\n[Result] No users registered. Exiting the system.")
    log_event("No users registered. Program exited.")
    exit()


winner = declare_winner(users)
log_event(f"Winner declared: {winner}")