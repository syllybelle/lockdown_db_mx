import unicodedata
from typing import Dict, List, Set

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from db_mx.db_config import DbProperties

covid_db: MySQLConnection = DbProperties().connect()
RESPONSE_ID = "ResponseId"
DRY_RUN_MODE = True

zero_scoring_ids: List[str] = ["R_1C2Nvn9hF0TlXAM", "R_1esEk9xNs4rhvSo", "R_1kTiMsWyipy2zCb", "R_1kTVFKFErSuUhmE",
                               "R_1o0H0AxuHMO0mIG", "R_24pmO4VoYi7u4qz", "R_24X92PX6PwAvNM5", "R_25NtqxqecfLs1Uk",
                               "R_2900JEZ6QPEVeOZ", "R_29mQfr3oL0jfNoD", "R_2OVWyamhV8TFcSf", "R_2QGI6mfVGIPO2MN",
                               "R_2rdEMn0LsT1NxjH", "R_3eleXmtn4Mh0tKb", "R_3e8hgA0qJBhAufC", "R_3HBUe0hrbedJobf",
                               "R_3McHwH3oLgRsAUt", "R_eDxIaZUZcc2XwM9", "R_1g0gGa6LnbOyuTL", "R_1Ho5RevKYwifzoL",
                               "R_1iq7f7dLUKfHTe6", "R_1NnqGzZnVv9NEVe", "R_1nO5gC12ysrhRiB", "R_2f0yW0B9vTo2vDi",
                               "R_6m7z1KVFOdQQIYV", "R_8dJqj4CaMGgm35v", "R_BsMfIjrN3O9DKXn", "R_2yl5e4V8B5UZiNn",
                               "R_3L4KM3YO1cgK0T4", "R_2vdEjd3YL6DaEWc"]
translated_responses: Dict[str, str] = {
    "R_1jWaEHKIRg2eIOk": 'DANCING, SILENCE, SHAKE, NOT DEAD, INVISIBLE, KISS, FEAR, PROPHET',
    "R_1mngOPI0Lg7RvpF": 'kissing, bus, fear, scientist, priest, folding, multiplies, bird singing, '
                         'silence, door, cardboard, secretly,',
    "R_1MSsqR45puZ9GJc": 'viral, shudder, door, carton, sack, vegetables, imagining, swarming, undead, sucking, lungs, '
                         'kissing, jumping, bus, fear, plain, risk, charlatan, prophet, scientist, secretly, priest, '
                         'submission, multiplies, delighted, birds singing, dancing, silence ',
    "R_1OYOVQjVivDcbg7": 'viral, bag, bus, door, bird song',
    "R_2akK4RJTO43byVG": 'viral, shudder, door, carton, sack of vegetables, swarming, undead, kissing, bus, fear, '
                         'lungs, plain, risk, jumping in,',
    "R_3kk14qRrJ0Awr4x": 'singing bird, quack, priest, fear, viral, door, undead, cardboard, vegetables, vegetables',
    "R_SNSU9tYCB3EM9ih": 'viral, shudder, cardboard, sack, sucking, bus, fear, risk, plain',
    "R_1QavI6Gv6lpOiES": 'Viralize, door, cardboard, bag, vegetables, undead, lifeless, kiss, climb, fear.',
    "R_2uJNufxGSKtQDDZ": 'hello, covid, death, virus, money, sex, drugs',
    "R_30ujMEwnwQzfri5": 'Climb, fear, ordinary, bird, silence, carton, vegetables  flora, viralise, lungs, risk, '
                         'effort',
    "R_6h4VQa2gs5VXZTj": 'gymse',
    "R_AjKDPOPl6Kuf9aV": 'priest, kiss',
    "R_Y3LualhYSKbWXAJ": 'fear, virologist,',
    "R_1Y0E18a2A86bQ6B": 'Kissing lungs',
    "R_2roPhyRqJ4aUFCK": 'priest',
    "R_3NUKi6InGBW0VQ9": 'Birdsong, quack, fear, doctors, fast, scary',
    "R_WljVLhyJLAvjrwJ": 'peacocks, priest',
    "R_2dgwXnnovdlSlDo": 'viral, lungs shake swarm door',
    "R_A1BpM7J4H6s4ToB": 'viral, kiss, vegetable, bird',
    "R_3nUT1KWOXBTGWei": 'fear, virus, bus',
    "R_1dAJsOvEKBUda9D": 'fear, bus, body',
    "R_qIwcj0OgQKoMEr7": 'Kissing, bus, submitting, priest, thrilled, bag, viral, carton, vegetables, dancing, '
                         'birdsong, silence, jumping, fear, risk, ordinary',
    "R_pmWx62gTWH8plAd": 'viral, door, carton, bag, vegetables, unliving, undead, imagining, bus, fear, priest, risk, '
                         'kissing, jumping,',
    "R_2YQxvyOZAfoKD8V": 'viral, door, carton, bag, swarming, lungs, kissing, jumping, bus, quack, ordinary, priest, '
                         'dancing, silence',
    "R_1faeQGmAQ0QpYAQ": 'viral, shuddering, door, carton, bag, vegetables, imagining, swarming, unseeable, undead, '
                         'unliving, suctuin, lungs, kissing, jumping, bus, fear, ordinary, risk, quack scietist, '
                         'secretly, priest submiting',
    "R_1es0YS0XT2ACzxt": "VIRAL,DOOR,CARTON, BAG VEGETABLES,IMAGINING,UNSECABLE,BUS ,PROPHET,SCIENTIST,BIRDSONG,"
                         "DANCING,FEAR, risk, BLOBS,SUCTION,",
    "R_0BNDKuheaDzLlMB": 'viral, shuddering, door, bag, vegetables, fear, ordinary, risk, quack,  dancing, silence',
    "R_3gZZaa4sWZP93YF": "bold"
}

