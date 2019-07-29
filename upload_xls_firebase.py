import xlrd
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import re
from models.player import Player
from models.stats import Stats

cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()


loc = ("./fa-player-stats.xls") 
wb = xlrd.open_workbook(loc) 

years = ['2017', '2018']
attrs = [
  'opp', 'team_offensive_plays', 'team_tds', 'game_date', 'snaps', 'pass_att', 'pass_cmp_perc', 'pass_yds', 'pass_td', 'pass_int',
  'pass_sacked', 'pass_rating', 'pass_2pc', 'rush_att', 'rush_yds', 'rush_td', 'rush_2pc', 
  'targets','rec_drops', 'rec', 'rec_yds', 'rec_td', 'rec_2pc', 
  'fumbles', 'fumbles_lost', 'fumbles_rec', 'fumbles_rec_td',
  'kick_ret', 'kick_ret_td', 'punt_ret', 'punt_ret_td', 
  'fga', 'fgm', 
]

for i, year in enumerate(years):
  sheet = wb.sheet_by_index(i) 
  headers = sheet.row_values(0)

  for index in range(1, 2):
    row = sheet.row_values(index)
    url = row[0]
    p = re.compile("[^/]+(?=.htm/$|.htm$)")
    pid = p.search(url).group()
    
    existing_player = db.collection(u'players').document(pid)
    data = {}
    if existing_player:
      data = {}
    else:
      data = {
        u'id': pid,
        u'first_name': row[1],
        u'last_name': row[2],
        u'position': row[3],
        u'current_team': row[4],
      }
      for idx, attr in enumerate(attrs):
        data[attr] = row[idx + 5]
      db.collection(u'players').document(pid).set(data)


  
  
  
  # if soup.body.find('table', id='returns'):
  #   rows = soup.body.find('table', id='returns').tbody.find_all('tr')
  #   for row in rows:
  #     stat = Stats()
  #     raw_stat_list = row.find_all('td')

  #     for cell in raw_stat_list:
  #       if cell['data-stat'] in link_list:
  #         setattr(stat, cell['data-stat'], cell.a.text)
  #       else:
  #         setattr(stat, cell['data-stat'], cell.text)
    
      # player.logs.append(stat)

  
  # print('success')

  # Profile page
  # profile_link = website + player_href
  # r = requests.get(team_link)
  # soup = BeautifulSoup(r.text, 'lxml')

      


  # driver.get(players_link)

  
  # player = driver.find_element_by_xpath("//a[text()='%s']" % fullName)
  # print(player.get_attribute('href'))
  # driver.get(player.get_attribute('href'))

  # years = driver.find_elements_by_xpath("//*[@data-stat='year_id'&contains(text(), '2017'|'2018')]")

  # for year in years:
  #   print(year)

  





cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'users').limit(2)

try:
    docs = doc_ref.stream()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'Missing data')