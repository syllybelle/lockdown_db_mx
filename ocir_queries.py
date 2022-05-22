from typing import Dict

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from db_mx.db_config import DbProperties

covid_db: MySQLConnection = DbProperties().connect()

# 18 questions, subdivided into 6 categories, scored on likert scale from 0-4. score of >= 21 is considered positive
# All questions use the same set of options, no reverse scoring


DRY_RUN_MODE = True
RESPONSE_ID = "ResponseId"

question_dict: Dict[str, str] = {
    "1": "I have saved up so many things that they get in the way",
    "2": "I check things more often than necessary",
    "3": "I get upset if objects are not arranged properly",
    "4": "I feel compelled to count while I am doing things",
    "5": "I find it difficult to touch an object when I know it has been touched by strangers or certain people",
    "6": "I find it difficult to control my thoughts",
    "7": "I collect things I don't need",
    "8": "I repeatedly check doors, windows, drawers, etc.",
    "9": "I get upset if others change the way I have arranged things",
    "10": "I feel I have to repeat certain numbers",
    "11": "I sometimes have to wash or clean myself simply because I feel contaminated",
    "12": "I am upset by unpleasant thoughts that come into my mind against my will",
    "13": "I avoid throwing things away because I am afraid I might need them later",
    "14": "I repeatedly check gas and water taps and light switches after turning them off",
    "15": "I need things to be arranged in a particular order",
    "16": "I feel that there are good numbers and bad numbers",
    "17": "I wash my hands more often and longer than necessary",
    "18": "I frequently get nasty thoughts and have difficulty in getting rid of them"
}

options_1: Dict[int, str] = {
    1: "Not at all",
    2: "A little",
    3: "Moderately",
    4: "A lot",
    5: "Extremely"
}

# subgroups: Dict[str, List[str]] = {
#     "hoarding": ["1", "7", "13"],
#     "checking": ["2", "8", "14"],
#     "ordering": ["3", "9", "15"],
#     "neutralising": ["4", "10", "16"],
#     "washing": ["5", "8", "17"],
#     "obsessing": ["6", "9", "18"]
# }

subgroups: Dict[str, str] = {
    "1": "hoarding",
    "2": "checking",
    "3": "ordering",
    "4": "neutralising",
    "5": "washing",
    "6": "obsessing",
    "7": "hoarding",
    "8": "checking",
    "9": "ordering",
    "10": "neutralising",
    "11": "washing",
    "12": "obsessing",
    "13": "hoarding",
    "14": "checking",
    "15": "ordering",
    "16": "neutralising",
    "17": "washing",
    "18": "obsessing"
}


def create_columns() -> None:
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    # OCIR
    i = 0
    while i < 18:
        query: str = f'ALTER TABLE text_questions ADD OCIR_{i + 1} VARCHAR(10)'
        i += 1
        cur.execute(query)
    covid_db.commit()


def build_move_query(source_table: str, column: str, dest_table: str) -> str:
    query: str = f"UPDATE {dest_table}, {source_table} \n" \
                 f"SET {dest_table}.{column}={source_table}.{column} \n" \
                 f"WHERE {dest_table}.{RESPONSE_ID}={source_table}.{RESPONSE_ID};" \
                 f""
    return query


def move_columns() -> None:
    destination_table: str = "text_questions"
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    # # OCIR
    # i = 0
    # while i < 18:
    #     column_name: str = "OCIR_" + str(i + 1)
    #     query: str = build_move_query("ocir", column_name, destination_table)
    #     i += 1
    #     cur.execute(query)
    covid_db.commit()


def comment_columns(questions: Dict[str, str], groups: Dict[str, str]) -> None:
    """creates a comment for each column containing the question"""
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    for key, value in questions.items():
        comment_query: str = f'ALTER TABLE ocir MODIFY q{key} TINYINT(1) COMMENT "Subgroup: {groups[key]}. ' \
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


def query_builder_5(question_number: int, option_list: Dict[int, str]) -> str:
    """creates a query for a given question number with 5 options from a provided dictionary"""
    source_column: str = "OCIR_" + str(question_number)
    dest_column: str = "q" + str(question_number)
    query: str = f"""
        update ocir
            set {dest_column} = case
                when {source_column} = '{option_list[1]}' then 0 
                when {source_column} = '{option_list[2]}' then 1 
                when {source_column} = '{option_list[3]}' then 2
                when {source_column} = '{option_list[4]}' then 3
                when {source_column} = '{option_list[5]}' then 4
            end;
    """
    return query


def transform_options(no_of_questions: int) -> None:
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    i: int = 0
    while i < no_of_questions:
        safe_execute(query_builder_5(i + 1, options_1), cur)
        i += 1
    covid_db.commit()


def main() -> None:
    # move_columns()
    # create_columns()
    # transform_options()
    # comment_columns(question_dict, subgroups)

    """creates string queries for all ocir questions"""
    # transform_options(18)
    # comment_columns(question_dict, subgroups)


main()
