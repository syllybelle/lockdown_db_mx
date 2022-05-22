from subprocess import check_call
from typing import Dict, List, Set
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from db_mx.db_config import DbProperties
from db_mx.value_lables import write_demographics_query, write_hads_query, write_lockdown_query, write_ocir_query, \
    write_srq_query, write_compiled_query

covid_db: MySQLConnection = DbProperties().connect()

 # copy to clipboard only funcitonal in windows. If using a different OS, use the print statement and copy manually
 # when pasting syntax, ensure you are pasting into a clean workbook

question_dict: Dict[str, Dict[str, str]] = {
    "demographics": {"ResponseId": "",
                     "progress_complete": "all questions up to the end of HADS answered",
                     "Progress": "",
                     "progress_group": "progress group defined by the last fully completed section",
                     "Durationinseconds": "",
                     "Finished": "",
                     "consent": "",
                     "dem_1_age": "age",
                     "dem_1_age_group": "quartiles of age distribution",
                     "dem_2_gender": "gender",
                     "dem_3_country": "country",
                     "dem_4_politics": "political divide",
                     "dem_5_brexit": "Brexit",
                     "dem_6_loe": "highest level of education",
                     "StartDate": "date as yy/mm/dd",
                     "EndDate": "date as yy/mm/dd",
                     "RecordedDate": "date as yy/mm/dd",
                     "dem_3_continent": "regional grouping for participant_s country",
                     "dem_3_hrs": "human rights scale score for participant_s country, from -4 to 4",
                     "dem_3_hrs_group": "human rights scale category",
                     "dem_3_hdi": "human development index score for participant_s country, from 0 to 1",
                     "dem_3_hdi_group": "human development index category",
                     "dem_3_OxCGRT_gov": "score for country on day of starting quiz for overall government response to covid",
                     "dem_3_OxCGRT_econ": "score for country on day of starting quiz for economic support to citizens and provision of foreign aid",
                     "dem_3_OxCGRT_contain": "score for country on day of starting quiz for containment and health system policies",
                     "dem_3_OxCGRT_str": "score for country on day of starting quiz for the stringency of the country_s lockdown",
                     "dem_factor_ncrf": "average of scores for OxCGRT_gov, OxCGRT_contain and OxCGRT_str",
                     "dem_factor_ssf": "average of scores for OxCGRT_econ, hrs and hdi",
                     "adherence_dv": "sum of scores for questions relating to adherence max 60",
                     "poor_coping_dv": "sum of scores for questions relating to poor coping max 61"
                     },
    "free_recall": {"ResponseId": "",
                    "progress_complete": "all questions up to the end of HADS answered",
                    "free_recall_input": "the participants original answer",
                    "free_recall": "the answer as processed for scoring",
                    "total_score": "number of correct words",
                    "total_abstract": "",
                    "total_concrete": "",
                    "total_neutral": "",
                    "total_emotional": "",
                    "non_matching_words": "words that were not scored",
                    "translated": "1 = free recall input was manually translated by us"},
    "working_memory": {"ResponseId": "",
                       "progress_complete": "all questions up to the end of HADS answered",
                       "q1_a": "B-R-N",
                       "q2_a": "Q-R-T-S",
                       "q3_a": "H-W-D-N-P",
                       "q4_a": "Y-P-K-D-F-C",
                       "q5_a": "M-F-S-G-B-R-K",
                       "q6_a": "P-M-J-H-S-W-C-N",
                       "q7_a": "K-N-P-F-G-Q-S-L-P",
                       "q8_a": "P-K-M-H-L-G-D-W-Z-Q",
                       "q1": "score for q1",
                       "q2": "score for q2",
                       "q3": "score for q3",
                       "q4": "score for q4",
                       "q5": "score for q5",
                       "q6": "score for q6",
                       "q7": "score for q7",
                       "q8": "score for q8",
                       "score_8": "each correct answer scores 1 out of a possible 8",
                       "score_36": "each question is scored according to the number of extra letters - q1 receives 1 point, q2 receives 2 points if correct, q8 receives 8 points.",
                       "score_hardest_correct": "the score represents the hardest question they answered correctly: if a participant got q7 wrong but question 8 right, they received a score of 8",
                       "score_to_first_mistake": "number of letters in last correct answer up to the first mistake",
                       "diff_free_recall_wm_36": "score for working_memory score out of 36 and subtracted free_recall total score (max 30)",
                       "to_be_excluded": "gives a 1 to participants  where score_36 >= 35 and diff_free_recall >= 34 as well as participants who were not analysed in working memory"},
    "lockdown": {"ResponseId": "",
                 "progress_complete": "all questions up to the end of HADS answered",
                 "q1": "I followed the COVID lockdown rules",
                 "q2": "I supported lockdown measures",
                 "q3": "SPACE: I am adhering to social distancing rules",
                 "q4": "HANDS: I wash hands more often for at least 20 seconds",
                 "q5": "I cover my mouth when coughing",
                 "q6": "I avoid close contact with someone who is infected",
                 "q7": "I have been avoiding places where many people are most likely to gather (e.g. parks, beaches, other outdoor spaces)",
                 "q8": "I have been taking homeopathic remedies to help overcome the coronavirus",
                 "q9": "I have been taking herbal remedies to help overcome the coronavirus",
                 "q10": "I have been avoiding eating meat to help overcome the coronavirus",
                 "q11": "I have been drinking ginger tea to help overcome the coronavirs",
                 "q12": "I have been using antibiotics to help overcome the coronavirus",
                 "q13": "During the COVID lockdown I met up with friends or family outside the home",
                 "q14": "During the COVID lockdown had friends or family visit me at home",
                 "q15": "I have been outside when having coronavirus-like symptoms",
                 "q16": "I have had a confirmed case of coronavirus",
                 "q17": "I have NOT had a confirmed case of coronavirus, but I think I MIGHT have had it",
                 "q18": "I have been in contact with a counselling or support service",
                 "q19": "I support police powers during the COVID crisis",
                 "q20": "I agree with the following statement: Too much fuss is being made about the risk of coronavirus:",
                 "q21": "I agree with the following statement: The coronavirus was probably created in a laboratory:",
                 "q22": "I agree with the following statement: Most people in the UK have already had coronavirus without realising it:",
                 "q23": "I agree with the following statement: Pets can transmit coronavirus:",
                 "q24": "I agree with the following statement: Coronavirus can last on some surfaces for up to 7 days:",
                 "q25": "I agree with the following statement: Sanitising hand gels are more effective at and water: coronavirus than washing your hands with soap protecting you from",
                 "q26": "FACE: I agree with the following statement: The NHS recommends that you should wear a face mask when you are out, even if you do not have coronavirus",
                 "q27": "I agree with the following statement: There will be a quick resolution to the coronavirus crisis and lockdown measures will end soon:",
                 "q28": "I am closely following official guidance/recommendations on how to protect myself and others",
                 "q29": "I have lost sleep over coronavirus",
                 "q30": "My eating patterns have changed during the coronavirus lockdown:",
                 "q31": "I am eating much more HEALTHY food",
                 "q32": "I am eating much more UNHEALTHY food",
                 "q33": "I am drinking much more alcohol",
                 "q34": "I am using non-prescription drugs (e.g. painkillers, other over-the-counter rememdies) much more",
                 "q35": "I am finding the coronavirus outbreak and/or the lockdown measures extremely difficult to cope with",
                 "q36": "I have been spending time thinking about the coronavirus",
                 "q37": "I have argued more with family/people in the home during the COVID lockdown",
                 "q38": "I feel more anxious since the lockdown measures were introduced",
                 "q39": "I feel more depressed since the lockdown measures were introduced",
                 "q40": "I feel helpless as a result of coronavirus",
                 "q41": "I will lose my job as a result of coronavirus and/or the lockdown",
                 "q42": "I will experience financial difficulties as a result of coronavirus and/or the lockdown",
                 "q43": "Life will return to normal soon",
                 "q44": "The economy will start to grow again soon",
                 "q45": "We will be able to vaccinate the population against coronavirus soon",
                 "q46": "Schools will stay closed in the future",
                 "q47": "Older people and those with underlying health issues will continue to be asked to remain home",
                 "q48": "My countrys government has handled the crisis:",
                 "q49": "I would describe my trust in my countrys government to control the spread of coronavirus as:",
                 "q50": "I would describe my trust in the coronavirus information my countrys government provides as:",
                 "q51": "My belief that the government acted too slowly to control the spread of coronavirus is:",
                 "q52": "My belief that the government communication provided helpful advice:",
                 "q53": "My belief that the government plan responded well to the changing scientific information and situation:",
                 "q54": "I check social media for information or updates about coronavirus:",
                 "self_medication": "qs 8-12, 15, 34.",
                 "government_response": "qs 48-53",
                 "anxiety_mood": "qs 29, 35-40",
                 "adherence": "qs 1-7, 28",
                 "skepticism_paranoia": "qs 20-22",
                 "hopefulness": "qs 27, 43-45",
                 "unhealthy_consumption": "qs 30, 32, 33",
                 "social_contact": "qs 13, 14",
                 "continued_lockdown": "qs 46, 47",
                 "fomites": "qs 23, 24",
                 "financial_insecurity": "qs 41, 42",
                 "suspected_infection": "q 17"},
    "ocir": {"ResponseId": "",
             "progress_complete": "all questions up to the end of HADS answered",
             "q1": "hoarding: I have saved up so many things that they get in the way",
             "q2": "checking: I check things more often than necessary",
             "q3": "ordering: I get upset if objects are not arranged properly",
             "q4": "neutralising: I feel compelled to count while I am doing things",
             "q5": "washing: I find it difficult to touch an object when I know it has been touched by strangers or certain people",
             "q6": "obsessing: I find it difficult to control my thoughts",
             "q7": "hoarding: I collect things I dont need",
             "q8": "checking: I repeatedly check doors, windows, drawers, etc.",
             "q9": "ordering: I get upset if others change the way I have arranged things",
             "q10": "neutralising: I feel I have to repeat certain numbers",
             "q11": "washing: I sometimes have to wash or clean myself simply because I feel contaminated",
             "q12": "obsessing: I am upset by unpleasant thoughts that come into my mind against my will",
             "q13": "hoarding: I avoid throwing things away because I am afraid I might need them later",
             "q14": "checking: I repeatedly check gas and water taps and light switches after turning them off",
             "q15": "ordering: I need things to be arranged in a particular order",
             "q16": "neutralising: I feel that there are good numbers and bad numbers",
             "q17": "washing: I wash my hands more often and longer than necessary",
             "q18": "obsessing: I frequently get nasty thoughts and have difficulty in getting rid of them",
             "hoarding_score": "qs 1, 7, 13",
             "checking_score": "qs 2, 8, 14",
             "ordering_score": "qs 3, 9, 15",
             "neutralising_score": "qs 4, 10, 16",
             "washing_score": "qs 5, 11, and 17",
             "obsessing_score": "qs 6, 12, 18",
             "total_score": "total score out of 72"},
    "srq": {"ResponseId": "",
            "progress_complete": "all questions up to the end of HADS answered",
            "q1": "Receiving: I usually keep track of my progress toward my goals",
            "q2": "evaluating: My behaviour is not that different from other peoples",
            "q3": "triggering: Others tell me that I keep on with things too long.",
            "q4": "searching: I doubt I could change even if I wanted to",
            "q5": "planning: I have trouble making up my mind about things",
            "q6": "implementing: I get easily distracted from my plans",
            "q7": "assessing: I reward myself with progress toward my goals",
            "q8": "Receiving: I dont notice the effects of my actions until its too late",
            "q9": "evaluating: My behaviour is similar to that of my friends",
            "q10": "triggering: Its hard for me to see anything helpful about changing my ways",
            "q11": "searching: I am able to accomplish goals I set for myself",
            "q12": "planning: I put off making decisions",
            "q13": "implementing: I have so many plans that its hard for me to focus on any one of them",
            "q14": "assessing: I change the way I do things when I see a problem with how things are going",
            "q15": "Receiving: Its hard for me to notice when Ive had enough (alcohol, food, sweets)",
            "q16": "evaluating: I think a lot about what other people think of me",
            "q17": "triggering: I am willing to consider other ways of doing things",
            "q18": "searching: If I wanted to change, I am confident that I could do it",
            "q19": "planning: When it comes to deciding about a change, I feel overwhelmed by the choices",
            "q20": "implementing: I have trouble following through with things once Ive made up my mind to do something",
            "q21": "assessing: I dont seem to learn from my mistakes",
            "q22": "Receiving: Im usually careful not to overdo it when working, eating, drinking",
            "q23": "evaluating: I tend to compare myself with other people",
            "q24": "triggering: I enjoy a routine, and like things to stay the same",
            "q25": "searching: I have sought out advice or information about changing",
            "q26": "planning: I can come up with lots of ways to change, but its hard for me to decide which one to use",
            "q27": "implementing: I can stick to a plan thats working well",
            "q28": "assessing: I usually only have to make a mistake one time in order to learn from it",
            "q29": "Receiving: I dont learn well from punishment",
            "q30": "evaluating: I have personal standards, and try to live up to them",
            "q31": "triggering: I am set in my ways",
            "q32": "searching: As soon as I see a problem or challenge, I start looking for possible solutions",
            "q33": "planning: I have a hard time setting goals for myself",
            "q34": "implementing: I have a lot of willpower",
            "q35": "assessing: When Im trying to change something, I pay a lot of attention to how Im doing",
            "q36": "Receiving: I usually judge what Im doing by the consequences of my actions",
            "q37": "evaluating: I dont care if Im different from most people",
            "q38": "triggering: As soon as I see things arent going right I want to do something about it",
            "q39": "searching: There is usually more than one way to accomplish something",
            "q40": "planning: I have trouble making plans to help me reach my goals",
            "q41": "implementing: I am able to resist temptation",
            "q42": "assessing: I set goals for myself and keep track of my progress",
            "q43": "Receiving: Most of the time I dont pay attention to what Im doing",
            "q44": "evaluating: I try to be like people around me",
            "q45": "triggering: I tend to keep doing the same thing, even when it doesnt work",
            "q46": "searching: I can usually find several different possibilities when I want to change something",
            "q47": "planning: Once I have a goal, I can usually plan how to reach it",
            "q48": "implementing: I have rules that I stick by no matter what",
            "q49": "assessing: If I make a resolution to change something, I pay a lot of attention to how Im doing",
            "q50": "Receiving: Often I dont notice what Im doing until someone calls it to my attention",
            "q51": "evaluating: I think a lot about how Im doing",
            "q52": "triggering: Usually I see the need to change before others do",
            "q53": "searching: Im good at finding different ways to get what I want",
            "q54": "planning: I usually think before I act",
            "q55": "implementing: Little problems or distractions throw me off course",
            "q56": "assessing: I feel bad when I dont meet my goals",
            "q57": "Receiving: I learn from my mistakes",
            "q58": "evaluating: I know how I want to be",
            "q59": "triggering: It bothers me when things arent the way I want them",
            "q60": "searching: I call in others for help when I need it",
            "q61": "planning: Before making a decision, I consider what is likely to happen if I do one thing or another",
            "q62": "implementing: I give up quickly",
            "q63": "assessing: I usually decide to change and hope for the best",
            "receiving_score": "qs 1, 8, 15, 22, 29, 36, 43, 50, 57:",
            "evaluating_score": "qs 2, 9, 16, 23, 30, 37, 44, 51, 58",
            "triggering_score": "qs 3, 10, 17, 24, 31, 38, 45, 52, 59",
            "searching_score": "qs 4, 11, 18, 25, 32, 39, 46, 53, 60",
            "planning_score": "qs 5, 12, 19, 26, 33, 40, 47, 54, 61",
            "implementing_score": "qs 6, 13, 20, 27, 34, 41, 48, 55, 62",
            "assessing_score": "qs 7, 14, 21, 28, 35, 42, 49, 56, 63",
            "total_score": "total score out of 315"},
    "hads": {"ResponseId": "",
             "progress_complete": "all questions up to the end of HADS answered",
             "q1": "A: I feel tense or wound up",
             "q2": "D: I feel as if I am slowed down",
             "q3": "D: I still enjoy the things I used to enjoy",
             "q4": "A: I get a sort of frightened feeling like butterflies in the stomach:",
             "q5": "A: I get a sort of frightened feeling as if something awful is about to happen",
             "q6": "D: I have lost interest in my appearance",
             "q7": "D: I can laugh and see the funny side of things",
             "q8": "A: I feel restless as I have to be on the move",
             "q9": "A: Worrying thoughts go through my mind",
             "q10": "D: I look forward with enjoyment to things",
             "q11": "D: I feel cheerful",
             "q12": "A: I can sit at ease and feel relaxed",
             "q13": "A: I get sudden feelings of panic",
             "q14": "D: I can enjoy a good book or programme",
             "depression_score": "qs 2, 3, 6, 7, 10, 11, 14",
             "anxiety_score": "qs 1, 4, 5, 8, 9, 12, 13",
             "total_score": "total score (most studies look at anxiety and depression separately rather than a total score)"},
    "text_questions": {"ResponseId": "None",
                       "progress_complete": "all questions up to the end of HADS answered",
                       "dem_3_location_input": "location",
                       "dem_6_loe_input": "level of education",
                       "source_status": "either IP address or spam",
                       "distribution_channel": "all responses are marked as anonymous",
                       "user_language": "all responses were set to english, irrespective of response language",
                       "start_date_bad_format": "date as month/day/year",
                       "end_date_bad_format": "date as month/day/year",
                       "recorded_date_bad_format": "date as month/day/year",
                       "ld_1": "I followed the COVID lockdown rules",
                       "ld_2": "I supported lockdown measures",
                       "ld_3": "SPACE: I am adhering to social distancing rules",
                       "ld_4": "HANDS: I wash hands more often for at least 20 seconds",
                       "ld_5": "I cover my mouth when coughing",
                       "ld_6": "I avoid close contact with someone who is infected",
                       "ld_7": "I have been avoiding places where many people are most likely to gather (e.g. parks, beaches, other outdoor spaces)",
                       "ld_8": "I have been taking homeopathic remedies to help overcome the coronavirus",
                       "ld_9": "I have been taking herbal remedies to help overcome the coronavirus",
                       "ld_10": "I have been avoiding eating meat to help overcome the coronavirus",
                       "ld_11": "I have been drinking ginger tea to help overcome the coronavirs",
                       "ld_12": "I have been using antibiotics to help overcome the coronavirus",
                       "ld_13": "During the COVID lockdown I met up with friends or family outside the home",
                       "ld_14": "During the COVID lockdown had friends or family visit me at home",
                       "ld_15": "I have been outside when having coronavirus-like symptoms",
                       "ld_16": "I have had a confirmed case of coronavirus",
                       "ld_17": "I have NOT had a confirmed case of coronavirus, but I think I MIGHT have had it",
                       "ld_18": "I have been in contact with a counselling or support service",
                       "ld_19": "I support police powers during the COVID crisis",
                       "ld_20": "I agree with the following statement: Too much fuss is being made about the risk of coronavirus:",
                       "ld_21": "I agree with the following statement: The coronavirus was probably created in a laboratory:",
                       "ld_22": "I agree with the following statement: Most people in the UK have already had coronavirus without realising it:",
                       "ld_23": "I agree with the following statement: Pets can transmit coronavirus:",
                       "ld_24": "I agree with the following statement: Coronavirus can last on some surfaces for up to 7 days:",
                       "ld_25": "I agree with the following statement: Sanitising hand gels are more effective at and water: coronavirus than washing your hands with soap protecting you from",
                       "ld_26": "FACE: I agree with the following statement: The NHS recommends that you should wear a face mask when you are out, even if you do not have coronavirus",
                       "ld_27": "I agree with the following statement: There will be a quick resolution to the coronavirus crisis and lockdown measures will end soon:",
                       "ld_28": "I am closely following official guidance/recommendations on how to protect myself and others",
                       "ld_29": "I have lost sleep over coronavirus",
                       "ld_30": "My eating patterns have changed during the coronavirus lockdown:",
                       "ld_31": "I am eating much more HEALTHY food",
                       "ld_32": "I am eating much more UNHEALTHY food",
                       "ld_33": "I am drinking much more alcohol",
                       "ld_34": "I am using non-prescription drugs (e.g. painkillers, other over-the-counter rememdies) much more",
                       "ld_35": "I am finding the coronavirus outbreak and/or the lockdown measures extremely difficult to cope with",
                       "ld_36": "I have been spending time thinking about the coronavirus",
                       "ld_37": "I have argued more with family/people in the home during the COVID lockdown",
                       "ld_38": "I feel more anxious since the lockdown measures were introduced",
                       "ld_39": "I feel more depressed since the lockdown measures were introduced",
                       "ld_40": "I feel helpless as a result of coronavirus",
                       "ld_41": "I will lose my job as a result of coronavirus and/or the lockdown",
                       "ld_42": "I will experience financial difficulties as a result of coronavirus and/or the lockdown",
                       "ld_43": "Life will return to normal soon",
                       "ld_44": "The economy will start to grow again soon",
                       "ld_45": "We will be able to vaccinate the population against coronavirus soon",
                       "ld_46": "Schools will stay closed in the future",
                       "ld_47": "Older people and those with underlying health issues will continue to be asked to remain home",
                       "ld_48": "My countrys government has handled the crisis:",
                       "ld_49": "I would describe my trust in my countrys government to control the spread of coronavirus as:",
                       "ld_50": "I would describe my trust in the coronavirus information my countrys government provides as:",
                       "ld_51": "My belief that the government acted too slowly to control the spread of coronavirus is:",
                       "ld_52": "My belief that the government communication provided helpful advice:",
                       "ld_53": "My belief that the government plan responded well to the changing scientific information and situation:",
                       "ld_54": "I check social media for information or updates about coronavirus:",
                       "OCIR_1": "hoarding: I have saved up so many things that they get in the way",
                       "OCIR_2": "checking: I check things more often than necessary",
                       "OCIR_3": "ordering: I get upset if objects are not arranged properly",
                       "OCIR_4": "neutralising: I feel compelled to count while I am doing things",
                       "OCIR_5": "washing: I find it difficult to touch an object when I know it has been touched by strangers or certain people",
                       "OCIR_6": "obsessing: I find it difficult to control my thoughts",
                       "OCIR_7": "hoarding: I collect things I dont need",
                       "OCIR_8": "checking: I repeatedly check doors, windows, drawers, etc.",
                       "OCIR_9": "ordering: I get upset if others change the way I have arranged things",
                       "OCIR_10": "neutralising: I feel I have to repeat certain numbers",
                       "OCIR_11": "washing: I sometimes have to wash or clean myself simply because I feel contaminated",
                       "OCIR_12": "obsessing: I am upset by unpleasant thoughts that come into my mind against my will",
                       "OCIR_13": "hoarding: I avoid throwing things away because I am afraid I might need them later",
                       "OCIR_14": "checking: I repeatedly check gas and water taps and light switches after turning them off",
                       "OCIR_15": "ordering: I need things to be arranged in a particular order",
                       "OCIR_16": "neutralising: I feel that there are good numbers and bad numbers",
                       "OCIR_17": "washing: I wash my hands more often and longer than necessary",
                       "OCIR_18": "obsessing: I frequently get nasty thoughts and have difficulty in getting rid of them",
                       "SRQ_1": "Receiving: I usually keep track of my progress toward my goals",
                       "SRQ_2": "evaluating: My behaviour is not that different from other peoples",
                       "SRQ_3": "triggering: Others tell me that I keep on with things too long.",
                       "SRQ_4": "searching: I doubt I could change even if I wanted to",
                       "SRQ_5": "planning: I have trouble making up my mind about things",
                       "SRQ_6": "implementing: I get easily distracted from my plans",
                       "SRQ_7": "assessing: I reward myself with progress toward my goals",
                       "SRQ_8": "receiving: I dont notice the effects of my actions until its too late",
                       "SRQ_9": "evaluating: My behaviour is similar to that of my friends",
                       "SRQ_10": "triggering: Its hard for me to see anything helpful about changing my ways",
                       "SRQ_11": "searching: I am able to accomplish goals I set for myself",
                       "SRQ_12": "planning: I put off making decisions",
                       "SRQ_13": "implementing: I have so many plans that its hard for me to focus on any one of them",
                       "SRQ_14": "assessing: I change the way I do things when I see a problem with how things are going",
                       "SRQ_15": "Receiving: Its hard for me to notice when Ive had enough (alcohol, food, sweets)",
                       "SRQ_16": "evaluating: I think a lot about what other people think of me",
                       "SRQ_17": "triggering: I am willing to consider other ways of doing things",
                       "SRQ_18": "searching: If I wanted to change, I am confident that I could do it",
                       "SRQ_19": "planning: When it comes to deciding about a change, I feel overwhelmed by the choices",
                       "SRQ_20": "implementing: I have trouble following through with things once Ive made up my mind to do something",
                       "SRQ_21": "assessing: I dont seem to learn from my mistakes",
                       "SRQ_22": "Receiving: Im usually careful not to overdo it when working, eating, drinking",
                       "SRQ_23": "evaluating: I tend to compare myself with other people",
                       "SRQ_24": "triggering: I enjoy a routine, and like things to stay the same",
                       "SRQ_25": "searching: I have sought out advice or information about changing",
                       "SRQ_26": "planning: I can come up with lots of ways to change, but its hard for me to decide which one to use",
                       "SRQ_27": "implementing: I can stick to a plan thats working well",
                       "SRQ_28": "assessing: I usually only have to make a mistake one time in order to learn from it",
                       "SRQ_29": "Receiving: I dont learn well from punishment",
                       "SRQ_30": "evaluating: I have personal standards, and try to live up to them",
                       "SRQ_31": "triggering: I am set in my ways",
                       "SRQ_32": "searching: As soon as I see a problem or challenge, I start looking for possible solutions",
                       "SRQ_33": "planning: I have a hard time setting goals for myself",
                       "SRQ_34": "implementing: I have a lot of willpower",
                       "SRQ_35": "assessing: When Im trying to change something, I pay a lot of attention to how Im doing",
                       "SRQ_36": "Receiving: I usually judge what Im doing by the consequences of my actions",
                       "SRQ_37": "evaluating: I dont care if Im different from most people",
                       "SRQ_38": "triggering: As soon as I see things arent going right I want to do something about it",
                       "SRQ_39": "searching: There is usually more than one way to accomplish something",
                       "SRQ_40": "planning: I have trouble making plans to help me reach my goals",
                       "SRQ_41": "implementing: I am able to resist temptation",
                       "SRQ_42": "assessing: I set goals for myself and keep track of my progress",
                       "SRQ_43": "Receiving: Most of the time I dont pay attention to what Im doing",
                       "SRQ_44": "evaluating: I try to be like people around me",
                       "SRQ_45": "triggering: I tend to keep doing the same thing, even when it doesnt work",
                       "SRQ_46": "searching: I can usually find several different possibilities when I want to change something",
                       "SRQ_47": "planning: Once I have a goal, I can usually plan how to reach it",
                       "SRQ_48": "implementing: I have rules that I stick by no matter what",
                       "SRQ_49": "assessing: If I make a resolution to change something, I pay a lot of attention to how Im doing",
                       "SRQ_50": "Receiving: Often I dont notice what Im doing until someone calls it to my attention",
                       "SRQ_51": "evaluating: I think a lot about how Im doing",
                       "SRQ_52": "triggering: Usually I see the need to change before others do",
                       "SRQ_53": "searching: Im good at finding different ways to get what I want",
                       "SRQ_54": "planning: I usually think before I act",
                       "SRQ_55": "implementing: Little problems or distractions throw me off course",
                       "SRQ_56": "assessing: I feel bad when I dont meet my goals",
                       "SRQ_57": "Receiving: I learn from my mistakes",
                       "SRQ_58": "evaluating: I know how I want to be",
                       "SRQ_59": "triggering: It bothers me when things arent the way I want them",
                       "SRQ_60": "searching: I call in others for help when I need it",
                       "SRQ_61": "planning: Before making a decision, I consider what is likely to happen if I do one thing or another",
                       "SRQ_62": "implementing: I give up quickly",
                       "SRQ_63": "assessing: I usually decide to change and hope for the best",
                       "HADS_1": "A: I feel tense or wound up",
                       "HADS_2": "D: I feel as if I am slowed down",
                       "HADS_3": "D: I still enjoy the things I used to enjoy",
                       "HADS_4": "A: I get a sort of frightened feeling like butterflies in the stomach:",
                       "HADS_5": "A: I get a sort of frightened feeling as if something awful is about to happen",
                       "HADS_6": "D: I have lost interest in my appearance",
                       "HADS_7": "D: I can laugh and see the funny side of things",
                       "HADS_8": "A: I feel restless as I have to be on the move",
                       "HADS_9": "A: Worrying thoughts go through my mind",
                       "HADS_10": "D: I look forward with enjoyment to things",
                       "HADS_11": "D: I feel cheerful",
                       "HADS_12": "A: I can sit at ease and feel relaxed",
                       "HADS_13": "A: I get sudden feelings of panic",
                       "HADS_14": "D: I can enjoy a good book or programme"},
    "compiled_data": {"ResponseId": "",
                      "Participant_ID": "deprecated: correlates to previous data-set",
                      "cluster": "cluster based on K-means analysis of lockdwon factors.",
                      "KCL_Categories": "from a previous study",
                      "Cluster_No": "to be redone",
                      "Progress": "progress as a percent",
                      "consent": "",
                      "dem_1_age": "age",
                      "dem_1_age_group": "quartiles of age distribution",
                      "dem_2_gender": "gender",
                      "dem_3_country": "country",
                      "dem_3_continent": "regional grouping for participant_s country",
                      "dem_3_hrs": "human rights scale score for participant_s country, from -4 to 4",
                      "dem_3_hrs_group": "human rights scale category",
                      "dem_3_hdi": "human development index score for participant_s country, from 0 to 1",
                      "dem_3_hdi_group": "human development index category",
                      "dem_3_OxCGRT_gov": "score for country on day of starting quiz for overall government response to covid",
                      "dem_3_OxCGRT_econ": "score for country on day of starting quiz for economic support to citizens and provision of foreign aid",
                      "dem_3_OxCGRT_contain": "score for country on day of starting quiz for containment and health system policies",
                      "dem_3_OxCGRT_str": "score for country on day of starting quiz for the stringency of the country_s lockdown",
                      "dem_4_politics": "political divide",
                      "dem_5_brexit": "Brexit",
                      "dem_6_loe": "highest level of education",
                      "StartDate": "date as yy/mm/dd",
                      "EndDate": "date as yy/mm/dd",
                      "RecordedDate": "date as yy/mm/dd",
                      "dem_factor_ncrf": "average of scores for OxCGRT_gov, OxCGRT_contain and OxCGRT_str",
                      "dem_factor_ssf": "average of scores for OxCGRT_econ, hrs and hdi",
                      "free_recall": "the answer as processed for scoring",
                      "free_recall_translated": "1 = free recall input was manually translated by us",
                      "free_recall_total_score": "number of correct words",
                      "free_recall_total_abstract": "",
                      "free_recall_total_concrete": "",
                      "free_recall_total_neutral": "",
                      "free_recall_total_emotional": "",
                      "free_recall_non_matching_words": "",
                      "wm_q1": "score for q1",
                      "wm_q2": "score for q2",
                      "wm_q3": "score for q3",
                      "wm_q4": "score for q4",
                      "wm_q5": "score for q5",
                      "wm_q6": "score for q6",
                      "wm_q7": "score for q7",
                      "wm_q8": "score for q8",
                      "wm_score_8": "each correct answer scores 1 out of a possible 8",
                      "wm_score_36": "each question is scored according to the number of extra letters - q1 receives 1 point, q2 receives 2 points if correct, q8 receives 8 points.",
                      "wm_score_hardest_correct": "question number of the hardest question correctly answered",
                      "wm_score_to_first_mistake": "number of letters in last correct answer up to the first mistake",
                      "wm_diff_free_recall_wm_36": "score for working_memory score out of 36 and subtracted free_recall total score (max 30)",
                      "wm_to_be_excluded": "gives a 1 to participants  where score_36 >= 35 and diff_free_recall >= 34 as well as participants who were not analysed in working memory",
                      "ld_q1": "I followed the COVID lockdown rules",
                      "ld_q2": "I supported lockdown measures",
                      "ld_q3": "SPACE: I am adhering to social distancing rules",
                      "ld_q4": "HANDS: I wash hands more often for at least 20 seconds",
                      "ld_q5": "I cover my mouth when coughing",
                      "ld_q6": "I avoid close contact with someone who is infected",
                      "ld_q7": "I have been avoiding places where many people are most likely to gather (e.g. parks, beaches, other outdoor spaces)",
                      "ld_q8": "I have been taking homeopathic remedies to help overcome the coronavirus",
                      "ld_q9": "I have been taking herbal remedies to help overcome the coronavirus",
                      "ld_q10": "I have been avoiding eating meat to help overcome the coronavirus",
                      "ld_q11": "I have been drinking ginger tea to help overcome the coronavirs",
                      "ld_q12": "I have been using antibiotics to help overcome the coronavirus",
                      "ld_q13": "During the COVID lockdown I met up with friends or family outside the home",
                      "ld_q14": "During the COVID lockdown had friends or family visit me at home",
                      "ld_q15": "I have been outside when having coronavirus-like symptoms",
                      "ld_q16": "I have had a confirmed case of coronavirus",
                      "ld_q17": "I have NOT had a confirmed case of coronavirus, but I think I MIGHT have had it",
                      "ld_q18": "I have been in contact with a counselling or support service",
                      "ld_q19": "I support police powers during the COVID crisis",
                      "ld_q20": "I agree with the following statement: Too much fuss is being made about the risk of coronavirus:",
                      "ld_q21": "I agree with the following statement: The coronavirus was probably created in a laboratory:",
                      "ld_q22": "I agree with the following statement: Most people in the UK have already had coronavirus without realising it:",
                      "ld_q23": "I agree with the following statement: Pets can transmit coronavirus:",
                      "ld_q24": "I agree with the following statement: Coronavirus can last on some surfaces for up to 7 days:",
                      "ld_q25": "I agree with the following statement: Sanitising hand gels are more effective at and water: coronavirus than washing your hands with soap protecting you from",
                      "ld_q26": "FACE: I agree with the following statement: The NHS recommends that you should wear a face mask when you are out, even if you do not have coronavirus",
                      "ld_q27": "I agree with the following statement: There will be a quick resolution to the coronavirus crisis and lockdown measures will end soon:",
                      "ld_q28": "I am closely following official guidance/recommendations on how to protect myself and others",
                      "ld_q29": "I have lost sleep over coronavirus",
                      "ld_q30": "My eating patterns have changed during the coronavirus lockdown:",
                      "ld_q31": "I am eating much more HEALTHY food",
                      "ld_q32": "I am eating much more UNHEALTHY food",
                      "ld_q33": "I am drinking much more alcohol",
                      "ld_q34": "I am using non-prescription drugs (e.g. painkillers, other over-the-counter rememdies) much more",
                      "ld_q35": "I am finding the coronavirus outbreak and/or the lockdown measures extremely difficult to cope with",
                      "ld_q36": "I have been spending time thinking about the coronavirus",
                      "ld_q37": "I have argued more with family/people in the home during the COVID lockdown",
                      "ld_q38": "I feel more anxious since the lockdown measures were introduced",
                      "ld_q39": "I feel more depressed since the lockdown measures were introduced",
                      "ld_q40": "I feel helpless as a result of coronavirus",
                      "ld_q41": "I will lose my job as a result of coronavirus and/or the lockdown",
                      "ld_q42": "I will experience financial difficulties as a result of coronavirus and/or the lockdown",
                      "ld_q43": "Life will return to normal soon",
                      "ld_q44": "The economy will start to grow again soon",
                      "ld_q45": "We will be able to vaccinate the population against coronavirus soon",
                      "ld_q46": "Schools will stay closed in the future",
                      "ld_q47": "Older people and those with underlying health issues will continue to be asked to remain home",
                      "ld_q48": "My countrys government has handled the crisis:",
                      "ld_q49": "I would describe my trust in my countrys government to control the spread of coronavirus as:",
                      "ld_q50": "I would describe my trust in the coronavirus information my countrys government provides as:",
                      "ld_q51": "My belief that the government acted too slowly to control the spread of coronavirus is:",
                      "ld_q52": "My belief that the government communication provided helpful advice:",
                      "ld_q53": "My belief that the government plan responded well to the changing scientific information and situation:",
                      "ld_q54": "I check social media for information or updates about coronavirus:",
                      "ld_self_medication": "higher score = high consumption of homeopathic and herbal remedies, avoids eating meat, drinks ginger tea, uses antibiotics, uses non-prescription drugs, has been outside with coronavirus-like symptoms",
                      "ld_government_response": "higher score = believes that their government has handled the crisis consistently and organisedly and has responded well to the changing evidence and situation, has high trust/faith in the government's ability to control the virus"
                                                "and provide information, does not believe that the govenment acted too slowly",
                      "ld_anxiety_mood": "higher score = has lost sleep, has found the outbreak/lockdown measures difficult to cope with, has spent a lot of time thinking about the virus, is arguing more, feels more anxious, depressed and helpless ",
                      "ld_adherence": "higher score = reports following lockdown rules more, supports lockdown measures, adheres to social distancing, washes hands for at least 20 secs, covers their mouth "
                                      "avoids contact with those infected, avoids gathering places, closely follows guidelines",
                      "ld_skepticism_paranoia": "higher score = believes that too much fuss is being made over the virus, that it was probably created in a laboratory, and that most people in the UK have already had the virus",
                      "ld_hopefulness": "higher score = believes that there will be a quick resolution and that things will return to normal soon, that the economy will start to grow again soon, and that they would be able to vaccinate people soon",
                      "ld_unhealthy_consumption": "higher score = has been eating more than usual, has been eating more unhealthy food, and has been drinking more alcohol",
                      "ld_social_contact": "higher score = has met up more frequently with others outside the home and had people visit more often",
                      "ld_continued_lockdown": "higher score = believes that schools will stay closed and that older people will continue to be asked to remain at home",
                      "ld_fomites": "higher score = agrees more that pets can transmit the virus and that coronavirus can last on some surfaces for up to 7 days",
                      "financial_insecurity": "higher score = is certain that they will lose their job and experience financial difficulties because of the virus/lockdown",
                      "ld_suspected_infection": "2 = has not had a confirmed case, but thinks they might have had it. 1= does not think they have had it",
                      "adherence_dv": "sum of scores for questions relating to adherence max 60",
                      "poor_coping_dv": "sum of scores for questions relating to poor coping max 61",
                      "ocir_q1": "hoarding: I have saved up so many things that they get in the way",
                      "ocir_q2": "checking: I check things more often than necessary",
                      "ocir_q3": "ordering: I get upset if objects are not arranged properly",
                      "ocir_q4": "neutralising: I feel compelled to count while I am doing things",
                      "ocir_q5": "washing: I find it difficult to touch an object when I know it has been touched by strangers or certain people",
                      "ocir_q6": "obsessing: I find it difficult to control my thoughts",
                      "ocir_q7": "hoarding: I collect things I dont need",
                      "ocir_q8": "checking: I repeatedly check doors, windows, drawers, etc.",
                      "ocir_q9": "ordering: I get upset if others change the way I have arranged things",
                      "ocir_q10": "neutralising: I feel I have to repeat certain numbers",
                      "ocir_q11": "washing: I sometimes have to wash or clean myself simply because I feel contaminated",
                      "ocir_q12": "obsessing: I am upset by unpleasant thoughts that come into my mind against my will",
                      "ocir_q13": "hoarding: I avoid throwing things away because I am afraid I might need them later",
                      "ocir_q14": "checking: I repeatedly check gas and water taps and light switches after turning them off",
                      "ocir_q15": "ordering: I need things to be arranged in a particular order",
                      "ocir_q16": "neutralising: I feel that there are good numbers and bad numbers",
                      "ocir_q17": "washing: I wash my hands more often and longer than necessary",
                      "ocir_q18": "obsessing: I frequently get nasty thoughts and have difficulty in getting rid of them",
                      "ocir_hoarding_score": "qs 1, 7, 13",
                      "ocir_checking_score": "qs 2, 8, 14",
                      "ocir_ordering_score": "qs 3, 9, 15",
                      "ocir_neutralising_score": "qs 4, 10, 16",
                      "ocir_washing_score": "qs 5, 11, and 17",
                      "ocir_obsessing_score": "qs 6, 12, 18",
                      "ocir_total_score": "total score out of 72",
                      "srq_q1": "Receiving: I usually keep track of my progress toward my goals",
                      "srq_q2": "evaluating: My behaviour is not that different from other peoples",
                      "srq_q3": "triggering: Others tell me that I keep on with things too long.",
                      "srq_q4": "triggering: I doubt I could change even if I wanted to",
                      "srq_q5": "searching: I have trouble making up my mind about things",
                      "srq_q6": "planning: I get easily distracted from my plans",
                      "srq_q7": "implementing: I reward myself with progress toward my goals",
                      "srq_q8": "assessing: I dont notice the effects of my actions until its too late",
                      "srq_q9": "evaluating: My behaviour is similar to that of my friends",
                      "srq_q10": "triggering: Its hard for me to see anything helpful about changing my ways",
                      "srq_q11": "searching: I am able to accomplish goals I set for myself",
                      "srq_q12": "planning: I put off making decisions",
                      "srq_q13": "implementing: I have so many plans that its hard for me to focus on any one of them",
                      "srq_q14": "assessing: I change the way I do things when I see a problem with how things are going",
                      "srq_q15": "Receiving: Its hard for me to notice when Ive had enough (alcohol, food, sweets)",
                      "srq_q16": "evaluating: I think a lot about what other people think of me",
                      "srq_q17": "triggering: I am willing to consider other ways of doing things",
                      "srq_q18": "searching: If I wanted to change, I am confident that I could do it",
                      "srq_q19": "planning: When it comes to deciding about a change, I feel overwhelmed by the choices",
                      "srq_q20": "implementing: I have trouble following through with things once Ive made up my mind to do something",
                      "srq_q21": "assessing: I dont seem to learn from my mistakes",
                      "srq_q22": "Receiving: Im usually careful not to overdo it when working, eating, drinking",
                      "srq_q23": "evaluating: I tend to compare myself with other people",
                      "srq_q24": "triggering: I enjoy a routine, and like things to stay the same",
                      "srq_q25": "searching: I have sought out advice or information about changing",
                      "srq_q26": "planning: I can come up with lots of ways to change, but its hard for me to decide which one to use",
                      "srq_q27": "implementing: I can stick to a plan thats working well",
                      "srq_q28": "assessing: I usually only have to make a mistake one time in order to learn from it",
                      "srq_q29": "Receiving: I dont learn well from punishment",
                      "srq_q30": "evaluating: I have personal standards, and try to live up to them",
                      "srq_q31": "triggering: I am set in my ways",
                      "srq_q32": "searching: As soon as I see a problem or challenge, I start looking for possible solutions",
                      "srq_q33": "planning: I have a hard time setting goals for myself",
                      "srq_q34": "implementing: I have a lot of willpower",
                      "srq_q35": "assessing: When Im trying to change something, I pay a lot of attention to how Im doing",
                      "srq_q36": "Receiving: I usually judge what Im doing by the consequences of my actions",
                      "srq_q37": "evaluating: I dont care if Im different from most people",
                      "srq_q38": "triggering: As soon as I see things arent going right I want to do something about it",
                      "srq_q39": "searching: There is usually more than one way to accomplish something",
                      "srq_q40": "planning: I have trouble making plans to help me reach my goals",
                      "srq_q41": "implementing: I am able to resist temptation",
                      "srq_q42": "assessing: I set goals for myself and keep track of my progress",
                      "srq_q43": "Receiving: Most of the time I dont pay attention to what Im doing",
                      "srq_q44": "evaluating: I try to be like people around me",
                      "srq_q45": "triggering: I tend to keep doing the same thing, even when it doesnt work",
                      "srq_q46": "searching: I can usually find several different possibilities when I want to change something",
                      "srq_q47": "planning: Once I have a goal, I can usually plan how to reach it",
                      "srq_q48": "implementing: I have rules that I stick by no matter what",
                      "srq_q49": "assessing: If I make a resolution to change something, I pay a lot of attention to how Im doing",
                      "srq_q50": "Receiving: Often I dont notice what Im doing until someone calls it to my attention",
                      "srq_q51": "evaluating: I think a lot about how Im doing",
                      "srq_q52": "triggering: Usually I see the need to change before others do",
                      "srq_q53": "searching: Im good at finding different ways to get what I want",
                      "srq_q54": "planning: I usually think before I act",
                      "srq_q55": "implementing: Little problems or distractions throw me off course",
                      "srq_q56": "assessing: I feel bad when I dont meet my goals",
                      "srq_q57": "Receiving: I learn from my mistakes",
                      "srq_q58": "evaluating: I know how I want to be",
                      "srq_q59": "triggering: It bothers me when things arent the way I want them",
                      "srq_q60": "searching: I call in others for help when I need it",
                      "srq_q61": "planning: Before making a decision, I consider what is likely to happen if I do one thing or another",
                      "srq_q62": "implementing: I give up quickly",
                      "srq_q63": "assessing: I usually decide to change and hope for the best",
                      "srq_receiving_score": "qs 1, 8, 15, 22, 29, 36, 43, 50, 57:",
                      "srq_evaluating_score": "qs 2, 9, 16, 23, 30, 37, 44, 51, 58",
                      "srq_triggering_score": "qs 3, 10, 17, 24, 31, 38, 45, 52, 59",
                      "srq_searching_score": "qs 4, 11, 18, 25, 32, 39, 46, 53, 60",
                      "srq_planning_score": "qs 5, 12, 19, 26, 33, 40, 47, 54, 61",
                      "srq_implementing_score": "qs 6, 13, 20, 27, 34, 41, 48, 55, 62",
                      "srq_assessing_score": "qs 7, 14, 21, 28, 35, 42, 49, 56, 63",
                      "srq_total_score": "total score out of 315",
                      "hads_q1": "A: I feel tense or wound up",
                      "hads_q2": "D: I feel as if I am slowed down",
                      "hads_q3": "D: I still enjoy the things I used to enjoy",
                      "hads_q4": "A: I get a sort of frightened feeling like butterflies in the stomach:",
                      "hads_q5": "A: I get a sort of frightened feeling as if something awful is about to happen",
                      "hads_q6": "D: I have lost interest in my appearance",
                      "hads_q7": "D: I can laugh and see the funny side of things",
                      "hads_q8": "A: I feel restless as I have to be on the move",
                      "hads_q9": "A: Worrying thoughts go through my mind",
                      "hads_q10": "D: I look forward with enjoyment to things",
                      "hads_q11": "D: I feel cheerful",
                      "hads_q12": "A: I can sit at ease and feel relaxed",
                      "hads_q13": "A: I get sudden feelings of panic",
                      "hads_q14": "D: I can enjoy a good book or programme",
                      "hads_depression_score": "qs 2, 3, 6, 7, 10, 11, 14",
                      "hads_anxiety_score": "qs 1, 4, 5, 8, 9, 12, 13",
                      "hads_total_score": "total score (most studies look at anxiety and depression separately rather than a total score)"},
    "dreams": {"ResponseId": "",
               "progress_complete": "all questions up to the end of HADS answered",
               "dream": ""}
}


