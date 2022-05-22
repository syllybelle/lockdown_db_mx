from typing import Dict, List

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from db_mx.db_config import DbProperties

covid_db: MySQLConnection = DbProperties().connect()

RESPONSE_ID = "ResponseId"
DRY_RUN_MODE = True

ben_id: str = "Participant_ID"
ben_date: str = "RecordedDate"
ben_progress: str = "Progress"
ben_dur: str = "Duration"
ben_q1: str = "Q1_Dem1"
ben_q2: str = "Q2_Dem2_Tran"
ben_q3: str = "Q3_Dem3"
ben_q4: str = "Q4_Dem4_Tran"
ben_q5: str = "Q5_Dem5_Tran"
ben_q6: str = "Q6_Dem6" 
svb_id: str = "ResponseId"
svb_date: str = "RecordedDate"
svb_progress: str = "Progress"
svb_dur: str = "Durationinseconds"
svb_q1: str = "dem_1_age"
svb_q2: str = "dem_2_gender"
svb_q3: str = "dem_3_location_input"
svb_q4: str = "dem_4_politics"
svb_q5: str = "dem_5_brexit"
svb_q6: str = "dem_6_loe_input"

fetch_ben_data_query: str = f"""
                        select Participant_ID, RecordedDate, Progress, Duration, Q1_Dem1, Q2_Dem2_Tran, Q3_Dem3, 
                            Q4_Dem4_Tran, Q5_Dem5_Tran, Q6_Dem6 
                        FROM covid_data.ben_data
                        where Participant_ID != null 
                        or Participant_ID != '' 
                        order by Progress desc, RecordedDate desc, Q1_Dem1 desc, Q2_Dem2_Tran desc, Q3_Dem3 desc, 
                            Q4_Dem4_Tran desc, Q5_Dem5_Tran desc, Q6_Dem6  desc
                        ;
                        """
fetch_svb_data_query: str = f"""
                            select demographics.ResponseId, RecordedDate, Progress, Durationinseconds, dem_1_age, 
                                dem_2_gender, dem_3_location_input, dem_4_politics, dem_5_brexit, dem_6_loe_input 
                            FROM covid_data.demographics
                            JOIN text_questions ON text_questions.ResponseId = demographics.ResponseId 
                            where demographics.ResponseId != null 
                            or demographics.ResponseId != '' 
                            order by Progress desc, RecordedDate desc, Durationinseconds desc, dem_1_age desc, 
                                dem_2_gender desc, dem_3_location_input desc, dem_4_politics desc, dem_5_brexit desc, 
                                dem_6_loe_input desc
                            ;
                            """


def compare(ben_data: List[Dict[str, any]], svb_data: List[Dict[str, any]]) -> Dict[str, str]:
    # key = ben_id, value = s id
    id_matches: Dict[str, str] = {}

    # row = dict where k = column name and v = cell data
    for b_row in ben_data:
        # print(b_row)
        # exit(1)
        for s_row in svb_data:
            # print(s_row)
            # exit(1)
            # print(b_row[ben_dur])
            # print(s_row[svb_date])
            # exit(1)
            if b_row[ben_date] != s_row[svb_date]:
                continue
            elif int(b_row[ben_progress]) != int(s_row[svb_progress]):
                continue
            elif int(b_row[ben_dur]) != int(s_row[svb_dur]):
                continue
            # elif int(b_row[ben_q1]) != int(s_row[svb_q1]):
            #     continue
            # elif str(b_row[ben_q2]) not in str(s_row[svb_q2]):
            #     continue
            # elif str(b_row[ben_q3]) not in str(s_row[svb_q3]):
            #     continue
            # elif str(b_row[ben_q4]) not in str(s_row[svb_q4]):
            #     continue
            # elif str(b_row[ben_q5]) not in str(s_row[svb_q1]):
            #     continue
            # elif str(b_row[ben_q6]) not in str(s_row[svb_q6]):
            #     continue
            # if all above statements are false, all values in the two rows are compatible
            # check if the id from svb_db has been used before:
            if s_row[svb_id] in id_matches.values():
                exit(1)
            id_matches[str(b_row[ben_id])] = s_row[svb_id]
            continue
        continue
    return id_matches


def add_linked_id_to_db(id_dict: Dict[str, str]) -> None:
    for b_id, s_id in id_dict.items():
        query = f"""
            update ben_data
            set ResponseId = '{s_id}'
            where Participant_ID = '{b_id}'
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


def main() -> None:
    cursor: MySQLCursor = covid_db.cursor(dictionary=True)
    cursor.execute(fetch_ben_data_query)
    ben_raw_data: List[Dict[str, any]] = cursor.fetchall()
    cursor.execute(fetch_svb_data_query)
    svb_raw_data: List[Dict[str, any]] = cursor.fetchall()
    comparison: Dict[str, str] = compare(ben_raw_data, svb_raw_data)
    print(len(comparison))



    # cur2: MySQLCursor = covid_db.cursor(dictionary=True)
    # cur2.execute("select ResponseId, free_recall from free_recall where ResponseId = 'R_01HO4jj0kUTEY9z';")
    # new_data = cur2.fetchall()
    # print(new_data)


main()
