from typing import Dict

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from db_mx.db_config import DbProperties

covid_db: MySQLConnection = DbProperties().connect()

DRY_RUN_MODE = True
RESPONSE_ID = "ResponseId"

question_dict: Dict[str, str] = {
    "1": "I followed the COVID lockdown rules",
    "2": "I supported lockdown measures",
    "3": "I am adhering to social distancing rules",
    "4": "I wash hands more often for at least 20 seconds",
    "5": "I cover my mouth when coughing",
    "6": "I avoid close contact with someone who is infected",
    "7": "I have been avoiding places where many people are most likely to gather (e.g. parks, beaches, other "
         "outdoor spaces)",
    "8": "I have been taking homeopathic remedies to help overcome the coronavirus",
    "9": "I have been taking herbal remedies to help overcome the coronavirus",
    "10": "I have been avoiding eating meat to help overcome the coronavirus",
    "11": "I have been drinking ginger tea to help overcome the coronavirus",
    "12": "I have been using antibiotics to help overcome the coronavirus",
    "13": "During the COVID lockdown I met up with friends or family outside the home",
    "14": "During the COVID lockdown had friends or family visit me at home",
    "15": "I have been outside when having coronavirus-like symptoms",
    "16": "I have had a confirmed case of coronavirus",
    "17": "I have NOT had a confirmed case of coronavirus, but I think I MIGHT have had it",
    "18": "I have been in contact with a counselling or support service",
    "19": "I support police powers during the COVID crisis",
    "20": "I agree with the following statement: 'Too much fuss is being made about the risk of coronavirus':",
    "21": "I agree with the following statement: 'The coronavirus was probably created in a laboratory':",
    "22": "I agree with the following statement: 'Most people in the UK have already had coronavirus without "
          "realising it':",
    "23": "I agree with the following statement: 'Pets can transmit coronavirus':",
    "24": "I agree with the following statement: 'Coronavirus can last on some surfaces for up to 7 days':",
    "25": "I agree with the following statement: 'Sanitising hand gels are more effective at protecting you from "
          "coronavirus than washing your hands with soap and water':",
    "26": "I agree with the following statement: 'The NHS recommends that you should wear a face mask when you "
          "are out, even if you do not have coronavirus':",
    "27": "I agree with the following statement: 'There will be a quick resolution to the coronavirus crisis and "
          "lockdown measures will end soon':",
    "28": "I am closely following official guidance/recommendations on how to protect myself and others",
    "29": "I have lost sleep over coronavirus",
    "30": "My eating patterns have changed during the coronavirus lockdown:",
    "31": "I am eating much more HEALTHY food (e.g. vegetarian, low-fat, salads, vegetables, fruit etc) since the "
          "coronavirus outbreak:",
    "32": "I am eating much more UNHEALTHY food (e.g. takeaways, high calorie, chocolate, snacks, fatty food etc) "
          "since the coronavirus outbreak:",
    "33": "I am drinking much more alcohol since the coronavirus outbreak:",
    "34": "I am using non-prescription drugs (e.g. painkillers, other over-the-counter rememdies) much more since "
          "the coronavirus outbreak:",
    "35": "I am finding the coronavirus outbreak and/or the lockdown measures extremely difficult to cope with",
    "36": "I have been spending time thinking about the coronavirus",
    "37": "I have argued more with family/people in the home during the COVID lockdown",
    "38": "I feel more anxious since the lockdown measures were introduced",
    "39": "I feel more depressed since the lockdown measures were introduced",
    "40": "I feel helpless as a result of coronavirus",
    "41": "I will lose my job as a result of coronavirus and/or the lockdown",
    "42": "I will experience financial difficulties as a result of coronavirus and/or the lockdown",
    "43": "Life will return to normal soon",
    "44": "The economy will start to grow again soon",
    "45": "We will be able to vaccinate the population against coronavirus soon",
    "46": "Schools will stay closed in the future",
    "47": "Older people and those with underlying health issues will continue to be asked to remain home",
    "48": "My country's government has handled the crisis:",
    "49": "I would describe my trust in my country's government to control the spread of coronavirus as:",
    "50": "I would describe my trust in the coronavirus information my country's government provides as:",
    "51": "My belief that the government acted too slowly to control the spread of coronavirus is:",
    "52": "My belief that the government communication provided helpful advice:",
    "53": "My belief that the government plan responded well to the changing scientific information and situation:",
    "54": "I check social media for information or updates about coronavirus:"
}

