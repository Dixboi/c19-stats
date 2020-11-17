
import re
import os
import sys
import requests
from bs4 import BeautifulSoup
 
def instructions():
  print(
    '''
    COVID-19 Country Statistics

    COMMAND                                    FUNCTION
    //glo                                      --> Display the global stat
    //a                                        --> Display all information
    //co + {starting letter/s}                 --> Displays all country's information that starts
                                                   with the letter of your entry
                                                   Example: //co Ph
    //ca + {starting number} + {ending number} --> Displays all country's information where the
                                                   cases are within the range of your entry
                                                   Example: //ca 1000 2000
    //re + {starting number} + {ending number} --> Displays all country's information where the
                                                   recoveries are within the range of your entry
                                                   Example: //re 3000 100000
    //de + {starting number} + {ending number} --> Displays all country;s information where the
                                                   deaths are within the range of your entry
                                                   Example: //de 0 100
    //cls                                      --> Clears the screem
    //help                                     --> Display the instructions
    //term                                     --> Exits the program
    '''
)

def global_():
  link = 'https://covid19stats.ph/'
  page = requests.get(link)
  soup = BeautifulSoup(page.content, 'html.parser')

  record_cases = soup.find_all(class_ = "text-right")
  total_cases = record_cases[2].get_text().replace("\n", "").replace(" ", "").replace(",", "")
  recoveries = record_cases[3].get_text().replace("\n", "").replace(" ", "").replace(",", "")
  deaths = record_cases[4].get_text().replace("\n", "").replace(" ", "").replace(",", "")
  cfr = round(int(deaths)/int(total_cases), 2)
  crr = round(int(recoveries)/int(total_cases), 2)
  print(f'Total Confirmed Cases: {total_cases}')
  print(f'Total Recovered: {recoveries}')
  print(f'Total Deaths: {deaths}')
  print(f'Fatality Rate: {cfr}')
  print(f'Recovery Rate: {crr}')

def all_names(country_names):
  return [names.get_text().replace("  ", "").replace("\n", "") for names in country_names]

def all_cases(country_cases):
  return [country_cases[case] for case in range(3, len(country_cases), 3)]

def all_recoveries(country_recoveries):
  return [country_recoveries[recov] for recov in range(4, len(country_recoveries), 3)]

def all_deaths(country_deaths):
  return [country_deaths[death] for death in range(5, len(country_deaths), 3)]

def all_fatality_rates(country_cfr):
  country_cases = all_cases(country_cfr)
  country_deaths = all_deaths(country_cfr)
  return [str(round(int(country_deaths[I])/int(country_cases[I]) * 100, 2)) + "%" for I in range(len(country_cases))]

def all_recovery_rates(country_crr):
  country_cases = all_cases(country_crr)
  country_recovs = all_recoveries(country_crr)
  return [str(round(int(country_recovs[I])/int(country_cases[I]) * 100, 2)) + "%" for I in range(len(country_cases))]

def HORIZONTAL_BORDER():
  print("#"* 74) 

def CATEGORIES():
  print("#NAME" + (" " * 24) + "CASES" + (" " * 5) + "RECOV" + (" " * 5) + "DEATHS" + (" " * 4) + "CFR" + (" " * 4) + "CRR" + (" " * 4) + "#")

def HEADER():
  HORIZONTAL_BORDER()
  CATEGORIES()
  HORIZONTAL_BORDER()

def DISPLAY(names, cases, recoveries, deaths, cfr, crr):
  name = "#" + names + (" " * (27 - len(names)))
  case = str(cases) + (" " * (9 - len(str(cases))))
  recov = str(recoveries) + (" " * (9 - len(str(recoveries))))
  death = str(deaths) + (" " * (9 - len(str(deaths))))
  cFr = str(cfr) + (" " * (6 - len(str(cfr))))
  cRr = str(crr) + (" " * (6 - len(str(crr))) + " #")
  print(name, case, recov, death, cFr, cRr)

def display_all_info(names, cases, recoveries, deaths, cfr, crr):
  NAMES = all_names(names)
  CASES = all_cases(cases)
  RECOVERIES = all_recoveries(recoveries)
  DEATHS = all_deaths(deaths)
  CFR = all_fatality_rates(cfr)
  CRR = all_recovery_rates(crr)
  counter = 0
  HEADER()
  for stats in range(len(NAMES)):
    DISPLAY(NAMES[counter], CASES[counter], RECOVERIES[counter], DEATHS[counter], CFR[counter], CRR[counter])
    counter += 1
  HORIZONTAL_BORDER()

def regex_by_name(key, names, cases, recoveries, deaths, cfr, crr):
  NAMES = all_names(names)
  CASES = all_cases(cases)
  RECOVERIES = all_recoveries(recoveries)
  DEATHS = all_deaths(deaths)
  CFR = all_fatality_rates(cfr)
  CRR = all_recovery_rates(crr)
  pattern = "^{}".format(key)
  HEADER()
  for NAME in NAMES:
    searching = re.search(pattern, NAME)
    if searching:
      position = NAMES.index(NAME)
      DISPLAY(NAMES[position], CASES[position], RECOVERIES[position], DEATHS[position], CFR[position], CRR[position])
  HORIZONTAL_BORDER()

def regex_by_cases(start, end, names, cases, recoveries, deaths, cfr, crr):
  NAMES = all_names(names)
  CASES = list(map(lambda value: int(value), all_cases(cases)))
  RECOVERIES = all_recoveries(recoveries)
  DEATHS = all_deaths(deaths)
  CFR = all_fatality_rates(cfr)
  CRR = all_recovery_rates(crr)
  start = int(start)
  end = int(end)
  HEADER()
  for CASE in CASES:
    if start <= CASE <= end:
      position = CASES.index(CASE)
      DISPLAY(NAMES[position], CASES[position], RECOVERIES[position], DEATHS[position], CFR[position], CRR[position])
  HORIZONTAL_BORDER()

def regex_by_recoveries(start, end, names, cases, recoveries, deaths, cfr, crr):
  NAMES = all_names(names)
  CASES = all_cases(cases)
  RECOVERIES = list(map(lambda value: int(value), all_recoveries(recoveries)))
  DEATHS = all_deaths(deaths)
  CFR = all_fatality_rates(cfr)
  CRR = all_recovery_rates(crr)
  start = int(start)
  end = int(end)
  HEADER()
  for RECOV in RECOVERIES:
    if start <= RECOV <= end:
      position = RECOVERIES.index(RECOV)
      DISPLAY(NAMES[position], CASES[position], RECOVERIES[position], DEATHS[position], CFR[position], CRR[position])
  HORIZONTAL_BORDER()

def regex_by_deaths(start, end, names, cases, recoveries, deaths, cfr, crr):
  NAMES = all_names(names)
  CASES = all_cases(cases)
  RECOVERIES = all_recoveries(recoveries)
  DEATHS = list(map(lambda value: int(value), all_deaths(deaths)))
  CFR = all_fatality_rates(cfr)
  CRR = all_recovery_rates(crr)
  start = int(start)
  end = int(end)
  HEADER()
  for DEATH in DEATHS:
    if start <= DEATH <= end:
      position = DEATHS.index(DEATH)
      DISPLAY(NAMES[position], CASES[position], RECOVERIES[position], DEATHS[position], CFR[position], CRR[position])
  HORIZONTAL_BORDER()

def clear_screen():
  print("\n" * 40)
  os.system('cls')
  instructions()

def exit_program():
  print("Are you sure you want to exit the program?")
  print("Type 'y' for yes, Press 'Enter' for no")
  isQuit = input()
  if isQuit == "y":
    sys.exit("Quitting program")


