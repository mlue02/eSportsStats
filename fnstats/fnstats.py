import pandas as pd
import numpy as np
import os
import re
import requests
import time
import bs4
import matplotlib.pyplot as plt

def eventData(url):
    url = "https://fortnitetracker.com/events/epicgames_S21_PgodCup_NAW?window=S21_PgodCup_NAW_Round1"
    data = requests.get(url).text
    soup = bs4.BeautifulSoup(data, 'html.parser')
    stats = soup.find_all('script')[51].text.split('"entries": [')[1]
    #Regex to access session data
    pattern = r'"sessionStats": [\d\w\s\{\}.:",]+'

    teamStats = re.findall(pattern, stats)
    cleanStats = []
    for team in teamStats:
        pattern = r'"elims": ([0-9]+),'
        elims = re.findall(pattern, team)[0]
        pattern = r'"wins": ([0-9]+),'
        wins = re.findall(pattern, team)[0]
        pattern = r'"matches": ([0-9]+),'
        matches = re.findall(pattern, team)[0]
        pattern = r'"avgPoints": ([0-9.]+),'
        avgPoints = re.findall(pattern, team)[0]
        pattern = r'"avgPlace": ([0-9.]+),'
        avgPlace = re.findall(pattern, team)[0]
        pattern = r'"avgElims": ([0-9.]+),'
        avgElims = re.findall(pattern, team)[0]
        pattern = r'"kdRatio": ([0-9.]+),'
        kdRatio = re.findall(pattern, team)[0]
        cleanStats.append({'elims': elims, 'wins': wins, 'matches': matches, 'avgPoints': avgPoints, 'avgElims': avgElims, 'avgPlace': avgPlace, 'kdRatio': kdRatio})

    pattern = r'"pointsEarned": ([0-9]+),'
    points = re.findall(pattern, stats)
    pattern = r'"rank": ([0-9]+),'
    rank = re.findall(pattern, stats)

    df = pd.DataFrame(cleanStats)
    df['points'] = points
    df['rank'] = rank
    df = df.astype(float)

    #Finding Elimination/Placement Point Distribution Stats
    elimLine = soup.find_all('div', {'class': 'fne-scores__entry'})[-1].text
    pattern = r'\nEach Elimination\n\+ ([0-9]+)\n'
    elimVal = float(re.findall(pattern, elimLine)[0])
    df['elimPoints'] = df['elims'] * elimVal
    df['placementPoints'] = df['points'] - df['elimPoints']
    df['elimPtsProportion'] = df['elimPoints']/df['points']
    df['placementPtsProportion'] = df['placementPoints']/df['points']
    df['winrate'] = df['wins']/df['matches']
    return df