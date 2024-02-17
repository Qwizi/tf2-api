"""Worker class."""
from pathlib import Path

import httpx
import vdf
from django.conf import settings
from github import Github
import colors

from colors.models import Color
from maps.models import Map
from qualities.models import Quality
from worker.models import TrackFile


class BaseWorker:
    """Base Worker class."""

    def __init__(self, file_name: str) -> None:
        """Initialize BaseWorker class."""
        self.github_client = Github()
        self.repo_name = "SteamDatabase/GameTracking-TF2"
        self.repo_file_path = ""
        self.file_path = Path(settings.STATICFILES_DIRS[0]) / file_name
        self.client = httpx.Client()
        self.file_name = file_name

    def file_need_update(self) -> bool:
        """Check for updates in the file."""
        repo = self.github_client.get_repo(self.repo_name)
        last_modified = repo.get_contents(self.repo_file_path).last_modified_datetime
        track_file = TrackFile.objects.get(file_name=self.file_name)
        if last_modified != track_file.last_modified:
            return True
        return False

    def download_file(self) -> str:
        """Download file to static directory."""
        try:
            repo = self.github_client.get_repo(self.repo_name)
            download_url = repo.get_contents(self.repo_file_path).download_url
            response = self.client.get(download_url)
            response.raise_for_status()
            with Path.open(self.file_path, "w") as file:
                file.write(response.text)
            track_file = TrackFile.objects.get(file_name=self.file_name)
            track_file.last_modified=repo.get_contents(self.repo_file_path).last_modified_datetime
            track_file.save()
            print(track_file.last_modified)
        except httpx.HTTPError as exc:
            print(f"An error occurred while requesting {self.file_name}: {exc}")
            return ""
        else:
            return self.file_path

class WorkerManger:
    """Worker class."""

    def __init__(self) -> None:
        """Initialize Worker class with name and age."""
        self.workers: list[BaseWorker] = []

    def add_worker(self, worker: BaseWorker) -> None:
        """Add a worker to the list of workers."""
        self.workers.append(worker)

    def get_workers(self) -> list[BaseWorker]:
        """Get the list of workers."""
        return self.workers

    def init_track_files_models(self) -> None:
        """Initialize the TrackFiles model."""
        for worker in self.workers:
            TrackFile.objects.get_or_create(file_name=worker.file_name)

    def run_workers(self) -> None:
        """Run all workers."""
        for worker in self.workers:
            # if worker.file_need_update():
            #     worker.download_file()
            worker.process_file()


class ItemsGameFileWorker(BaseWorker):
    """Worker class for the items_game.txt file."""

    def __init__(self, file_name: str) -> None:
        """Initialize ItemsGameFileWorker class."""
        super().__init__(file_name)
        self.repo_file_path = f"tf/scripts/items/{file_name}"

    def process_maps(self, master_maps_list: dict) -> None:
        """Process the maps from the items_game.txt file."""
        try:
            maps = []
            for key, value in master_maps_list.items():
                maps.append(Map.objects.get_or_create(
                    game_item_id=key,
                    name=value.get("name", ""),
                    localizedname=value.get("localizedname", ""),
                    authors=value.get("authors", ""),
                ))
        except ValueError as exc:
            print(f"An error occurred while processing the maps: {exc}")
        else:
            return maps

    def process_qualities(self, qualities: dict) -> None:
        """Process the qualities from the items_game.txt file."""
        try:
            qualities_obj = []
            for key, value in qualities.items():
                qualities_obj.append(Quality.objects.get_or_create(
                    game_item_id=key,
                    value=value.get("value", ""),
                ))
        except ValueError as exc:
            print(f"An error occurred while processing the qualities: {exc}")
        else:
            return qualities_obj

    def process_colors(self, colors: dict) -> None:
        """Process the colors from the items_game.txt file."""
        try:
            colors_obj = []
            hex_colors = {
                "desc_level": "#756B5E",
                "desc_attrib_neutral": "#EBE2CA",
                "desc_attrib_positive": "#99CCFF",
                "desc_attrib_negative": "#FF4040",
                "desc_default": "#B2B2B2",
                "desc_itemset_name": "#E1FF0F",
                "desc_itemset_desc": "#95AF0C",
                "desc_itemset_missing": "#8B8989",
                "desc_bundle": "#95AF0C",
                "desc_limited_use": "#00A000",
                "desc_flags": "#756B5E",
                "desc_strange": "#CD9B1D",
                "desc_unusual": "#8650AC",
            }
            for key, value in colors.items():
                colors_obj.append(Color.objects.get_or_create(
                    game_item_id=key,
                    color_name=value.get("color_name", ""),
                    color_hex=hex_colors.get(key, ""),
                ))
        except ValueError as exc:
            print(f"An error occurred while processing the colors: {exc}")
        else:
            return colors_obj

    def process_file(self) -> None:
        """Process the items_game.txt file."""
        try:
            items_game_vdf = vdf.load(self.file_path.open("r", encoding="utf-8"))
            maps = items_game_vdf["items_game"]["master_maps_list"]
            qualities = items_game_vdf["items_game"]["qualities"]
            colors = items_game_vdf["items_game"]["colors"]
            processed_maps = self.process_maps(maps)
            processed_qualities = self.process_qualities(qualities)
            processed_colors = self.process_colors(colors)
            print(processed_colors)
        except ValueError as exc:
            print(f"An error occurred while processing the items_game.txt file: {exc}")

        # maps = items_game_vdf["items_game"]["master_maps_list"]
        # parse_maps.delay(maps)

