#!/usr/bin/env python3

import requests
import argparse
from concurrent.futures import ThreadPoolExecutor

# set up for LiveTennisAPI
API_KEY = "twjp_247958374cef9cb6ef560d37434c1afa"
BASE_URL = "https://api.livetennisapi.com/api/public/v1"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

def is_valid_singles_player(player: dict, tour: str) -> bool:
    """determine if a given player is valid"""

    return (
        player['tour'] == tour.lower() and
        player['ranking'] is not None and
        not player['is_doubles_team']
    )

def fetch_tour_data(tour: str) -> tuple[str, list[dict]]:
    """returns player data from the given tour"""

    url = f"{BASE_URL}/players"
    params = {"limit": 200}  # API free version only allows for 200 per request

    # retrieve data with requests
    response = requests.get(url, headers=headers, params=params)
    data = response.json()['data']

    return (tour, data)

def fetch_all_data(tours: list[str], num_players: int = 10, display_reverse: bool = False) -> dict[str, list[dict]]:
    """return filtered/sorted player data based on the given parameters"""

    results = {}

    # use concurrent.futures to allow for concurrency when displaying both tours simultaneously
    with ThreadPoolExecutor(max_workers=len(tours)) as thread:
        tour_data = thread.map(fetch_tour_data, tours)

        for tour, data in tour_data:
            
            # functional programming to filter and then sort the data
            filtered = filter(lambda p: is_valid_singles_player(p, tour), data)
            if display_reverse:
                sorted_players = sorted(filtered, key=lambda p: -p['ranking'])  # reverse sort
            else:
                sorted_players = sorted(filtered, key=lambda p: p['ranking'])  # normal sort

            results[tour] = sorted_players[:num_players]  # add on only the top num_players players

    return results

def get_movement_arrow(movement: str) -> str:
    """returns unicode for up or down arrow"""

    arrows = {
        "up": "\N{UPWARDS ARROW}",  
        "down": "\N{DOWNWARDS ARROW}"
    }

    return arrows.get(movement, "-")

def display_data(players: list, tour: str, display_reverse: bool):
    """displays data in a table form about the players in the given tour"""

    if not players:
        print("No Players Found")
        return

    # display header
    if not display_reverse:
        print(f"\nCurrent Top {len(players)} {tour.upper()} Players by Ranking")  # header for Top X players
    else:
        print(f"\nCurrent Bottom {len(players)} {tour.upper()} Players by Ranking")  # header for Bottom X players
    print("=" * 65)
    print(f"{"Rank":<8}{"Move":<6}{"Name":<32}{"Country":<10}{"Points":<10}")
    print("-" * 65)

    # display info for each player
    for player in players:

        ranking = player['ranking']
        arrow = get_movement_arrow(player['ranking_movement'])
        name = player['name']
        country = player['country'].upper()
        points = player['ranking_points']
        print(f"{ranking:<8}{arrow:<6}{name:<32}{country:<10}{points:<10}")

if __name__ == "__main__":

    # parse command line arguments
    parser = argparse.ArgumentParser(description="Current ATP/WTA Tennis Rankings")

    tour_group = parser.add_mutually_exclusive_group(required=True)
    tour_group.add_argument("-m", "--mens", dest="tour", action="store_const", const="atp", help="ATP")
    tour_group.add_argument("-w", "--womens", dest="tour", action="store_const", const="wta", help="WTA")
    tour_group.add_argument("-b", "--both", dest="tour", action="store_const", const="both", help="ATP & WTA")

    parser.add_argument("-n", "--num", type=int, default=10, help="Number of Players")
    parser.add_argument("-r", "--reverse", action="store_true", help="Reverse")

    args = parser.parse_args()

    target_tours = ['atp', 'wta'] if args.tour == 'both' else [args.tour]

    tour_results = fetch_all_data(target_tours, args.num, args.reverse)

    for tour, players in tour_results.items():
        display_data(players, tour, args.reverse)
