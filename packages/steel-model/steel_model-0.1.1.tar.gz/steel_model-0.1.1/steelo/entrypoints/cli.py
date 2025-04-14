"""
Command line interface for the steelo package.
"""

import sys
import argparse
from pathlib import Path
import logging

from rich.console import Console

from ..adapters.repositories import InMemoryRepository, JsonRepository, Repository
from ..adapters.dataprocessing.excel_reader import read_plants_into_repository, read_demand_centers_into_repository
from ..adapters.dataprocessing.preprocessing.cost_of_x_data_processing import merge_geographical_data
from ..bootstrap import bootstrap
from ..config import settings
from ..domain.models import Plant
from ..service_layer import get_markers, UnitOfWork
from ..simulation import Simulation, SimulationConfig, SimulationRunner
from ..economic_models import PlantsGoOutOfBusinessOverTime


def show_plants_on_map() -> str:
    console = Console()

    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Show the location of steel plants on a map.")

    # Add the mp3_url positional argument
    default_csv_path = settings.steel_plants_csv
    default_map_path = settings.root / "output" / "steel_plants_map.html"
    parser.add_argument("--use_csv", action="store_true", help="Whether to use csv input or not. Default is False.")
    parser.add_argument(
        "steel_source", type=str, nargs="?", default=str(default_csv_path), help="Path to the steel csv source file."
    )
    default_production_source = settings.hist_production_csv
    parser.add_argument(
        "production_source",
        type=str,
        nargs="?",
        default=str(default_production_source),
        help="Path to the historical production csv source file.",
    )
    default_gravity_distances_source = settings.gravity_distances_csv
    parser.add_argument(
        "gravity_distances",
        type=str,
        nargs="?",
        default=str(default_gravity_distances_source),
        help="Path to the gravity_distances csv source file.",
    )
    default_iron_production_source = settings.reg_hist_production_iron_csv
    parser.add_argument(
        "iron_production",
        type=str,
        nargs="?",
        default=str(default_iron_production_source),
        help="Path to the historical iron production csv source file.",
    )
    default_steel_production_source = settings.reg_hist_production_steel_csv
    parser.add_argument(
        "steel_production",
        type=str,
        nargs="?",
        default=str(default_steel_production_source),
        help="Path to the historical steel production csv source file.",
    )
    parser.add_argument(
        "html_output", type=str, nargs="?", default=str(default_map_path), help="Path to the html map output file."
    )

    # Parse the command-line arguments
    try:
        args = parser.parse_args()
        use_csv = args.use_csv
        if use_csv:
            steel_source = args.steel_source
            settings.steel_plants_csv = Path(steel_source)
            production_source = args.production_source
            settings.hist_production_csv = Path(production_source)
            gravity_distances = args.gravity_distances
            settings.gravity_distances_csv = Path(gravity_distances)
            iron_production = args.iron_production
            settings.reg_hist_production_iron_csv = Path(iron_production)
            steel_production = args.steel_production
            settings.reg_hist_production_steel_csv = Path(steel_production)
        map_path = args.html_output
    except argparse.ArgumentError as e:
        console.print(f"[red]Argument parsing error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error during argument parsing: {e}[/red]")
        sys.exit(1)

    # Start drawing the map
    def draw_the_map(plants) -> str:
        repository = InMemoryRepository()
        for plant in plants:
            repository.plants.add(plant)
        markers = get_markers(repository)

        import folium  # type: ignore

        m = folium.Map(location=[20, 0], zoom_start=2)
        for kwargs in markers:
            marker = folium.Marker(**kwargs)
            marker.add_to(m)

        m.save(map_path)

        return str(map_path)

    def run_simulation() -> list[Plant]:
        repository: Repository
        if use_csv:
            repository = read_plants_into_repository()
        else:
            repository = JsonRepository(settings.sample_plants_json_path)

        economic_model = PlantsGoOutOfBusinessOverTime()
        uow = UnitOfWork(repository=repository)
        bus = bootstrap(uow=uow)

        simulation_service = Simulation(bus=bus, economic_model=economic_model)
        simulation_service.run_simulation()
        return simulation_service.bus.uow.plants.list()

    try:
        console.print("[blue]Starting drawing the map[/blue]")
        # run the simulation
        plants = run_simulation()

        # draw the map
        map_path = draw_the_map(plants)
        console.print(f"[green]Map written to[/green]: {map_path}")
        return "Map successfully drawn!"
    except Exception as e:
        raise e
        # console.print(f"[red]Error drawing the map: {e}[/red]")
        # sys.exit(1)


