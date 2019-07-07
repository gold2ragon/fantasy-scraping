import xlrd
import xlwt 
from xlwt import Workbook 

import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
from models.player import Player
from models.stats import Stats

loc = ("./name_list.xlsx") 
website = 'https://www.pro-football-reference.com'

wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
headers = sheet.row_values(0)

# Workbook is created 
wb = Workbook() 

years = ['2017', '2018']
sheets = []
sheetIndex = 0

for shi, year in enumerate(years):
  # add_sheet is used to create sheet. 
  sheets.append(None)
  sheets[shi] = wb.add_sheet(year) 
  
  sheets[shi].write(0, 0, 'Link')
  for hi, header in enumerate(headers):
    sheets[shi].write(0, hi+1, header) 

attrs = [
  'opp', 'team_offensive_plays', 'team_tds', 'game_date', 'snaps', 'pass_att', 'pass_cmp_perc', 'pass_yds', 'pass_td', 'pass_int',
  'pass_sacked', 'pass_rating', 'pass_2pc', 'rush_att', 'rush_yds', 'rush_td', 'rush_2pc', 
  'targets','rec_drops', 'rec', 'rec_yds', 'rec_td', 'rec_2pc', 
  'fumbles', 'fumbles_lost', 'fumbles_rec', 'fumbles_rec_td',
  'kick_ret', 'kick_ret_td', 'punt_ret', 'punt_ret_td', 
  'fga', 'fgm', 
]

rowIndex = [1, 1]
for index in range(1, sheet.nrows):
  row = sheet.row_values(index)
  player = Player()
  player.first_name = row[0]
  player.last_name = row[1]
  player.position = row[2]
  player.current_team = row[3] 

  # Find the link with Name
  fullName = "%s %s" % (player.first_name, player.last_name)
  print(index, ':', fullName)
  
  players_link = website + '/players/' + player.last_name[0]
  r = requests.get(players_link)
  r.raise_for_status()
  soup = BeautifulSoup(r.text, 'lxml')
  a = None
  matches = soup.body.find_all('a', text=fullName)
  if matches:
    for match in matches:
      pos = str(match.nextSibling).strip()
      if pos == "(%s)" % player.position:
        a = match
        break
  # a = soup.body.find_element_by_xpath("//p/b/a[text()=%s)]" % fullName)

  # if a is None:
  #   players_link = website + '/players/' + player.last_name[0]
  #   r = requests.get(players_link)
  #   r.raise_for_status()
  #   soup = BeautifulSoup(r.text, 'lxml')
  #   a = soup.body.find('a', text=fullName)

  if a is not None:
    player_href = a['href']

    for shi, year in enumerate(years):
      player_link = website + player_href + '/gamelog/' + year
      r = requests.get(player_link)
      soup = BeautifulSoup(r.text, 'lxml')

      # Stats Table
      if soup.body.find('table', id='stats'):
        rows = soup.body.find('table', id='stats').tbody.find_all('tr')
        # Team page
        teamName = ''

        # Fantasy Page
        fantasy_link = website + player_href + '/fantasy/' + year
        r = requests.get(fantasy_link)
        fantasy_stats = BeautifulSoup(r.text, 'lxml').find('table', id='player_fantasy').tbody

        # link list
        link_list = ['game_date', 'team', 'opp', 'game_result']

        for row in rows:
          stat = Stats()
          raw_stat_list = row.find_all('td')

          for cell in raw_stat_list:
            if cell['data-stat'] == 'team':
              if cell.a.text != teamName:
                teamName = cell.a.text
                team_link = website + cell.a['href']
                r = requests.get(team_link)
                team_logs = BeautifulSoup(r.text, 'lxml').find('table', id='games').tbody
                team_stats = BeautifulSoup(r.text, 'lxml').find('table', id='team_stats').tbody

              team_log = team_logs.find('td', {'csk': stat.game_date}).parent
              stat.pass_yds_off = int(team_log.find('td', {'data-stat': 'pass_yds_off'}).text)
              stat.rush_yds_off = int(team_log.find('td', {'data-stat': 'rush_yds_off'}).text)
              stat.team_offensive_plays = stat.pass_yds_off + stat.rush_yds_off
              
              stat.team_tds = int(team_stats.find('td', {'data-stat': 'pass_td'}).text)\
                            + int(team_stats.find('td', {'data-stat': 'pass_td'}).text)

            elif cell['data-stat'] in link_list:
              setattr(stat, cell['data-stat'], cell.a.text)
            else:
              setattr(stat, cell['data-stat'], cell.text)
          
          try:
            snap_row = fantasy_stats.find('a', text=stat.game_date).parent.parent
            stat.snaps  = int(snap_row.find('td', {'data-stat': 'offense'}).text)\
                        + int(snap_row.find('td', {'data-stat': 'defense'}).text)\
                        + int(snap_row.find('td', {'data-stat': 'special_teams'}).text)
          except:
            stat.snaps = ''
          
          
          if hasattr(stat, 'pass_att') and hasattr(stat, 'pass_cmp'):
            stat.rec_drops = int(stat.pass_att) - int(stat.pass_cmp)

          if hasattr(stat, 'fumbles') and hasattr(stat, 'fumbles_forced'):
            stat.fumbles_lost = int(stat.fumbles) - int(stat.fumbles_forced)

          # player.logs.append(stat)
          # print(stat)

          
          ### Write player info in excel
          sheets[shi].write(rowIndex[shi], 0, website + player_href)
          sheets[shi].write(rowIndex[shi], 1, player.first_name)
          sheets[shi].write(rowIndex[shi], 2, player.last_name) 
          sheets[shi].write(rowIndex[shi], 3, player.position) 
          sheets[shi].write(rowIndex[shi], 4, player.current_team)

          colIndex = 5
          for attr in attrs:
            sheets[shi].write(rowIndex[shi], colIndex, getattr(stat, attr, ''))
            colIndex = colIndex + 1

          rowIndex[shi] = rowIndex[shi] + 1
          
  wb.save('fa-player-stats.xls')
  # Kick & Punt Returns
  
  
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

  





# cred = credentials.Certificate("./ServiceAccountKey.json")
# app = firebase_admin.initialize_app(cred)

# store = firestore.client()
# doc_ref = store.collection(u'users').limit(2)

# try:
#     docs = doc_ref.stream()
#     for doc in docs:
#         print(u'Doc Data:{}'.format(doc.to_dict()))
# except google.cloud.exceptions.NotFound:
#     print(u'Missing data')