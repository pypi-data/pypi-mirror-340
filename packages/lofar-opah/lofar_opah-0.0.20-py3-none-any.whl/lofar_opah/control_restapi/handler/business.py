import grpc

# Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0


def get_grpc_channel(
    logger, station_name, station_suffix, remote_grpc_port, remote_grpc_host
):
    """Create a grpc Stub to the station"""

    grpc_endpoint = (
        f"{remote_grpc_host}:{remote_grpc_port}"
        if remote_grpc_host
        else f"{station_name}{station_suffix}:{remote_grpc_port}"
    )
    logger.debug("REST API Will Remotely connect to  %s", grpc_endpoint)
    return grpc.insecure_channel(grpc_endpoint)
