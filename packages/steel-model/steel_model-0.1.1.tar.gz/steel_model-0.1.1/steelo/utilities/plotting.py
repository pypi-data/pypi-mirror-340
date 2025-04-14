from typing import cast

import matplotlib.pyplot as plt
import logging
import cartopy.crs as ccrs  # type: ignore
import cartopy.feature as cfeature  # type: ignore
import geopandas as gpd  # type: ignore
import cartopy.io.shapereader as shpreader  # type: ignore
from cartopy.mpl.geoaxes import GeoAxes  # type: ignore
from folium.map import Figure as FoliumFigure

import pandas as pd
import numpy as np

from matplotlib.figure import Figure

import folium

from ..domain import Volumes, Year
from ..domain.models import SteelAllocations

from ..adapters.repositories.interface import PlantRepository


def plot_cost_curve_per_plant(plants: PlantRepository) -> Figure:
    # Initialize variables for plotting
    current_capacity = 0
    rectangles = []

    # Collect data for rectangle plotting
    for plant in plants.list():
        if hasattr(plant, "average_steel_cost") is False or hasattr(plant, "steel_capacity") is False:
            continue
        width = plant.steel_capacity / 1000000  # Convert to megatonstons
        height = plant.average_steel_cost
        rectangles.append((current_capacity, height, width))
        current_capacity += width

    # Sort rectangles by height (average cost) in ascending order
    rectangles.sort(key=lambda x: x[1])

    # Reset current capacity for sorted rectangles
    current_capacity = 0
    sorted_rectangles = []
    for _, height, width in rectangles:
        sorted_rectangles.append((current_capacity, height, width))
        current_capacity += width

    # Plot the rectangles
    fig, ax = plt.subplots(figsize=(10, 6))
    for x_start, height, width in sorted_rectangles:
        ax.bar(x_start, height, width=width, align="edge", edgecolor="black", color="lightblue")

    # Add labels and grid
    ax.set_xlabel("Cumulative Annual Capacity [megaton per year]", fontsize=12)
    ax.set_ylabel("Cost per Unit [US$/t]", fontsize=12)
    ax.set_title("Cost Curve per Plant", fontsize=14)
    ax.grid(True, linestyle="--", alpha=0.6)

    # Show the plot
    return fig


def plot_steel_cost_curve(curve, demand):
    """
    Plots a steel cost curve (sorted by ascending cost) and indicates the
    marginal producer for a given demand level.

    :param curve: A list of dictionaries of the form
                  [
                    {"cumulative_capacity": float, "production_cost": float},
                    ...
                  ],
                  assumed to be sorted in ascending order of production cost
                  (i.e., a "cost curve").
    :param demand: A float indicating the demanded capacity. The function will
                   highlight the point on the curve where this demand level
                   intersects.
    """

    # Extract x (cumulative capacities) and y (production costs) from the curve
    cumulative_capacities = [point["cumulative_capacity"] for point in curve]
    production_costs = [point["production_cost"] for point in curve]

    # Find maximum capacity to check demand boundaries
    max_capacity = cumulative_capacities[-1] if curve else 0

    # If demand is out of range, we can clip or just note it
    if demand < 0:
        demand = 0
    elif demand > max_capacity:
        print(
            f"Demand ({demand}) exceeds total available capacity ({max_capacity}). "
            "Marginal producer cost will be that of the final producer."
        )
        demand = max_capacity

    # Find the marginal producer:
    # The marginal producer is the first point where cumulative_capacity >= demand
    marginal_producer = None
    for point in curve:
        if point["cumulative_capacity"] >= demand:
            marginal_producer = point
            break

    # Plot the cost curve
    plt.figure(figsize=(8, 5))

    # Often cost curves are visualized as a step plot:
    #   The 'where="post"' makes the step stay at the current y until x changes.
    #   You can also use a simple line plot if you prefer.
    plt.step(cumulative_capacities, production_costs, where="post", label="Cost Curve")

    # Plot a vertical line at the demand level
    plt.axvline(x=demand, color="red", linestyle="--", label="Demand")

    # If we found a valid marginal producer, annotate it
    if marginal_producer:
        marginal_x = demand
        marginal_cost = marginal_producer["production_cost"]

        # A horizontal line at the marginal cost (optional)
        plt.axhline(y=marginal_cost, color="gray", linestyle="--")

        # Mark the intersection
        plt.scatter(marginal_x, marginal_cost, color="red", zorder=5)

        # Add text annotation
        plt.text(
            marginal_x,
            marginal_cost,
            f"  Marginal producer cost = {marginal_cost:.2f}",
            color="red",
            verticalalignment="bottom",
        )

    # Labeling the plot
    plt.title("Steel Cost Curve")
    plt.xlabel("Cumulative Capacity")
    plt.ylabel("Production Cost")
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()