def show_cost_of_x_on_map() -> str:
    console = Console()

    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Show the cost of debt, equity, and capital.")
    choices = [
        "Cost of debt - renewables",
        "Cost of debt - industrial assets",
        "Cost of equity - renewables",
        "Cost of equity - industrial assets",
        "Cost of capital - renewables",
        "Cost of capital - industrial assets",
    ]
    # Add the options for what to visualize
    parser.add_argument(
        "visualization_type",
        type=str,
        choices=choices,
        help="Type of visualization: 'Cost of debt - renewables','Cost of debt - industrial assets', 'Cost of equity - renewables', 'Cost of equity - industrial assets', 'Cost of capital - renewables', 'Cost of capital - industrial assets'.",
    )

    # Add the csv_source and html_output positional arguments
    default_json_path = settings.cost_of_x_csv
    parser.add_argument(
        "json_source", type=str, nargs="?", default=str(default_json_path), help="Path to the json source file."
    )

    # Parse the command-line arguments
    try:
        args = parser.parse_args()
        visualization_type = args.visualization_type
        json_source = args.json_source
        settings.cost_of_x_csv = Path(json_source)
        default_map_path = settings.root / "output" / f"{visualization_type.replace(' ', '_').lower()}_map.jpeg"
        map_path = default_map_path
    except argparse.ArgumentError as e:
        console.print(f"[red]Argument parsing error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error during argument parsing: {e}[/red]")
        sys.exit(1)

    import geopandas as gpd  # type: ignore
    import pandas as pd
    import matplotlib.pyplot as plt  # type: ignore
    import matplotlib.colors as mcolors  # type: ignore

    # Start drawing the map
    def plot_choropleth_map(geo_df: gpd.GeoDataFrame, value_column: str, cmap: str = "viridis"):
        """
        Plots a choropleth map with optional handling for zero values.

        Parameters:
            geo_df (GeoDataFrame): A GeoDataFrame containing geometry and data.
            value_column (str): The column to use for coloring the map.
            title (str): The title of the map.
            cmap (str): The colormap to use for the choropleth. Default is 'viridis'.
        """
        # Fill missing values and normalize the value range
        geo_df = gpd.GeoDataFrame(geo_df, geometry="geometry")
        norm = mcolors.Normalize(vmin=geo_df[value_column].min(), vmax=geo_df[value_column].max())

        # Create the plot
        fig, ax = plt.subplots(1, 1, figsize=(20, 5))

        # Plot the main choropleth
        geo_df.plot(
            column=value_column,
            ax=ax,
            legend=True,
            cmap=cmap,
            edgecolor="black",
            linewidth=0.5,
            norm=norm,
            missing_kwds={"color": "white"},
        )

        # Add a title and remove axes
        ax.set_title(value_column, fontsize=16)
        ax.axis("off")

        plt.savefig(map_path)
        plt.close(fig)

        return str(map_path)

    try:
        console.print("[blue]Starting drawing the map[/blue]")
        # draw the map based on the visualization type
        data_cost_of_x_df = pd.read_json(json_source)
        geo_cost_of_x_df = merge_geographical_data(data_cost_of_x_df, "Country code")
        map_path = plot_choropleth_map(geo_cost_of_x_df, visualization_type)
        console.print(f"[green]Map written to[/green]: {map_path}")
        return "Map successfully drawn!"
    except Exception as e:
        console.print(f"[red]Error drawing the map: {e}[/red]")
        sys.exit(1)


