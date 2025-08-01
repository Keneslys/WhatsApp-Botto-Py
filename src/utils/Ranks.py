ranks = {
    "Recruit": {"exp": 0, "emoji": "🔨"},
    "Apprentice": {"exp": 1000, "emoji": "🛠️"},
    "Disciple": {"exp": 5000, "emoji": "⚒️"},
    "Adept": {"exp": 10000, "emoji": "🍀"},
    "Master": {"exp": 20000, "emoji": "〽️"},
    "Grandmaster": {"exp": 50000, "emoji": "🔮"},
    "Legendary": {"exp": 100000, "emoji": "👑"},
    "Legendary II": {"exp": 135000, "emoji": "👑"},
    "Legendary III": {"exp": 175000, "emoji": "👑"},
    "Mythical": {"exp": 200000, "emoji": "🌟"},
    "Mythical II": {"exp": 350000, "emoji": "🌟"},
    "Mythical III": {"exp": 425000, "emoji": "🌟"},
    "Immortal": {"exp": 500000, "emoji": "💀"},
    "Immortal II": {"exp": 650000, "emoji": "💀"},
    "Immortal III": {"exp": 850000, "emoji": "💀"},
    "Radiant": {"exp": 1000000, "emoji": "💫"},
    "Divine": {"exp": 2000000, "emoji": "🔥"},
}


def get_rank(exp):
    current_name = "Recruit"
    current_rank = ranks["Recruit"]
    for key, value in ranks.items():
        if exp >= value["exp"]:
            current_name = key
            current_rank = value
        else:
            break
    return {"name": current_name, "data": current_rank}