fetch_data_query: str = f"""
                        select ResponseId, free_recall 
                        FROM covid_data.free_recall 
                        where free_recall is not null;
                        """
fetch_non_matching_data_query: str = f"""
                        select non_matching_words 
                        FROM covid_data.free_recall 
                        where free_recall_input is not null;
                        """

recall_words: Set[str] = {"viral", "shuddering", "door", "carton", "bag", "vegetables", "imagining", "swarming",
                          "unseeable", "undead", "unliving", "suction", "lungs", "kissing", "jumping", "bus", "fear",
                          "ordinary", "risk", "quack", "prophet", "scientist", "secretly", "priest", "submitting",
                          "proliferates", "thrilled", "birdsong", "dancing", "silence"}
abstract_words: Set[str] = {"viral", "imagining", "unseeable", "undead", "unliving", "fear", "ordinary", "risk",
                            "secretly", "submitting", "proliferates", "thrilled", "silence", "birdsong", "dancing",
                            "shuddering", "suction", "quack"}
concrete_words: Set[str] = {"door", "carton", "bag", "vegetables", "swarming", "lungs", "kissing", "jumping", "bus",
                            "prophet", "scientist", "priest"}
neutral_words: Set[str] = {"door", "carton", "bag", "vegetables", "imagining", "suction", "lungs", "jumping", "bus",
                           "ordinary", "quack", "scientist", "submitting", "proliferates", "silence"}
emotional_words: Set[str] = {"viral", "shuddering", "swarming", "unseeable", "undead", "unliving", "kissing", "fear",
                             "risk", "secretly", "thrilled", "birdsong", "dancing", "prophet", "priest"}

