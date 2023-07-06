from collections import namedtuple

from oracledb import DB_TYPE_CURSOR
from schemas import Designation
from sqlalchemy import Connection

Agent = namedtuple("Agent", ["designation", "code", "phone"])


def fetch_phone_numbers(agent_desg: Designation, db: Connection, hour: int):
    connection = db.connection

    cursor = connection.cursor()
    cursor_result = cursor.callfunc(
        "DEV_ADMIN.ORG_TR_LIC_SMS", DB_TYPE_CURSOR, [agent_desg, hour]
    )
    cursor_result.rowfactory = Agent
    return cursor_result
