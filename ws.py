
import requests
from bs4 import BeautifulSoup

def global_():
    GLOBAL_LINK ="https://covid19stats.ph/"
    GLOBAL_REQUESTS = requests.get(GLOBAL_LINK)
    GLOBAL_CONTENT = BeautifulSoup(GLOBAL_REQUESTS.content, 'html.parser')

    records = GLOBAL_CONTENT.find_all(class_="text-right")
    total_cases = records[2].get_text().replace("\n", "").replace("  ","")
    total_recovs = records[3].get_text().replace("\n", "").replace("  ","")
    total_deaths = records[4].get_text().replace("\n", "").replace("  ","")

    int_cases = int(total_cases.replace(",", ""))
    int_recovs = int(total_recovs.replace(",", ""))
    int_deaths = int(total_deaths.replace(",", ""))

    fatality = round(int_deaths/int_cases, 2)
    recovery = round(int_recovs/int_cases, 2)

    print(total_cases)
    print(total_recovs)
    print(total_deaths)
    print(fatality)
    print(recovery)

LINK = "https://covid19stats.ph/stats/by-country/name"
REQUEST = requests.get(LINK)
CONTENT = BeautifulSoup(REQUEST.content, 'html.parser')

#6 lists: names, cases, recovs, deaths, fr, rr

countries = CONTENT.find_all(class_="ellipsis")
#names
all_countries = [data.get_text().replace("\n", "").replace("  ","") for data in countries]

numbers = CONTENT.find_all(class_="text-right")

#cases
all_cases = [numbers[data].get_text().replace("\n", "").replace("  ","").replace(",", "") for data in range(3, len(numbers), 3)]

#recovs
all_recovs = [numbers[data].get_text().replace("\n", "").replace("  ","").replace(",", "") for data in range(4, len(numbers), 3)]

#deaths
all_deaths = [numbers[data].get_text().replace("\n", "").replace("  ","").replace(",", "") for data in range(5, len(numbers), 3)]

#fr
def fatality_rate(deaths, cases):
    fatality_list = []
    for i in range(len(deaths)):
        fr = round(int(deaths[i])/int(cases[i]), 2)
        fatality_list.append(fr)
    return fatality_list

fr = fatality_rate(all_deaths, all_cases)

#rr
def recovery_rate(recovs, cases):
    recovery_list = []
    for i in range(len(recovs)):
        rr = round(int(recovs[i])/int(cases[i]), 2)
        recovery_list.append(rr)
    return recovery_list

rr = recovery_rate(all_recovs, all_cases)

def DISPLAY(name, case, recov, death, fr, rr):
    print(name)
    print(f"Cases: {case}")
    print(f"Recoveries: {recov}")
    print(f"Deaths: {death}")
    print(f"Fatality Rate: {fr}")
    print(f"Recovery Rate: {rr}")

def display_all_info(name, case, recov, death, fr, rr):
    for i in range(len(countries)):
        DISPLAY(name[i], case[i], recov[i], death[i], fr[i], rr[i])

display_all_info(all_countries, all_cases, all_recovs, all_deaths, fr, rr)