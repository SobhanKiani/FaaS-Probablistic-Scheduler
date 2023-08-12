import time
import random
import os


def f1():
    d = 0.5
    max_d = d + 0.15 
    min_d = d - 0.15
    start_time = time.time()

    st = random.uniform(min_d, max_d)
    time.sleep(st)

    end_time = time.time()
    duration = end_time - start_time
    print(duration)

    # Store the duration in a file
    with open(f"/app/output/durations.txt", "a") as f:
        f.write(str(duration) + "\n")

    time.sleep(2)

    return duration
