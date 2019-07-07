import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

import re
from pro_football_ref_scraper import ProFbRefScraper
from player import Player

""" **************************************************
  Firebase
************************************************** """
cred = credentials.Certificate("./MyServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()



""" **************************************************
  Scraping
************************************************** """
# years = [2017, 2018]
# stats = ['rushing', 'passing', 'receiving', 'kicking', 'returns', 'scoring', 'fantasy', 'defense']

years = [2017]
stats = ['rushing']

# Create object.
pro_fb_ref = ProFbRefScraper()

for year in years:
  p = re.compile("[^/]+(?=.htm%d$)" % year)
  
  for item in stats:
    
    

    # Get a data frame of a specific table.
    passing_df = pro_fb_ref.get_data(start_year=year, end_year=year, table_type=item)
    print(type(passing_df))
    # Save a data fram to a csv file.
    passing_df.to_csv("%s_%d.csv" % (item, year))

    

    for label, content in passing_df.iterrows():
      id = re.findall(p, label)[0]
      data = content.to_json()
      # print(type(content))
      
      if db.collection(u'players').document(id):
        player = db.collection(u'players').document(id)
        player.set(content.to_json())

      # print(id)
      # print('label:', label)
      
      


    