options_1: Dict[int, str] = {
    1: "None of the time",
    2: "Hardly ever",
    3: "Some of the time",
    4: "Nearly all the time",
    5: "Completely"
}

options_2: Dict[int, str] = {
    1: "None of the time",
    2: "Hardly ever",
    3: "Some of the time",
    4: "Nearly all the time",
    5: "Often"
}

options_3: Dict[int, str] = {
    0: "No",
    1: "Yes"
}

options_4: Dict[int, str] = {
    1: "I am not following any of the recommendations",
    2: "Hardly any recommendations",
    3: "Some recommendations",
    4: "Most recommendations",
    5: "All recommendations"
}

options_5: Dict[int, str] = {
    1: "None of the time",
    2: "Hardly ever",
    3: "Some of the time",
    4: "Worse than usual",
    5: "Completely"
}

options_6: Dict[int, str] = {
    1: "Eating less than usual",
    2: "Eating more or less the same as usual",
    3: "Eating more than usual",
}

options_7: Dict[int, str] = {
    1: "Definitely not",
    2: "Not really",
    3: "Unsure",
    4: "Somewhat",
    5: "Definitely"
}

options_8: Dict[int, str] = {
    1: "Definitely not",
    2: "Unlikely",
    3: "Unsure",
    4: "Likely",
    5: "Certain"
}

options_9: Dict[int, str] = {
    1: "Inconsistently and confused",
    2: "Somewhat inconsistent and confused",
    3: "Unsure",
    4: "Somewhat consistent and organised",
    5: "Consistently and organised"
}

options_10: Dict[int, str] = {
    1: "Less than once a week or never",
    2: "Once a week",
    3: "Once every few days",
    4: "Once a day",
    5: "Daily or more frequenty"
}


def create_columns() -> None:
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    # LD
    i = 0
    while i < 54:
        query: str = f'ALTER TABLE text_questions ADD ld_{i + 1} VARCHAR(45)'
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
    # # LD
    # i = 0
    # while i < 54:
    #     column_name: str = "ld_" + str(i + 1)
    #     query: str = build_move_query("lockdown", column_name, destination_table)
    #     i += 1
    #     cur.execute(query)
    covid_db.commit()


def comment_columns(questions: Dict[str, str]) -> None:
    """creates a comment for each column containing the question"""
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    for key, value in questions.items():
        comment_query: str = f'ALTER TABLE lockdown MODIFY q{key} TINYINT(1) COMMENT "{value}";'
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


def query_builder_2(question_number: int, option_list: Dict[int, str]) -> str:
    """creates a query for a given question number two options from a provided dictionary"""
    source_column: str = "ld_" + str(question_number)
    dest_column: str = "q" + str(question_number)
    query: str = f"""
        update lockdown
            set {dest_column} = case
                when {source_column} = '{option_list[1]}' then 0
                when {source_column} = '{option_list[2]}' then 1
            end;
    """
    return query


def query_builder_3(question_number: int, option_list: Dict[int, str]) -> str:
    """creates a query for a given question number with 3 options from a provided dictionary"""
    source_column: str = "ld_" + str(question_number)
    dest_column: str = "q" + str(question_number)
    query: str = f"""
        update lockdown
            set {dest_column} = case
                when {source_column} = '{option_list[1]}' then 1 
                when {source_column} = '{option_list[2]}' then 2 
                when {source_column} = '{option_list[3]}' then 3
            end;
    """
    return query


