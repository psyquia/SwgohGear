import json
import coreapi
client = coreapi.Client()

def get_player_data(ally_code):
	player_data = client.get("http://swgoh.gg/api/player/{}/".format(ally_code))
	return player_data

def get_gear_data(gear_id):
	gear_data = client.get("http://swgoh.gg/api/gear/{}/".format(gear_id))
	return gear_data

def get_all_gear_data():
	gear_data = client.get("http://swgoh.gg/api/gear/")
	return gear_data

def gen_gear_map(gear_data):
	gear_map = {}
	for item in gear_data:
		gear_map[item["base_id"]] = item
	write_data(gear_map, "json/gear_map.json")
	return gear_map

def update_gear_map():
	data = get_all_gear_data()
	gen_gear_map(data)

def get_toon_data(toon_id):
	toon_data = client.get("http://swgoh.gg/api/characters/{}/".format(toon_id))
	return toon_data

def get_all_toons():
	toon_data = client.get("https://swgoh.gg/api/characters/")
	# write_data(toon_data, "characters.json")
	gen_toon_map(toon_data)
	return toon_data

def gen_toon_map(toon_data):
	toon_map = {}
	for item in toon_data:
		toon_map[item["base_id"]] = item
	write_data(toon_map, "json/toon_map.json")
	return toon_map

def update_toon_map():
	data = get_all_toons()
	gen_toon_map(data)

def gen_baseid_2_pk_map(toon_data):
	map = {}
	for toon in toon_data:
		map[toon["base_id"]] = toon["pk"]
	write_data(map, "baseid_2_pk.json")
	return map

def write_data(data, path):
	with open(path, 'w') as json_file:
  		json.dump(data, json_file, indent=4)

def read_data(path):
	with open(path) as f:
  		data = json.load(f)
	return data

def print_data(data):
	print('\n<----------------------------------------------------->')
	print(f' {"index":^10} {"toon":^10} {"drops":^10} {"attempts":^10} {"%":^10}')
	for i in range(len(data)):
		name = data[i]['name']
		shards = data[i]['shards']
		attempts = data[i]['attempts']
		rate = data[i]['%']
		print(f' {i:^10}|{name:^10}|{shards:^10}|{attempts:^10}|{rate:>7.2f} %')
	print('<----------------------------------------------------->\n')

def print_help(data):
	print('\n<---- implement this later ---->')

def exit(data):
	print('exiting...')

def is_gear_obtained(toon_data, gear_lvl, slot):
	if(gear_lvl > toon_data["gear_level"]):
		return False
	if(gear_lvl < toon_data["gear_level"]):
		return True
	for item in toon_data["gear"]:
		if(slot == item["slot"]):
			return item["is_obtained"]
