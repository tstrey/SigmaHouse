"""Defines CRUD operations with house models."""
from datetime import datetime
from flask import abort,request


HOUSES = {
    "1337CAFECODE": {
        "unique_id": "1337CAFECODE",
        "ip_address": "192.168.1.42",
        "state": {
            "alarm": False,
            "led": {
                "active": False,
                "timestamp": 0,
            },
            "wall_msg": "",
        },
        "timestamp": 52181,
    },
    "1337C0FFFEEE": {
        "unique_id": "1337C0FFFEEE",
        "ip_address": "192.168.1.24",
        "state": {
            "alarm": False,
            "led": {
                "active": False,
                "timestamp": 0,
            },
            "wall_msg": "",
        },
        "timestamp": 9891,
    },
}


def get_timestamp():
    """Provide human-readable timestamp."""
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def read_all():
    """Get the list of registered houses."""
    return list(HOUSES.values())


def update(house):
    """Register a new house."""
    unique_id = house.get("unique_id")
    ip_address = house.get("ip_address", "")

    if unique_id in HOUSES:
        HOUSES[unique_id] = house
        print(HOUSES[unique_id])
        return HOUSES[unique_id], 200

    else:
        abort(
            407,
            f"House with ID:{unique_id} already exists",
        )


def create(house):
    """Register a new house."""

    unique_id = house.get("unique_id")
    ip_address = house.get("ip_address", "")
    if ip_address == 'TBD':
        ip_address = request.remote_addr
        unique_id = ip_address
    client_ip = request.remote_addr

    if unique_id and unique_id not in HOUSES:
        HOUSES[unique_id] = {
            "unique_id": unique_id,
            "ip_address": ip_address,
            "timestamp": get_timestamp(),
        }

        return HOUSES[unique_id], 201

    else:
        abort(
            406,
            f"House with ID:{unique_id} already exists",
        )
