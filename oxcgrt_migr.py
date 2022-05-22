from datetime import datetime
from typing import Dict, List

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from db_mx.db_config import DbProperties

covid_db: MySQLConnection = DbProperties().connect()
analysis_db: MySQLConnection = DbProperties("covid_analysis").connect()

# fixme: create classes rather than use indices
# fixme: don't use terms tables and rows etc.

DRY_RUN_MODE = False
RESPONSE_ID = "ResponseId"


def convert_datetime(date: datetime) -> str:
    year: str = date.strftime("%Y")
    month: str = date.strftime("%m")
    day: str = date.strftime("%d")
    formatted_date: str = f"{year}-{month}-{day}"
    return formatted_date


def fetch_dem_table() -> Dict[str, List[any]]:
    cursor: MySQLCursor = covid_db.cursor(dictionary=True)
    cursor.execute("select ResponseId, dem_3_country, StartDate from demographics")
    table_raw: List[Dict[str, any]] = cursor.fetchall()
    dem_table: Dict[str, List[any]] = {}
    for row in table_raw:
        dem_table[row['ResponseId']] = [row['dem_3_country'], convert_datetime(row['StartDate'])]
    return dem_table


look_up_table: Dict[str, int] = {
    "2020-07-20": 0,
    "2020-07-21": 1,
    "2020-07-22": 2,
    "2020-07-23": 3,
    "2020-07-24": 4,
    "2020-07-25": 5,
    "2020-07-26": 6,
    "2020-07-27": 7,
    "2020-07-28": 8,
    "2020-07-29": 9,
    "2020-07-30": 10,
    "2020-07-31": 11,
    "2020-08-01": 12,
    "2020-08-02": 13,
    "2020-08-03": 14,
    "2020-08-04": 15,
    "2020-08-05": 16,
    "2020-08-06": 17,
    "2020-08-07": 18,
    "2020-08-08": 19,
    "2020-08-09": 20,
    "2020-08-10": 21,
    "2020-08-11": 22,
    "2020-08-12": 23,
    "2020-08-13": 24,
    "2020-08-14": 25,
    "2020-08-15": 26,
    "2020-08-16": 27,
    "2020-08-17": 28,
    "2020-08-18": 29,
    "2020-08-19": 30,
    "2020-08-20": 31,
    "2020-08-21": 32,
    "2020-08-22": 33,
    "2020-08-23": 34,
    "2020-08-24": 35,
    "2020-08-25": 36,
    "2020-08-26": 37,
    "2020-08-27": 38,
    "2020-08-28": 39,
    "2020-08-29": 40,
    "2020-08-30": 41,
    "2020-08-31": 42,
    "2020-09-01": 43,
    "2020-09-02": 44,
    "2020-09-03": 45,
    "2020-09-04": 46,
    "2020-09-05": 47,
    "2020-09-06": 48,
    "2020-09-07": 49,
    "2020-09-08": 50,
    "2020-09-09": 51
}


def fetch_oxcgrt_table(table_name: str) -> Dict[int, List[any]]:
    cursor: MySQLCursor = analysis_db.cursor(dictionary=True)
    cursor.execute(f"select * from covid_analysis.{table_name}")
    raw_table: List[Dict[str, any]] = cursor.fetchall()
    oxcgrt_table: Dict[int, List[any]] = {}
    for row in raw_table:
        value_list: List[any] = []
        for column_name, value in row.items():
            value_list.append(str(value))
        oxcgrt_table[row["country_num"]] = value_list[3:]
    return oxcgrt_table


def set_oxcgrt_val(dem_table: Dict[str, List[any]], oxcgrt_table: Dict[int, List[any]], output_column: str) -> None:
    cursor: MySQLCursor = covid_db.cursor(dictionary=True)
    for responseid, demographics in dem_table.items():
        oxcgrt_value: str = ""
        date: str = demographics[1]
        country_code: int = demographics[0]
        oxcgrt_column_index: int = look_up_table[date]
        oxcgrt_row: List[any] = oxcgrt_table[country_code]
        oxcgrt_value += oxcgrt_row[oxcgrt_column_index]
        query: str = f"""update covid_data.demographics
                        set {output_column} = {oxcgrt_value}
                        where ResponseId = "{responseid}";
                    """
        # print(query)
        # cursor.execute(query)
        response: str = safe_execute(query, cursor)
        if response == "n":
            covid_db.commit()
            return
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


def main() -> None:
    table_name: str = ""
    output_column: str = ""
    table_question: str = input("""Import:
                            ox_cgrt_containment: 1
                            ox_cgrt_econ_support: 2
                            ox_cgrt_gov_resp: 3
                            ox_cgrt_stringency: 4
                            any other key to abort
                            Your choice: """)
    if table_question == "1":
        table_name = "ox_cgrt_containment"
        output_column = "dem_3_OxCGRT_contain"
    elif table_question == "2":
        table_name = "ox_cgrt_econ_support"
        output_column = "dem_3_OxCGRT_econ"
    elif table_question == "3":
        table_name = "ox_cgrt_gov_resp"
        output_column = "dem_3_OxCGRT_gov"
    elif table_question == "4":
        table_name = "ox_cgrt_stringency"
        output_column = "dem_3_OxCGRT_str"
    else:
        exit(1)
    dem_table: Dict[str, List[any]] = fetch_dem_table()
    oxcgrt_table: Dict[int, List[any]] = fetch_oxcgrt_table(table_name)
    set_oxcgrt_val(dem_table, oxcgrt_table, output_column)


main()
