"""
Script to download MLB team logos and add white outlines
"""
import os
import requests
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO

# MLB teams with their abbreviations and logo URLs
MLB_TEAMS = {
    'ARI': {'name': 'Arizona Diamondbacks', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/ari.png'},
    'ATL': {'name': 'Atlanta Braves', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/atl.png'},
    'BAL': {'name': 'Baltimore Orioles', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/bal.png'},
    'BOS': {'name': 'Boston Red Sox', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/bos.png'},
    'CHC': {'name': 'Chicago Cubs', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/chc.png'},
    'CWS': {'name': 'Chicago White Sox', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/chw.png'},
    'CIN': {'name': 'Cincinnati Reds', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/cin.png'},
    'CLE': {'name': 'Cleveland Guardians', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/cle.png'},
    'COL': {'name': 'Colorado Rockies', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/col.png'},
    'DET': {'name': 'Detroit Tigers', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/det.png'},
    'HOU': {'name': 'Houston Astros', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/hou.png'},
    'KC': {'name': 'Kansas City Royals', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/kc.png'},
    'LAA': {'name': 'Los Angeles Angels', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/laa.png'},
    'LAD': {'name': 'Los Angeles Dodgers', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/lad.png'},
    'MIA': {'name': 'Miami Marlins', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/mia.png'},
    'MIL': {'name': 'Milwaukee Brewers', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/mil.png'},
    'MIN': {'name': 'Minnesota Twins', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/min.png'},
    'NYM': {'name': 'New York Mets', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/nym.png'},
    'NYY': {'name': 'New York Yankees', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/nyy.png'},
    'OAK': {'name': 'Oakland Athletics', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/oak.png'},
    'PHI': {'name': 'Philadelphia Phillies', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/phi.png'},
    'PIT': {'name': 'Pittsburgh Pirates', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/pit.png'},
    'SD': {'name': 'San Diego Padres', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/sd.png'},
    'SF': {'name': 'San Francisco Giants', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/sf.png'},
    'SEA': {'name': 'Seattle Mariners', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/sea.png'},
    'STL': {'name': 'St. Louis Cardinals', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/stl.png'},
    'TB': {'name': 'Tampa Bay Rays', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/tb.png'},
    'TEX': {'name': 'Texas Rangers', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/tex.png'},
    'TOR': {'name': 'Toronto Blue Jays', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/tor.png'},
    'WSH': {'name': 'Washington Nationals', 'url': 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/wsh.png'},
}


def add_white_outline(image, outline_width=8):
    """
    Add white outline to an image with transparency
    
    Args:
        image: PIL Image object
        outline_width: Width of the outline in pixels
    
    Returns:
        PIL Image with white outline
    """
    # Ensure image has alpha channel
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Create a slightly larger canvas
    width, height = image.size
    new_size = (width + outline_width * 2, height + outline_width * 2)
    
    # Create new image with transparent background
    outlined_image = Image.new('RGBA', new_size, (0, 0, 0, 0))
    
    # Create outline by drawing the image multiple times with white color
    # Extract alpha channel
    alpha = image.split()[-1]
    
    # Create white version of the logo
    white_logo = Image.new('RGBA', image.size, (255, 255, 255, 255))
    white_logo.putalpha(alpha)
    
    # Draw white outline by offsetting in multiple directions
    for angle in range(0, 360, 45):
        import math
        x_offset = int(outline_width * math.cos(math.radians(angle)))
        y_offset = int(outline_width * math.sin(math.radians(angle)))
        outlined_image.paste(white_logo, 
                            (outline_width + x_offset, outline_width + y_offset),
                            white_logo)
    
    # Paste the original image on top
    outlined_image.paste(image, (outline_width, outline_width), image)
    
    return outlined_image


def download_and_process_logo(team_abbr, team_info, output_dir):
    """
    Download a team logo and add white outline
    
    Args:
        team_abbr: Team abbreviation (e.g., 'NYY')
        team_info: Dictionary with team name and logo URL
        output_dir: Directory to save the processed logo
    """
    try:
        print(f"Downloading {team_info['name']} logo...")
        
        # Download the logo
        response = requests.get(team_info['url'], timeout=10)
        response.raise_for_status()
        
        # Open image from bytes
        original_image = Image.open(BytesIO(response.content))
        
        # Add white outline
        outlined_image = add_white_outline(original_image, outline_width=10)
        
        # Save the processed image
        output_path = os.path.join(output_dir, f"{team_abbr.lower()}.png")
        outlined_image.save(output_path, 'PNG')
        
        print(f"✓ Saved {team_abbr} logo to {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {team_abbr}: {str(e)}")
        return False


def main():
    """Main function to download all MLB logos"""
    # Get the assets/mlb directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'assets', 'mlb')
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Downloading and processing MLB logos to {output_dir}")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    for team_abbr, team_info in MLB_TEAMS.items():
        if download_and_process_logo(team_abbr, team_info, output_dir):
            successful += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"Complete! Successfully processed {successful}/{len(MLB_TEAMS)} logos")
    if failed > 0:
        print(f"Failed: {failed} logos")


if __name__ == '__main__':
    main()
