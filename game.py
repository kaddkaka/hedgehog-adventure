from time import sleep

position = "Landing Lake"
inventory = []


class goto:
	def __init__(self, dest, *, desc=""):
		self.dest = dest
		self.desc = desc

	def __call__(self):
		global position
		position = self.dest


def desc(description):
	def wrapper(func):
		func.desc = description
		return func
	return wrapper


@desc("The water seems cool")
def search_lake():
	print("You dive down into the lake. Trying to keep your breath and looking around you see a wrench. You take it!")
	global inventory
	inventory.append("wrench")
	global search_lake
	search_lake = lambda: None


@desc("She seem to be looking for something")
def mom():
	global inventory
	if "wrench" in inventory:
		print("Wow my wrench! Just what I needed now I can fix this car and get the children to summer camp, thanks!")
		inventory.pop()
		return "WIN"
	else:
		print("Waah, my head is exploding, how can I make this work??!? The tools are gone too ...")


@desc("Perhaps there is some way to make the little one stop crying")
def kid():
	print("Wuuuuuaaaaaahhh!")
	print(" - Happy singing make yous smi~~ii~iiiillee")
	print("??? Whu-")
	print("Wuuuuuaaaaaaaaaaaaaaaaaaahhh!")

locs = {
	"Landing Lake": {
		"desc": "Your ship has crash landed into a lake, a bunch of bushes surrounds it. A vague pillar of light can be seen in the North.",
		"actions": [
			("go east", goto("Broken Car", desc="You glimpse the sun reflecting of some flat surface")),
			("go north", goto("Brick wall", desc="There seems to be beaten path through the bushes")),
			("dive", search_lake),
	]
	},
	"Brick wall": {
		"desc": "It's just a big wall of bricks. You can't seem to see any hole in it. You go back ...",
		"bounce": goto("Landing Lake"),
	},
	"Broken Car": {
		"desc": "A Family of hedgehogs are quarreling about a car the hasn't been working for the last 5 years, if you were to guess. The little one is crying his heart out.",
		"actions": [
			("go west", goto("Landing Lake", desc="Back to the lake where you started")),
			("talk to mother", mom),
			("talk to kid", kid),
	],
	}
}


def select_action(actions):
	by_num = {}
	by_name = {}
	for i, (action_name, action) in enumerate(actions):
		by_num[str(i+1)] = action
		by_name[action_name.lower()] = action
		print(f"{i+1}. '{action_name}': {action.desc}")

	while True:
		select = input("What do you want to do?:")
		if select in by_num:
			return by_num[select]
		if select in by_name:
			return by_name[select]
		print("I'm not sure what to do.")


def slow_print(msg):
	for char in msg:
		print(char, end="")
		sleep(0.01)


def game_loop():
	result = None
	while result == None:
		print("-" * 60)
		print(f"Current position: {position}")
		print("Inventory:", inventory)
		loc = locs[position]
		print()
		print(loc["desc"])
		print()

		if "bounce" in loc:
			loc["bounce"]()
			continue

		action = select_action(loc["actions"])
		result = action()

	if result == "WIN":
		print("\n" * 5)
		win_msg = """
***                                    ***
 *                                      *  
 *                                      *  
*** Congratulations! You won the game! *** 
 *                                      *  
 *                                      *  
***                                    *** 
****************************************** 
 *               CREDITS                *  
 *        ~ A Bump in the Road ~        *  
 *             David Moberg             *  
 *                                      * 
 """ 

		slow_print(win_msg)

game_loop()
