# Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0
from flask import jsonify
from http import HTTPStatus
from lofar_sid.interface.stationcontrol import station_pb2, station_pb2_grpc
from lofar_opah.control_restapi._decorators import grpc_error_handler
from lofar_opah.control_restapi.handler.business import get_grpc_channel


def get_grpc_stub(
    logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
):
    """Return StationStub stub"""
    channel = get_grpc_channel(
        logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
    )
    return station_pb2_grpc.StationStub(channel)


def cast_station_state_reply_to_json(response):
    """Convert StationStateReply to JSON"""
    return jsonify(
        {
            "result": {
                "station_state": response.result.station_state,
            },
        }
    )


def register_station_routes(
    app, logger, station_suffix, remote_grpc_port, remote_grpc_host
):
    @app.route("/v1/<station_name>/station/stationstate", methods=["GET"])
    @grpc_error_handler
    def get_stationstate(station_name):
        """Get station state
        ---
        parameters:
          - name: station_name
            in: path
            type: string
            required: true
        responses:
          200:
            description: Station State
        """
        station_request = station_pb2.GetStationStateRequest()
        stub = get_grpc_stub(
            logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
        )
        response = stub.GetStationState(station_request)
        return cast_station_state_reply_to_json(response), HTTPStatus.OK

    @app.route(
        "/v1/<station_name>/station/stationstate/<int:station_state>", methods=["POST"]
    )
    @grpc_error_handler
    def set_stationstate(station_name, station_state):
        """Set the station state
        ---
        parameters:
          - name: station_name
            in: path
            type: string
            required: true
          - name: station_state
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Station State
        """
        station_request = station_pb2.SetStationStateRequest(
            station_state=station_state
        )
        stub = get_grpc_stub(
            logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
        )
        response_stream = stub.SetStationState(station_request)
        final_response = next(response_stream)  # assuming one response for now
        return cast_station_state_reply_to_json(final_response), HTTPStatus.OK

    @app.route("/v1/<station_name>/station/reset/soft", methods=["POST"])
    @grpc_error_handler
    def soft_station_reset(station_name):
        """Do a soft reset
        ---
        parameters:
          - name: station_name
            in: path
            type: string
            required: true
        responses:
          200:
            description: Station State
        """
        station_request = station_pb2.SoftStationResetRequest()
        stub = get_grpc_stub(
            logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
        )
        response_stream = stub.SoftStationReset(station_request)
        final_response = next(response_stream)
        return cast_station_state_reply_to_json(final_response), HTTPStatus.OK

    @app.route("/v1/<station_name>/station/reset/hard", methods=["POST"])
    @grpc_error_handler
    def hard_station_reset(station_name):
        """Do a hard reset
        ---
        parameters:
          - name: station_name
            in: path
            type: string
            required: true
        responses:
          200:
            description: Station State
        """
        station_request = station_pb2.HardStationResetRequest()
        stub = get_grpc_stub(
            logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
        )
        response_stream = stub.HardStationReset(station_request)
        final_response = next(response_stream)
        return cast_station_state_reply_to_json(final_response), HTTPStatus.OK
