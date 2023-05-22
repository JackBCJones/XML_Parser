import json

def calculate_rarity(events):
    output_data = []
    for row in events:
        x = float(row["x"])
        y = float(row["y"])
        if (0 <= x < 6 and 27 < y < 47) or (109 < x <= 115 and 27 < y < 47) or (x <= 0 and y >= 74) or (x >= 115 and y >= 74) or (x <= 0 and y <= 0) or (x >= 115 and y <= 0):
            rarity = "ULTRA"
        elif (0 <= x <= 28 and 15 <= y <= 59) or (87 <= x <= 115 and 15 <= y <= 59) or (x == 57.5 and y == 37):
            rarity = "RARE"
        elif (0 <= x < 43 and 0 <= y < 74) or (72 < x <= 115 and 0 <= y < 74):
            rarity = "PREM"
        else:
            rarity = "BASE"
        row["rarity"] = rarity
        output_data.append(row)
    return output_data

# ------------------------------------------------------------------------------------------------


def assign_names(events):
    output_data = []
    # Loop through each event and assign a score based on the data points
    previous_event = None
    for event in events:
        event['names'] = []
        type_id = event['type_id']
        outcome = event['outcome']
        qualifiers = event['qualifiers']

        if previous_event is not None:

            # YELLOW CARD 
            if previous_event.get('type_id') == 17 and 31 in previous_event.get("qualifiers"):
                event['names'].append("yellow")

            # SECOND YELLOW CARD
            if (previous_event.get("type_id") == 17 and
                (32 in previous_event.get("qualifiers"))):
                event['names'].append("2yellow")

            # RED CARD 
            if (previous_event.get("type_id") == 17 and
                (33 in previous_event.get("qualifiers"))):
                event['names'].append("red")

        # FOUL

        if ((type_id == 4 or type_id == 17) and
            13 in qualifiers and outcome == 1):
            event['names'].append("foul")

        # GOAL
        if ((type_id == 16) and
            outcome == 1):
            event['names'].append("goal")

        # OWN GOAL
        if ((type_id == 16) and
            28 in qualifiers and
            outcome == 1):
            event['names'].append("owngoal")
            
        # ASSISTS 
        if ((type_id == 13 or type_id == 14 or type_id == 15 or type_id == 16 or type_id == 60) and
            29 in qualifiers and
            outcome == 1):
            event['names'].append("assist")

        # CORNER 
        if ((type_id == 1 or type_id == 2) and
            6 in qualifiers and
            outcome == 1):
                event['names'].append("corner")

        # TACKLE 
        if (type_id == 7 and
            outcome == 1):
            event['names'].append("tackle")

        # FREE KICK 
        if ((type_id == 13 or type_id == 14 or type_id == 15 or type_id == 16 or type_id == 65) and
            26 in qualifiers and
            outcome == 1):
            event['names'].append("free")

        # HEADER 
        if ((type_id == 8 or type_id == 12 or type_id == 13 or type_id == 14 or type_id == 15 or type_id == 16) and
            15 in qualifiers and
            outcome == 1):
            event['names'].append("header")

        # BLOCKING - interception, save  
        if ((type_id == 10 or type_id == 74 or type_id == 8) and
            outcome == 1 and 94 in qualifiers):
            event['names'].append("block")

        # PASSES
        if (type_id == 1 and
            outcome == 1):
            event['names'].append("pass")

        else:
            event['names'].append("other")

        previous_event = event

        output_data.append(event)

    return output_data
# ------------------------------------------------------------------------------------------------

