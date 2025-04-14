from typing import Callable

import numpy as np
import geopandas as gpd  # type: ignore
import shapely.geometry as shp_geom
import osmnx as ox
from sklearn.preprocessing import MinMaxScaler  # type: ignore


class GeoSpatialAdapter:
    @staticmethod
    def get_country_boundary(country_name: str) -> gpd.GeoDataFrame:
        boundary = ox.geocode_to_gdf(country_name)
        return boundary.to_crs("EPSG:4326")

    @staticmethod
    def create_grid(boundary: gpd.GeoDataFrame, cell_size: float) -> list[dict[str, float]]:
        minx, miny, maxx, maxy = boundary.total_bounds

        # Use numpy.arange to handle floating-point cell sizes
        x_coords = np.arange(minx, maxx, cell_size)
        y_coords = np.arange(miny, maxy, cell_size)

        grid_polygons = [shp_geom.box(x, y, x + cell_size, y + cell_size) for x in x_coords for y in y_coords]
        grid = gpd.GeoDataFrame({"geometry": grid_polygons}, crs="EPSG:4326")

        # Ensure valid intersection
        clipped_grid = gpd.overlay(grid, boundary, how="intersection")
        clipped_grid = clipped_grid[clipped_grid.is_valid]  # Filter invalid geometries

        result = []
        for geometry in clipped_grid.geometry:
            if geometry.is_empty:  # Skip empty geometries
                continue
            bounds = geometry.bounds  # Extract numeric bounds directly
            result.append(
                {
                    "geometry": geometry,
                    "minx": float(bounds[0]),
                    "miny": float(bounds[1]),
                    "maxx": float(bounds[2]),
                    "maxy": float(bounds[3]),
                }
            )
        return result

    @staticmethod
    def compute_distances(
        grid: list[dict[str, float]], infrastructure: dict[str, gpd.GeoDataFrame]
    ) -> list[dict[str, float]]:
        for infra_type, gdf in infrastructure.items():
            # Re-project the infrastructure to a suitable CRS (e.g., EPSG:3857 for meters)
            projected_gdf = gdf.to_crs("EPSG:3857")

            for row in grid:
                # Re-project the grid point to match the projected CRS
                point = shp_geom.Point((row["minx"], row["miny"]))
                projected_point = gpd.GeoSeries([point], crs="EPSG:4326").to_crs("EPSG:3857").iloc[0]

                # Calculate distance in meters
                row[f"distance_to_{infra_type}_meters"] = projected_gdf.geometry.distance(projected_point).min()

        return grid

    @staticmethod
    def get_scaler() -> Callable[[list[list[float]]], list[list[float]]]:
        """
        Provide a scaling function using scikit-learn's MinMaxScaler.

        Returns:
            Callable: A scaling function that can be used in the domain.
        """
        scaler = MinMaxScaler()

        def scale(data: list[list[float]]) -> list[list[float]]:
            return scaler.fit_transform(data).tolist()

        return scale
