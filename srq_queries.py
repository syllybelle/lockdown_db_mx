from typing import Dict, List

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from db_mx.db_config import DbProperties

covid_db: MySQLConnection = DbProperties().connect()

# 63 questions, subdivided into 7 categories, scored on likert scale from 1-5.
# >= 239 - intact self regulation, 214-338 - intermediate self regulation capacity, <=213, low/impaired self-regulation
# All questions use the same set of options, some questions have reverse scoring.


DRY_RUN_MODE = True
RESPONSE_ID = "ResponseId"

# FIXME: should be hash-set
reverse_scored_questions: List[str] = [2, 3, 4, 5, 6, 8, 10, 12, 13, 15, 19, 20, 21, 24, 26,
                                       29, 31, 33, 37, 40, 43, 45, 50, 55, 62, 63]
max_question_score: int = 5
question_dict: Dict[str, str] = {
    "1": "I usually keep track of my progress toward my goals",
    "2": "My behaviour is not that different from other people's",
    "3": "Others tell me that I keep on with things too long.",
    "4": "I doubt I could change even if I wanted to",
    "5": "I have trouble making up my mind about things",
    "6": "I get easily distracted from my plans",
    "7": "I reward myself with progress toward my goals",
    "8": "I don't notice the effects of my actions until it's too late",
    "9": "My behaviour is similar to that of my friends",
    "10": "It's hard for me to see anything helpful about changing my ways",
    "11": "I am able to accomplish goals I set for myself",
    "12": "I put off making decisions",
    "13": "I have so many plans that it's hard for me to focus on any one of them",
    "14": "I change the way I do things when I see a problem with how things are going",
    "15": "It's hard for me to notice when I've 'had enough' (alcohol, food, sweets)",
    "16": "I think a lot about what other people think of me",
    "17": "I am willing to consider other ways of doing things",
    "18": "If I wanted to change, I am confident that I could do it",
    "19": "When it comes to deciding about a change, I feel overwhelmed by the choices",
    "20": "I have trouble following through with things once I've made up my mind to do something",
    "21": "I don't seem to learn from my mistakes",
    "22": "I'm usually careful not to overdo it when working, eating, drinking",
    "23": "I tend to compare myself with other people",
    "24": "I enjoy a routine, and like things to stay the same",
    "25": "I have sought out advice or information about changing",
    "26": "I can come up with lots of ways to change, but it's hard for me to decide which one to use",
    "27": "I can stick to a plan that's working well",
    "28": "I usually only have to make a mistake one time in order to learn from it",
    "29": "I don't learn well from punishment",
    "30": "I have personal standards, and try to live up to them",
    "31": "I am set in my ways",
    "32": "As soon as I see a problem or challenge, I start looking for possible solutions",
    "33": "I have a hard time setting goals for myself",
    "34": "I have a lot of willpower",
    "35": "When I'm trying to change something, I pay a lot of attention to how I'm doing",
    "36": "I usually judge what I'm doing by the consequences of my actions",
    "37": "I don't care if I'm different from most people",
    "38": "As soon as I see things aren't going right I want to do something about it",
    "39": "There is usually more than one way to accomplish something",
    "40": "I have trouble making plans to help me reach my goals",
    "41": "I am able to resist temptation",
    "42": "I set goals for myself and keep track of my progress",
    "43": "Most of the time I don't pay attention to what I'm doing",
    "44": "I try to be like people around me",
    "45": "I tend to keep doing the same thing, even when it doesn't work",
    "46": "I can usually find several different possibilities when I want to change something",
    "47": "Once I have a goal, I can usually plan how to reach it",
    "48": "I have rules that I stick by no matter what",
    "49": "If I make a resolution to change something, I pay a lot of attention to how I'm doing",
    "50": "Often I don't notice what I'm doing until someone calls it to my attention",
    "51": "I think a lot about how I'm doing",
    "52": "Usually I see the need to change before others do",
    "53": "I'm good at finding different ways to get what I want",
    "54": "I usually think before I act",
    "55": "Little problems or distractions throw me off course",
    "56": "I feel bad when I don't meet my goals",
    "57": "I learn from my mistakes",
    "58": "I know how I want to be",
    "59": "It bothers me when things aren't the way I want them",
    "60": "I call in others for help when I need it",
    "61": "Before making a decision, I consider what is likely to happen if I do one thing or another",
    "62": "I give up quickly",
    "63": "I usually decide to change and hope for the best"
}