def recreate_plants_sample_data():
    """
    Recreate the JSON sample plants data from the current CSV file.
    """
    console = Console()
    read_repository = read_plants_into_repository()
    sample_plants_json_path = settings.sample_plants_json_path
    console.print(f"[blue]Writing to[/blue]: {sample_plants_json_path}")
    write_repository = JsonRepository(sample_plants_json_path)
    plants_list = read_repository.plants.list()
    console.print(f"[blue]Number of plants to write[/blue]: {len(plants_list)}")
    write_repository.plants.add_list(plants_list)
    console.print(f"[green]Sample plants data written to[/green]: {sample_plants_json_path}")


def recreate_demand_center_data(repository=None):
    """
    Recreate the JSON sample demand center data from the current CSV file.
    """

    read_repository = read_demand_centers_into_repository(
        demand_excel_path="../data/data_collection_ultimate_steel.xlsx",
        demand_sheet_name="Steel_Demand_Chris Bataille",
        location_csv="../data/countries.csv",
        repository=repository,
    )
    demand_centers_json_path = settings.sample_demand_center_json_path
    write_repository = JsonRepository(demand_centers_json_path)
    write_repository.demand_center.add_list(read_repository.demand_center.list())
    console = Console()
    console.print(f"[green]Sample demand center data written to[/green]: {demand_centers_json_path}")


def run_full_simulation() -> str:
    """
    Run a full simulation from start to end year with the
    configuration provided via command line arguments.
    """
    console = Console()

    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Run a full steel model simulation.")

    # Add the options for the simulation
    parser.add_argument("--start-year", type=int, default=2025, help="The year to start the simulation (default: 2025)")
    parser.add_argument("--end-year", type=int, default=2027, help="The year to end the simulation (default: 2027)")
    parser.add_argument(
        "--plants-json",
        type=str,
        default=None,
        help=f"Path to the plants JSON file (default: {settings.sample_plants_json_path})",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=None,
        help=f"Path for the output JSON file (default: {settings.intermediate_outputs_simulation_run})",
    )
    parser.add_argument(
        "--demand-excel",
        type=str,
        default=None,
        help=f"Path to the demand excel file (default: {settings.demand_center_xlsx})",
    )
    parser.add_argument(
        "--demand-sheet",
        type=str,
        default="Steel_Demand_Chris Bataille",
        help="Sheet name in the demand excel file (default: 'Steel_Demand_Chris Bataille')",
    )
    parser.add_argument(
        "--location-csv",
        type=str,
        default=None,
        help=f"Path to the location CSV file (default: {settings.location_csv})",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Set the logging level (default: WARNING)",
    )

    # Parse the command-line arguments
    try:
        args = parser.parse_args()

        # Convert string paths to Path objects if provided
        plants_json_path = Path(args.plants_json) if args.plants_json else settings.sample_plants_json_path
        output_file = Path(args.output_file) if args.output_file else settings.intermediate_outputs_simulation_run
        demand_excel = Path(args.demand_excel) if args.demand_excel else settings.demand_center_xlsx
        location_csv = Path(args.location_csv) if args.location_csv else settings.location_csv

        # Map log level string to logging constants
        log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        log_level = log_levels[args.log_level]

        # Create the simulation configuration
        config = SimulationConfig(
            plants_json_path=plants_json_path,
            start_year=args.start_year,
            end_year=args.end_year,
            output_file=output_file,
            demand_center_xlsx=demand_excel,
            demand_sheet_name=args.demand_sheet,
            location_csv=location_csv,
            log_level=log_level,
        )

    except argparse.ArgumentError as e:
        console.print(f"[red]Argument parsing error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error during argument parsing: {e}[/red]")
        sys.exit(1)

    # Run the simulation
    try:
        console.print("[blue]Starting simulation[/blue]")
        runner = SimulationRunner(config)
        runner.run()

        if config.output_file:
            console.print(f"[green]Simulation results written to[/green]: {config.output_file}")

        return "Simulation completed successfully!"
    except Exception as e:
        console.print(f"[red]Error during simulation: {e}[/red]")
        sys.exit(1)
