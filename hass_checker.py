#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import subprocess
import platform
import time
import logging
import sys
import os
from urllib.parse import urlsplit

# Configuration
PUSH_TOKEN = os.environ.get("PUSH_TOKEN")
HASS_URL = os.environ.get("HASS_URL")
CHECK_INTERVAL = 5 * 60  # 5 minutes
TIMEOUT = 5

# Messages
HASS_UNAVAILABLE_TITLE   = "⭕ Home Assistant is down"
HOST_UNAVAILABLE_TITLE   = "🔴 Home Assistant is down"
HASS_AVAILABLE_TITLE     = "🟢 Home Assistant is up"

HASS_UNAVAILABLE_MESSAGE = "The web server is currently not responding"
HOST_UNAVAILABLE_MESSAGE = "Host is currently not responding"
HASS_AVAILABLE_MESSAGE   = ""


def logger():
    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(
        stream=sys.stdout,
        format=FORMAT,
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger()


def ping_ip(current_ip_address):
    try:
        output = subprocess.check_output(
            "ping -{} 1 {}".format(
                ("n" if platform.system().lower() == "windows" else "c"),
                current_ip_address,
            ),
            shell=True,
            universal_newlines=True,
        )
        if "unreachable" in output:
            return False
        else:
            return True
    except Exception:
        return False


def send_push_notification(title, message, push_token):
    data = {
        "message": message,
        "title": title,
        "data": {"push": {"category": "hass-state", "thread-id": "hass-state"}},
        "push_token": push_token,
        "registration_info": {"app_id": "requests"},
    }

    requests.post(
        "https://mobile-apps.home-assistant.io/api/sendPushNotification", json=data
    )


def check_availability(url, interval, push_token, timeout, logger=logger()):
    alive = True
    host = urlsplit(url).hostname
    print("Watching {}...".format(url))
    while True:
        try:
            r = requests.get(url , timeout=timeout)
            r.raise_for_status()
            if alive == False:
                logger.info("Server is up")
                send_push_notification(
                    HASS_AVAILABLE_TITLE, HASS_AVAILABLE_MESSAGE, push_token
                )
                alive = True
        except (requests.exceptions.RequestException,requests.exceptions.HTTPError):
            if alive:
                alive = False
                logger.info("Ping {}".format(host))
                if ping_ip(host):
                    logger.error("Server is down")
                    send_push_notification(
                        HASS_UNAVAILABLE_TITLE, HASS_UNAVAILABLE_MESSAGE, push_token
                    )
                else:
                    logger.error("Host is down")
                    send_push_notification(
                        HOST_UNAVAILABLE_TITLE, HOST_UNAVAILABLE_MESSAGE, push_token
                    )

        time.sleep(interval)

if __name__ == "__main__":
    check_availability(
        HASS_URL, interval=CHECK_INTERVAL, timeout=TIMEOUT, push_token=PUSH_TOKEN
    )
