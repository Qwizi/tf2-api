"""Worker class."""
from pathlib import Path
import time

import httpx
import polib
import vdf
from django.conf import settings
from github import Github

from colors.models import Color
from maps.models import Map
from prefabs.models import Prefab
from qualities.models import Quality
from rarites.models import Rarity
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
            #     # sleep for 1 minute, to avoid rate limit
            #     time.sleep(60)
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

    def process_rarites(self, rarities: dict) -> None:
        """Process the rarities from the items_game.txt file."""
        try:
            rarities_obj = []
            for key, value in rarities.items():
                color = Color.objects.get(game_item_id=value.get("color", ""))
                rarity = Rarity.objects.get_or_create(
                    game_item_id=key,
                    value=value.get("value", ""),
                    color=color,
                )
            for key, value in rarities.items():
                rarity = Rarity.objects.get(game_item_id=key)
                next_rarity_exists = value.get("next_rarity", None)
                if next_rarity_exists:
                    rarity.next_rarity = Rarity.objects.get(game_item_id=value.get("next_rarity", ""))
                    rarity.save()
            rarities_obj.append(rarity)
        except ValueError as exc:
            print(f"An error occurred while processing the rarities: {exc}")
        else:
            return rarities_obj

    def process_prefabs(self, prefabs: dict) -> None:
        """Process the prefabs from the items_game.txt file."""
        try:
            for key, value in prefabs.items():
                game_item_id = key
                item_class = value.get("item_class", None)
                item_name = value.get("item_name", None)
                item_type_name = value.get("item_type_name", None)
                item_description = value.get("item_description", None)
                item_quality = Quality.objects.get(game_item_id=value.get("item_quality")) if value.get("item_quality", None) else None
                item_slot = value.get("item_slot", None)
                craft_class = value.get("craft_class", None)
                craft_material_type = value.get("craft_material_type", None)
                image_inventory = value.get("image_inventory", None)
                equip_region = value.get("equip_region", None)
                mouse_pressed_sound = value.get("mouse_pressed_sound", None)
                drop_sound = value.get("drop_sound", None)
                tags = value.get("tags", None)
                tags_is_cosmetic = False
                tags_is_taunt_item = False
                tags_can_deal_damage = False
                tags_can_deal_gib_damage = False
                tags_can_be_equipped_by_soldier_or_demo = False
                tags_can_deal_posthumous_damage = False
                tags_can_deal_critical_damage = False
                tags_can_deal_long_distance_damage = False
                tags_can_headshot = False
                tags_can_deal_mvm_penetration_damage = False
                tags_can_heal_allies = False
                tags_can_destroy_sappers = False
                tags_can_reflect_projectiles = False
                tags_can_extinguish = False
                tags_is_flamethrower = False
                tags_can_apply_soldier_buff = False
                tags_can_deal_taunt_damage = False
                if tags:
                    tags_is_cosmetic = tags.get("is_cosmetic", False)
                    tags_is_taunt_item = tags.get("is_taunt_item", False)
                    tags_can_deal_damage = tags.get("can_deal_damage", False)
                    tags_can_deal_gib_damage = tags.get("can_deal_gib_damage", False)
                    tags_can_be_equipped_by_soldier_or_demo = tags.get("can_be_equipped_by_soldier_or_demo", False)
                    tags_can_deal_posthumous_damage = tags.get("can_deal_posthumous_damage", False)
                    tags_can_deal_critical_damage = tags.get("can_deal_critical_damage", False)
                    tags_can_deal_long_distance_damage = tags.get("can_deal_long_distance_damage", False)
                    tags_can_headshot = tags.get("can_headshot", False)
                    tags_can_deal_mvm_penetration_damage = tags.get("can_deal_mvm_penetration_damage", False)
                    tags_can_heal_allies = tags.get("can_heal_allies", False)
                    tags_can_destroy_sappers = tags.get("can_destroy_sappers", False)
                    tags_can_reflect_projectiles = tags.get("can_reflect_projectiles", False)
                    tags_can_extinguish = tags.get("can_extinguish", False)
                    tags_is_flamethrower = tags.get("is_flamethrower", False)
                    tags_can_apply_soldier_buff = tags.get("can_apply_soldier_buff", False)
                    tags_can_deal_taunt_damage = tags.get("can_deal_taunt_damage", False)
                used_by_classes = value.get("used_by_classes", None)
                used_by_scout = False
                used_by_sniper = False
                used_by_soldier = False
                used_by_demoman = False
                used_by_medic = False
                used_by_heavy = False
                used_by_spy = False
                used_by_pyro = False
                used_by_engineer = False
                if used_by_classes:
                    used_by_scout = used_by_classes.get("scout", False)
                    used_by_sniper = used_by_classes.get("sniper", False)
                    used_by_soldier = used_by_classes.get("soldier", False)
                    used_by_demoman = used_by_classes.get("demoman", False)
                    used_by_medic = used_by_classes.get("medic", False)
                    used_by_heavy = used_by_classes.get("heavy", False)
                    used_by_spy = used_by_classes.get("spy", False)
                    used_by_pyro = used_by_classes.get("pyro", False)
                    used_by_engineer = used_by_classes.get("engineer", False)
                public_prefab = value.get("public_prefab", False)
                show_in_armory = value.get("show_in_armory", False)
                min_ilevel = value.get("min_ilevel", None)
                max_ilevel = value.get("max_ilevel", None)
                prefab, created = Prefab.objects.get_or_create(
                    game_item_id=game_item_id,
                    defaults={
                        "item_class": item_class,
                        "item_name": item_name,
                        "item_type_name": item_type_name,
                        "item_description": item_description,
                        "item_quality": item_quality,
                        "item_slot": item_slot,
                        "craft_class": craft_class,
                        "craft_material_type": craft_material_type,
                        "image_inventory": image_inventory,
                        "equip_region": equip_region,
                        "mouse_pressed_sound": mouse_pressed_sound,
                        "drop_sound": drop_sound,
                        "tags_is_cosmetic": tags_is_cosmetic,
                        "tags_is_taunt_item": tags_is_taunt_item,
                        "tags_can_deal_damage": tags_can_deal_damage,
                        "tags_can_deal_gib_damage": tags_can_deal_gib_damage,
                        "tags_can_be_equipped_by_soldier_or_demo": tags_can_be_equipped_by_soldier_or_demo,
                        "tags_can_deal_posthumous_damage": tags_can_deal_posthumous_damage,
                        "tags_can_deal_critical_damage": tags_can_deal_critical_damage,
                        "tags_can_deal_long_distance_damage": tags_can_deal_long_distance_damage,
                        "tags_can_headshot": tags_can_headshot,
                        "tags_can_deal_mvm_penetration_damage": tags_can_deal_mvm_penetration_damage,
                        "tags_can_heal_allies": tags_can_heal_allies,
                        "tags_can_destroy_sappers": tags_can_destroy_sappers,
                        "tags_can_reflect_projectiles": tags_can_reflect_projectiles,
                        "tags_can_extinguish": tags_can_extinguish,
                        "tags_is_flamethrower": tags_is_flamethrower,
                        "tags_can_apply_soldier_buff": tags_can_apply_soldier_buff,
                        "tags_can_deal_taunt_damage": tags_can_deal_taunt_damage,
                        "public_prefab": public_prefab,
                        "show_in_armory": show_in_armory,
                        # "used_by_scout": used_by_scout,
                        # "used_by_sniper": used_by_sniper,
                        # "used_by_soldier": used_by_soldier,
                        # "used_by_demoman": used_by_demoman,
                        # "used_by_medic": used_by_medic,
                        # "used_by_heavy": used_by_heavy,
                        # "used_by_spy": used_by_spy,
                        # "used_by_pyro": used_by_pyro,
                        # "used_by_engineer": used_by_engineer,
                        "min_ilevel": min_ilevel,
                        "max_ilevel": max_ilevel,
                    },
                    
                )
        except ValueError as exc:
            print(f"An error occurred while processing the prefabs: {exc}")

    def process_file(self) -> None:
        """Process the items_game.txt file."""
        try:
            items_game_vdf = vdf.load(self.file_path.open("r", encoding="utf-8"))
            maps = items_game_vdf["items_game"]["master_maps_list"]
            qualities = items_game_vdf["items_game"]["qualities"]
            colors = items_game_vdf["items_game"]["colors"]
            rarities = items_game_vdf["items_game"]["rarities"]
            prefabs = items_game_vdf["items_game"]["prefabs"]
            
            processed_maps = self.process_maps(maps)
            processed_qualities = self.process_qualities(qualities)
            processed_colors = self.process_colors(colors)
            process_rarites = self.process_rarites(rarities)
            process_prefabs = self.process_prefabs(prefabs)
            print(processed_colors)
        except ValueError as exc:
            print(f"An error occurred while processing the items_game.txt file: {exc}")

        # maps = items_game_vdf["items_game"]["master_maps_list"]
        # parse_maps.delay(maps)

