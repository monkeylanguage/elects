import xml.etree.ElementTree as ET
from typing import List, Tuple, Dict
import unicodedata
import requests
import os, sys, json, math

frondes = {
    "1": {"name": "Občanská demokratická strana", "ansi_color": ""},
    "2": {"name": "Řád národa - Vlastenecká unie", "ansi_color": ""},
    "3": {"name": "CESTA ODPOVĚDNÉ SPOLEČNOSTI", "ansi_color": ""},
    "4": {"name": "Česká str.sociálně demokrat.", "ansi_color": "94"},
    "5": {"name": "Volte Pr.Blok www.cibulka.net22", "ansi_color": ""},
    "6": {"name": "Radostné Česko", "ansi_color": ""},
    "7": {"name": "STAROSTOVÉ A NEZÁVISLÍ", "ansi_color": "93"},
    "8": {"name": "Komunistická str.Čech a Moravy", "ansi_color": "91"},
    "9": {"name": "Strana zelených", "ansi_color": "92"},
    "10": {"name": "ROZUMNÍ-stop migraci,diktát.EU", "ansi_color": ""},
    "11": {"name": "Společ.proti výst.v Prok.údolí", "ansi_color": ""},
    "12": {"name": "Strana svobodných občanů", "ansi_color": ""},
    "13": {"name": "Blok proti islam.-Obran.domova", "ansi_color": ""},
    "14": {"name": "Občanská demokratická aliance", "ansi_color": ""},
    "15": {"name": "Česká pirátská strana", "ansi_color": "90"},
    "16": {"name": "OBČANÉ 2011-SPRAVEDL. PRO LIDI", "ansi_color": ""},
    "17": {"name": "Unie H.A.V.E.L.", "ansi_color": ""},
    "19": {"name": "Referendum o Evropské unii", "ansi_color": ""},
    "20": {"name": "TOP 09", "ansi_color": "96"},
    "21": {"name": "ANO 2011", "ansi_color": "95"},
    "22": {"name": "Dobrá volba 2016", "ansi_color": ""},
    "23": {"name": "SPR-Republ.str.Čsl. M.Sládka", "ansi_color": ""},
    "24": {"name": "Křesť.demokr.unie-Čs.str.lid.", "ansi_color": ""},
    "25": {"name": "Česká strana národně sociální", "ansi_color": ""},
    "26": {"name": "REALISTÉ", "ansi_color": ""},
    "27": {"name": "SPORTOVCI", "ansi_color": ""},
    "28": {"name": "Dělnic.str.sociální spravedl.", "ansi_color": ""},
    "29": {"name": "Svob.a př.dem.-T.Okamura (SPD)", "ansi_color": ""},
    "30": {"name": "Strana Práv Občanů", "ansi_color": ""},
    "31": {"name": "Národ Sobě", "ansi_color": ""},
    "18": {"name": "Česká národní fronta", "ansi_color": ""},
}

def strip_accents(text):
	try:
		text = unicode(text, 'utf-8')
	except (TypeError, NameError):
		pass
	text = unicodedata.normalize('NFD', text)
	text = text.encode('ascii', 'ignore')
	text = text.decode("utf-8")
	return str(text)

def get_xml_attributes(xml: str, attributes: List = []) -> Dict:
	for child in (xml):
		if len(child.attrib)!= 0:
			attributes.append(child.attrib)
		get_xml_attributes(child,attributes)
	return attributes

def get_villages() -> Dict:
	with open('villages.json') as f:
		data = json.load(f)
	return data

def get_village_data_dict(village_data: Dict, village_id: str) -> Dict:
	data = []
	found = False
	for row in village_data:
		if row.get("CIS_OBEC", "") != "":
			if row.get("CIS_OBEC", "") == village_id:
				found = True
			else:
				found = False
		if found:
			data.append(row)
	return data

def get_simple_chart_by_village(village2find: Dict) -> Dict:
	response = requests.get(f"""https://volby.cz/pls/ps2017nss/vysledky_okres?nuts={village2find["nuts"]}""")
	villages_data = get_xml_attributes(ET.fromstring(response.text))
	village_data = get_village_data_dict(villages_data, village2find["id"])

	voted = list(filter(lambda x: x.get("KSTRANA"), village_data))
	total_votes = village_data[1]["PLATNE_HLASY"]

	tick = "▇"
	print(f"\n----------------------------------------------------")
	print(f""" Elect results for village {village2find["name"]} ({village2find["nuts_name"]})""")
	print(f"----------------------------------------------------")
	for _voted in voted:
		ansi_color = frondes[_voted["KSTRANA"]]["ansi_color"] if frondes[_voted["KSTRANA"]]["ansi_color"] != "" else 97
		print(f"""{_voted["KSTRANA"]}\033[{ansi_color}m{" " if len(_voted["KSTRANA"])<2 else ""}| {tick*math.ceil((100*int(_voted["HLASY"])/int(total_votes)))} ({frondes[_voted["KSTRANA"]]["name"]} - {_voted["PROC_HLASU"]} %)\033[0m""")
	print(f"----------------------------------------------------")

def get_village_name_from_user(retry: bool = False) -> str:
	i = input("No village entered as an argument - provide it here:\n" if not retry else "Empty input - enter the village again:\n")
	return i if i != "" else get_village_name_from_user(True)

def choose_exact_village(village2find_query: str, retry: bool = False) -> str:
	# get available villages + filter them by search string
	villages = get_villages()
	villages2select = list(filter(lambda x: strip_accents(village2find_query).lower() in strip_accents(x["name"]).lower(), villages))

	# return if there is only one village to be shown
	if len(villages2select)==1:
		return villages2select[0]

	if len(villages2select)==0:
		print("\nNo villages found!\n")
		return

	if not retry:
		print("\nMultiple villages found - select the target name by its number below:\n")

	# show them as options
	for idx, village in enumerate(villages2select):
		print(f"""{idx+1}) {village["name"]} ({village["nuts_name"]})""")

	i = input("\nEnter the number of the target village: ")

	# return village or retry choosing exact villages when wrong or no village selected
	if i.isnumeric() and 0 < int(i) <= len(villages2select):
		return villages2select[int(i)-1]
	else:
		print("Not a valid choice, choose again 😕\n")
		return choose_exact_village(village2find_query, True)