def write_labels(specified_table: str) -> str:
    query_str: str = "variable labels "
    for column_name, label in question_dict[specified_table].items():
        query_str += column_name + " '" + label + "'/"
    query_str = query_str[:-1] + "."
    return query_str


def get_tables(cursor: MySQLCursor) -> Set[str]:
    cursor.execute("SHOW TABLES from covid_data;")
    tables_raw: List[Dict[str, str]] = cursor.fetchall()
    tables: Set[str] = set()
    for row in tables_raw:
        if row['Tables_in_covid_data'] == "ben_data":
            continue
        else:
            tables.add(row['Tables_in_covid_data'])
    return tables


def create_import_query(table_list: Set[str]) -> Dict[str, str]:
    import_queries: Dict[str, str] = {}
    for table in table_list:
        query_string: str = f"""
            GET DATA
            /TYPE=ODBC
            /CONNECT='DSN=localdb;UID=root;PWD=,f#P,l-^,~(w#N(t%y!M/B$w-A&y!W+M,w#w/M/X,r;'
            /SQL='SELECT *'+
            'FROM covid_data.{table}'
            /ASSUMEDSTRWIDTH=255.
            CACHE.
            EXECUTE.
            DATASET NAME {table} WINDOW=FRONT.
            """
        import_queries[table] = query_string
    return import_queries