def plot_cost_curve_per_region(plants: PlantRepository) -> Figure:
    # Initialize variables for plotting
    current_capacity = 0
    rectangles = []
    regional_data: dict = {}

    # Collect data for rectangle plotting
    for plant in plants.list():
        if hasattr(plant, "average_steel_cost") is False or hasattr(plant, "steel_capacity") is False:
            continue
        region = plant.location.region
        regional_data[region] = regional_data.get(region, []) + [
            (plant.steel_capacity * plant.average_steel_cost, plant.steel_capacity)
        ]

    for region, data in regional_data.items():
        total_cost = sum([x[0] for x in data])
        total_capacity = sum([x[1] for x in data])
        width = total_capacity / 1000000  # Convert to megatonstons
        height = total_cost / total_capacity
        rectangles.append((current_capacity, height, width))
        current_capacity += total_capacity

    # Reset current capacity for sorted rectangles
    current_capacity = 0
    sorted_rectangles = []
    region_colors = {}
    color_palette = plt.cm.get_cmap("tab20", len(regional_data))

    for idx, (region, data) in enumerate(regional_data.items()):
        total_cost = sum([x[0] for x in data])
        total_capacity = sum([x[1] for x in data])
        width = total_capacity / 1000000  # Convert to megatons
        height = total_cost / total_capacity
        sorted_rectangles.append((current_capacity, height, width, region))
        region_colors[region] = color_palette(idx)
        current_capacity += width

    # Sort rectangles by height (average cost) in ascending order
    sorted_rectangles.sort(key=lambda x: x[1])

    # Sort rectangles by height (average cost) in ascending order
    sorted_rectangles.sort(key=lambda x: x[1])

    # Reset current capacity for sorted rectangles
    current_capacity = 0
    final_rectangles = []
    for x_start, height, width, region in sorted_rectangles:
        final_rectangles.append((current_capacity, height, width, region))
        current_capacity += width

    # Plot the rectangles
    fig, ax = plt.subplots(figsize=(10, 6))
    for x_start, height, width, region in final_rectangles:
        ax.bar(x_start, height, width=width, align="edge", edgecolor="black", color=region_colors[region], label=region)

    # Add legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), title="Region")

    # Add labels and grid
    ax.set_xlabel("Cumulative Annual Capacity [megaton per year]", fontsize=12)
    ax.set_ylabel("Cost per Unit [US$/t]", fontsize=12)
    ax.set_title("Cost Curve per Region", fontsize=14)
    ax.grid(True, linestyle="--", alpha=0.6)

    # Show the plot
    return fig