def assign_scores(events):
    output_data = []
    # Loop through each event and assign a score based on the data points
    for event in events:
        names = event['names']
        rarity = event['rarity']
        team_id = event['team_id']
        score = 0
        home_team = 43
        away_team = 45


        
        if ("owngoal" in names):
            if (team_id == home_team):
                if (rarity == 'BASE'):
                    score = -100
                elif (rarity == 'PREM'):
                    score = -100
                elif (rarity == 'RARE'):
                    score = -100
                elif (rarity == 'ULTRA'):
                    score = -100
            
            elif (team_id == away_team):
                if (rarity == 'BASE'):
                    score = 100
                elif (rarity == 'PREM'):
                    score = 100
                elif (rarity == 'RARE'):
                    score = 100
                elif (rarity == 'ULTRA'):
                    score = 100
        
        elif ("goal" in names):
            if (team_id == home_team):
                if (rarity == 'BASE'):
                    score = 200
                elif (rarity == 'PREM'):
                    score = 100
                elif (rarity == 'RARE'):
                    score = 100
                elif (rarity == 'ULTRA'):
                    score = 100
            
            elif (team_id == away_team):
                if (rarity == 'BASE'):
                    score = -200
                elif (rarity == 'PREM'):
                    score = -100
                elif (rarity == 'RARE'):
                    score = -100
                elif (rarity == 'ULTRA'):
                    score = -100

        elif ("red" in names):
            if (team_id == home_team):
                if (rarity == 'BASE'):
                    score = -60
                elif (rarity == 'PREM'):
                    score = -60
                elif (rarity == 'RARE'):
                    score = -80
                elif (rarity == 'ULTRA'):
                    score = -100
            
            elif (team_id == away_team):
                if (rarity == 'BASE'):
                    score = 60
                elif (rarity == 'PREM'):
                    score = 60
                elif (rarity == 'RARE'):
                    score = 80
                elif (rarity == 'ULTRA'):
                    score = 100



        elif ("free" in names):
            if (team_id == home_team):
                if (rarity == 'BASE'):
                    score = 30
                elif (rarity == 'PREM'):
                    score = 50
                elif (rarity == 'RARE'):
                    score = 70
                elif (rarity == 'ULTRA'):
                    score = 90
            
            elif (team_id == away_team):
                if (rarity == 'BASE'):
                    score = -30
                elif (rarity == 'PREM'):
                    score = -50
                elif (rarity == 'RARE'):
                    score = -70
                elif (rarity == 'ULTRA'):
                    score = -90

        elif ("assist" in names):
            if (team_id == home_team):
                if (rarity == 'BASE'):
                    score = 20
                elif (rarity == 'PREM'):
                    score = 40
                elif (rarity == 'RARE'):
                    score = 60
                elif (rarity == 'ULTRA'):
                    score = 80
            elif (team_id == away_team):
                if (rarity == 'BASE'):
                    score = -20
                elif (rarity == 'PREM'):
                    score = -40
                elif (rarity == 'RARE'):
                    score = -60
                elif (rarity == 'ULTRA'):
                    score = -80
        
        elif ("yellow" in names or "2yellow" in names):
            if (team_id == home_team):
                if (rarity == 'BASE'):
                    score = -40
                elif (rarity == 'PREM'):
                    score = -40
                elif (rarity == 'RARE'):
                    score = -60
                elif (rarity == 'ULTRA'):
                    score = -80
            elif (team_id == away_team):
                if (rarity == 'BASE'):
                    score = 40
                elif (rarity == 'PREM'):
                    score = 40
                elif (rarity == 'RARE'):
                    score = 60
                elif (rarity == 'ULTRA'):
                    score = 80
        
        elif ("tackle" in names):
            if (team_id == home_team):
                if (rarity == 'BASE'):
                    score = 20
                elif (rarity == 'PREM'):
                    score = 30
                elif (rarity == 'RARE'):
                    score = 40
                elif (rarity == 'ULTRA'):
                    score = 60
            elif (team_id == away_team):
                if (rarity == 'BASE'):
                    score = -20
                elif (rarity == 'PREM'):
                    score = -30
                elif (rarity == 'RARE'):
                    score = -40
                elif (rarity == 'ULTRA'):
                    score = -60
        
        elif ("header" in names):
            if (team_id == home_team):
                if (rarity == 'BASE'):
                    score = 10
                elif (rarity == 'PREM'):
                    score = 25
                elif (rarity == 'RARE'):
                    score = 30
                elif (rarity == 'ULTRA'):
                    score = 50
            elif (team_id == away_team):
                if (rarity == 'BASE'):
                    score = -10
                elif (rarity == 'PREM'):
                    score = -25
                elif (rarity == 'RARE'):
                    score = -30
                elif (rarity == 'ULTRA'):
                    score = -50

        elif ("block" in names):
            if (team_id == home_team):
                if (rarity == 'BASE'):
                    score = 10
                elif (rarity == 'PREM'):
                    score = 25
                elif (rarity == 'RARE'):
                    score = 30
                elif (rarity == 'ULTRA'):
                    score = 40
            elif (team_id == away_team):
                if (rarity == 'BASE'):
                    score = -10
                elif (rarity == 'PREM'):
                    score = -25
                elif (rarity == 'RARE'):
                    score = -30
                elif (rarity == 'ULTRA'):
                    score = -40

        elif ("corner" in names):
            if (team_id == home_team):
                score = 40
            else:
                score = -40

        elif ("foul" in names):
            if (team_id == home_team):
                if (rarity == 'BASE'):
                    score = -10
                elif (rarity == 'PREM'):
                    score = -25
                elif (rarity == 'RARE'):
                    score = -30
                elif (rarity == 'ULTRA'):
                    score = -40
            elif (team_id == away_team):
                if (rarity == 'BASE'):
                    score = 10
                elif (rarity == 'PREM'):
                    score = 25
                elif (rarity == 'RARE'):
                    score = 30
                elif (rarity == 'ULTRA'):
                    score = 40

        elif ("pass" in names):
            if (team_id == home_team):
                if (rarity == 'BASE'):
                    score = 10
                elif (rarity == 'PREM'):
                    score = 20
                elif (rarity == 'RARE'):
                    score = 30
                elif (rarity == 'ULTRA'):
                    score = 50
            elif (team_id == away_team):
                if (rarity == 'BASE'):
                    score = -10
                elif (rarity == 'PREM'):
                    score = -20
                elif (rarity == 'RARE'):
                    score = -30
                elif (rarity == 'ULTRA'):
                    score = -50

        else:
            score = 0

        event['score'] = score
        output_data.append(event)

    return output_data