no_of_qs: int = len(question_dict)

options_1: Dict[int, str] = {
    1: "Strongly disagree",
    2: "Disagree",
    3: "Uncertain or unsure",
    4: "Agree",
    5: "Strongly agree"
}

subgroups: Dict[str, str] = {
    "1": "receiving",
    "2": "evaluating",
    "3": "triggering",
    "4": "searching",
    "5": "planning",
    "6": "implementing",
    "7": "assessing",
    "8": "receiving",
    "9": "evaluating",
    "10": "triggering",
    "11": "searching",
    "12": "planning",
    "13": "implementing",
    "14": "assessing",
    "15": "receiving",
    "16": "evaluating",
    "17": "triggering",
    "18": "searching",
    "19": "planning",
    "20": "implementing",
    "21": "assessing",
    "22": "receiving",
    "23": "evaluating",
    "24": "triggering",
    "25": "searching",
    "26": "planning",
    "27": "implementing",
    "28": "assessing",
    "29": "receiving",
    "30": "evaluating",
    "31": "triggering",
    "32": "searching",
    "33": "planning",
    "34": "implementing",
    "35": "assessing",
    "36": "receiving",
    "37": "evaluating",
    "38": "triggering",
    "39": "searching",
    "40": "planning",
    "41": "implementing",
    "42": "assessing",
    "43": "receiving",
    "44": "evaluating",
    "45": "triggering",
    "46": "searching",
    "47": "planning",
    "48": "implementing",
    "49": "assessing",
    "50": "receiving",
    "51": "evaluating",
    "52": "triggering",
    "53": "searching",
    "54": "planning",
    "55": "implementing",
    "56": "assessing",
    "57": "receiving",
    "58": "evaluating",
    "59": "triggering",
    "60": "searching",
    "61": "planning",
    "62": "implementing",
    "63": "assessing"
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
        query: str = f'ALTER TABLE srq ADD q{i + 1} tinyint(1)'
        i += 1
        cur.execute(query)
    covid_db.commit()


def move_columns() -> None:
    destination_table: str = "text_questions"
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    # # SRQ
    # i = 0
    # while i < 63:
    #     column_name: str = "SRQ_" + str(i + 1)
    #     query: str = build_move_query("srq", column_name, destination_table)
    #     i += 1
    #     cur.execute(query)
    covid_db.commit()


def comment_columns(questions: Dict[str, str], groups: Dict[str, str]) -> None:
    """creates a comment for each column containing the question"""
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    for key, value in questions.items():
        comment_query: str = f'ALTER TABLE srq MODIFY q{key} TINYINT(1) COMMENT "Subgroup: {groups[key]}. ' \
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


def check_and_reverse_score(question_no: int, score: int) -> int:
    final_score: int = score
    if question_no in reverse_scored_questions:
        final_score = (max_question_score + 1) - final_score
    return final_score


def build_query(question_number: int, option_list: Dict[int, str]) -> str:
    """creates a query for a given question number with 5 options from a provided dictionary,
     setting a column comment containing the question"""
    source_column: str = "SRQ_" + str(question_number)
    dest_column: str = "q" + str(question_number)
    query: str = f"""
        update srq
            set {dest_column} = case
                when {source_column} = '{option_list[1]}' then {check_and_reverse_score(question_number, 1)} 
                when {source_column} = '{option_list[2]}' then {check_and_reverse_score(question_number, 2)} 
                when {source_column} = '{option_list[3]}' then {check_and_reverse_score(question_number, 3)}
                when {source_column} = '{option_list[4]}' then {check_and_reverse_score(question_number, 4)}
                when {source_column} = '{option_list[5]}' then {check_and_reverse_score(question_number, 5)}
            end;
    """
    return query


def transform_options(no_of_questions: int) -> None:
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    i: int = 0
    while i < no_of_questions:
        safe_execute(build_query(i + 1, options_1), cur)
        i += 1
    covid_db.commit()


def main() -> None:
    """creates string queries for all srq questions"""
    # move_columns()
    # create_columns(no_of_qs)
    # transform_options(no_of_qs)
    # comment_columns(question_dict, subgroups)


main()
