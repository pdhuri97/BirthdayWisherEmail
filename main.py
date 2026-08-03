# 1. Declaring variables
import os
import pandas as pd
import datetime as dt
import random
import smtplib

SENDER_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")
LETTER=""

# 2. Read the birthdays.csv file and create a dictionary
birthday_data=pd.read_csv('birthdays.csv')
birthday_records=birthday_data.to_dict(orient='records')

# 3. Get today's date and month
now=dt.datetime.now()
current_day=now.day
current_month=now.month

# 4. Select letter from letters folder
def select_letter(name):
    global LETTER
    with open(f"letter_templates/letter_{random.randint(1, 3)}.txt", "r") as file:
        LETTER = file.read()
        return LETTER.replace("[NAME]",f"{name}")

# 5. Generate birthday email and send to receiver.
def generate_email(receiver_email,receiver_name):
    message = select_letter(name=receiver_name)
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=SENDER_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=SENDER_EMAIL,
                            to_addrs=receiver_email,
                            msg=f"Subject:Birthday Wishes\n\n{message}")

# 6. Go through birthday dictionary data and look for people whose birthday is today.
for record in range(0,len(birthday_records)):
    if birthday_records[record]["month"]==current_month and birthday_records[record]["day"]==current_day:
        person_name=birthday_records[record]["name"]
        person_email = birthday_records[record]["email"]
        generate_email(receiver_email=person_email,receiver_name=person_name)