# TODO: Align with Marcus & Shajee on colours and style
def plot_global_heatmap_per_country(
    df: pd.DataFrame,
    var_name: str,
    title: str,
    colormap_type: str = "continous_high_best",
    outlier_treatment: bool = False,
    outlier_side="both",
) -> None:
    """
    Reads in global country level data, converts the country name to the corresponding geometry and plots a global heatmap
    of a certain variable per country. Missing values (and outliers, if applicable) are hatched.
        Inputs:
            - df: DataFrame with the data to plot. Must contain a "Country" column and a column "var_name" with the variable to plot (at least).
            - var_name: Name of the column in df with the variable to plot.
            - title: Title of the plot.
            - colormap_type: Type of colormap to use. Options: "divergent_low_best", "divergent_high_best", "continuous_low_best", "continuous_high_best".
            - outlier_treatment: If True, outliers are set to nan to avoid distorting the color scale.
            - outlier_side: If "both", outliers on both sides are set to nan. If "high"/"low", only high/low outliers are set to nan.
    """

    # Load world geometries from Cartopy's naturalearth_shapefile
    shapefile = shpreader.natural_earth(resolution="110m", category="cultural", name="admin_0_countries")
    reader = shpreader.Reader(shapefile)
    world = reader.records()
    countries_geom = {record.attributes["NAME"]: record.geometry for record in world}
    countries_geom_df = pd.DataFrame(list(countries_geom.items()), columns=["Country", "Geometry"]).set_index("Country")

    # Create a GeoDataFrame
    for i in countries_geom_df.index:
        if i not in df.index:
            logging.warning(f"Warning: {i} not found in df")
    df_with_geom = df.merge(countries_geom_df, left_index=True, right_index=True)
    gdf = gpd.GeoDataFrame(df_with_geom, geometry="Geometry")
    # Rename the column which contains var_name to var_name
    gdf = gdf.rename(columns={col: var_name for col in gdf.columns if str(var_name) in str(col)})

    # Set outliers to nan to avoid distorting the color scale
    if outlier_treatment:
        mean = gdf[var_name].mean()
        if outlier_side in ["both", "high"]:
            gdf.loc[gdf[var_name] > 2 * mean, var_name] = np.nan
        if outlier_side in ["both", "low"]:
            gdf.loc[gdf[var_name] < 0.5 * mean, var_name] = np.nan

    # Set colormap
    if "divergent" in colormap_type:
        colormap = "RdBu"
    elif "continuous" in colormap_type:
        colormap = "Blues"
    if "low_best" in colormap_type:
        colormap = colormap + "_r"

    # Plot heatmap
    fig, ax = plt.subplots(1, 1, figsize=(15, 10), subplot_kw={"projection": ccrs.PlateCarree()})
    assert isinstance(ax, GeoAxes)
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=":")
    ax.add_feature(cfeature.LAND, edgecolor="black")
    gdf.plot(
        ax=ax,
        column=var_name,
        cmap=colormap,
        missing_kwds={
            "color": "none",
            "edgecolor": "black",
            "alpha": 0.5,
            "hatch": "//////",
            "label": "Missing values",
        },
    )
    sm = plt.cm.ScalarMappable(cmap=colormap, norm=plt.Normalize(vmin=gdf[var_name].min(), vmax=gdf[var_name].max()))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation="horizontal", pad=0.05, shrink=0.5, label=var_name)
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(var_name, fontsize=18)
    ax.set_title(title, fontsize=20)
    fig.tight_layout()
    plt.show()
    plt.close()


#######################
#######################
#######################


