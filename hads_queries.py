from typing import Dict

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from db_mx.db_config import DbProperties

covid_db: MySQLConnection = DbProperties().connect()

"""
14 questions, subdivided into 2 categories, scored on likert scale from 0-3. 
Scoring per subgroup. 0-7 = normal, 8-10 = borderline, 11-21 = abnormal
All questions have individual scoring. 
"""

DRY_RUN_MODE = True
RESPONSE_ID = "ResponseId"

question_dict: Dict[str, str] = {
    "1": "I feel tense or wound up",
    "2": "I feel as if I am slowed down",
    "3": "I still enjoy the things I used to enjoy",
    "4": "I get a sort of frightened feeling like 'butterflies' in the stomach:",
    "5": "I get a sort of frightened feeling as if something awful is about to happen",
    "6": "I have lost interest in my appearance",
    "7": "I can laugh and see the funny side of things",
    "8": "I feel restless as I have to be on the move",
    "9": "Worrying thoughts go through my mind",
    "10": "I look forward with enjoyment to things",
    "11": "I feel cheerful",
    "12": "I can sit at ease and feel relaxed",
    "13": "I get sudden feelings of panic",
    "14": "I can enjoy a good book or programme"
}

no_of_qs: int = len(question_dict)

options_dict: Dict[int, Dict[int, str]] = {
    1: {
        # I feel tense or wound up
        0: "Not at all",
        1: "Occasionally",
        2: "A lot of the time",
        3: "Most of the time"
    },
    2: {
        # I feel as if I am slowed down
        0: "Not at all",
        1: "Sometimes",
        2: "Very often",
        3: "Nearly all of the time"

    },
    3: {
        # I still enjoy the things I used to enjoy
        0: "Definitely as much",
        1: "Not quite so much",
        2: "Only a little",
        3: "Hardly at all"
    },
    4: {
        # I get a sort of frightened feeling like 'butterflies' in the stomach:"""
        0: "Not at all",
        1: "Occasionally",
        2: "Quite often",
        3: "Very often"
        },
    5: {
        # I get a sort of frightened feeling as if something awful is about to happen
        0: "Not at all",
        1: "A little",
        2: "Not too badly",
        3: "Quite badly"
        },
    6: {
        # I have lost interest in my appearance
        0: "I take just as much care as ever",
        1: "I make not take quite as much care",
        2: "I don't take as much care as I should",
        3: "Definitely"
    },
    7: {
        # I can laugh and see the funny side of things
        0: "As much as I always could",
        1: "Not quite so much now",
        2: "Definitely not so much now",
        3: "Not at all"
    },
    8: {
        # I feel restless as I have to be on the move
        0: "Not at all",
        1: "Not very much",
        2: "Quite a lot",
        3: "Very much indeed"
    },
    9: {
        # Worrying thoughts go through my mind
        0: "Only occasionally",
        1: "From time to time",
        2: "A lot of the time",
        3: "A great deal of the time"
        },
    10: {
        # I look forward with enjoyment to things
        0: "As much as I ever did",
        1: "Rather less than I used to",
        2: "Definitely less than I used to",
        3: "Hardly at all"
        },
    11: {
        # I feel cheerful
        0: "A lot",
        1: "Sometimes",
        2: "Not often",
        3: "Not at all"
    },
    12: {
        # I can sit at ease and feel relaxed
        0: "Definitely",
        1: "Usually",
        2: "Not often",
        3: "Not at all"
    },
    13: {
        # I get sudden feelings of panic
        0: "Not at all",
        1: "Not often",
        2: "Sometimes",
        3: "Very often"
    },
    14: {
        # I can enjoy a good book or programme
        0: "Often",
        1: "Sometimes",
        2: "Not often",
        3: "Very seldon"
    }
}

subgroups: Dict[str, str] = {
    "1": "anxiety",
    "2": "depression",
    "3": "depression",
    "4": "anxiety",
    "5": "anxiety",
    "6": "depression",
    "7": "depression",
    "8": "anxiety",
    "9": "anxiety",
    "10": "depression",
    "11": "depression",
    "12": "anxiety",
    "13": "anxiety",
    "14": "depression"
}


def build_move_query(source_table: str, column: str, dest_table: str) -> str:
    query: str = f"UPDATE {dest_table}, {source_table} \n" \
                 f"SET {dest_table}.{column}={source_table}.{column} \n" \
                 f"WHERE {dest_table}.{RESPONSE_ID}={source_table}.{RESPONSE_ID};" \
                 f""
    return query


def create_columns(number_of_qs: int) -> None:
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    i = 0
    while i < number_of_qs:
        query: str = f'ALTER TABLE hads ADD q{i + 1} tinyint(1)'
        i += 1
        cur.execute(query)
    covid_db.commit()


def move_columns() -> None:
    destination_table: str = "text_questions"
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    # HADS
    i = 0
    while i < 14:
        column_name: str = "HADS_" + str(i + 1)
        query: str = build_move_query("hads", column_name, destination_table)
        i += 1
        cur.execute(query)
    covid_db.commit()


def comment_columns(questions: Dict[str, str], groups: Dict[str, str]) -> None:
    """creates a comment for each column containing the question"""
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    for key, value in questions.items():
        comment_query: str = f'ALTER TABLE hads MODIFY q{key} TINYINT(1) COMMENT "Subgroup: {groups[key]}. ' \
                             f'Question: {value}";'
        input_value: str = safe_execute(comment_query, cur)
        if input_value == "n":
            break
    covid_db.commit()


def safe_execute(query: str, cur: MySQLCursor) -> str:
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


def DANGEROUS_execute(query: str, cur: MySQLCursor) -> str:
    print(query)
    cur.execute(query)
    return "y"


def build_query(question_no: int, options: Dict[int, str]) -> str:
    """creates all queries using a dictionary containing the responses for each question"""
    # key: int, value: Dict[int, str]
    source_column: str = "HADS_" + str(question_no)
    dest_column: str = "q" + str(question_no)
    cases: str = ""
    for option_no, question_text in options.items():
        cases += f'when {source_column} = "{question_text}" then {option_no} \n'
    query: str = f"""
        update hads
            set {dest_column} = case
                {cases}
            end;
        """
    return query


def transform_options() -> None:
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    for question_no, options in options_dict.items():
        result: str = safe_execute(build_query(question_no, options), cur)
        if result == 'n':
            break
    covid_db.commit()


def main() -> None:
    """creates string queries for all hads questions"""
    # move_columns()
    # create_columns(no_of_qs)
    transform_options()
    # comment_columns(question_dict, subgroups)


main()
