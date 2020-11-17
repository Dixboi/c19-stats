import requests
from bs4 import BeautifulSoup
import functions as func

if __name__ == '__main__':
  stat_name = 'https://covid19stats.ph/stats/by-country/name'
  page_name = requests.get(stat_name)
  soup_name = BeautifulSoup(page_name.content, 'html.parser')

  country_name = soup_name.find_all(class_ = 'ellipsis')
  stats = soup_name.find_all(class_ = "text-right")
  info = [data.get_text().replace("  ", "").replace("\n", "").replace(",", "") for data in stats]

  func.instructions()
  user = "Python|User|command>>"
  
  while True:
    command = input(user).split()
    if len(command) > 0:
      if command[0] == "//term":
        func.exit_program()
      elif command[0] != "//term":
        try:
          if command[0] == "//a":
            func.display_all_info(country_name, info, info, info, info , info)
          elif command[0] == "//co":
            func.regex_by_name(command[1], country_name, info, info, info, info, info)
          elif command[0] == "//ca":
            func.regex_by_cases(command[1], command[2], country_name, info, info, info, info, info)
          elif command[0] == "//re":
            func.regex_by_recoveries(command[1], command[2], country_name, info, info, info, info, info)
          elif command[0] == "//de":
            func.regex_by_deaths(command[1], command[2], country_name, info, info, info, info, info)
          elif command[0] == "//cls":
            func.clear_screen()
          elif command[0] == "//glo":
            func.global_()
          elif command[0] == "//hlp":
            func.instructions()
          else:
            command = " ".join(command)
            print(f'"{command}" is not recognized as a valid command in this program.')
        except:
          print("Invalid entry.")
      else:
        print(f'"{command}" is not recognized as a valid command in this program.')
