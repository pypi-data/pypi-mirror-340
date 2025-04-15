# Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0

from flask import Flask, request, redirect, url_for
from flask_cors import CORS
from flasgger import Swagger
from waitress import serve

from lofar_opah.control_restapi.handler.station_handler import register_station_routes
from lofar_opah.control_restapi.handler.antenna_handler import register_antenna_routes
from lofar_opah.control_restapi.handler.antennafield_handler import (
    register_antennafield_routes,
)


def create_app(
    logger=None,
    station_suffix="",
    remote_grpc_port=None,
    remote_grpc_host=None,
):
    """Starts a REST API server that acts as a proxy to gRPC."""
    app = Flask(__name__)
    CORS(app)
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "The Lofar Control API",
            "description": "API for controlling Lofar Antennas and Antennafields",
        },
        "basePath": "/v1",
    }
    Swagger(app, template=swagger_template)

    if logger:

        @app.after_request
        def log_failed_requests(response):
            """Log requests that resulted in client or server errors."""
            logmessage = (
                f"Method: {request.method} | Path: {request.path} | "
                f"Status: {response.status_code} | IP: {request.remote_addr} | "
                f"User-Agent: {request.user_agent}"
            )
            if response.status_code >= 400:
                logger.error(logmessage)
            else:
                logger.debug(logmessage)
            return response

    @app.route("/")
    def redirect_to_apidocs():
        return redirect(url_for("flasgger.apidocs"))

    register_antenna_routes(
        app, logger, station_suffix, remote_grpc_port, remote_grpc_host
    )

    register_antennafield_routes(
        app, logger, station_suffix, remote_grpc_port, remote_grpc_host
    )

    register_station_routes(
        app, logger, station_suffix, remote_grpc_port, remote_grpc_host
    )

    return app


def start_rest_server(
    logger, rest_port, station_suffix, remote_grpc_port, remote_grpc_host
):
    """Starts a REST API server that acts as a proxy to gRPC."""
    station_suffix = station_suffix if station_suffix is not None else ""

    logger.debug(
        'start_rest_server(rest_port:%s, station_suffix:"%s",'
        "remote-grpc-port:%s, remote-grpc-host:%s)",
        rest_port,
        station_suffix,
        remote_grpc_port,
        remote_grpc_host,
    )

    app = create_app(logger, station_suffix, remote_grpc_port, remote_grpc_host)
    logger.info("Control REST API server started on port %s", rest_port)
    serve(app, host="0.0.0.0", port=rest_port)