def copy2clip(txt) -> int:
    cmd = 'echo ' + txt.strip() + '|clip'
    return check_call(cmd, shell=True)


def create_query_to_set_value_labels(table_names: Set[str], include_measure: bool) -> Dict[str, str]:
    value_label_query: Dict[str, str] = {}
    for table in table_names:
        print(table)
        query: str = ""
        if table == 'compiled_data':
            query: str = write_compiled_query()
            if include_measure is True:
                query += "\nVARIABLE LEVEL Progress (scale) / cluster (nominal) / dem_1_age (scale) / dem_1_age_group (ordinal) /" \
                         "dem_2_gender to dem_3_continent (nominal) / dem_3_hrs (scale) / dem_3_hrs_group (ordinal) / " \
                         "dem_3_hdi (scale) / dem_3_hdi_group (ordinal) / dem_3_OxCGRT_gov to dem_3_OxCGRT_str (scale) / " \
                         "dem_4_politics to dem_6_loe (ordinal) / StartDate to free_recall_total_emotional (scale) / " \
                         "wm_q1 to wm_q8 (ordinal) / wm_score_8 to wm_diff_free_recall_wm_36 (scale)/" \
                         "wm_to_be_excluded (nominal)/" \
                         "ld_q1 to hads_total_score  (scale)\n"
        elif table == 'demographics':
            query: str = write_demographics_query()
            if include_measure is True:
                query += "\n VARIABLE LEVEL Progress (scale) / progress_group (ordinal) / cluster (nominal) / Durationinseconds (scale) / " \
                         "dem_1_age (scale) / dem_1_age_group (ordinal) / dem_2_gender to dem_3_continent (nominal) / " \
                         "dem_3_hrs (scale) / dem_3_hrs_group (ordinal) / dem_3_hdi (scale) / dem_3_hdi_group (ordinal) / " \
                         "dem_3_OxCGRT_gov to dem_3_OxCGRT_str (scale) / dem_4_politics to dem_6_loe (ordinal) / " \
                         "StartDate to poor_coping_dv (scale) \n"
        elif table == 'hads':
            query = write_hads_query()
            if include_measure is True:
                query += "\nVARIABLE LEVEL q1 to total_score (scale)\n"
        elif table == 'lockdown':
            query = write_lockdown_query()
            if include_measure is True:
                query += "\nVARIABLE LEVEL q1 to suspected_infection (scale)\n"
        elif table == 'ocir':
            query = write_ocir_query()
            if include_measure is True:
                query += "\nVARIABLE LEVEL q1 to total_score (scale)\n"
        elif table == 'srq':
            query = write_srq_query()
            if include_measure is True:
                query += "\nVARIABLE LEVEL q1 to total_score (scale)\n"
        elif table == 'working_memory' and include_measure is True:
            query = "\nVARIABLE LEVEL q1 to q8 (ordinal) / score_8 to diff_free_recall_wm_36 (scale) / " \
                    "to_be_excluded (nominal) \n"
            response: str = input(f"table {table} does not have a script to write value labels: continue? a to abort")
            if response.lower() == "a":
                exit(1)
        elif table == 'free_recall' and include_measure is True:
            query = "\nVARIABLE LEVEL total_score to total_emotional (scale)\n"
            response: str = input(f"table {table} does not have a script to write value labels: continue? a to abort")
            if response.lower() == "a":
                exit(1)
        else:
            response: str = input(f"table {table} does not have a script to write value labels: continue? a to abort")
            if response.lower() == "a":
                exit(1)
        value_label_query[table] = query
    return value_label_query


