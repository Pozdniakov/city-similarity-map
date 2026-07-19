"""Curated list of major world cities (~124, metro population roughly >1M,
globally prominent), grouped by region.

Each entry: (display_name, region, extra_token_candidates).
Token candidates are tried in order against the GoogleNews word2vec vocabulary;
auto-generated variants (underscored display name, diacritics stripped) are
appended by the extractor, so extra candidates are only listed where the
vocabulary token differs from the obvious form (e.g. "Kiev" for Kyiv in the
2013-era GoogleNews corpus).
"""

CITIES = [
    # --- North America ---
    ("New York", "North America", ["New_York_City", "New_York"]),
    ("Los Angeles", "North America", []),
    ("Chicago", "North America", []),
    ("Houston", "North America", []),
    ("Phoenix", "North America", []),
    ("Philadelphia", "North America", []),
    ("San Francisco", "North America", []),
    ("Boston", "North America", []),
    ("Seattle", "North America", []),
    ("Atlanta", "North America", []),
    ("Dallas", "North America", []),
    ("Denver", "North America", []),
    ("Miami", "North America", []),
    ("Washington DC", "North America", ["Washington_DC", "Washington_D.C.", "Washington"]),
    ("Toronto", "North America", []),
    ("Montreal", "North America", []),
    ("Vancouver", "North America", []),
    # no Mexico_City token exists, so this falls through to COMPOSE_FALLBACK.
    # The all-caps dateline token MEXICO_CITY was tried and rejected: its
    # neighbor *ranking* is cleaner, but dateline-register cosines are
    # uniformly depressed (max 0.44), so metric MDS exiles the city to the map
    # periphery instead of placing it beside Monterrey/Guadalajara
    ("Mexico City", "North America", ["Mexico_City"]),
    ("Guadalajara", "North America", []),
    ("Monterrey", "North America", []),
    ("Havana", "North America", []),

    # --- South America ---
    ("Sao Paulo", "South America", ["Sao_Paulo", "São_Paulo"]),
    ("Rio de Janeiro", "South America", ["Rio_de_Janeiro", "Rio"]),
    ("Brasilia", "South America", ["Brasilia", "Brasília"]),
    ("Buenos Aires", "South America", []),
    ("Lima", "South America", []),
    ("Bogota", "South America", ["Bogota", "Bogotá"]),
    ("Medellin", "South America", ["Medellin", "Medellín"]),
    ("Santiago", "South America", []),
    ("Caracas", "South America", []),
    ("Quito", "South America", []),
    ("Montevideo", "South America", []),

    # --- Europe ---
    ("London", "Europe", []),
    ("Paris", "Europe", []),
    ("Berlin", "Europe", []),
    ("Madrid", "Europe", []),
    ("Barcelona", "Europe", []),
    ("Rome", "Europe", []),
    ("Milan", "Europe", []),
    ("Amsterdam", "Europe", []),
    ("Brussels", "Europe", []),
    ("Vienna", "Europe", []),
    ("Munich", "Europe", []),
    ("Zurich", "Europe", []),
    ("Prague", "Europe", []),
    ("Warsaw", "Europe", []),
    ("Budapest", "Europe", []),
    ("Bucharest", "Europe", []),
    ("Athens", "Europe", []),
    ("Stockholm", "Europe", []),
    ("Copenhagen", "Europe", []),
    ("Dublin", "Europe", []),
    ("Lisbon", "Europe", []),
    ("Kyiv", "Europe", ["Kyiv", "Kiev"]),
    ("Moscow", "Europe", []),
    # Saint_Petersburg first: the more frequent St._Petersburg token is dominated
    # by St. Petersburg, Florida (sim to Tampa 0.68 vs Moscow 0.60)
    ("St Petersburg", "Europe", ["Saint_Petersburg", "St._Petersburg", "St_Petersburg"]),

    # --- Middle East & North Africa ---
    ("Istanbul", "Middle East & North Africa", []),
    ("Ankara", "Middle East & North Africa", []),
    ("Cairo", "Middle East & North Africa", []),
    ("Tehran", "Middle East & North Africa", []),
    ("Baghdad", "Middle East & North Africa", []),
    ("Riyadh", "Middle East & North Africa", []),
    ("Jeddah", "Middle East & North Africa", []),
    ("Dubai", "Middle East & North Africa", []),
    ("Abu Dhabi", "Middle East & North Africa", []),
    ("Doha", "Middle East & North Africa", []),
    ("Amman", "Middle East & North Africa", []),
    ("Beirut", "Middle East & North Africa", []),
    ("Jerusalem", "Middle East & North Africa", []),
    ("Tel Aviv", "Middle East & North Africa", []),
    ("Casablanca", "Middle East & North Africa", []),
    ("Algiers", "Middle East & North Africa", []),
    ("Tunis", "Middle East & North Africa", []),

    # --- Sub-Saharan Africa ---
    ("Lagos", "Sub-Saharan Africa", []),
    ("Kinshasa", "Sub-Saharan Africa", []),
    ("Johannesburg", "Sub-Saharan Africa", []),
    ("Cape Town", "Sub-Saharan Africa", []),
    ("Nairobi", "Sub-Saharan Africa", []),
    ("Addis Ababa", "Sub-Saharan Africa", []),
    ("Dar es Salaam", "Sub-Saharan Africa", []),
    ("Accra", "Sub-Saharan Africa", []),
    ("Abidjan", "Sub-Saharan Africa", []),
    ("Dakar", "Sub-Saharan Africa", []),
    ("Luanda", "Sub-Saharan Africa", []),
    ("Khartoum", "Sub-Saharan Africa", []),

    # --- South Asia ---
    ("Mumbai", "South Asia", []),
    ("Delhi", "South Asia", ["New_Delhi", "Delhi"]),
    ("Kolkata", "South Asia", []),
    ("Chennai", "South Asia", []),
    ("Bangalore", "South Asia", []),
    ("Hyderabad", "South Asia", []),
    ("Karachi", "South Asia", []),
    ("Lahore", "South Asia", []),
    ("Islamabad", "South Asia", []),
    ("Dhaka", "South Asia", []),
    ("Colombo", "South Asia", []),
    ("Kathmandu", "South Asia", []),

    # --- East Asia ---
    ("Tokyo", "East Asia", []),
    ("Osaka", "East Asia", []),
    ("Seoul", "East Asia", []),
    ("Beijing", "East Asia", []),
    ("Shanghai", "East Asia", []),
    ("Guangzhou", "East Asia", []),
    ("Shenzhen", "East Asia", []),
    ("Chengdu", "East Asia", []),
    ("Wuhan", "East Asia", []),
    ("Chongqing", "East Asia", []),
    ("Tianjin", "East Asia", []),
    ("Hong Kong", "East Asia", []),
    ("Taipei", "East Asia", []),

    # --- Southeast Asia ---
    ("Jakarta", "Southeast Asia", []),
    ("Manila", "Southeast Asia", []),
    ("Bangkok", "Southeast Asia", []),
    ("Singapore", "Southeast Asia", []),
    ("Kuala Lumpur", "Southeast Asia", []),
    ("Ho Chi Minh City", "Southeast Asia", ["Ho_Chi_Minh_City", "Saigon"]),
    ("Hanoi", "Southeast Asia", []),
    ("Yangon", "Southeast Asia", ["Yangon", "Rangoon"]),
    ("Phnom Penh", "Southeast Asia", []),

    # --- Oceania ---
    ("Sydney", "Oceania", []),
    ("Melbourne", "Oceania", []),
    ("Brisbane", "Oceania", []),
    ("Perth", "Oceania", []),
    ("Auckland", "Oceania", []),
]


