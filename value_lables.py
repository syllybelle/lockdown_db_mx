from typing import Dict

ld_options_1: Dict[int, str] = {
    1: "None of the time",
    2: "Hardly ever",
    3: "Some of the time",
    4: "Nearly all the time",
    5: "Completely"
}
ld_options_2: Dict[int, str] = {
    1: "None of the time",
    2: "Hardly ever",
    3: "Some of the time",
    4: "Nearly all the time",
    5: "Often"
}
ld_options_3: Dict[int, str] = {
    0: "No",
    1: "Yes"
}
ld_options_4: Dict[int, str] = {
    1: "I am not following any of the recommendations",
    2: "Hardly any recommendations",
    3: "Some recommendations",
    4: "Most recommendations",
    5: "All recommendations"
}
ld_options_5: Dict[int, str] = {
    1: "None of the time",
    2: "Hardly ever",
    3: "Some of the time",
    4: "Worse than usual",
    5: "Completely"
}
ld_options_6: Dict[int, str] = {
    1: "Eating less than usual",
    2: "Eating more or less the same as usual",
    3: "Eating more than usual",
}
ld_options_7: Dict[int, str] = {
    1: "Definitely not",
    2: "Not really",
    3: "Unsure",
    4: "Somewhat",
    5: "Definitely"
}
ld_options_8: Dict[int, str] = {
    1: "Definitely not",
    2: "Unlikely",
    3: "Unsure",
    4: "Likely",
    5: "Certain"
}
ld_options_9: Dict[int, str] = {
    1: "Inconsistently and confused",
    2: "Somewhat inconsistent and confused",
    3: "Unsure",
    4: "Somewhat consistent and organised",
    5: "Consistently and organised"
}
ld_options_10: Dict[int, str] = {
    1: "Less than once a week or never",
    2: "Once a week",
    3: "Once every few days",
    4: "Once a day",
    5: "Daily or more frequenty"
}
ocir_options: Dict[int, str] = {
    1: "Not at all",
    2: "A little",
    3: "Moderately",
    4: "A lot",
    5: "Extremely"}
srq_options: Dict[int, str] = {
    1: "Strongly disagree",
    2: "Disagree",
    3: "Uncertain or unsure",
    4: "Agree",
    5: "Strongly agree"
}

demographics_variables: Dict[str, Dict[int, str]] = {
    "progress_group": {0: "LD not complete",
                       1: "LD complete, OCIR not complete",
                       2: "OCIR complete, SRQ not complete",
                       3: "SRQ complete, HADS not complete",
                       4: "HADS complete"},
    "cluster": {1: "general population",
                2: "extreme responders",
                3: "sufferers"},
    "consent": {0: "no consent",
                1: "consent given"},
    "dem_1_age_group": {0: "<18 or > 75>",
                        1: "18-21",
                        2: "22-25",
                        3: "26-32",
                        4: "33-75"},
    "dem_2_gender": {1: "Male",
                     2: "Female",
                     3: "Prefer not to be identified by gender",
                     4: "Other", },
    "dem_3_country": {
        8: "Albania",
        24: "Angola",
        36: "Australia",
        50: "Bangladesh",
        56: "Belgium",
        76: "Brazil",
        100: "Bulgaria",
        124: "Canada",
        144: "Sri Lanka",
        152: "Chile",
        158: "Taiwan, Republic of China",
        203: "Czech Republic",
        208: "Denmark",
        233: "Estonia",
        246: "Finland",
        250: "France",
        268: "Georgia",
        276: "Germany",
        300: "Greece",
        344: "Hong Kong, SAR China",
        348: "Hungary",
        356: "India",
        360: "Indonesia",
        372: "Ireland",
        376: "Israel",
        380: "Italy",
        392: "Japan",
        410: "Korea (South)",
        428: "Latvia",
        458: "Malaysia",
        484: "Mexico",
        504: "Morocco",
        528: "Netherlands",
        566: "Nigeria",
        578: "Norway",
        586: "Pakistan",
        616: "Poland",
        620: "Portugal",
        642: "Romania",
        643: "Russian Federation",
        705: "Slovenia",
        710: "South Africa",
        724: "Spain",
        752: "Sweden",
        756: "Switzerland",
        760: "Syrian Arab Republic (Syria)",
        804: "Ukraine",
        826: "United Kingdom",
        840: "United States of America"},
    "dem_3_continent": {
        1: "North America",
        2: "Western Europe",
        3: "Central and Eastern Europe",
        4: "Latin America and the Caribbean",
        5: "Asia and Australasia",
        6: "Middle East and North Africa",
        7: "Sub-Saharan Africa"},
    "dem_3_hrs_group": {
        1: "score of < -3",
        2: "score of >= -3 , < -2",
        3: "score of >= -2 , < -1",
        4: "score of >= -1 , < 0",
        5: "score of >= 0, < 1",
        6: "score of >= 1, < 2",
        7: "score of >= 2, < 3",
        8: "score of >= 3"},
    "dem_3_hdi_group": {
        1: "low: < 0.55",
        2: "medium >= 0.55, <0.7",
        3: "high >= 0.7, <0.8",
        4: "very high >= 0.8, <0.9",
        5: "exceptionally high >= 0.9"},
    "dem_4_politics": {1: "Far left",
                       2: "Left",
                       3: "Central",
                       4: "Right",
                       5: "Far right",
                       0: "No political interest"},
    "dem_5_brexit": {2: "For Brexit (to leave the European Union)",
                     4: "For Remain (to stay in the European Union)",
                     3: "Undecided",
                     0: "Not interested",
                     1: "Other"},
    "dem_6_loe": {10: "phd degree",
                  9: "phd incomplete",
                  8: "masters/postgraduate degree",
                  7: "masters/postgraduate incomplete",
                  6: "undergraduate degree",
                  5: "undergraduate incomplete",
                  4: "college/A-levels/diploma",
                  3: "high school completed",
                  2: "vocational/technical school",
                  1: "school incomplete",
                  # '': "unknown",
                  0: "invalid"}}
