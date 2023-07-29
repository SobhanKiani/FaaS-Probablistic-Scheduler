import time
import random
import os


def f1():
    start_time = time.time()

    st = random.uniform(2.75, 3.25)
    time.sleep(st)

    end_time = time.time()
    duration = end_time - start_time
    print(duration)

    # Store the duration in a file
    with open(f"/app/output/durations.txt", "a") as f:
        f.write(str(duration) + "\n")

    return duration
