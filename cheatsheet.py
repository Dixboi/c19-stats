
import requests
from bs4 import BeautifulSoup
import re

def help():
    print(
    '''
    COVID-19 Country Statistics

    COMMAND                                    FUNCTION
    //glo                                      --> Display the global stat
    //a                                        --> Display all information
    //co + {starting letter/s}                 --> Displays all country's information that starts
                                                   with the letter of your entry
                                                   Example: //co Ph
    //help                                      --> Display the instructions
    //term                                     --> Exits the program
                                                   '''
)

def global_():
    GLOBAL_LINK = "https://covid19stats.ph/"
    GLOBAL_REQUEST = requests.get(GLOBAL_LINK)
    GLOBAL_CONTENT = BeautifulSoup(GLOBAL_REQUEST.content, 'html.parser')

    records = GLOBAL_CONTENT.find_all(class_='text-right')
    total_cases = records[2].get_text().replace('\n', "").replace("  ", "")
    total_recoveries = records[3].get_text().replace('\n', "").replace("  ", "")
    total_deaths = records[4].get_text().replace('\n', "").replace("  ", "")

    int_cases = int(total_cases.replace(",", ""))
    int_recoveries = int(total_recoveries.replace(",", ""))
    int_deaths = int(total_deaths.replace(",", ""))
    fatality_rate = round(int_deaths/int_cases, 2)
    recovery_rate = round(int_recoveries/int_cases, 2)

    print("Total Confimed Cases: " + total_cases)
    print("Total Recoveries: " + total_recoveries)
    print("Total Deaths: " + total_deaths)
    print("Fatality Rate: " + str(fatality_rate))
    print("Recovery Rate: " + str(recovery_rate))

LINK = "https://covid19stats.ph/stats/by-country/name"
REQUEST = requests.get(LINK)
CONTENT = BeautifulSoup(REQUEST.content, 'html.parser')

country_records = CONTENT.find_all(class_="ellipsis")
num_records = CONTENT.find_all(class_="text-right")

#names
all_countries = [data.get_text().replace('\n', "").replace("  ", "") for data in country_records]

#cases
all_cases = [num_records[data].get_text().replace('\n', "").replace("  ", "").replace(",", "") for data in range(3, len(num_records), 3)]

#recoveries
all_recovs = [num_records[data].get_text().replace('\n', "").replace("  ", "").replace(",", "") for data in range(4, len(num_records), 3)]

#deaths
all_deaths = [num_records[data].get_text().replace('\n', "").replace("  ", "").replace(",", "") for data in range(5, len(num_records), 3)]

#fatality rate
def fatal_rate(deaths, cases):
    fatal_rate_list = []
    for i in range(len(deaths)):
        fr = round(int(deaths[i])/int(cases[i]), 2)
        fatal_rate_list.append(fr)

    return fatal_rate_list

f_list = fatal_rate(all_deaths, all_cases)

#recovery rate
def recov_rate(recovs, cases):
    recov_rate_list = []
    for i in range(len(recovs)):
        rr = round(int(recovs[i])/int(cases[i]), 2)
        recov_rate_list.append(rr)

    return recov_rate_list

r_list = recov_rate(all_recovs, all_cases)

def DISPLAY(names, cases, recoveries, deaths, fr, rr):
    print(names)
    print(f"Cases: {cases}")
    print(f"Recoveries: {recoveries}")
    print(f"Deaths: {deaths}")
    print(f"Fatality Rate: {fr}")
    print(f"Recovery Rate: {rr}")

def display_all_info(names, cases, recoveries, deaths, fr, rr):
    for i in range(len(names)):
        DISPLAY(names[i], cases[i], recoveries[i], deaths[i], fr[i], rr[i])

def regex_by_name(key, names, cases, recoveries, deaths, fr, rr):
    pattern = "^{}".format(key)
    for country in names:
        searching = re.search(pattern, country)
        if searching:
            position = names.index(country)
            DISPLAY(names[position], cases[position], recoveries[position], deaths[position], fr[position], rr[position])


run = True
help()
while run:
    user_input = input("Enter command: ").split()
    if len(user_input) > 0:
        if user_input[0] == "//glo":
            global_()
        elif user_input[0] == "//a":
            display_all_info(all_countries, all_cases, all_recovs, all_deaths, f_list, r_list)
        elif user_input[0] == "//co":
            regex_by_name(user_input[1], all_countries, all_cases, all_recovs, all_deaths, f_list, r_list)
        elif user_input[0] == "//help":
            help()
        elif user_input[0] == "//term":
            run = False
        else:
            print("invalid")