# typo config
# map of typos to correct words
typos: Dict[str, str] = {}
typo_config: Dict[str, List[str]] = {
    "viral": ["viral”", "virual", "viural", "virale", "virul", "virial", "varial"
              # , "virus", "wirus", "viruses", "viralise", "viralizarse", "virologic", "viruis", "viralize",
              # "virologist", "virusologist", "vital", "virilizarse", "viralizs", "virologist"
              ],
    "shuddering": ["shaddering", "shruddering", "shurddering", "shudddering", "shudering", "shuderring", "schuddering"
                   # "shudders", "shudders", "shuddered", "shudderry", "shuderry", "shivering", "shrudding",
                   # "shadered", "shudder", "shiver", "shaking", "shake", "flinch", "shrudder", "pudder", "flutter"
                   ],
    "door": ["doors", "doord", "doo", "dior", "oor",
             # "doorknob", "doorway", "doorhandle"
             ],
    "carton": ["cardon", "cartons", "carto",
               # "cart", "cartoon", "cartoons", "cartoony", "box", "package"
               ],
    "bag": ["bags", "bah"
            # "sack", "sac"
            ],
    "vegetables": ["vagetables", "vedgetables", "vegatables", "vegateables", "vegeta", "veggetables",
                   "vegtables", "vegetable", "vegeables", "vegetbles", "vegetabels", "vegitable",
                   "vegetales", "vegetalbles", "vegeatables", "vegetale"
                   # "vegetarian",
                   ],
    "imagining": ["imaginning", "imagininf", "inagininf", "imaganing"
                  # "imaginating", "unimagianble", "unimaginable", "imageing", "imagine", "imaginable", "imaging",
                  # "image", "imagination", "imaginary",
                  ],
    "swarming": ["swaming", "sawrming", "swarning",
                 # "swarmed", "swarm", "teeming"
                 ],
    "unseeable": ["unsecable", "unseable", "useeable", "inseeable", "unseesable", "unsseable", "unseaable", "unseealbe",
                  "unseeabel", "unseedable"
                  # "unseen", "unseeing", "unseen", "see", "unforseen", "unnseeing", "sea", "unsean",
                  # "forseable", "unseeded", "seed", "seeds", "unsee", "unseething", "unseed", "unseeded", "invisible",
                  # "unforseen", "unsimeengly"
                  ],
    "undead": ["udead", "unded", "undeae", "undeed"
               # , "dead", "undeadble", "deadly", "undeadly", "undeath", "undying", "notdead"
               ],
    "unliving": ["univing", "unlicing", "unliiving", "unliing", "inlivig", "inliving", "unlivings"
                 # , "living", "unlivining", "unlived", "unlivable", "ulively", "unliveable", "unlivable", "lifeless",
                 # "inanimate",
                 ],
    "suction": ["sunction", "suctuin", "succion", "suctio", "uction", "suctions"
                # , "sucking", "suckers", "suck", "sucker", "suctioning",
                ],
    "lungs": ["lung", "lugs"
              # , "luts"
              ],
    "kissing": ["kisssing", "kissig", "kising"
                # , "kiss", "kissed", "kisse", "kisses", "kidding"
                ],
    "jumping": ["jumbing", "jumkping", "jumpiong", "jmping"
                # , "jump", "jumper", "jung", "spring"
                ],
    "bus": ["buss", "buw"
            # , "bud", "bug"
            ],
    "fear": [
        # "feat", "fest", "scare", "scared", "scary"
    ],
    "ordinary": ["odrinary", "ordanary", "ordinairy", "oridinary", "orinary"
                 # "usual",
                 ],
    "risk": ["risj", "risks", "riska"
             # "riest", "rinsk"
             ],
    "quack": ["quak", "quac", "quacks",
              # "quacking", "charlatan", "quark", "quick", "quarck"
              ],
    "prophet": ["prophets", "propher", "propphet", "prophits", "prophit", "propeht", "profet", "prophes", "phophet",
                "prhphet", "prophed"
                # , "profit", "profiterole", "profiteroles",
                ],
    "scientist": ["scientists", "sciencist", "cientist", "scientins", "scientinst", "scientistm", "sientist",
                  "sceinctist", "scientis", "scientisti", "scietist", "sciencists"
                  # "sciets", "science", "scientific", "cience", "sciece",
                  ],
    "secretly": ["secretely", "secratly", "sicretly", "sectetly", "secretlym", "secretl"
                 # "secret", "secretive", "secrecy", "secretively"
                 ],
    "priest": ["priests", "pries", "priste", "preist", "preists", "pruest", "piest", "pirest"
               # "bishops",
               ],
    "submitting": ["submiting", "sibmitting", "submittinging", "submimting", "submmiting"
                   # "submit", "submitted", "submission", "subliming", "submittions",
                   ],
    "proliferates": ["proliferate", "prolipherate", "prolifiates", "proliforates", "proliferathes", "prolifelates",
                     "profilerate", "prolieferates", "prolifeates", "prolifilate", "prolifarate", "porilifarate",
                     "proliferated",
                     # "profiterole", "prolifertating", "proliferating", "prolifering", "reproduce", "profiferantes",
                     # "preforious", "proliferation", "prolific", "profligate", "prolificience", "profiteroles",
                     # "multiplies", "spread", "spreads"
                     ],
    "thrilled": ["thriled", "trilled",
                 # "thrilling", "thrills", "thrill", "thriller", "delighted"
                 ],
    "birdsong": ["bridsong", "birdson", "birdsongt", "birdsony", "birdsongs",
                 # "brids", "birds", "bird", "birdcage", "song", "singing", "birdchips", "sing", "songbirds",
                 # "songbird", "songbirds"
                 ],
    "dancing": ["dansing", "danxing", "bancing", "dacing", "danching"
                # "dance", "dancer"
                ],
    "silence": ["silience", "slience"
                # "silent", "silenced", "silences",
                ]
}
for correct_word, typo_list in typo_config.items():
    for typo in typo_list:
        typos[typo] = correct_word


def detypo(word: str) -> str:
    if word in typos:
        return typos[word]
    return word


def reset_data() -> None:
    query: str = f"""UPDATE covid_data.free_recall \n
                SET free_recall.free_recall = free_recall.free_recall_input;
                ;"""
    DANGEROUS_execute(query)
    covid_db.commit()


def correct_answers() -> None:
    for each in zero_scoring_ids:
        query: str = f"UPDATE covid_data.free_recall \n" \
                     f"SET free_recall.free_recall = '0' \n" \
                     f"WHERE {RESPONSE_ID} = '{each}';"
        DANGEROUS_execute(query)
    for each, response in translated_responses.items():
        query: str = f"UPDATE covid_data.free_recall \n" \
                     f'SET free_recall.free_recall = "{response}" \n' \
                     f'WHERE {RESPONSE_ID} = "{each}";'
        DANGEROUS_execute(query)
    covid_db.commit()


