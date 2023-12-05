import os


class Job:
    def __init__(self, topic: str, value) -> None:
        self.topic = topic
        self.value = value


def store_in_file(file_path, data):
    duration, ram, cs_duration, cs_count = data
    zipped_data = zip(duration, ram, cs_duration, cs_count)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as f:
        for d, r, cs_d, cs_c in zipped_data:
            f.write(f"{d},{r},{cs_d},{cs_c}\n")
