from random import randrange

import requests
import sys
import getopt
import time

CHANNEL_URL = "https://hooks.slack.com/services/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"
MIN_THRESHOLD = 10
MAX_OFFSET = 10000000
TARGET_FILES = [
    "https://cdn.hle.com.tw/110下/國小/02題庫光碟/(新課綱)110下翰林國小1年級題庫.iso",
    "https://cdn.hle.com.tw/110下/國小/02題庫光碟/(舊課綱)110下翰林國小6年級題庫.iso",
    "https://cdn.hle.com.tw/110下/國小/02題庫光碟/(舊課綱)110下翰林國小5年級題庫.iso",
    "https://cdn.hle.com.tw/110下/國小/02題庫光碟/(舊課綱)110下翰林國小4年級題庫.iso",
    "https://cdn.hle.com.tw/110下/國小/02題庫光碟/(新課綱)110下翰林國小3年級題庫.iso",
]
TARGET_LENGTH = len(TARGET_FILES)


def download_metrics():
    start_bytes = randrange(MAX_OFFSET)
    last_byte = 104857600 + start_bytes

    try:
        init_time = time.time()
        url = TARGET_FILES[randrange(TARGET_LENGTH)]
        headers = {"Range": f"bytes={start_bytes}-{last_byte}"}  # offset 100 MB
        r = requests.get(url, headers=headers)

        return time.time() - init_time

    except:
        return 0


def generate_message(lag_time):
    if lag_time == 0:
        downstream_speed = 0
    else:
        downstream_speed = 100 / lag_time

    slack_message = f'{time.strftime("%Y/%m/%d %H:%M", time.localtime(time.time()))}: download speed from aws is {downstream_speed:0.2f} MB/s'
    if downstream_speed < MIN_THRESHOLD:
        slack_message = f'<!channel> :bomb: {slack_message}'

    return slack_message


def send_slack_message(slack_message):
    payload = f'{{"text": "{slack_message}" }}'
    response = requests.post(CHANNEL_URL, data=payload)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lag = download_metrics()
    message = generate_message(lag)
    send_slack_message(message)