# Real (latitude, longitude) in degrees, used only to orient the finished MDS
# map to geographic north/east (orthogonal Procrustes in run_mds.py). This is a
# rigid rotation+reflection of the embedding — it never touches the distances,
# only which way is "up".
CITY_LATLON = {
    "New York": (40.71, -74.01), "Los Angeles": (34.05, -118.24),
    "Chicago": (41.88, -87.63), "Houston": (29.76, -95.37),
    "Phoenix": (33.45, -112.07), "Philadelphia": (39.95, -75.17),
    "San Francisco": (37.77, -122.42), "Boston": (42.36, -71.06),
    "Seattle": (47.61, -122.33), "Atlanta": (33.75, -84.39),
    "Dallas": (32.78, -96.80), "Denver": (39.74, -104.99),
    "Miami": (25.76, -80.19), "Washington DC": (38.90, -77.04),
    "Toronto": (43.65, -79.38), "Montreal": (45.50, -73.57),
    "Vancouver": (49.28, -123.12), "Mexico City": (19.43, -99.13),
    "Guadalajara": (20.68, -103.35), "Monterrey": (25.69, -100.32),
    "Havana": (23.11, -82.37),
    "Sao Paulo": (-23.55, -46.63), "Rio de Janeiro": (-22.91, -43.17),
    "Brasilia": (-15.79, -47.88), "Buenos Aires": (-34.60, -58.38),
    "Lima": (-12.05, -77.04), "Bogota": (4.71, -74.07),
    "Medellin": (6.24, -75.58), "Santiago": (-33.45, -70.67),
    "Caracas": (10.48, -66.90), "Quito": (-0.18, -78.47),
    "Montevideo": (-34.90, -56.16),
    "London": (51.51, -0.13), "Paris": (48.86, 2.35),
    "Berlin": (52.52, 13.40), "Madrid": (40.42, -3.70),
    "Barcelona": (41.39, 2.17), "Rome": (41.90, 12.50),
    "Milan": (45.46, 9.19), "Amsterdam": (52.37, 4.90),
    "Brussels": (50.85, 4.35), "Vienna": (48.21, 16.37),
    "Munich": (48.14, 11.58), "Zurich": (47.37, 8.54),
    "Prague": (50.08, 14.44), "Warsaw": (52.23, 21.01),
    "Budapest": (47.50, 19.04), "Bucharest": (44.43, 26.10),
    "Athens": (37.98, 23.73), "Stockholm": (59.33, 18.07),
    "Copenhagen": (55.68, 12.57), "Dublin": (53.35, -6.26),
    "Lisbon": (38.72, -9.14), "Kyiv": (50.45, 30.52),
    "Moscow": (55.76, 37.62), "St Petersburg": (59.93, 30.34),
    "Istanbul": (41.01, 28.98), "Ankara": (39.93, 32.86),
    "Cairo": (30.04, 31.24), "Tehran": (35.69, 51.39),
    "Baghdad": (33.31, 44.36), "Riyadh": (24.71, 46.68),
    "Jeddah": (21.49, 39.19), "Dubai": (25.20, 55.27),
    "Abu Dhabi": (24.45, 54.38), "Doha": (25.29, 51.53),
    "Amman": (31.95, 35.93), "Beirut": (33.89, 35.50),
    "Jerusalem": (31.77, 35.21), "Tel Aviv": (32.09, 34.78),
    "Casablanca": (33.57, -7.59), "Algiers": (36.75, 3.06),
    "Tunis": (36.81, 10.18),
    "Lagos": (6.52, 3.38), "Kinshasa": (-4.32, 15.31),
    "Johannesburg": (-26.20, 28.05), "Cape Town": (-33.92, 18.42),
    "Nairobi": (-1.29, 36.82), "Addis Ababa": (9.03, 38.74),
    "Dar es Salaam": (-6.79, 39.21), "Accra": (5.60, -0.19),
    "Abidjan": (5.36, -4.01), "Dakar": (14.72, -17.47),
    "Luanda": (-8.84, 13.23), "Khartoum": (15.50, 32.56),
    "Mumbai": (19.08, 72.88), "Delhi": (28.70, 77.10),
    "Kolkata": (22.57, 88.36), "Chennai": (13.08, 80.27),
    "Bangalore": (12.97, 77.59), "Hyderabad": (17.39, 78.49),
    "Karachi": (24.86, 67.00), "Lahore": (31.55, 74.34),
    "Islamabad": (33.68, 73.05), "Dhaka": (23.81, 90.41),
    "Colombo": (6.93, 79.86), "Kathmandu": (27.72, 85.32),
    "Tokyo": (35.68, 139.69), "Osaka": (34.69, 135.50),
    "Seoul": (37.57, 126.98), "Beijing": (39.90, 116.41),
    "Shanghai": (31.23, 121.47), "Guangzhou": (23.13, 113.26),
    "Shenzhen": (22.54, 114.06), "Chengdu": (30.57, 104.07),
    "Wuhan": (30.59, 114.31), "Chongqing": (29.56, 106.55),
    "Tianjin": (39.34, 117.36), "Hong Kong": (22.32, 114.17),
    "Taipei": (25.03, 121.57),
    "Jakarta": (-6.21, 106.85), "Manila": (14.60, 120.98),
    "Bangkok": (13.76, 100.50), "Singapore": (1.35, 103.82),
    "Kuala Lumpur": (3.14, 101.69), "Ho Chi Minh City": (10.82, 106.63),
    "Hanoi": (21.03, 105.85), "Yangon": (16.87, 96.20),
    "Phnom Penh": (11.56, 104.92),
    "Sydney": (-33.87, 151.21), "Melbourne": (-37.81, 144.96),
    "Brisbane": (-27.47, 153.03), "Perth": (-31.95, 115.86),
    "Auckland": (-36.85, 174.76),
}


# Cities whose name has no single token in the GoogleNews vocabulary (verified
# by a full-vocabulary scan): fall back to averaging these component tokens.
COMPOSE_FALLBACK = {
    "Mexico City": ["Mexico", "City"],
}


def strip_diacritics(s: str) -> str:
    import unicodedata
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def candidates_for(display_name: str, extra: list[str]) -> list[str]:
    """Token candidates in priority order, de-duplicated, for one city."""
    cands = list(extra)
    for base in (display_name, strip_diacritics(display_name)):
        cands.append(base.replace(" ", "_"))
    seen, out = set(), []
    for c in cands:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


if __name__ == "__main__":
    regions = {}
    for name, region, _ in CITIES:
        regions.setdefault(region, []).append(name)
    print(f"{len(CITIES)} cities in {len(regions)} regions")
    for r, names in regions.items():
        print(f"  {r}: {len(names)}")