class TranslationFileWorker(BaseWorker):
    """Worker class for the translation files."""

    def __init__(self, language_code: str, language: str, file_name: str) -> None:
        """Initialize TranslationFileWorker class."""
        super().__init__(file_name)
        self.language_code = language_code
        self.language = language
        self.repo_file_path = f"tf/resource/{file_name}"
        self.translation_dir = Path(__file__).resolve().parent.parent / "locale" / self.language_code / "LC_MESSAGES"
        self.translation_path = self.translation_dir / "django.po"

    def process_file(self) -> None:
        print(f"Processing translation file {self.file_name} for {self.language_code} - {self.language}")
        Path(self.translation_dir).mkdir(parents=True, exist_ok=True)
        try:
            translation_file_vdf = vdf.load(self.file_path.open("r", encoding="utf-8"))
        except FileNotFoundError as exc:
            return
        tokens = translation_file_vdf["lang"]["Tokens"]
        po = polib.POFile()
        po.metadata = {
            "Project-Id-Version": "1.0",
            "Report-Msgid-Bugs-To": "you@example.com",
            "POT-Creation-Date": "2007-10-18 14:00+0100",
            "PO-Revision-Date": "2007-10-18 14:00+0100",
            "Last-Translator": "you <you@example.com>",
            "Language-Team": "English <yourteam@example.com>",
            "MIME-Version": "1.0",
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Transfer-Encoding": "8bit",
        }
        for key, value in tokens.items():
            formated_value = value.replace("", "").replace("", "").replace("", "").replace("", "").replace("", "").replace("", "").replace("", "").replace("", "")
            formated_value = f"{formated_value.strip()}"
            entry = polib.POEntry(
                msgid=key,
                msgstr=formated_value,
                occurrences=[("welcome.py", "12"), ("anotherfile.py", "34")],
            )
            po.append(entry)
        po.save(self.translation_path)
        po.save_as_mofile(self.translation_path.with_suffix(".mo"))
        print(f"File {self.file_name} for {self.language_code} - {self.language} has been processed.")

