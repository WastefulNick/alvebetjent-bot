import requests
import json

class API():
    def getScoreBoard(self):
        r = requests.get('https://dass.npst.no/.netlify/functions/scoreboard');
        try:
            results = json.loads(r.text)['result']
            return results
        except:
            return None