# Updating MLB Droughts
import pandas as pd
import numpy as np
# Helper Functions
def extract_paren(string):
    open_ = string.index('(')
    close = string.index(')')
    return string[open_+1: close]

def replace_last_latest(df):
    new_df = df.copy()
    col = new_df.columns[1]
    new_df[col] = df[col].map(extract_paren)
    return new_df

def new_col(df):
    new_df = df.copy()
    col = new_df.columns[1]
    new = new_df[col].apply(lambda x: str(int(x)+1))
    new_df.insert(1, str(int(col)+1), new)
    return new_df

def add_one(team, names):
    if team in names:
        open_ = team.index('(')
        close = team.index(')')
        count = int(team[open_+1: close])
        return team[:open_+1] + str(count+1) + ')'
    else:
        return team
    
def new_ver(df):
    new_df = df.copy()
    ranks = new_df.iloc[:, 1].map(int).rank(method='min', ascending=False).map(int)
    new_ver = np.array([])
    for j in range(len(ranks)):
        new_ver = np.append(new_ver, str(ranks[j]) + ' (' + str(df.iloc[j, 1]) + ')')
    new_df.iloc[:, 1] = new_ver
    return new_df

# Main Function
def update_table(post_teams, lcsp_teams, ws_teams, champ_team, new_year):

    """
    Each teams parameter except the last should have the form of a list; all should
    have the team names listed with their respective counts for the previous year.
    
    The new_year should be entered as a string.
    
    Examples:
    post_teams = ['Rays (6)', 'Red Sox (24)', 'Yankees (56)', 'White Sox (10)', 'Astros (14)',
                'Braves (26)', 'Brewers (7)', 'Cardinals (30)', 'Giants (26)', 'Dodgers (34)']
    lcsp_teams = ['Red Sox (18)', 'Astros (8)', 'Braves (16)', 'Dodgers (27)']

    Read in the data
    champ = pd.read_excel('../Sports-Data/mlb_playoff_droughts/MLBPlayoffDroughts.xls', sheet_name=0)
    ws = pd.read_excel('../Sports-Data/mlb_playoff_droughts/MLBPlayoffDroughts.xls', sheet_name=1)
    lcsp = pd.read_excel('../Sports-Data/mlb_playoff_droughts/MLBPlayoffDroughts.xls', sheet_name=2)
    post = pd.read_excel('../Sports-Data/mlb_playoff_droughts/MLBPlayoffDroughts.xls', sheet_name=3)
    """
    
    post = pd.read_csv('./baseball/data/postseason_droughts.csv')
    lcsp = pd.read_csv('./baseball/data/lcsp_droughts.csv')
    ws = pd.read_csv('./baseball/data/ws_droughts.csv')
    champ = pd.read_csv('./baseball/data/champ_droughts.csv')
    
    # Extract last year's num from parens
    post = replace_last_latest(post)
    post = new_col(post)

    lcsp = replace_last_latest(lcsp)
    lcsp = new_col(lcsp)
    
    ws = replace_last_latest(ws)
    ws = new_col(ws)
    
    champ = replace_last_latest(champ)
    champ = new_col(champ)

    # Grab the relevant indices for this year's teams
    post_inds = post[post['TEAM/YEAR'].isin(post_teams)].index
    lcsp_inds = lcsp[lcsp['TEAM/YEAR'].isin(lcsp_teams)].index
    ws_inds = ws[ws['TEAM/YEAR'].isin(ws_teams)].index
    champ_ind = champ[champ['TEAM/YEAR'] == champ_team].index

    # Add 0's
    post.loc[post_inds, new_year] = '0'
    lcsp.loc[lcsp_inds, new_year] = '0'
    ws.loc[ws_inds, new_year] = '0'
    champ.loc[champ_ind, new_year] = '0'

    # Re-order
    post[new_year] = post[new_year].map(int)
    post = post.sort_values(by=[new_year, 'TEAM/YEAR'], ascending=[False, True])\
        .reset_index().drop('index', axis=1)
    post[new_year] = post[new_year].map(str)

    lcsp[new_year] = lcsp[new_year].map(int)
    lcsp = lcsp.sort_values(by=[new_year, 'TEAM/YEAR'], ascending=[False, True])\
        .reset_index().drop('index', axis=1)
    lcsp[new_year] = lcsp[new_year].map(str)
    
    ws[new_year] = ws[new_year].map(int)
    ws = ws.sort_values(by=[new_year, 'TEAM/YEAR'], ascending=[False, True])\
        .reset_index().drop('index', axis=1)
    ws[new_year] = ws[new_year].map(str)
    
    champ[new_year] = champ[new_year].map(int)
    champ = champ.sort_values(by=[new_year, 'TEAM/YEAR'], ascending=[False, True])\
        .reset_index().drop('index', axis=1)
    champ[new_year] = champ[new_year].map(str)

    # Apply add_one() to the relevant teams' totals
    post['TEAM/YEAR'] = post['TEAM/YEAR'].map(lambda x: add_one(x, names=post_teams))
    lcsp['TEAM/YEAR'] = lcsp['TEAM/YEAR'].map(lambda x: add_one(x, names=lcsp_teams))
    ws['TEAM/YEAR'] = ws['TEAM/YEAR'].map(lambda x: add_one(x, names=ws_teams))
    champ['TEAM/YEAR'] = champ['TEAM/YEAR'].map(lambda x: add_one(x, names=[champ_team]))

    
    prev_year = str(int(new_year)-1)
    post.loc[0, prev_year] += '*'
    

    lcsp.loc[0, prev_year] += '*'
    ws.loc[0, prev_year] += '*'
    champ.loc[0, prev_year] += '*'

    post = new_ver(post)
    lcsp = new_ver(lcsp)
    ws = new_ver(ws)
    champ = new_ver(champ)

    # Re-create .csv files
    post.to_csv('./baseball/data/postseason_droughts.csv', index=False)
    lcsp.to_csv('./baseball/data/lcsp_droughts.csv', index=False)
    ws.to_csv('./baseball/data/ws_droughts.csv', index=False)
    champ.to_csv('./baseball/data/champ_droughts.csv', index=False)