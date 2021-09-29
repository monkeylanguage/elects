import argparse
from typing import List, Tuple, Dict
from helpers import *
import os

def init_args() -> Dict:
	parser = argparse.ArgumentParser(
		description="""Draw a chart for elect results for given village name \n(source: https://volby.cz/opendata/ps2017nss/PS_nuts.htm)""",
		formatter_class=argparse.RawTextHelpFormatter
	)
	parser.add_argument("-n", "--name", help="Name of the village (cAsE + accents insensitive)")

	if not os.path.isfile("villages.json"):
		print("Make sure to have the village.json file in the same folder as this script!")
		sys.exit(2)

	return vars(parser.parse_args())

def main():
	args = init_args()
	village2find_query = args.get("name")

	if not village2find_query:
		village2find_query = get_village_name_from_user()

	village2find = choose_exact_village(village2find_query)

	if village2find:
		get_simple_chart_by_village(village2find)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nBye ;-)")
		sys.exit(0)
