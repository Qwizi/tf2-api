from pathlib import Path
import vdf
import polib
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def view(request):
    items_game_path = Path.parent / Path("static/items_game.txt")
    items_game = vdf.load(items_game_path.open())

    return Response({"message": "Hello, world!"})