ld_variables: Dict[str, Dict[int, str]] = {
    "q1": ld_options_1,
    "q2": ld_options_1,
    "q3": ld_options_1,
    "q4": ld_options_1,
    "q5": ld_options_1,
    "q6": ld_options_1,
    "q7": ld_options_1,
    "q8": ld_options_2,
    "q9": ld_options_2,
    "q10": ld_options_2,
    "q11": ld_options_2,
    "q12": ld_options_2,
    "q13": ld_options_2,
    "q14": ld_options_2,
    "q15": ld_options_2,
    "q16": ld_options_3,
    "q17": ld_options_3,
    "q18": ld_options_2,
    "q19": ld_options_1,
    "q20": ld_options_1,
    "q21": ld_options_1,
    "q22": ld_options_1,
    "q23": ld_options_1,
    "q24": ld_options_1,
    "q25": ld_options_1,
    "q26": ld_options_1,
    "q27": ld_options_1,
    "q28": ld_options_4,
    "q29": ld_options_5,
    "q30": ld_options_6,
    "q31": ld_options_7,
    "q32": ld_options_7,
    "q33": ld_options_7,
    "q34": ld_options_7,
    "q35": ld_options_7,
    "q36": ld_options_1,
    "q37": ld_options_1,
    "q38": ld_options_1,
    "q39": ld_options_1,
    "q40": ld_options_1,
    "q41": ld_options_8,
    "q42": ld_options_8,
    "q43": ld_options_8,
    "q44": ld_options_8,
    "q45": ld_options_8,
    "q46": ld_options_8,
    "q47": ld_options_8,
    "q48": ld_options_9,
    "q49": ld_options_8,
    "q50": ld_options_8,
    "q51": ld_options_8,
    "q52": ld_options_8,
    "q53": ld_options_8,
    "q54": ld_options_10}
ocir_variables: Dict[str, Dict[int, str]] = {
    "q1": ocir_options,
    "q2": ocir_options,
    "q3": ocir_options,
    "q4": ocir_options,
    "q5": ocir_options,
    "q6": ocir_options,
    "q7": ocir_options,
    "q8": ocir_options,
    "q9": ocir_options,
    "q10": ocir_options,
    "q11": ocir_options,
    "q12": ocir_options,
    "q13": ocir_options,
    "q14": ocir_options,
    "q15": ocir_options,
    "q16": ocir_options,
    "q17": ocir_options,
    "q18": ocir_options}
srq_variables: Dict[str, Dict[int, str]] = {
    "q1": srq_options,
    "q2": srq_options,
    "q3": srq_options,
    "q4": srq_options,
    "q5": srq_options,
    "q6": srq_options,
    "q7": srq_options,
    "q8": srq_options,
    "q9": srq_options,
    "q10": srq_options,
    "q11": srq_options,
    "q12": srq_options,
    "q13": srq_options,
    "q14": srq_options,
    "q15": srq_options,
    "q16": srq_options,
    "q17": srq_options,
    "q18": srq_options,
    "q19": srq_options,
    "q20": srq_options,
    "q21": srq_options,
    "q22": srq_options,
    "q23": srq_options,
    "q24": srq_options,
    "q25": srq_options,
    "q26": srq_options,
    "q27": srq_options,
    "q28": srq_options,
    "q29": srq_options,
    "q30": srq_options,
    "q31": srq_options,
    "q32": srq_options,
    "q33": srq_options,
    "q34": srq_options,
    "q35": srq_options,
    "q36": srq_options,
    "q37": srq_options,
    "q38": srq_options,
    "q39": srq_options,
    "q40": srq_options,
    "q41": srq_options,
    "q42": srq_options,
    "q43": srq_options,
    "q44": srq_options,
    "q45": srq_options,
    "q46": srq_options,
    "q47": srq_options,
    "q48": srq_options,
    "q49": srq_options,
    "q50": srq_options,
    "q51": srq_options,
    "q52": srq_options,
    "q53": srq_options,
    "q54": srq_options,
    "q55": srq_options,
    "q56": srq_options,
    "q57": srq_options,
    "q58": srq_options,
    "q59": srq_options,
    "q60": srq_options,
    "q61": srq_options,
    "q62": srq_options,
    "q63": srq_options}
