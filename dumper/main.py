from datetime import datetime
from typing import Annotated

import typer
from config import ROOT_DIR
from db import engine
from rich.progress import track
from schemas import Designation
from utils import make_file_name, write_csv_file

app = typer.Typer(name="Dumper")


@app.command(short_help="Dump Agents Number by providing Designation & Training Hour")
def export(
    desg: Annotated[Designation, typer.Option()],
    hour: Annotated[int, typer.Option()] = 72,
):
    """
    Export Agents Number by providing Designation and Training Hour.

    Parameters:
    - desg (Designation): The designation of the agents.
    - hour (int): The training hour (default: 72).

    This command exports the numbers of agents based on the provided designation and training hour. It creates a CSV file with the agent numbers in the specified output directory.

    Example usage:
    ```
    $ python main.py export --desg FA --hour 48
    ```

    Output:
    - The command will generate a CSV file with the agent numbers in the output directory.
    - It will print a message to the console confirming the file export.
    """
    file_name = make_file_name(desg, hour)

    today = datetime.today()

    output_dir = ROOT_DIR / "output" / today.strftime("%d-%b-%Y")

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{file_name}_{datetime.today().date()}.csv"

    with engine.connect() as conn:
        write_csv_file(output_file, desg, conn, hour)
        print(f"File: {file_name}.csv has been exported to output dir.")


@app.command(short_help="Dump All Agents Designation Number by providing Traning Hour")
def export_all_desg(hour: Annotated[int, typer.Option()]):
    """
    Export All Agents Designation Number by providing Training Hour.

    Parameters:
    - hour (int): The training hour.

    This command exports the designation numbers of all agents based on the provided training hour. It creates a CSV file for each designation in the specified output directory.

    Example usage:
    ```
    $ python main.py export-all-desg --hour 0 | 36 | 72
    ```

    Output:
    - The command will generate CSV files for each designation in the output directory.
    - It will print the names of the exported files to the console.
    """
    today = datetime.today()

    output_dir = ROOT_DIR / "output" / today.strftime("%d-%b-%Y")

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    with engine.connect() as connection:
        for desg in track(
            Designation.__members__.values(), description="Processing..."
        ):
            file_name = make_file_name(desg, hour=hour)
            output_file = output_dir / f"{file_name}.csv"
            write_csv_file(output_file, desg, connection, hour)
            print(f"File has been Exported: {file_name}.csv")


if __name__ == "__main__":
    app()