def print_query() -> None:
    include_measure: bool = False
    if input("""Include measure (orinal, scale) etc - NB if column order has changed, values will be wrong.
                "y" to include""").lower() == "y":
        include_measure = True
    table_names_to_import: Set[str] = set()
    cursor: MySQLCursor = covid_db.cursor(dictionary=True)
    tables: Set[str] = get_tables(cursor)
    for table in tables:
        response: str = input(f"Import {table} to SPSS? \n y(es)/n(o)/a(bort): ")
        if response == "y":
            table_names_to_import.add(table)
        if response == "a":
            exit(1)
    """ asks for user input for which tables to print queries for, then prints a unified query"""
    import_queries: Dict[str, str] = create_import_query(table_names_to_import)
    set_values_queries: Dict[str, str] = create_query_to_set_value_labels(table_names_to_import, include_measure)
    version_number: str = "v" + input("Version number (a to abort): v_ ")
    if version_number == 'a':
        exit(1)
    for table in table_names_to_import:
        print_response: str = input(f"Print query for {table} ? y(es)/n(o)/(a)bort: ")
        if print_response == "a":
            exit(1)
        elif print_response == "y":
            final_query: str = f"""
                    {import_queries[table]}\n
                    {set_values_queries[table]}\n
                    {write_labels(table)}\n
                    SAVE OUTFILE='C:\w\covid\data-snapshots\covid_data_{version_number}_{table}.sav'
                    """
            print(final_query)
            # Not working: (text too big for echo):
#             copy2clip(final_query)


def main() -> None:
    print_query()
    # for table in question_dict.keys():
    #     print(f"\n\nYOU ARE PRINTING VALUES FOR {table}\n\n" + write_labels(table))


main()
