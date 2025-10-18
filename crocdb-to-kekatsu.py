"""
This script fetches game entries from the CrocDB API for specified platforms, processes the data,
and creates a Kekatsu-compatible database file. The database is then moved to a specified directory.
"""
import requests
import os
import json
import shutil

API_BASE_URL = 'https://api.crocdb.net'

DB_VERSION = 1
DELIMITER = '\t'

REGION_MAP = {
    'us': 'NTSC-U',
    'eu': 'PAL',
    'jp': 'NTSC-J',
    'other': 'OTHER'
}


def load_config(file_path='config.json'):
    """Load configuration from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def fetch_entries(platforms):
    """Fetch game entries from the CrocDB API for the specified platforms."""
    all_results = []
    page = 1
    while True:
        r = requests.post(f'{API_BASE_URL}/search', json={
            'platforms': platforms,
            'page': page
        })

        if not r.ok:
            return None

        data = r.json()['data']
        results = data['results']
        if not results:
            break

        all_results.extend(results)

        page += 1
        if page == data['total_pages']:
            break

    return all_results


def select_best_link(links, platform):
    """Select the best download link for a game entry based on platform and host preference."""
    allowed_formats = {
        'nds': ['nds', 'dsi'],
        'dsi': ['nds', 'dsi'],
        'wii': ['wbfs']
    }

    filtered_links = []
    for link in links:
        if link['format'] in allowed_formats[platform]:
            filtered_links.append(link)

    # Prefer MarioCube and Myrient among the filtered links
    for link in filtered_links:
        host = link['host']
        if host == 'MarioCube':
            return link
        elif host == 'Myrient':
            return link

    return filtered_links[0] if filtered_links else None


def create_kekatsu_entry(entry):
    """Create a Kekatsu-compatible database entry from a game entry."""
    platform = entry['platform']
    best_link = select_best_link(entry['links'], platform)
    if not best_link:
        return None

    title = entry['title']
    regions = entry['regions']
    region = REGION_MAP[regions[0]] if regions else 'ANY'
    boxart_url = entry['boxart_url']
    download_url = best_link['url']
    file_name = best_link['filename']
    size = str(best_link['size'])

    row = []
    for element in [title, platform, region, '', '', download_url, file_name, size, boxart_url]:
        if not element:
            element = ''
        row.append(element)

    return DELIMITER.join(row)


def create_kekatsu_database(platforms, output_file, kekatsu_dbs_dir):
    """Create a Kekatsu-compatible database file for the specified platforms."""
    print(f"Creating database ({', '.join(platforms)}) ({output_file})")

    entries = fetch_entries(platforms)
    if not entries:
        print(
            f"Failed to get entries ({', '.join(platforms)}) ({output_file})")
        return

    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w', encoding='ascii', errors='replace') as f:
        f.write(f'{DB_VERSION}\n')
        f.write(f'{DELIMITER}\n')

        for entry in entries:
            kekatsu_entry = create_kekatsu_entry(entry)
            if kekatsu_entry:
                f.write(f'{kekatsu_entry}\n')

    print(f"Database created ({', '.join(platforms)}) ({output_file})")

    destination_path = os.path.join(kekatsu_dbs_dir, output_file)
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    if os.path.exists(destination_path):
        os.remove(destination_path)

    shutil.move(output_file, destination_path)

    print(
        f"Database ({', '.join(platforms)}) ({output_file}) moved to {destination_path}")


if __name__ == '__main__':
    # Change directory to script location
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    config = load_config('config.json')
    kekatsu_dbs_dir = config.get('kekatsu_dbs_dir', '')

    create_kekatsu_database(['nds', 'dsi'], 'ds', kekatsu_dbs_dir)
    create_kekatsu_database(['nds'], 'nds', kekatsu_dbs_dir)
    create_kekatsu_database(['dsi'], 'dsi', kekatsu_dbs_dir)
