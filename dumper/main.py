from datetime import datetime
from typing import Annotated

import typer
from config import ROOT_DIR
from db import engine
from schemas import Designation
from utils import make_file_name, write_csv_file

app = typer.Typer(name="Dumper")


@app.command()
def export(
    desg: Annotated[Designation, typer.Option()],
    hour: Annotated[int, typer.Option()] = 72,
):
    file_name = make_file_name(desg, hour)

    today = datetime.today()

    output_dir = ROOT_DIR / "output" / today.strftime("%d-%b-%Y")

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{file_name}_{datetime.today().date()}.csv"

    with engine.connect() as conn:
        write_csv_file(output_file, desg, conn, hour)
        print(f"File: {file_name}.csv has been exported to output dir.")


@app.command()
def export_all_desg(hour: Annotated[int, typer.Option()]):
    today = datetime.today()

    output_dir = ROOT_DIR / "output" / today.strftime("%d-%b-%Y")

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    with engine.connect() as connection:
        for desg in Designation.__members__.values():
            file_name = make_file_name(desg, hour=hour)
            output_file = output_dir / f"{file_name}.csv"
            write_csv_file(output_file, desg, connection, hour)
            print(f"File has been Exported: {file_name}.csv")


if __name__ == "__main__":
    app()