hads_variables: Dict[str, Dict[int, str]] = {
    "q1": {0: "Not at all",
           1: "Occasionally",
           2: "A lot of the time",
           3: "Most of the time"},
    "q2": {0: "Not at all",
           1: "Sometimes",
           2: "Very often",
           3: "Nearly all of the time"},
    "q3": {0: "Definitely as much",
           1: "Not quite so much",
           2: "Only a little",
           3: "Hardly at all"},
    "q4": {0: "Not at all",
           1: "Occasionally",
           2: "Quite often",
           3: "Very often"},
    "q5": {0: "Not at all",
           1: "A little",
           2: "Not too badly",
           3: "Quite badly"},
    "q6": {0: "I take just as much care as ever",
           1: "I make not take quite as much care",
           2: "I dont take as much care as I should",
           3: "Definitely"},
    "q7": {0: "As much as I always could",
           1: "Not quite so much now",
           2: "Definitely not so much now",
           3: "Not at all"},
    "q8": {0: "Not at all",
           1: "Not very much",
           2: "Quite a lot",
           3: "Very much indeed"},
    "q9": {0: "Only occasionally",
           1: "From time to time",
           2: "A lot of the time",
           3: "A great deal of the time"},
    "q10": {0: "As much as I ever did",
            1: "Rather less than I used to",
            2: "Definitely less than I used to",
            3: "Hardly at all"},
    "q11": {0: "A lot",
            1: "Sometimes",
            2: "Not often",
            3: "Not at all"},
    "q12": {0: "Definitely",
            1: "Usually",
            2: "Not often",
            3: "Not at all"},
    "q13": {0: "Not at all",
            1: "Not often",
            2: "Sometimes",
            3: "Very often"},
    "q14": {0: "Often",
            1: "Sometimes",
            2: "Not often",
            3: "Very seldon"},
}


def write_compiled_query() -> str:
    big_query: str = ""
    for column, options in demographics_variables.items():
        query: str = f"VALUE LABELS {column} \n"
        for option_no, text_val in options.items():
            temp_string: str = f"{option_no} '{text_val}' "
            query += temp_string + "\n"
        big_query += query + "\n"
    for column, options in ld_variables.items():
        query: str = f"VALUE LABELS ld_{column} \n"
        for option_no, text_val in options.items():
            temp_string: str = f"{option_no} '{text_val}' "
            query += temp_string + "\n"
        big_query += query + "\n"
    for column, options in ocir_variables.items():
        query: str = f"VALUE LABELS ocir_{column} \n"
        for option_no, text_val in options.items():
            temp_string: str = f"{option_no} '{text_val}' "
            query += temp_string + "\n"
        big_query += query + "\n"
    for column, options in srq_variables.items():
        query: str = f"VALUE LABELS srq_{column} \n"
        for option_no, text_val in options.items():
            temp_string: str = f"{option_no} '{text_val}' "
            query += temp_string + "\n"
        big_query += query + "\n"
    for column, options in hads_variables.items():
        query: str = f"VALUE LABELS hads_{column} \n"
        for option_no, text_val in options.items():
            temp_string: str = f"{option_no} '{text_val}' "
            query += temp_string + "\n"
        big_query += query + "\n"
    return big_query


def write_demographics_query() -> str:
    big_query: str = ""
    for column, options in demographics_variables.items():
        query: str = f"VALUE LABELS {column} \n"
        for option_no, text_val in options.items():
            temp_string: str = f"{option_no} '{text_val}' "
            query += temp_string + "\n"
        big_query += query + "\n"
    return big_query


def write_lockdown_query() -> str:
    big_query: str = ""
    for column, options in ld_variables.items():
        query: str = f"VALUE LABELS {column} \n"
        for option_no, text_val in options.items():
            temp_string: str = f"{option_no} '{text_val}' "
            query += temp_string + "\n"
        big_query += query + "\n"
    return big_query


def write_ocir_query() -> str:
    big_query: str = ""
    for column, options in ocir_variables.items():
        query: str = f"VALUE LABELS {column} \n"
        for option_no, text_val in options.items():
            temp_string: str = f"{option_no} '{text_val}' "
            query += temp_string + "\n"
        big_query += query + "\n"
    return big_query


def write_srq_query() -> str:
    big_query: str = ""
    for column, options in srq_variables.items():
        query: str = f"VALUE LABELS {column} \n"
        for option_no, text_val in options.items():
            temp_string: str = f"{option_no} '{text_val}' "
            query += temp_string + "\n"
        big_query += query + "\n"
    return big_query


def write_hads_query() -> str:
    big_query: str = ""
    for column, options in hads_variables.items():
        query: str = f"VALUE LABELS {column} \n"
        for option_no, text_val in options.items():
            temp_string: str = f"{option_no} '{text_val}' "
            query += temp_string + "\n"
        big_query += query + "\n"
    return big_query


def main() -> None:
    print(write_compiled_query())
    print(write_demographics_query())
    print(write_hads_query())
    print(write_lockdown_query())
    print(write_ocir_query())
    print(write_srq_query())

# main()
