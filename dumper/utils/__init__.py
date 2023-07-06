import csv

from query import fetch_phone_numbers
from schemas import Designation
from sqlalchemy import Connection


def make_file_name(desg: Designation, hour: int = 0) -> str:
    def put_hour(desg: Designation, hour: int) -> str:
        return f"{desg.value}_{hour}H_Traning_Not_Completed"

    if hour:
        file_name = put_hour(desg, hour)
    else:
        file_name = f"{desg.value}_License_Expired"
    return file_name


def write_csv_file(file_path, desg: Designation, db: Connection, hour: int):
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["mobile"])
        for agent in fetch_phone_numbers(agent_desg=desg, db=db, hour=hour):
            writer.writerow([agent.phone])
