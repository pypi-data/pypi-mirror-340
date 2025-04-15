# Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0
from flask import jsonify
from http import HTTPStatus
from lofar_sid.interface.stationcontrol import antennafield_pb2, antennafield_pb2_grpc
from lofar_opah.control_restapi._decorators import grpc_error_handler
from lofar_opah.control_restapi.handler.business import get_grpc_channel


def get_grpc_stub(
    logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
):
    """Return Antennafield stub"""
    channel = get_grpc_channel(
        logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
    )
    return antennafield_pb2_grpc.AntennafieldStub(channel)


def cast_antennafieldreply_to_json(response):
    """Clear Cast, gets rid of additional grpc fields"""

    return jsonify(
        {
            "success": response.success,
            "exception": response.exception,
            "result": {
                "power_status": response.result.power_status,
            },
            "identifier": {
                "antenna_field_id": response.result.identifier.antenna_field_id
            },
        }
    )


def register_antennafield_routes(
    app, logger, station_suffix, remote_grpc_port, remote_grpc_host
):
    @app.route(
        "/v1/<station_name>/antennafield/<antenna_field_id>/power", methods=["GET"]
    )
    @grpc_error_handler
    def get_antennafield_power(station_name, antenna_field_id):
        """Get Antennafield Information
        ---
        parameters:
          - name: station_name
            description : the station_name
            in: path
            type: string
            required: true
          - name: antenna_field_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Antennafield information retrieved successfully
        """
        antennafield_request = antennafield_pb2.GetAntennafieldRequest(
            identifier=antennafield_pb2.AntennafieldIdentifier(
                antenna_field_id=antenna_field_id,
            )
        )

        stub = get_grpc_stub(
            logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
        )
        response = stub.GetAntennafieldPower(antennafield_request)
        return cast_antennafieldreply_to_json(response), (
            HTTPStatus.OK if response.success else HTTPStatus.BAD_GATEWAY
        )

    @app.route(
        "/v1/<station_name>/antennafield/<antenna_field_id>/power/<int:power_status>",
        methods=["POST"],
    )
    @grpc_error_handler
    def set_antennafield_power_status(station_name, antenna_field_id, power_status):
        """Set Antennafield Power Status
        ---
        parameters:
          - name: station_name
            description : the station_name
            in: path
            type: string
            required: true
          - name: antennafield_id
            in: path
            type: string
            required: true
          - name: power_status
            in: path
            type: integer
            enum: [0, 1]
            description: >
            Power status values:
            - 0: OFF
            - 1: ON
            required: true
        responses:
          200:
            description: Power status updated
        """
        anntennafield_request = antennafield_pb2.SetAntennafieldRequest(
            identifier=antennafield_pb2.AntennafieldIdentifier(
                antenna_field_id=antenna_field_id
            )
        )
        stub = get_grpc_stub(
            logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
        )
        response = stub.SetAntennafieldPower(anntennafield_request)
        return cast_antennafieldreply_to_json(response), (
            HTTPStatus.OK if response.success else HTTPStatus.BAD_GATEWAY
        )
