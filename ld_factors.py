from decimal import *
from typing import Dict, List, Set

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from db_mx.db_config import DbProperties

covid_db: MySQLConnection = DbProperties().connect()

# for decimal operations:
getcontext().prec = 6
getcontext().rounding = ROUND_HALF_UP
DRY_RUN_MODE = True

question_total_score_config: Dict[int, int] = {
    # scores that are not out of 5:
    16: 1,
    17: 1,
    30: 3,
}

columns_not_to_append: Set[str] = {"ResponseId", "self_medication", "government_response", "anxiety_mood", "adherence",
                                   "skepticism_paranoia", "hopefulness", "unhealthy_consumption", "social_contact",
                                   "continued_lockdown", "fomites", "financial_insecurity", "suspected infection"}

inverse_scores_config: Dict[str, List[int]] = {
    "government_response": [51],
}
factors_config: Dict[str, List[int]] = {
    "self_medication": [8, 9, 10, 11, 12, 15, 34],
    "government_response": [48, 49, 50, 51, 52, 53],
    "anxiety_mood": [29, 35, 36, 37, 38, 39, 40],
    "adherence": [1, 2, 3, 4, 5, 6, 7, 28],
    "skepticism_paranoia": [20, 21, 22],
    "hopefulness": [27, 43, 44, 45],
    "unhealthy_consumption": [30, 32, 33],
    "social_contact": [13, 14],
    "continued_lockdown": [46, 47],
    "fomites": [23, 24],
    "financial_insecurity": [41, 42],
    "suspected_infection": [17]
}


def reformat_data_dict(raw_data: List[Dict[str, any]]) -> Dict[str, Dict[int, int]]:
    """ reformat raw data which is a list of dictionaries of the column name as key and the row value as value to a
    dictionary with the ResponseID as the key, and the value as a list of values for each column
    NOTE: list index is zero indexed so to prevent typos, list[0] will be an item of value zero, so list[1] = q1"""
    new_data: Dict[str, Dict[int, int]] = {}
    for row in raw_data:
        question_responses: Dict[int, int] = {}
        new_data[row["ResponseId"]] = question_responses
        for column, value in row.items():
            if "q" in column and column not in columns_not_to_append:
                column_num: int = int(column[1:])
                question_responses[column_num] = value
    # print(new_data)
    return new_data


def generate_scores(clean_data: Dict[str, Dict[int, int]]) -> None:
    for participant, response_dict in clean_data.items():
        # print(participant)
        for factor, q_list in factors_config.items():
            n: Decimal = Decimal(len(q_list))
            score: Decimal = Decimal(0)
            for q in q_list:
                highest_score: int = 5
                current_item_score: Decimal = Decimal(0)
                # print(str(q) + " " + str(response_dict[q]) + " score in initial outer scope")
                if factor in inverse_scores_config:
                    """if the factor has a question that is inversely scored is the current question is inversely 
                        scored:"""
                    if q in inverse_scores_config.get(factor):
                        """if the factor has a question that is inversely scored and 
                        the current question is inversely scored, does the question have an abnormal total score? """
                        if q in question_total_score_config:
                            highest_score = (question_total_score_config[q])
                        temp: Decimal = Decimal(highest_score) + Decimal(1) - Decimal(response_dict[q])
                        current_item_score = temp / Decimal(highest_score)
                        # print("hello" + str(current_item_score))
                        score = score + current_item_score
                        continue
                    """if the factor has a question that is inversely scored AND the current question is NOT 
                    inversely scored, does the current question have an abnormal total score?"""
                    if q in question_total_score_config:
                        highest_score = (question_total_score_config[q])
                        current_item_score = Decimal(response_dict[q]) / Decimal(highest_score)
                        score = score + current_item_score
                        continue
                    """if the factor has a question that is inversely scored AND the current question is NOT 
                    inversely scored, AND does not have an abnormal total score: """
                    current_item_score = Decimal(response_dict[q]) / Decimal(highest_score)
                    # print("noooo" + str(current_item_score))
                    score = score + current_item_score
                elif q in question_total_score_config:
                    highest_score = (question_total_score_config[q])
                    current_item_score = Decimal(response_dict[q]) / Decimal(highest_score)
                    # print(current_item_score)
                    score = score + current_item_score
                else:
                    current_item_score = Decimal(response_dict[q]) / Decimal(highest_score)
                    # print(current_item_score)
                    score = score + current_item_score
                # print(str(score))
            temp_score: Decimal = (score / n * 5)
            # print(temp_score)
            total_score: Decimal = round(temp_score, 2)
            # print("am I smaller? " + str(total_score))
            query: str = f"""
            UPDATE lockdown
            SET {factor} = {total_score}
            WHERE ResponseId = "{participant}";
            """
            #         # end = safe_execute(query)
            #         # if end == "n":
            #         #     continue
            DANGEROUS_execute(query)
    covid_db.commit()


def DANGEROUS_execute(query: str) -> str:
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    # print(query)
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


def main() -> None:
    cursor: MySQLCursor = covid_db.cursor(dictionary=True)
    fetch_table_data_query: str = f""" SELECT * FROM covid_data.lockdown;"""
    cursor.execute(fetch_table_data_query)
    raw_table_data: List[Dict[str, any]] = cursor.fetchall()
    clean_data: Dict[str, Dict[int, int]] = reformat_data_dict(raw_table_data)
    generate_scores(clean_data)


main()
