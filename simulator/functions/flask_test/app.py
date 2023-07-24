from flask import Flask
import time
import random
import requests

app = Flask(__name__)


@app.route('/test')
def test():
    start_time = time.time()

    st = random.uniform(2, 2.5)
    time.sleep(st)

    end_time = time.time()
    duration = end_time - start_time
    print(duration)

    # Store the duration in a file
    with open(f"/app/output/durations.txt", "a") as f:
        f.write(str(duration) + "\n")

    return {"duration": duration}


def send_get_request(url):
    max_retries = 50
    retry_count = 0
    while retry_count < max_retries:
        print(f"Trying To Request The App: ", retry_count)
        try:
            res = requests.get(url)
            if res.status_code == 200:
                return res
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.InvalidSchema:
            pass

        time.sleep(1)
        retry_count += 1
    raise Exception(f"Failed to connect to {url}")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    send_get_request('http://127.0.0.1:5000/test')
