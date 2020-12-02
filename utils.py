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
    
    def getScoreUsersByName(self, score, input_users):
        embed_string = ''
        user_count = 0

        for x in range(len(score)):
            user = score[x]

            for arg in input_users:
                if arg.lower() in user['display_name'].lower():
                    user_count += 1
                    embed_string += f'#{x+1} {Utils().formatDisplayName(user["display_name"])} - {int(user["challenges_solved"]) * 10} poeng\n'
                    if user_count >= 15:
                        embed_string += '...'
                        return embed_string
        
        return embed_string