def plot_allocation_on_map_2(allocation: SteelAllocations, chosen_year: Year):
    """
    allocation.allocations is assumed to be a dictionary keyed by
    (plant, furnace_group, demand_center) -> volume.
    Each 'plant' and 'demand_center' has an 'id' (here used as plant.plant_id,
    demand_center.demand_center_id) and a 'location' with 'lat' and 'lon'.
    The 'furnace_group' has a 'technology' with a 'name'.
    """
    # 1) Create the base map
    m = folium.Map(location=[0, 0], zoom_start=2)

    # 2) Separate arcs by technology (so each tech can be toggled as a separate layer)
    arcs_by_tech: dict[str, list[dict]] = {}
    max_allocation = max(allocation.allocations.values())

    # Predefine known technologies (or create them on the fly)
    known_techs = ["BOF", "EAF", "OHF", "other", "unknown"]
    for tech in known_techs:
        arcs_by_tech[tech] = []

    # 3) Build a GeoJSON Feature for each arc
    for (plant, furnace_group, demand_center), volume in allocation.allocations.items():
        furnace_group = plant.get_furnace_group(furnace_group.furnace_group_id)
        tech_name = furnace_group.technology.name
        if tech_name not in arcs_by_tech:
            arcs_by_tech[tech_name] = []

        normalized_weight = (volume / max_allocation) * 10
        color_map = {
            "BOF": "black",
            "EAF": "darkgreen",
            "OHF": "pink",
            "other": "red",
            "unknown": "red",
        }
        default_color = color_map.get(tech_name, "blue")

        # Build a GeoJSON Feature (LineString)
        # Note we now add "volume" to properties for the tooltip
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [plant.location.lon, plant.location.lat],
                    [demand_center.center_of_gravity.lon, demand_center.center_of_gravity.lat],
                ],
            },
            "properties": {
                "start_node_id": plant.plant_id,  # ID of the plant
                "end_node_id": demand_center.demand_center_id,  # ID of the demand center
                "default_color": default_color,
                "default_weight": normalized_weight,
                "tech_name": tech_name,
                "volume": volume,  # <-- Add the volume here
            },
        }
        arcs_by_tech[tech_name].append(feature)

    # 4) Style function for arcs
    def style_function(feature):
        """Style each arc based on its default properties."""
        return {
            "color": feature["properties"]["default_color"],
            "weight": feature["properties"]["default_weight"] * 3,  # Multiply by 6 for a thick base
            "opacity": 1.0,
        }

    # 5) Helper function to add a GeoJson layer and register it
    def add_geojson_layer(map_obj, geojson_features, layer_name):
        """Create a GeoJson layer and register it in window.arcsLayers."""
        if not geojson_features:
            return None
        geojson_data = {"type": "FeatureCollection", "features": geojson_features}

        # Attach a tooltip that displays the "volume" property on hover
        layer = folium.GeoJson(
            data=geojson_data,
            style_function=style_function,
            name=layer_name,
            tooltip=folium.GeoJsonTooltip(fields=["volume"], aliases=["Volume: "]),
        )
        layer.add_to(map_obj)

        # Inject a small <script> to push this layer into window.arcsLayers
        script_str = f"""
        <script>
        (function() {{
            // Once the layer is added, push it into window.arcsLayers
            var gLayer = {layer.get_name()};
            gLayer.on('add', function(e) {{
                console.log("Layer added to arcsLayers:", gLayer);
                if (!window.arcsLayers) {{
                    window.arcsLayers = [];
                }}
                window.arcsLayers.push(gLayer);
            }});
        }})();
        </script>
        """
        layer.add_child(folium.Element(script_str))
        return layer

    # Create one layer per technology
    for tech_name, features in arcs_by_tech.items():
        add_geojson_layer(m, features, tech_name)

    # 6) Add Markers (plants & demand centers)
    #    We'll use folium.Html(..., script=True) + folium.Popup to preserve <button onclick=...>
    marker_fg = folium.FeatureGroup(name="Nodes", show=True)
    marker_fg.add_to(m)

    # Ensure marker_fg is properly referenced in the script_zoom
    script_zoom = f"""
    <script>
    (function() {{
      var markerLayer = {marker_fg.get_name()};
      var myMap = {m.get_name()};  // The main Leaflet map object

      // On zoomend, check the current zoom level.
      myMap.on('zoomend', function() {{
        var currentZoom = myMap.getZoom();
        // If zoom < 7, remove the layer group; else add it back
        if (currentZoom < 7) {{
          myMap.removeLayer(markerLayer);
        }} else {{
          myMap.addLayer(markerLayer);
        }}
      }});

      // Optionally, run it once at startup if you want them hidden initially when zoom < 7
      var initialZoom = myMap.getZoom();
      if (initialZoom < 7) {{
        myMap.removeLayer(markerLayer);
      }}
    }})();
    </script>
    """
    root: FoliumFigure = cast(FoliumFigure, m.get_root())
    root.html.add_child(folium.Element(script_zoom))
    marker_fg.add_to(m)

    for (plant, furnace_group, demand_center), _ in allocation.allocations.items():
        # Example: Summarize capacities by technology
        plant_capacity_by_tech = {}
        for fg in plant.furnace_groups:
            if fg.technology.product != "Steel":  # Skip non-steel technologies
                continue
            if fg.technology.name not in plant_capacity_by_tech:
                plant_capacity_by_tech[fg.technology.name] = fg.capacity
            else:
                plant_capacity_by_tech[fg.technology.name] = Volumes(
                    plant_capacity_by_tech[fg.technology.name] + fg.capacity
                )

        # Build plant popup HTML
        tech_capacity_str = ""
        for tname in plant_capacity_by_tech:
            tech_capacity_str += f"{tname}: {plant_capacity_by_tech[tname]:,.2f} t <br/>"
            tech_capacity_str += f"{tname}: {plant_capacity_by_tech[tname]:,.2f} t <br/>"
        plant_html_str = f"""
        <b>Plant: {plant.plant_id}</b><br/>
        {tech_capacity_str}
        <button onclick="window.toggleNode('{plant.plant_id}')">
            Toggle Node
        </button>
        """
        plant_html = folium.Html(plant_html_str, script=True)
        plant_popup = folium.Popup(plant_html, max_width=250)
        folium.Marker(
            location=[plant.location.lat, plant.location.lon],
            popup=plant_popup,
            icon=folium.Icon(icon="industry", color="blue", prefix="fa"),
        ).add_to(marker_fg)

        # Demand center marker
        demand_html_str = f"""
        <b>Demand Center: {demand_center.demand_center_id}</b><br/>
        Demand: {demand_center.demand_by_year[chosen_year]:,.2f} t</br>
        Demand: {demand_center.demand_by_year[chosen_year]:,.2f} t</br>
        <button onclick="window.toggleNode('{demand_center.demand_center_id}')">
            Toggle Node
        </button>
        """
        demand_html = folium.Html(demand_html_str, script=True)
        demand_popup = folium.Popup(demand_html, max_width=250)
        folium.Marker(
            location=[demand_center.center_of_gravity.lat, demand_center.center_of_gravity.lon],
            popup=demand_popup,
            icon=folium.Icon(icon="cart-shopping", color="red", prefix="fa"),
        ).add_to(marker_fg)

    marker_fg.add_to(m)

    # 7) Inject custom JavaScript for node toggling, highlight, and refresh
    custom_js = """
    <script>
    // Global arrays
    if (!window.selectedNodes) {
        window.selectedNodes = [];
    }
    if (!window.arcsLayers) {
        window.arcsLayers = [];
    }

    window.toggleNode = function(nodeId) {
        console.log("toggleNode called for node:", nodeId);
        var idx = window.selectedNodes.indexOf(nodeId);
        if (idx >= 0) {
            // Node is already selected, remove it
            window.selectedNodes.splice(idx, 1);
        } else {
            // Otherwise, add it
            window.selectedNodes.push(nodeId);
        }
        window.updateArcStyles();
    }

    window.clearSelections = function() {
        window.selectedNodes = [];
        window.updateArcStyles();
    }

    window.updateArcStyles = function() {
        console.log("updateArcStyles called. SelectedNodes:", window.selectedNodes);
        if (!window.arcsLayers) return;

        var noSelection = (window.selectedNodes.length === 0);

        window.arcsLayers.forEach(function(geoJsonLayer) {
            geoJsonLayer.eachLayer(function(layer) {
                var props = layer.feature && layer.feature.properties;
                if (!props) return;

                var startId = props.start_node_id;
                var endId   = props.end_node_id;
                var defColor = props.default_color;
                var defWeight = props.default_weight;

                // Check if the arc is connected to any selected node
                var connected = false;
                for (var i=0; i < window.selectedNodes.length; i++) {
                    var selNode = window.selectedNodes[i];
                    if (startId === selNode || endId === selNode) {
                        connected = true;
                        break;
                    }
                }

                if (noSelection) {
                    // Revert to normal
                    layer.setStyle({
                        color: defColor,
                        weight: defWeight,
                        opacity: 0.6
                    });
                } else if (connected) {
                    // Highlight
                    layer.setStyle({
                        color: defColor,
                        weight: defWeight * 3,
                        opacity: 1.0
                    });
                } else {
                    // Fade
                    layer.setStyle({
                        color: "gray",
                        weight: defWeight,
                        opacity: 0.3
                    });
                }
            });
        });
    }
    </script>
    """
    root.html.add_child(folium.Element(custom_js))

    # 8) Add a “Refresh” button in a fixed position on the map
    refresh_button_html = """
    <div style="
        position: fixed;
        top: 10px;
        left: 50px;
        z-index: 9999;
        background-color: white;
        padding: 5px 10px;
        border: 2px solid grey;
    ">
        <button onclick="window.clearSelections()">Refresh Highlight</button>
    </div>
    """
    root.html.add_child(folium.Element(refresh_button_html))

    script_zoom = f"""
    <script>
    (function() {{
      var markerLayer = {marker_fg.get_name()};
      var myMap = {m.get_name()};  // The main Leaflet map object

      // On zoomend, check the current zoom level.
      myMap.on('zoomend', function() {{
        var currentZoom = myMap.getZoom();
        // If zoom < 7, remove the layer group; else add it back
        if (currentZoom < 7) {{
          myMap.removeLayer(markerLayer);
        }} else {{
          myMap.addLayer(markerLayer);
        }}
      }});

      // Optionally, run it once at startup if you want them hidden initially when zoom < 7
      var initialZoom = myMap.getZoom();
      if (initialZoom < 7) {{
        myMap.removeLayer(markerLayer);
      }}
    }})();
    </script>
    """

    # 5. Add the JS to the final HTML
    root.html.add_child(folium.Element(script_zoom))

    # 9) Add LayerControl so user can toggle each technology layer
    folium.LayerControl().add_to(m)

    # Finally return the map
    return m


