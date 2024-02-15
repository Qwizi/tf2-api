from maps.models import Map


def parse_maps(master_maps_list: dict) -> None:
    """Parse the master_maps_list from items_game.txt."""
    for map in master_maps_list:
        map_obj = Map.objects.get_or_create(
            game_item_id=map, name=master_maps_list[map]["name"],
            localizedname=master_maps_list[map]["localizedname"],
            authors=master_maps_list[map].get("authors", ""),
        )
