from typing import Dict, List

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from db_mx.db_config import DbProperties

covid_db: MySQLConnection = DbProperties().connect()

RESPONSE_ID = "ResponseId"
DRY_RUN_MODE = False

levels_of_education: Dict[str, List[str]] = {
    # "phd degree"
    "10": ["PhD",
           "phd degree",
           "Doctorate",
           "Doctor degree",
           "pd"],
    # "phd incomplete"
    "9": ["in final year of PhD",
          "phd incomplete",
          "PhD student"],
    # "masters/postgraduate degree"
    "8": ["Master's degree",
          "Four year master’s degree",
          "Four year master's degree",
          "Graduate Certificate",
          "higher education master",
          "Licenciate degree",
          "Licenciate’s Degree",
          "Licenciate's Degree",
          "licenciatura",
          "licentiate degree",
          "M.A",
          "MA",
          "Magister",
          "Marsters degree",
          "Mastees degrees",
          "master",
          "Master degree",
          "master degree and postgraduate studies",
          "Master degree in mechanical engineer",
          "master of economic",
          "Master of science",
          "Master of Science in Mechanical Engineering",
          "Master’s",
          "Master’s degree",
          "Master’s degree in developmental psychology",
          "Master’s prefessional degree",
          "Mastera degree",
          "Masters",
          "Master's",
          "Masters (Integrated 5 year)",
          "Masters degree",
          "Masters degree - economy",
          "Masters degree (currently enrolled on a phd)",
          "Masters degree (Laurea specialistica in Italian)",
          "Masters Degree (MSc)",
          "Master's degree in developmental psychology",
          "Masters degree in Editorial, Public and Social Information Sciences",
          "Masters Degree Mech. Engineering",
          "Masters degree,currently",
          "Masters equivalent",
          "Masters of Science",
          "Master's prefessional degree",
          "Matser degree",
          "MBA",
          "MD",
          "Mestrado",
          "MFA",
          "MSc",
          "nivel 7",
          "PGCE",
          "Post Grad",
          "Post graduate certificate",
          "post graduate degree",
          "Postgrad",
          "Postgraduate",
          "Postgraduate",
          "Postgraduate degree",
          "Postgraduate diploma",
          "Post-graduate qualification",
          "Post-graduation",
          "Professional post grad qualification",
          "University Mgr",
          "Engineer's degree",
          "PharmD"],
    # "masters/postgraduate incomplete"
    "7": ["Completed BSc, soon to complete MSc",
          "Degree, currently studying for Masters Degree",
          "Enrolled in Masters program, completed undergrade degree",
          "High School A Tier (Doing Masters Degree right now)",
          "I'm doing my Masters degree",
          "School - level exams, currently doing Masters degree",
          "Taking my masters degree in Medicine"],
    # "undergraduate degree"
    "6": ['Undergraduate degree',
          "Acca",
          "B.A. hons",
          "B.Sc. (Hons)",
          "BA",
          "BA (Honours)",
          "BA (Hons)",
          "Ba (Hons) degree",
          "BA 1st.",
          "BA degree",
          "BA honours",
          "BA Hons",
          "BA Hons Degree",
          "BA(Hons)",
          "Bacchalor",
          "Bachelaret",
          "bachellor",
          "Bachelor",
          "Bachelor degree",
          "Bachelor Degree (4 years)",
          "Bachelor in Arts",
          "bachelor of engineering",
          "bachelor of engineering",
          "Bachelor of Science",
          "Bachelor´s Degree",
          "Bachelor’s (16 years of school)",
          "Bachelors",
          "bachelor's",
          "Bachelor's (16 years of school)",
          "Bachelors degree",
          "Bachelor's degree",
          "Bachelor's Degree (4 years)",
          "Bachelors degree in Business Management   & Marketing"
          "Bachelors degree in Business Management & Marketing",
          "Bachelor's degree in Paris France",
          "Bachelors Degree in Psychology",
          "Bachelors Degree in Psychology",
          "Bachelors in the Arts",
          "Bachelor's of Science",
          "Bachleor",
          "Bachleor Degree",
          "Bacholer degree",
          "Barchelor’s Degree",
          "Barchelor's Degree",
          "BBA + BA",
          "bechelor degree",
          "Belchior Degree",
          "BEng",
          "BFA",
          "BS, Computer Science",
          "Bsc",
          "BSc Degree",
          "BSc honours degree",
          "BSc(Hons)",
          "BSC, 4 year college",
          "BSc.",
          "BVSc - Veterinary Doctor with Hons in Wildlife Management",
          "Degree",
          "DEGREE FINISHED",
          "Degree in Languges and Lecteratures",
          "Degree undergraduate",
          "Engineer",
          "Engineer’s degree",
          "Finish University",
          "Foundation Degree",
          "full degree",
          "Graduate Degree",
          "Hbo",
          "LAUREA",
          "Law qualification",
          "licencjackie",
          "licencjat",
          "License",
          "license university",
          "MBBS",
          "telecom Engineering degree",
          "three-year degree",
          "Udergraduate",
          "udergraduate degree",
          "under graduate degree",
          "Undergrad",
          "Undergrad degree",
          "undergraduate",
          "Undergraduate college",
          "Undergraduate Degree (B.A.)",
          "Undergraduate Degree (BA)",
          "Undergraduate degree (Bachelors)",
          "Undergraduate degree (BSc)",
          "Undergraduate degree (what is known as a Bachelor)",
          "Undergraduate degree in paramedic science",
          "Undergraduate degree,",
          "Undergraduate degree, BA",
          "Undergraduate Degree, Bachelors of Engineering",
          "Undergraduate Degree, BSC Bachelor Of Animal Production",
          "Undergraduate degree, IT",
          "Undergraduate degreee",
          "Undergraduate deree",
          "undergraduate level",
          "Undergraduated degree",
          "Undergraduete degree University",
          "undergradute degree",
          "Undergrate degree",
          "Undergratuate degree",
          "Undergrduate degree",
          "ungergraduate degree",
          "Uni",
          "university",
          "University degree",
          "York University Bachelors of Arts",
          "Informatic degree",
          "titulo universitario"],
    # "undergraduate incomplete"
    "5": ["undergraduate incomplete",
          "12th Grade, studying for an undergraduate",
          "2 year of university",
          "2nd year university",
          "2º year of undergraduate degree",
          "3rd year of bachelor degree",
          "A- levels - currently completing undergraduate degree",
          "A Levels (Currently studying as undergraduate)",
          "Attending university",
          "bachleros degree",
          "collage",
          "Current undergraduate",
          "Currently at University, so highest is high school",
          "currently in the finals of the degree",
          "Currently in University",
          "Currently on my first year of Undergraduate degree.",
          "Currently receiving undergraduate degree",
          "Currently Studying in University, Finished School",
          "Currently, high school + classes at the university every 2 weeks",
          "during undergraduate studies",
          "Enrolled in University",
          "FdSc, 1 module away from BSc",
          "Finished high school and some university",
          "Finished high school, 2nd year of HBO Informatics",
          "finished High-school. Currently studying",
          "first year in university",
          "First year university certificate",
          "For now i am on second year of law studies",
          "Graduated from High School. Currently in Med School.",
          "Half year before the degree",
          "High School (working on Undergraduate Degree)",
          "HIgh school degree, i´m currently on my last year of college",
          "High -school diploma, I’m currently studying at universitiy",
          "High -school diploma, I'm currently studying at universitiy",
          "high school diploma, uncompleted degree",
          "High school, a year of undergraduate",
          "Honours degree",
          "I am currently in Biotechnology university. I have an highschool degree",
          "I finished highschool a couple years ago and am now attending college.",
          "I’m a student (first degree)",
          "I'm a student (first degree)",
          "In University",
          "Licenciatura but not completed",
          "matura exam, actial 3rd yeard of studing",
          "Now studying to get a degree",
          "Ongoing Undergraduate degree",
          "passed the Polish equivalent of A-levels (at 19yo), currently studying 5/6th year of medicine",
          "school level exams- currently completing undergrad",
          "School-level exams, currently undergraduate student",
          "senior year undergrad",
          "Some deegre",
          "Some degree",
          "Some undergraduate",
          "Some Undergraduate degree, not complete (3 out of 4 years)",
          "Some university",
          "Some University but no degree",
          "Some University Credits",
          "some university without a degree",
          "Some years of degree",
          "some years of university",
          "Student",
          "Student Undergraduate degree",
          "studies",
          "Studying Engineering",
          "Studying for Undergraduate",
          "Taking a Degree",
          "Tecnical high school, currently attending university",
          "third year of degree",
          "This year I will be Bachelor",
          "Undergraduate degree courses",
          "Undergraduate degree not completed",
          "undergraduate not completed",
          "Undergraduate student",
          "unfinished university, 2 years",
          "University Student",
          "university student (engineer)",
          "5 GCSES and 1 O’LEVEL",
          "two years of a four year Mechanical Engineering undergraduate degree"],
    # "college/A-levels/diploma"
    "4": ["''A'' level",
          "'A' level",
          'a levels',
          "A level",
          "A' level",
          "1 year college",
          "2.5 years of college",
          "3 years of college, no degree",
          "3rd year of college",
          "4 Years degree College",
          "A leval",
          "A level",
          "A level equivalent (highers)",
          "a level equivalents",
          "A level exams",
          "A level’s",
          "A level's",
          "A levels equivalent",
          "A levels equivalent",
          "AA degree",
          "Alevel",
          "A-Level",
          "Alevel / college diplomas",
          "A-Level exams",
          "A-Level, and further NVQ qualification",
          "A-Level, Sixth Form",
          "A-level/nvq",
          "Alevels",
          "A-levels",
          "Apprenticeship",
          "As level",
          "Associate degree",
          "Associate’s degree",
          "Associates Degree",
          "Associate's degree",
          "BTEC",
          "BTEC level 3 extended diploma",
          "Cert He",
          "certificate of higher education",
          "Collage A levels",
          "collage degree",
          "College",
          "College A LEVEL",
          "College A levels",
          "College course",
          "College deegree",
          "college degree",
          "College degree.",
          "College Diploma",
          "College graduate",
          "College graduate degree",
          "College nvq",
          "College Student",
          "College, A Levels",
          "college/A-levels",
          "Community College",
          "Completed GCSEs and Some College.",
          "Completed School-Level exams, currently studying for a Technical Degree",
          "DipHE",
          "diploma",
          "Diploma in Banking and Finance",
          "Diploma superiore",
          "engineering college degree",
          "Engineering Diploma",
          "Equivalent of A levels",
          "ESO",
          "Finished high school, 2nd year of HBO Informatics",
          "Finished high school, currently in college",
          "finishing college this year",
          "First year of College",
          "First year of College",
          "FORMACIÃ“N PROFESIONAL",
          "FORMACIÓN PROFESIONAL",
          "GCE O Level plus some college",
          "GED",
          "High school (Highers/A levels)",
          "High school degree (In Slovenia it's called Matura certificate)",
          "High school degree plus a lot of studies in private painting schools",
          "High school degree plus a lot of studies in private painting schools",
          "HIgh school degree, iÂ´m currently on my last year of college",
          "High School Diploma + Post Diploma 1-year course",
          "High school, logistics completed",
          "higher college",
          "Higher Education Diploma",
          "higher education, College diploma",
          "Higher National Diploma",
          "higher technical school",
          "Highschool A levels",
          "hnc",
          "HNC - engineering",
          "HND",
          "hnd in business",
          "I am currently studying in college.",
          "In college",
          "IT study",
          "IT Technic",
          "JD",
          "Level 3 apprenticeship (equivalent to 3 A levels)",
          "Level 3 diploma",
          "Level 4",
          "Matura exam - polish high school finals",
          "matura exam (equivalent of A-Lebels, post high-school)",
          "matura in polish high school",
          "Nearly college degree",
          "Nurse assistent degrees",
          "Nvq",
          "NVQ 3-College",
          "nvq level 3",
          "Nvq level 3 child care and education",
          "polish equivalent of A-level exams (matura)",
          "Post-secondary non-tertiary education",
          "Profesional Degree",
          "Professional course",
          "Professional degree",
          "Professional Degree (JD)",
          "professional work",
          "School level exams (A-Levels)",
          "School-level Exam (Matric Std 10 or Grade 12) Diploma in Nursing",
          "School-level Exams (A Levels)",
          "School-level exams, equivalent of a-levels",
          "Scottish higher",
          "Scottish highers",
          "Scottish Highers/Advanced Highers",
          "Some collage",
          "Some college",
          "Some college BTEC",
          "Some college but no degree",
          "Some college but not degree",
          "Some college education",
          "SOME COLLEGE, NO DEGREE",
          "some college, no degree.",
          "Some undergraduate college",
          "Still in college",
          "Szkoła średnia/Matura Exam (A levels)",
          "TAFE Diploma",
          "Technical",
          "technical collage IT, middle",
          "Technical college",
          "Technical college degree",
          "technical college, third grade",
          "technical professional course",
          "technician",
          "Trade or Craft Certificate",
          "Unfinished college",
          "Vocational College",
          "vocational course",
          "Vocational Qualification",
          "Vocational Training"],
    # "high school completed"
    "3": ["high  school",
          "12 years school",
          "12° grade",
          "12º",
          "12th year",
          "5 GCSES and 1 OLEVEL",
          "average",
          "BAC",
          "Basic",
          "Basic education",
          "chool-level exams",
          "Close to GSCE (in German: Mittlere Reife)",
          "Completed High School",
          "Computer technician (high school degree)",
          "Diploma of High School",
          "ESO ( Madatory Secondar School in Spain)",
          "finished high school",
          "Finished highschool",
          "Gce",
          "GCSE",
          "GCSE - School level exams",
          "GCSE’s",
          "GCSE's",
          "Graduated High School with exams",
          "Graduated highschool",
          "high school",
          "High dchool",
          "High Scholl Degree",
          "High School",
          "High School - level exams",
          "High school ( liceo)",
          "High School Bachelors Pass",
          "high school completed",
          "high school degree",
          "High school diploma",
          "high school diploma or equivalent",
          "High school education",
          "High School equivalent",
          "High school exams",
          "High School graduate",
          "High School Graduated",
          "high school graduation",
          "high school level",
          "High School level exams",
          "high school, post-secondary school",
          "High School-level exams",
          "Highchool",
          "HighSchool",
          "High-school",
          "High-school",
          "High-school certificate",
          "highschool degree",
          "High-school degree",
          "Highschool diploma",
          "High-school diploma",
          "High-school diploma",
          "Highschool finished",
          "Highschool graduate",
          "high-school graduate",
          "High-School graduate exam",
          "High-school level exams",
          "Hight school",
          "hihg school",
          "I levels",
          "level exams",
          "liceum",
          "Lower secondary education",
          "Matric",
          "Media inferiore",
          "Medium",
          "Medium School",
          "National Certificate",
          "National Senior Certificate",
          "o level",
          "O level gce",
          "O levels then nvq level 3",
          "Passed high school exams.",
          "school",
          "School - level exams",
          "School leavers exams",
          "School level",
          "School level exam",
          "School level exams",
          "School- level exams",
          "School level-exam",
          "School level-exams",
          "school-level",
          "school-level",
          "School-level (GCSEs)",
          "School-level exam",
          "School-level exams",
          "School-level exams (IB Diploma)",
          "School-level exams.",
          "scool-level exams",
          "Scottish standard grades",
          "Secondary",
          "secondary education",
          "secondary education with passed high school diploma",
          "secondary high school",
          "secondary school",
          "Secondary School (16)",
          "Secondary school certificate",
          "secondary school diploma",
          "Secondary school-leaving exam",
          "shool-level exams",
          "Sixth Form",
          "srednie",
          "The BAC in France",
          "Upper Secondary",
          "Upper Secondary Education",
          "videregående skole",
          "wykształcenie średnie (high school)",
          "Year 11 Leaving Certificate"],
    # "vocational/technical school"
    "2": ['Technical  school',
          "NVQ level 2",
          "Technical school",
          "technical high school",
          "technical school",
          "Trade school",
          "Vocational school",
          "zawodowa",
          "zawodówka"],
    # "school incomplete"
    "1": ["school incomplete",
          "Currently in High School",
          "Done some high-school",
          "Elementary school degree",
          "Elementary/Middle school diploma.",
          "I''m actually in high school, in Poland we describe it as a technical school (not finished yet)"
          "I’m actually in high school, in Poland we describe it as a technical school (not finished yet)",
          "I’m in high school",
          "I'm in high school",
          "junior high school, now im in high school",
          "Middle school",
          "middle school graduation",
          "midschool",
          "None",
          "primary school",
          "Primary school education",
          "Secondary school (unfinished)",
          "Secondary school certificate in next 2 years",
          "some high school",
          "Still in high school",
          "Still in High School.",
          "Uneducated, Elementary School",
          "9 ano"],
    # "unknown"
    "": ["A+ Student",
         "engenering degree",
         "Graduate",
         "Graduated",
         "Graduated Degree",
         "graduation",
         "Gradueted",
         "High school/ mechatronics",
         "Ph",
         "Preparatoria",
         "under",
         "Ungraduated"],
    # "invalid"
    "0": ["211212",
          "5ed8ea2842688141c50cc5b6",
          "5f14f7747a99fb5877be9042",
          "5f16cd081b2ba4000806c061",
          "African American",
          "dd",
          "I like it",
          "Prefer not to say.",
          "r6utf"]
}


def DANGEROUS_execute(query: str, cur: MySQLCursor) -> str:
    print(query)
    cur.execute(query)
    return "y"


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


def build_query(change_to: str, change_from: str) -> str:
    query: str = f" update demographics \n " \
                 f"set dem_6_loe = '{change_to}' \n" \
                 f'where dem_6_loe = "{change_from}";'
    return query


def refresh_db() -> None:
    cursor = covid_db.cursor(dictionary=True)
    refresh_query: str = """update demographics
                     JOIN text_questions
                     ON text_questions.ResponseId = demographics.ResponseId 
                     set demographics.dem_6_loe = text_questions.dem_6_loe_input;"""
    safe_execute(refresh_query, cursor)
    covid_db.commit()


def run_queries(dictionary: Dict[str, List[str]]) -> None:
    cur = covid_db.cursor(dictionary=True)

    for name, input_list in dictionary.items():
        for input_text in input_list:
            query = build_query(name, input_text)
            # response = safe_execute(query, cur)
            # if response == "n":
            #     break
            DANGEROUS_execute(query, cur)
    covid_db.commit()


def main() -> None:
    # refresh_db()
    run_queries(levels_of_education)


main()