##########################################
##########################################


# def build_dash_map_app(allocation, chosen_year: int = 2025):
#     """
#     Build a Dash Leaflet app that replicates (most of) the Folium functionality
#     from `plot_allocation_on_map_2`.

#     :param allocation: An object with .allocations (dict) keyed by
#                        (plant, furnace_group, demand_center) -> volume
#                        and presumably other info about plants/demand centers.
#     :param chosen_year: Which year's demand to display.
#     :return: dash.Dash app instance (not yet run).
#     """

#     # Create the Dash app
#     app = dash.Dash(__name__)

#     # -------------------------------------------------
#     # 1) Build arcs_by_tech
#     # -------------------------------------------------
#     arcs_by_tech = {}
#     known_techs = ["BOF", "EAF", "OHF", "other", "unknown"]

#     if allocation.allocations:
#         max_allocation = max(allocation.allocations.values())
#     else:
#         max_allocation = 1.0

#     # Initialize each known tech
#     for tech in known_techs:
#         arcs_by_tech[tech] = []

#     # Color mapping
#     color_map = {
#         "BOF": "black",
#         "EAF": "darkgreen",
#         "OHF": "pink",
#         "other": "red",
#         "unknown": "red",
#     }

#     # Populate arcs_by_tech
#     for (plant, furnace_group, demand_center), volume in allocation.allocations.items():
#         tech_name = furnace_group.technology.name
#         if tech_name not in arcs_by_tech:
#             arcs_by_tech[tech_name] = []

