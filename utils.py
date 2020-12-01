import requests
import json

class Utils():
    def getScoreBoard(self):
        r = requests.get('https://dass.npst.no/.netlify/functions/scoreboard')
        try:
            results = json.loads(r.text)['result']
            return results
        except:
            return None
    
    def formatDisplayName(self, display_name):
        illegal = ['👉', '👑']
        formatted = display_name[:20]
        if len(display_name) > 20:
            formatted += '...'
        for x in illegal:
            formatted = formatted.replace(x, '💩')
        
        return formatted