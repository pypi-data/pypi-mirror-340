# Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0
"""Main class for the  API Server"""

import logging
import argparse
from lofar_opah.control_restapi.rest_server import start_rest_server
from lofar_lotus.metrics import start_metrics_server
import sys

logger = logging.getLogger()
REST_PORT = 50052
STATION_SUFFIX = ".control.lofar"  # This is added to the stationname

logging.basicConfig(level=logging.DEBUG)


def _create_parser():
    """Define the parser"""
    parser = argparse.ArgumentParser(description="Serve the station rest interface.")
    parser.add_argument(
        "--port",
        default=50053,
        type=int,
        help="HTTP port to listen on. Defaults to 50053",
    )
    parser.add_argument(
        "--metrics-port",
        default=8002,
        type=int,
        help="Prometheus metrics HTTP port. Defaults to 8002",
    )
    parser.add_argument(
        "--stationsuffix",
        default="c.control.lofar",
        nargs="?",
        type=str,
        help=(
            "Append this to all station_name e.g. c.control.lofar."
            "Leave empty for rest on localserver. Defaults to c.control.lofar"
        ),
    )
    parser.add_argument(
        "--remote-grpc-port",
        default="50051",
        type=int,
        help="The port the remote grpc service is listening on. defaults to 50051",
    )

    parser.add_argument(
        "--remote-grpc-host",
        required=False,
        help=(
            "Overrides stationname (from api request) +stationsuffix "
            "being used as grpchost. "
            "instead it then directly uses this grpc host"
        ),
    )
    return parser


def main(argv=None):
    parser = _create_parser()
    args = parser.parse_args(argv or sys.argv[1:])
    start_metrics_server(args.metrics_port)

    logging.info(
        "Launching Control Rest Server port:%s, "
        "stationsuffix:%s,remote-grpc-port:%s,remote-grpc-host:%s",
        args.port,
        args.stationsuffix,
        args.remote_grpc_port,
        args.remote_grpc_host,
    )
    # Create Contral Api server
    start_rest_server(
        logger,
        args.port,
        args.stationsuffix,
        args.remote_grpc_port,
        args.remote_grpc_host,
    )


if __name__ == "__main__":
    main()
