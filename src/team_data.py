"""
MLB team data: primary/secondary colors and ESPN logo URL abbreviations.
"""

# Mapping: canonical 2-3 letter abbr -> team info
MLB_TEAMS: dict[str, dict] = {
    "ARI": {
        "name": "Arizona Diamondbacks",
        "short": "ARI D-BACKS",
        "primary_color": "#A71930",
        "secondary_color": "#E3D4AD",
        "espn_abbr": "ari",
    },
    "ATL": {
        "name": "Atlanta Braves",
        "short": "ATL BRAVES",
        "primary_color": "#CE1141",
        "secondary_color": "#13274F",
        "espn_abbr": "atl",
    },
    "BAL": {
        "name": "Baltimore Orioles",
        "short": "BAL ORIOLES",
        "primary_color": "#DF4601",
        "secondary_color": "#000000",
        "espn_abbr": "bal",
    },
    "BOS": {
        "name": "Boston Red Sox",
        "short": "BOS RED SOX",
        "primary_color": "#BD3039",
        "secondary_color": "#0D2B56",
        "espn_abbr": "bos",
    },
    "CHC": {
        "name": "Chicago Cubs",
        "short": "CHI CUBS",
        "primary_color": "#0E3386",
        "secondary_color": "#CC3433",
        "espn_abbr": "chc",
    },
    "CWS": {
        "name": "Chicago White Sox",
        "short": "CHI W SOX",
        "primary_color": "#27251F",
        "secondary_color": "#C4CED4",
        "espn_abbr": "chw",
    },
    "CIN": {
        "name": "Cincinnati Reds",
        "short": "CIN REDS",
        "primary_color": "#C6011F",
        "secondary_color": "#000000",
        "espn_abbr": "cin",
    },
    "CLE": {
        "name": "Cleveland Guardians",
        "short": "CLE GUARDIANS",
        "primary_color": "#00385D",
        "secondary_color": "#E31937",
        "espn_abbr": "cle",
    },
    "COL": {
        "name": "Colorado Rockies",
        "short": "COL ROCKIES",
        "primary_color": "#333366",
        "secondary_color": "#C4CED4",
        "espn_abbr": "col",
    },
    "DET": {
        "name": "Detroit Tigers",
        "short": "DET TIGERS",
        "primary_color": "#0C2340",
        "secondary_color": "#FA4616",
        "espn_abbr": "det",
    },
    "HOU": {
        "name": "Houston Astros",
        "short": "HOU ASTROS",
        "primary_color": "#002D62",
        "secondary_color": "#EB6E1F",
        "espn_abbr": "hou",
    },
    "KC": {
        "name": "Kansas City Royals",
        "short": "KC ROYALS",
        "primary_color": "#004687",
        "secondary_color": "#C09A5B",
        "espn_abbr": "kc",
    },
    "LAA": {
        "name": "Los Angeles Angels",
        "short": "LAA ANGELS",
        "primary_color": "#BA0021",
        "secondary_color": "#003263",
        "espn_abbr": "laa",
    },
    "LAD": {
        "name": "Los Angeles Dodgers",
        "short": "LAD DODGERS",
        "primary_color": "#005A9C",
        "secondary_color": "#EF3E42",
        "espn_abbr": "lad",
    },
    "MIA": {
        "name": "Miami Marlins",
        "short": "MIA MARLINS",
        "primary_color": "#00A3E0",
        "secondary_color": "#EF3340",
        "espn_abbr": "mia",
    },
    "MIL": {
        "name": "Milwaukee Brewers",
        "short": "MIL BREWERS",
        "primary_color": "#12284B",
        "secondary_color": "#FFC52F",
        "espn_abbr": "mil",
    },
    "MIN": {
        "name": "Minnesota Twins",
        "short": "MIN TWINS",
        "primary_color": "#002B5C",
        "secondary_color": "#D31145",
        "espn_abbr": "min",
    },
    "NYM": {
        "name": "New York Mets",
        "short": "NYM METS",
        "primary_color": "#002D72",
        "secondary_color": "#FF5910",
        "espn_abbr": "nym",
    },
    "NYY": {
        "name": "New York Yankees",
        "short": "NYY YANKEES",
        "primary_color": "#003087",
        "secondary_color": "#C4CED4",
        "espn_abbr": "nyy",
    },
    "OAK": {
        "name": "Oakland Athletics",
        "short": "OAK ATHLETICS",
        "primary_color": "#003831",
        "secondary_color": "#EFB21E",
        "espn_abbr": "oak",
    },
    "PHI": {
        "name": "Philadelphia Phillies",
        "short": "PHI PHILLIES",
        "primary_color": "#E81828",
        "secondary_color": "#002D72",
        "espn_abbr": "phi",
    },
    "PIT": {
        "name": "Pittsburgh Pirates",
        "short": "PIT PIRATES",
        "primary_color": "#27251F",
        "secondary_color": "#FDB827",
        "espn_abbr": "pit",
    },
    "SD": {
        "name": "San Diego Padres",
        "short": "SD PADRES",
        "primary_color": "#2F241D",
        "secondary_color": "#FFC425",
        "espn_abbr": "sdp",
    },
    "SF": {
        "name": "San Francisco Giants",
        "short": "SF GIANTS",
        "primary_color": "#27251F",
        "secondary_color": "#FD5A1E",
        "espn_abbr": "sf",
    },
    "SEA": {
        "name": "Seattle Mariners",
        "short": "SEA MARINERS",
        "primary_color": "#0C2C56",
        "secondary_color": "#005C5C",
        "espn_abbr": "sea",
    },
    "STL": {
        "name": "St. Louis Cardinals",
        "short": "STL CARDINALS",
        "primary_color": "#C41E3A",
        "secondary_color": "#0C2340",
        "espn_abbr": "stl",
    },
    "TB": {
        "name": "Tampa Bay Rays",
        "short": "TB RAYS",
        "primary_color": "#092C5C",
        "secondary_color": "#8FBCE6",
        "espn_abbr": "tb",
    },
    "TEX": {
        "name": "Texas Rangers",
        "short": "TEX RANGERS",
        "primary_color": "#003278",
        "secondary_color": "#C0111F",
        "espn_abbr": "tex",
    },
    "TOR": {
        "name": "Toronto Blue Jays",
        "short": "TOR BLUE JAYS",
        "primary_color": "#134A8E",
        "secondary_color": "#1D2D5C",
        "espn_abbr": "tor",
    },
    "WSH": {
        "name": "Washington Nationals",
        "short": "WSH NATIONALS",
        "primary_color": "#AB0003",
        "secondary_color": "#14225A",
        "espn_abbr": "wsh",
    },
}

# Alias map for alternate abbreviations users might supply
_ALIASES: dict[str, str] = {
    "CHW": "CWS",
    "SDP": "SD",
    "SFG": "SF",
    "KCR": "KC",
    "TBR": "TB",
    "WSN": "WSH",
}


def get_team(abbr: str) -> dict | None:
    """Return team data for *abbr*, accepting common alternate spellings."""
    key = abbr.upper()
    key = _ALIASES.get(key, key)
    return MLB_TEAMS.get(key)


def logo_url(abbr: str) -> str:
    """Return the ESPN CDN logo URL for *abbr*."""
    team = get_team(abbr)
    if team is None:
        raise ValueError(f"Unknown team abbreviation: {abbr!r}")
    return f"https://a.espncdn.com/i/teamlogos/mlb/500/{team['espn_abbr']}.png"