#         normalized_weight = (volume / max_allocation) * 3  # scale from 0..3
#         default_color = color_map.get(tech_name, "blue")

#         feature = {
#             "type": "Feature",
#             "geometry": {
#                 "type": "LineString",
#                 "coordinates": [
#                     [plant.location.lon, plant.location.lat],
#                     [demand_center.center_of_gravity.lon, demand_center.center_of_gravity.lat],
#                 ],
#             },
#             "properties": {
#                 "start_node_id": plant.plant_id,
#                 "end_node_id": demand_center.demand_center_id,
#                 "default_color": default_color,
#                 "default_weight": normalized_weight,
#                 "tech_name": tech_name,
#                 "volume": volume,
#                 "arrow": True,  # Indicate that this feature should be rendered as an arrow
#             },
#         }
#         arcs_by_tech[tech_name].append(feature)

#     # -------------------------------------------------
#     # 2) Build marker layer for plants and demand centers
#     # -------------------------------------------------
#     marker_features = []

#     def plant_to_feature(plant):
#         # Summarize capacities
#         tech_capacity_str = []
#         for fg in plant.furnace_groups:
#             if fg.technology.product == "Steel":  # skip if not steel
#                 tech_capacity_str.append(f"{fg.technology.name}: {fg.capacity:.2f} Mtpa")
#         popup_str = f"Plant: {plant.plant_id}<br>" + "<br>".join(tech_capacity_str)

