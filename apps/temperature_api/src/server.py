#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import random
import logging
from typing import Union

from flask import Flask, request


class TemperatureApiApp:
    http_server_app = Flask("TemperatureApiApp")

    def __init__(self):
        self.http_server_app.logger.setLevel(logging.INFO)
        self.setup_routes()

    def setup_routes(self):
        self.http_server_app.add_url_rule(
            "/temperature/<int:sensor_id>", methods=["GET"], view_func=self.temperature
        )

    def run(self, host: str, port: int):
        self.http_server_app.run(host=host, port=port)

    def temperature(self, sensor_id: int = 0):
        location = request.args.get("location", "", type=str)

        # If no location is provided, use a default based on sensor ID
        if location == "":
            if sensor_id == 1:
                location = "Living Room"
            elif sensor_id == 2:
                location = "Bedroom"
            elif sensor_id == 3:
                location = "Kitchen"
            else:
                location = "Unknown"

        # If no sensor ID is provided, generate one based on location
        if sensor_id == 0:
            if location == "Living Room":
                sensor_id = 1
            elif location == "Bedroom":
                sensor_id = 2
            elif location == "Kitchen":
                sensor_id = 3
            else:
                sensor_id = 0

        result = random.randint(-30, 50)
        self.http_server_app.logger.info(
            "Get Temperature result: %d. Location: %s; sensor_id: %d.",
            result,
            location,
            sensor_id,
        )
        return json.dumps({"value": result}), 200


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="server_test.py",
        description="""
        Test server for TemperatureApiApp. Request examples:
            curl -X GET http://127.0.0.1:8081/temperature
        """,
        epilog="Example: python3 server.py -p 8081",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        required=False,
        default=8081,
        help="Port for HTTPS server",
    )
    args = parser.parse_args()

    TemperatureApiApp().run("0.0.0.0", args.port)
