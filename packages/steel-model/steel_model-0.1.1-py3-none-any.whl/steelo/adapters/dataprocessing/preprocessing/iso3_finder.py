import pycountry

from geopy import distance  # type: ignore

import reverse_geocoder as rg  # type: ignore


def derive_iso3(lat: float, lon: float, max_distance_km: float = 200) -> str:
    """
    Derive the ISO3 code from latitude and longitude using reverse_geocoder

    Args:
        lat: Latitude (-90 to 90)
        lon: Longitude (-180 to 180)
        max_distance_km: Maximum allowed distance between input and result in km

    Returns:
        ISO3 country code

    Raises:
        ValueError: If coordinates are invalid or result is too far from input
    """
    # Validate coordinate ranges
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError(
            f"Invalid coordinates: ({lat}, {lon}). Latitude must be between -90 and 90, longitude between -180 and 180."
        )

    try:
        result = rg.search((lat, lon), mode=1)

        if not result or len(result) == 0:
            raise ValueError(f"No result found for coordinates ({lat}, {lon}).")

        result_lat, result_lon = float(result[0]["lat"]), float(result[0]["lon"])
        dist = distance.geodesic((lat, lon), (result_lat, result_lon)).kilometers

        # If the result is too far away, it's likely unreliable
        if dist > max_distance_km:
            raise ValueError(
                f"Result is {dist:.1f}km away from input coordinates. "
                f"This exceeds the maximum allowed distance of {max_distance_km}km. "
                f"Input: ({lat}, {lon}), Result: ({result_lat}, {result_lon})"
            )

        country_code = result[0]["cc"]
        country = pycountry.countries.get(alpha_2=country_code)

        if not country:
            raise ValueError(f"Could not find country with code {country_code} from result.")

        return country.alpha_3

    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Error processing coordinates ({lat}, {lon}): {str(e)}")