#         return {
#             "type": "Feature",
#             "geometry": {"type": "Point", "coordinates": [plant.location.lon, plant.location.lat]},
#             "properties": {
#                 "node_id": plant.plant_id,
#                 "popup": popup_str,
#                 "iconColor": "blue",
#             },
#         }

#     def dc_to_feature(demand_center, year):
#         popup_str = (
#             f"Demand Center: {demand_center.demand_center_id}<br>" f"Demand: {demand_center.demand[year]:,.2f} Mt"
#         )
#         return {
#             "type": "Feature",
#             "geometry": {
#                 "type": "Point",
#                 "coordinates": [demand_center.center_of_gravity.lon, demand_center.center_of_gravity.lat],
#             },
#             "properties": {
#                 "node_id": demand_center.demand_center_id,
#                 "popup": popup_str,
#                 "iconColor": "red",
#             },
#         }

#     # Gather unique (plant, demand_center) from the allocation
#     for (plant, furnace_group, demand_center), _ in allocation.allocations.items():
#         marker_features.append(plant_to_feature(plant))
#         marker_features.append(dc_to_feature(demand_center, chosen_year))

#     marker_collection = {"type": "FeatureCollection", "features": marker_features}

#     # -------------------------------------------------
#     # 3) Define style functions
#     # -------------------------------------------------
#     def style_arcs(feature):
#         """Default style for arcs (when no highlight)."""
#         return {
#             "color": feature["properties"]["default_color"],
#             "weight": feature["properties"]["default_weight"],
#             "opacity": 0.6,
#         }

#     def style_markers(feature):
#         """Basic circleMarker style for plants/demand centers."""
#         color = feature["properties"].get("iconColor", "blue")
#         return {
#             "color": color,
#             "fillColor": color,
#             "fillOpacity": 1.0,
#             "radius": 5,
#         }

#     # -------------------------------------------------
#     # 4) Build Overlays for each technology
#     # -------------------------------------------------
#     tech_overlays = []
#     for tech_name, features in arcs_by_tech.items():
#         if not features:
#             continue
#         geojson_data = {"type": "FeatureCollection", "features": features}
#         overlay = dl.Overlay(
#             dl.GeoJSON(
#                 id=f"{tech_name}-layer",
#                 data=geojson_data,
#                 hoverStyle={"weight": 4, "color": "#666", "dashArray": ""},
#                 options=dict(interactive=True),
#                 # style=style_arcs,
#             ),
#             name=tech_name,
#             checked=True,
#         )
#         tech_overlays.append(overlay)

#     # Single marker overlay for both plants & demand centers
#     markers_overlay = dl.Overlay(
#         dl.GeoJSON(
#             id="markers-layer",
#             data=marker_collection,
#             options=dict(
#                 pointToLayer=assign(
#                     """function(feature, latlng) {
#                 return L.circleMarker(latlng);
#             }"""
#                 )
#             ),
#             # style=style_markers,
#         ),
#         name="Nodes",
#         checked=True,
#     )

#     # -------------------------------------------------
#     # 5) Build the Dash layout
#     # -------------------------------------------------
#     the_map = dl.Map(
#         center=[0, 0],
#         zoom=2,
#         children=[
#             dl.LayersControl(
#                 [dl.BaseLayer(dl.TileLayer(), name="Base", checked=True)] + tech_overlays + [markers_overlay],
#                 id="layers-control",
#             ),
#             dl.ScaleControl(imperial=False, position="bottomleft"),
#         ],
#         style={"width": "100%", "height": "80vh"},
#         id="main-map",
#     )

#     app.layout = html.Div(
#         [
#             html.H3("Dash Leaflet Steel Allocation Map"),
#             html.Button("Refresh Highlight", id="btn-refresh", n_clicks=0),
#             dcc.Store(id="selected-nodes", data=[]),  # holds array of nodeIds
#             the_map,
#         ]
#     )

#     # -------------------------------------------------
#     # 6) Dash callbacks
#     # -------------------------------------------------

