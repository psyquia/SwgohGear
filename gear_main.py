import json
import time
import lib.gear_lib as api

class Backend:

  def __init__(self):
    self.check_for_update()

    self.ally_code = -1
    self.toon_map = api.read_data("json/toon_map.json")
    self.gear_map = api.read_data("json/gear_map.json")
    self.toonname_2_baseid = api.read_data("json/toonname_2_baseid.json")
    self.app_data = api.read_data("json/app_data.json")
    self.unused_gear = self.app_data['unused_gear']


  def get_last_toon(self):
    return self.app_data.get('toon_id', 0)

  def get_last_player(self):
    return self.app_data.get('ally_code', 0)

  def get_display_gear_data(self, toon, ally_code=0):
    if ally_code and ally_code != self.ally_code:
      try:
        self.player = api.get_player_data(ally_code)
      except:
        # invalid ally code
        return {}
      self.ally_code = ally_code

    if toon not in self.toon_map:
      # invalid toon id
      return {}

    player_toon = {}
    for unit in self.player["units"]:
      if unit["data"]["base_id"] == toon:
        player_toon = unit["data"]

    toon_data = self.toon_map[toon]
    gear_lvls = toon_data["gear_levels"]

    # toon not activated so set gear level to 0
    if not player_toon:
      player_toon = {'gear_level': 0}
    my_gear_lvl = player_toon["gear_level"]

    total_gear = {}
    equipped_gear = {}
    base = 0
    for gear_lvl in gear_lvls:
      level = gear_lvl["tier"]
      for slot, gear_id in enumerate(gear_lvl["gear"]):
        if gear_id == 9999:
          continue

        obtained = api.is_gear_obtained(player_toon, level, slot)

        gear_data = self.gear_map[str(gear_id)]
        for item in gear_data["ingredients"]:
          total_gear[item["gear"]] = total_gear.get(item["gear"], 0) + item["amount"]
          if obtained:
            equipped_gear[item["gear"]] = equipped_gear.get(item["gear"], 0) + item["amount"]

    for key in total_gear:
      if key not in equipped_gear:
        equipped_gear[key] = 0

    acquired_gear = {}
    progress_gear = {}
    for key, value in equipped_gear.items():
      acquired_gear[key] = value + self.unused_gear.get(key,0)
      progress_gear[key] = float(acquired_gear[key])/float(total_gear[key])

    return {
      'equipped_gear':      equipped_gear, 
      'total_gear':         total_gear, 
      'gear_map':           self.gear_map, 
      'unused_gear':        self.unused_gear, 
      'acquired_gear':      acquired_gear,
      'progress_gear':      progress_gear,
      'toon_data':          toon_data,
      'toonname_2_baseid':  self.toonname_2_baseid
    }


  def save_data(self, data):
    api.write_data(data, "json/app_data.json")
  
  def check_for_update(self):
    changed = False
    last_update = api.read_data("json/last_update.json")
    curr_time = time.time()
    # check if more than 7 days has passed
    if(curr_time - last_update['toon'] > 604800):
      api.update_toon_map()
      last_update['toon'] = curr_time
      changed = True
    if(curr_time - last_update['gear'] > 604800):
      api.update_gear_map()
      last_update['gear'] = curr_time
      changed = True

    if changed:
      api.write_data(last_update, "json/last_update.json")


