class Stats:
  ranker: 0
  game_date: ''             # Game Started
  game_num: 0
  age: 0
  team: ''
  game_location: 0
  opp: ''                   # Team Opponent
  game_result: ''
  gs: 0

  # team
  team_offensive_plays: 0
  team_tds: 0
  snaps: 0
  pass_yds_off: 0
  rush_yds_off: 0

  # passing
  pass_cmp: 0
  pass_att: 0              # Pass Attempts
  pass_cmp_perc: 0         # Pass completions
  pass_yds: 0              # Passing Yards
  pass_td: 0               
  pass_int: 0
  pass_rating: 0
  pass_sacked: 0
  pass_yds_per_att: 0
  pass_adj_yds_per_att: 0
  pass_2pc: ''

  # rushing
  rush_att: 0
  rush_yds: 0
  rush_yds_per_att: 0
  rush_td: 0
  rush_2pc: ''

  # receiving
  targets: 0
  rec: 0
  rec_yds: 0
  rec_yds_per_rec: 0
  rec_td: 0
  catch_pct: 0
  rec_yds_per_tgt: 0
  rec_drops: 0
  rec_2pc: ''


  # scoring
  two_pt_md: 0
  all_td: 0
  scoring: 0
  xpm: ''
  xpa: ''
  xp_perc: ''
  fgm: ''
  fga: ''
  fg_perc: ''


  # fumbles
  fumbles: 0
  fumbles_forced: 0
  fumbles_rec: 0
  fumbles_rec_yds: 0
  fumbles_rec_td: 0
  fumbles_lost: 0

  # kick returns
  kick_ret: 0
  kick_ret_yds: 0
  kick_ret_yds_per_ret: 0
  kick_ret_td: 0

  # Punt returns
  punt_ret: 0
  punt_ret_yds: 0
  punt_ret_yds_per_ret: 0
  punt_ret_td: 0