#     # (A) Toggle node selection when a user clicks a marker or an arc
#     # In your real code, add more layers for each tech if needed
#     # input_list = [
#     #    Input("markers-layer", "click_feature"),
#     #    Input("BOF-layer", "click_feature"),
#     #    Input("EAF-layer", "click_feature"),
#     #    # Add others if you have them: OHF-layer, ...
#     # ]

#     @app.callback(
#         Output("selected-nodes", "data"),
#         [
#             Input("markers-layer", "click_feature"),
#             Input("BOF-layer", "click_feature"),
#             Input("EAF-layer", "click_feature"),
#             Input("btn-refresh", "n_clicks"),
#         ],
#         State("selected-nodes", "data"),
#     )
#     def toggle_or_refresh(marker_click, bof_click, eaf_click, refresh_click, selected_nodes):
#         ctx = dash.callback_context
#         if not ctx.triggered:
#             return selected_nodes

#         # figure out which input triggered
#         trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

#         if trigger_id == "btn-refresh":
#             # user clicked the refresh button
#             return []

#         # otherwise, check for arc/marker clicks:
#         if trigger_id == "markers-layer" and marker_click:
#             node_id = marker_click["properties"]["node_id"]
#         elif trigger_id == "BOF-layer" and bof_click:
#             node_id = bof_click["properties"].get("start_node_id") or bof_click["properties"].get("end_node_id")
#         elif trigger_id == "EAF-layer" and eaf_click:
#             node_id = eaf_click["properties"].get("start_node_id") or eaf_click["properties"].get("end_node_id")
#         else:
#             node_id = None

#         if not node_id:
#             return selected_nodes

#         # toggle logic
#         if node_id in selected_nodes:
#             return [nid for nid in selected_nodes if nid != node_id]
#         else:
#             return selected_nodes + [node_id]

#     # (C) Re-style arcs based on selected nodes
#     def highlight_arcs(feature, selected_nodes_list):
#         props = feature["properties"]
#         start_id = props["start_node_id"]
#         end_id = props["end_node_id"]
#         def_color = props["default_color"]
#         def_weight = props["default_weight"]

#         connected = (start_id in selected_nodes_list) or (end_id in selected_nodes_list)
#         if not selected_nodes_list:
#             return {"color": def_color, "weight": def_weight, "opacity": 0.6}
#         elif connected:
#             return {"color": def_color, "weight": def_weight * 3, "opacity": 1.0}
#         else:
#             return {"color": "gray", "weight": def_weight, "opacity": 0.3}

#     def update_geojson_data(original_data, selected_nodes_list):
#         """Return a copy with updated 'style' for each feature."""
#         if not original_data:
#             return {}
#         import copy

#         new_data = copy.deepcopy(original_data)
#         for f in new_data.get("features", []):
#             f["style"] = highlight_arcs(f, selected_nodes_list)
#         return new_data

#     @app.callback(
#         [
#             Output("BOF-layer", "data"),
#             Output("EAF-layer", "data"),
#             # Add more if you have OHF-layer, etc.
#         ],
#         Input("selected-nodes", "data"),
#         [
#             State("BOF-layer", "data"),
#             State("EAF-layer", "data"),
#             # ...
#         ],
#     )
#     def style_arcs_layers(selected_nodes_list, bof_data, eaf_data):
#         bof_out = update_geojson_data(bof_data, selected_nodes_list)
#         eaf_out = update_geojson_data(eaf_data, selected_nodes_list)
#         return (bof_out, eaf_out)
#         # Add more returns if you have more layers.

#     # (D) Optionally hide markers if zoom < 7
#     # @app.callback(
#     #    Output("markers-layer", "data"),
#     #    Input("main-map", "viewport"),
#     #    State("markers-layer", "data"),
#     # )
#     # def hide_markers_on_zoom(viewport, orig_data):
#     #    zoom = viewport.get("zoom", 2)
#     # If we are below zoom 7, return empty data
#     #    if zoom < 7:
#     #        return {"type": "FeatureCollection", "features": []}
#     #    else:
#     #        return orig_data
#     return app
