from time import sleep

from celery import shared_task
from maps.models import Map

@shared_task()
def parse_maps(maps_list):
    """Parse maps from the list."""
    counter = 0
    for map_key in maps_list:
        name = maps_list[map_key].get("name", "")
        localizedname = maps_list[map_key].get("localizedname", "")
        authors = maps_list[map_key].get("authors", "")
        map_obj = Map.objects.get_or_create(game_item_id=map_key, name=name, localizedname=localizedname, authors=authors)
        print(f"Added map: {map_obj}")
        counter += 1

    return f"Added {counter} maps to database."
