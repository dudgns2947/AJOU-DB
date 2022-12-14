from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.op.gg/champion/aatrox/statistics/top/matchup")

soup = BeautifulSoup(html, "html.parser")

item_lists = soup.find_all("div", {"class": "champion-matchup-list__champion"})
num = 0
cnt = 0

print("*아트록스 챔피언 별 승률 지표*")

for item_list in item_lists:
  name = item_list.find("span")
  winrate = item_list.find("span", {"class": "champion-matchup-list__winrate"})
  print("name: {}".format(name.text))
  print("Winrate: {}".format(winrate.text))
  print("-----------------------------------------------------------")
  cnt += 1
  if cnt > 20:
    break
