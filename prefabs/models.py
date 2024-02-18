from django.db import models
from prefix_id import PrefixIDField


class Prefab(models.Model):
    """Model for a prefab."""

    id = PrefixIDField(primary_key=True, prefix="prefab")
    game_item_id = models.CharField(max_length=255)

    item_class = models.CharField(max_length=255, null=True, blank=True)
    item_name = models.CharField(max_length=255, null=True, blank=True)
    item_type_name = models.CharField(max_length=255, null=True, blank=True)
    item_description = models.CharField(max_length=255, null=True, blank=True)
    item_quality = models.ForeignKey("qualities.Quality", on_delete=models.CASCADE, null=True, blank=True)
    item_slot = models.CharField(max_length=255, null=True, blank=True)

    craft_class = models.CharField(max_length=255, null=True, blank=True)
    craft_material_type = models.CharField(max_length=255, null=True, blank=True)

    image_inventory = models.CharField(max_length=255, null=True, blank=True)
    
    equip_region = models.CharField(max_length=255, null=True, blank=True)

    mouse_pressed_sound = models.CharField(max_length=255, null=True, blank=True)
    drop_sound = models.CharField(max_length=255, null=True, blank=True)


    tags_is_cosmetic = models.BooleanField(null=True, blank=True, default=False)
    tags_is_taunt_item = models.BooleanField(null=True, blank=True, default=False)
    tags_can_deal_damage = models.BooleanField(null=True, blank=True, default=False)
    tags_can_deal_gib_damage = models.BooleanField(null=True, blank=True, default=False)
    tags_can_be_equipped_by_soldier_or_demo = models.BooleanField(null=True, blank=True, default=False)
    tags_can_deal_posthumous_damage = models.BooleanField(null=True, blank=True, default=False)
    tags_can_deal_critical_damage = models.BooleanField(null=True, blank=True, default=False)
    tags_can_deal_long_distance_damage = models.BooleanField(null=True, blank=True, default=False)
    tags_can_headshot = models.BooleanField(null=True, blank=True, default=False)
    tags_can_deal_mvm_penetration_damage = models.BooleanField(null=True, blank=True, default=False)
    tags_can_heal_allies = models.BooleanField(null=True, blank=True, default=False)
    tags_can_destroy_sappers = models.BooleanField(null=True, blank=True, default=False)
    tags_can_reflect_projectiles = models.BooleanField(null=True, blank=True, default=False)
    tags_can_extinguish =   models.BooleanField(null=True, blank=True, default=False)
    tags_is_flamethrower = models.BooleanField(null=True, blank=True, default=False)
    tags_can_apply_soldier_buff = models.BooleanField(null=True, blank=True, default=False)
    tags_can_deal_taunt_damage = models.BooleanField(null=True, blank=True, default=False)

    public_prefab = models.BooleanField(null=True, blank=True, default=False)
    show_in_armory = models.BooleanField(null=True, blank=True, default=False)


    used_by_scout = models.BooleanField(null=True, blank=True, default=False)
    used_by_sniper = models.BooleanField(null=True, blank=True, default=False)
    used_by_soldier = models.BooleanField(null=True, blank=True, default=False)
    used_by_demoman = models.BooleanField(null=True, blank=True, default=False)
    used_by_medic = models.BooleanField(null=True, blank=True, default=False)
    used_by_heavy = models.BooleanField(null=True, blank=True, default=False)
    used_by_spy = models.BooleanField(null=True, blank=True, default=False)
    used_by_pyro = models.BooleanField(null=True, blank=True, default=False)
    used_by_engineer = models.BooleanField(null=True, blank=True, default=False)

    prefabs = models.ManyToManyField("self", blank=True)


    min_ilevel = models.IntegerField(null=True, blank=True)
    max_ilevel = models.IntegerField(null=True, blank=True)






    def __str__(self) -> str:
        """Representation of the Prefab object."""
        return "Prefab: " + self.id