def clean_up(data: List[Dict[str, str]]) -> Dict[str, List[str]]:
    # row = list items
    # column_name = key in dict
    # value = value of column name
    clean_data: Dict[str, List[str]] = {}
    for row in data:
        # normalise separators
        free_recall_string: str = row['free_recall']
        free_recall_string = unicodedata.normalize("NFKD", free_recall_string.replace(" and ", " ").lower())
        free_recall_string = free_recall_string.replace("bird song", "birdsong")
        free_recall_string = free_recall_string.replace("not dead", "notdead")
        free_recall_string = free_recall_string.replace(" or ", " ")
        free_recall_string = free_recall_string.replace("¨", " ")
        free_recall_string = free_recall_string.replace('"', " ")
        free_recall_string = free_recall_string.replace(" to ", " ")
        free_recall_string = free_recall_string.replace(" ", ",")
        free_recall_string = free_recall_string.replace("?", ",")
        free_recall_string = free_recall_string.replace("!", ",")
        free_recall_string = free_recall_string.replace(".", ",")
        free_recall_string = free_recall_string.replace(";", ",")
        free_recall_string = free_recall_string.replace("-", ",")
        free_recall_string = free_recall_string.replace(",,", ",")
        free_recall_string = free_recall_string.replace(",,", ",")
        key: str = row['ResponseId']

        # correct typos, remove duplicates
        unique_words: Set[str] = set()
        for word in free_recall_string.split(','):
            unique_words.add(detypo(word))
        unique_word_list: List[str] = []
        for word in unique_words:
            unique_word_list.append(word)

        clean_data[key] = unique_word_list
    return clean_data


def score_data(data: Dict[str, List[str]]) -> None:
    """assigns score for each word in list and sends query and commits changes to database"""
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    for response_id, words in data.items():
        total_score: int = 0
        total_abstract: int = 0
        total_concrete: int = 0
        total_neutral: int = 0
        total_emotional: int = 0
        non_matching_words: List[str] = []
        for word in words:
            if word in recall_words:
                total_score += 1
            else:
                non_matching_words.append(word)
            if word in abstract_words:
                total_abstract += 1
            if word in concrete_words:
                total_concrete += 1
            if word in neutral_words:
                total_neutral += 1
            if word in emotional_words:
                total_emotional += 1
        words_clean: str = ",".join(words).replace("'", "")
        non_matching_words_clean: str = ",".join(non_matching_words).replace("'", "")
        query: str = f"""
            update covid_data.free_recall
            set free_recall = '{words_clean}',
                total_score = {total_score}, 
                total_abstract = {total_abstract},
                total_concrete = {total_concrete},
                total_neutral = {total_neutral},
                total_emotional = {total_emotional},
                non_matching_words = '{non_matching_words_clean}'
            where ResponseId = '{response_id}'
        """
        DANGEROUS_execute(query)
    covid_db.commit()


def DANGEROUS_execute(query: str) -> str:
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    print(query)
    cur.execute(query)
    return "y"


def safe_execute(query: str) -> str:
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    print(query)
    input_value: str = input("Execute? (y)es/(n)o/(a)bort: ")
    if input_value == "y":
        if DRY_RUN_MODE:
            print("Not executing (Dry-run).")
        else:
            cur.execute(query)
    elif input_value == "a":
        exit(1)
    return input_value


def create_unique_list(data: List[Dict[str, str]]) -> Set[str]:
    incorrect_words: Set[str] = set()
    # Dict key = column name, value = incorrect words
    for row in data:
        word_string: str = row['non_matching_words']
        word_list: List[str] = word_string.split(",")
        for word in word_list:
            incorrect_words.add(word)
    return incorrect_words


def main() -> None:
    cursor: MySQLCursor = covid_db.cursor(dictionary=True)
    # reset_data()
    # correct_answers()
    cursor.execute(fetch_data_query)
    raw_data: List[Dict[str, str]] = cursor.fetchall()
    print(raw_data)
    clean_data: Dict[str, List[str]] = clean_up(raw_data)
    score_data(clean_data)


main()

# def secondary() -> None:
#     """to be run after main transformation, to compile a list of words that did not match"""
#     cursor: MySQLCursor = covid_db.cursor(dictionary=True)
#     cursor.execute(fetch_non_matching_data_query)
#     new_data: List[Dict[str, str]] = cursor.fetchall()
#     wrong_words: Set[str] = create_unique_list(new_data)
#     print(wrong_words)

# secondary()
