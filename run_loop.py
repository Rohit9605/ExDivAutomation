import schedule
import time
import pandas as pd

def job():
    print("I'm working...")

times = pd.read_csv("timings.csv")
for i in range(len(times)):
    timing = times.iloc[i][0]
    print(timing)
    schedule.every().day.at(timing).do(job)
    
        
while True:
    schedule.run_pending()
    time.sleep(1)