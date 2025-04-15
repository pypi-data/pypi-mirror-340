#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

import argparse
from concurrent import futures
import logging
import sys

import grpc
from grpc_reflection.v1alpha import reflection
from lofar_sid.interface.opah import grafana_apiv3_pb2
from lofar_sid.interface.opah import grafana_apiv3_pb2_grpc
from .grafana_api import GrafanaAPIV3

from lofar_opah._logging import setup_logging_handler

from lofar_lotus.metrics import start_metrics_server


logger = logging.getLogger()


class Server:
    def __init__(
        self, stations: list[str], port: int, default_station: str | None = None
    ):
        # Initialise gRPC server
        logger.info("Initialising grpc server")
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        grafana_apiv3_pb2_grpc.add_GrafanaQueryAPIServicer_to_server(
            GrafanaAPIV3(stations, default_station), self.server
        )
        SERVICE_NAMES = (
            grafana_apiv3_pb2.DESCRIPTOR.services_by_name["GrafanaQueryAPI"].full_name,
            reflection.SERVICE_NAME,  # reflection is required by innius-gpc-datasource
        )
        reflection.enable_server_reflection(SERVICE_NAMES, self.server)

        self.port = self.server.add_insecure_port(f"0.0.0.0:{port}")
        logger.info(f"Server initialised, listening on port {self.port}")

    def handle_statistics_message(self, topic, timestamp, message):
        self.statistics_servicer.handle_statistics_message(topic, timestamp, message)

    def run(self):
        self.server.start()
        logger.info(f"Server running on port {self.port}")
        self.server.wait_for_termination()

    def stop(self):
        logger.info("Server stopping.")
        self.server.stop(grace=1.0)
        logger.info("Server stopped.")


def _create_parser():
    """Define the parser"""
    parser = argparse.ArgumentParser(description="Serve the station gRPC interface.")
    parser.add_argument(
        "--port",
        default=50051,
        type=int,
        help="HTTP port to listen on.",
    )
    parser.add_argument(
        "--metrics-port",
        default=8001,
        type=int,
        help="Prometheus metrics HTTP port.",
    )
    parser.add_argument(
        "--station",
        required=True,
        action="append",
        help="Station names (can supply multiple)",
    )
    parser.add_argument(
        "--default-station",
        help="Station name to use if none is specified",
    )
    return parser


def main(argv=None):
    parser = _create_parser()
    args = parser.parse_args(argv or sys.argv[1:])

    # Initialise simple subsystems
    logging.basicConfig(level=logging.DEBUG)
    logger.addHandler(setup_logging_handler())

    start_metrics_server(args.metrics_port)

    # Create gRPC server
    server = Server(args.station, args.port, args.default_station)

    # Serve indefinitely
    server.run()


if __name__ == "__main__":
    main()
