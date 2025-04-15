# Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0
from flask import jsonify
from lofar_sid.interface.stationcontrol import antenna_pb2, antenna_pb2_grpc

from lofar_opah.control_restapi._decorators import grpc_error_handler
from lofar_opah.control_restapi.handler.business import get_grpc_channel
from http import HTTPStatus


def get_grpc_stub(
    logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
):
    """Return AntennafieldStub"""
    channel = get_grpc_channel(
        logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
    )
    return antenna_pb2_grpc.AntennaStub(channel)


def cast_antennareply_to_json(response):
    """Clear Cast, gets rid of additional grpc fields"""

    return jsonify(
        {
            "success": response.success,
            "exception": response.exception,
            "result": {
                "antenna_use": response.result.antenna_use,
                "antenna_status": response.result.antenna_status,
            },
            "identifier": {
                "antennafield_name": response.result.identifier.antennafield_name,
                "antenna_name": response.result.identifier.antenna_name,
            },
        }
    )


def register_antenna_routes(
    app, logger, station_suffix, remote_grpc_port, remote_grpc_host
):
    @app.route(
        "/v1/<station_name>/antenna/<antennafield_name>/<antenna_name>", methods=["GET"]
    )
    @grpc_error_handler
    def get_antenna(station_name, antennafield_name, antenna_name):
        """Get Antenna Information
        ---
        parameters:
          - name: station_name
            description : the station_name
            in: path
            type: string
            required: true
          - name: antennafield_name
            in: path
            type: string
            required: true
          - name: antenna_name
            in: path
            type: string
            required: true
        responses:
          200:
            description: Antenna information retrieved successfully
        """
        antenna_request = antenna_pb2.GetAntennaRequest(
            identifier=antenna_pb2.Identifier(
                antennafield_name=antennafield_name,
                antenna_name=antenna_name,
            )
        )

        stub = get_grpc_stub(
            logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
        )
        response = stub.GetAntenna(antenna_request)
        return cast_antennareply_to_json(response), (
            HTTPStatus.OK if response.success else HTTPStatus.BAD_GATEWAY
        )

    @app.route(
        "/v1/<station_name>/antenna/"
        "<antennafield_name>/<antenna_name>"
        "/status/<int:status>",
        methods=["POST"],
    )
    @grpc_error_handler
    def set_antenna_status(station_name, antennafield_name, antenna_name, status):
        """Set Antenna Status
        ---
        parameters:
          - name: station_name
            description : the station_name
            in: path
            type: string
            required: true
          - name: antennafield_name
            in: path
            type: string
            required: true
          - name: antenna_name
            in: path
            type: string
            required: true
          - name: status
            in: path
            type: integer
            enum: [0, 1, 2, 3, 4]
            description: >
            Antenna status values:
            - 0: OK
            - 1: SUSPICIOUS
            - 2: BROKEN
            - 3: BEYOND_REPAIR
            - 4: NOT_AVAILABLE
            required: true
        responses:
          200:
            description: Antenna status updated
        """
        set_antenna_status_request = antenna_pb2.SetAntennaStatusRequest(
            identifier=antenna_pb2.Identifier(
                antennafield_name=antennafield_name,
                antenna_name=antenna_name,
            ),
            antenna_status=status,
        )
        stub = get_grpc_stub(
            logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
        )
        response = stub.SetAntennaStatus(set_antenna_status_request)
        return cast_antennareply_to_json(response), (
            HTTPStatus.OK if response.success else HTTPStatus.BAD_GATEWAY
        )

    @app.route(
        "/v1/<station_name>/antenna/<antennafield_name>/<antenna_name>/use/<int:use>",
        methods=["POST"],
    )
    @grpc_error_handler
    def set_antenna_use(station_name, antennafield_name, antenna_name, use):
        """Set Antenna Use
        ---
        parameters:
          - name: station_name
            in: path
            type: string
            required: true
          - name: antennafield_name
            in: path
            type: string
            required: true
          - name: antenna_name
            in: path
            type: string
            required: true
          - name: use
            in: path
            type: integer
            required: true
            enum: [0, 1, 2]
        responses:
          200:
            description: Antenna use updated
        """
        set_antenna_use_request = antenna_pb2.SetAntennaUseRequest(
            identifier=antenna_pb2.Identifier(
                antennafield_name=antennafield_name,
                antenna_name=antenna_name,
            ),
            antenna_use=use,
        )
        stub = get_grpc_stub(
            logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
        )
        response = stub.SetAntennaUse(set_antenna_use_request)
        return cast_antennareply_to_json(response), (
            HTTPStatus.OK if response.success else HTTPStatus.BAD_GATEWAY
        )