def query_builder_5(question_number: int, option_list: Dict[int, str]) -> str:
    """creates a query for a given question number with 5 options from a provided dictionary"""
    source_column: str = "ld_" + str(question_number)
    dest_column: str = "q" + str(question_number)
    query: str = f"""
        update lockdown
            set {dest_column} = case
                when {source_column} = '{option_list[1]}' then 1 
                when {source_column} = '{option_list[2]}' then 2 
                when {source_column} = '{option_list[3]}' then 3
                when {source_column} = '{option_list[4]}' then 4
                when {source_column} = '{option_list[5]}' then 5
            end;
    """
    return query


def transform_options() -> None:
    cur: MySQLCursor = covid_db.cursor(dictionary=True)
    safe_execute(query_builder_5(1, options_1), cur)
    safe_execute(query_builder_5(2, options_1), cur)
    safe_execute(query_builder_5(3, options_1), cur)
    safe_execute(query_builder_5(4, options_1), cur)
    safe_execute(query_builder_5(5, options_1), cur)
    safe_execute(query_builder_5(6, options_1), cur)
    safe_execute(query_builder_5(7, options_1), cur)
    safe_execute(query_builder_5(8, options_2), cur)
    safe_execute(query_builder_5(9, options_2), cur)
    safe_execute(query_builder_5(10, options_2), cur)
    safe_execute(query_builder_5(11, options_2), cur)
    safe_execute(query_builder_5(12, options_2), cur)
    safe_execute(query_builder_5(13, options_2), cur)
    safe_execute(query_builder_5(14, options_2), cur)
    safe_execute(query_builder_5(15, options_2), cur)
    safe_execute(query_builder_2(16, options_3), cur)
    safe_execute(query_builder_2(17, options_3), cur)
    safe_execute(query_builder_5(18, options_2), cur)
    safe_execute(query_builder_5(19, options_1), cur)
    safe_execute(query_builder_5(20, options_1), cur)
    safe_execute(query_builder_5(21, options_1), cur)
    safe_execute(query_builder_5(22, options_1), cur)
    safe_execute(query_builder_5(23, options_1), cur)
    safe_execute(query_builder_5(24, options_1), cur)
    safe_execute(query_builder_5(25, options_1), cur)
    safe_execute(query_builder_5(26, options_1), cur)
    safe_execute(query_builder_5(27, options_1), cur)
    safe_execute(query_builder_5(28, options_4), cur)
    safe_execute(query_builder_5(29, options_5), cur)
    safe_execute(query_builder_3(30, options_6), cur)
    safe_execute(query_builder_5(31, options_7), cur)
    safe_execute(query_builder_5(32, options_7), cur)
    safe_execute(query_builder_5(33, options_7), cur)
    safe_execute(query_builder_5(34, options_7), cur)
    safe_execute(query_builder_5(35, options_7), cur)
    safe_execute(query_builder_5(36, options_1), cur)
    safe_execute(query_builder_5(37, options_1), cur)
    safe_execute(query_builder_5(38, options_1), cur)
    safe_execute(query_builder_5(39, options_1), cur)
    safe_execute(query_builder_5(40, options_1), cur)
    safe_execute(query_builder_5(41, options_8), cur)
    safe_execute(query_builder_5(42, options_8), cur)
    safe_execute(query_builder_5(43, options_8), cur)
    safe_execute(query_builder_5(44, options_8), cur)
    safe_execute(query_builder_5(45, options_8), cur)
    safe_execute(query_builder_5(46, options_8), cur)
    safe_execute(query_builder_5(47, options_8), cur)
    safe_execute(query_builder_5(48, options_9), cur)
    safe_execute(query_builder_5(49, options_8), cur)
    safe_execute(query_builder_5(50, options_8), cur)
    safe_execute(query_builder_5(51, options_8), cur)
    safe_execute(query_builder_5(52, options_8), cur)
    safe_execute(query_builder_5(53, options_8), cur)
    safe_execute(query_builder_5(54, options_10), cur)
    covid_db.commit()


def main() -> None:
    # move_columns()
    # create_columns()
    """creates string queries for all lockdown questions"""
    # transform_options()
    # comment_columns(question_dict)


main()
