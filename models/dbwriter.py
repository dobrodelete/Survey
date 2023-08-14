import json
import sqlite3
from datetime import datetime

from config import DB_NAME


def create_answer_dict(d: dict):
    r = dict(d)
    if "fullname" not in r:
        name = "Unknown"
    else:
        name = r["fullname"]
    new = {"fullname": name,
           "iogv_id": r["iogv"],
           "post": r["post"],
           "subdivision": r["subdivision"],
           "answer_questions": []}
    if "fullname" in r:
        r.pop("fullname")
    r.pop("iogv")
    r.pop("post")
    r.pop("subdivision")
    i = 1
    for j in range(1, 67):
        new["answer_questions"].append({f"question": j, "reply": {}})
    for k, v in r.items():
        question = k.split("-")[0]
        type = k.split("-")[1]
        # print(k)
        for ans in new["answer_questions"]:
            if ans["question"] == int(question):
                a = ans["reply"]
                if type == "range":
                    a["answer"] = float(r[question + "-radio"]) + float(r[question + "-range"])
                elif type == "answer_range":
                    a["answer"] = v
                elif type == "textarea":
                    a["comment"] = v
        i += 1
    with open("template.json", "w", encoding="utf8") as file:
        json.dump(new, file)
    return new

def write_one_page_answer(surv: dict):
    try:
        conn = sqlite3.connect(f"{DB_NAME}")
        cur = conn.cursor()

        sql_add_user = "INSERT INTO users (fullname, post, subdivision, iogv, cxreated_at) VALUES (?, ?, ?, ?, ?)"
        now = datetime.now()
        user = ("Unknown", surv["post"], surv["subdivision"], surv["iogv_id"], now)
        cur.execute(sql_add_user, user)
        conn.commit()
        sqltemp = "SELECT * FROM users ORDER BY id DESC LIMIT 1;"
        cur.execute(sqltemp)
        user_id = cur.fetchone()[0]

        sql_add_record = "INSERT INTO record (uid, created_at) VALUES (?, ?)"
        record = (user_id, now)
        cur.execute(sql_add_record, record)
        conn.commit()

        sqltemp = "SELECT * FROM record ORDER BY id DESC LIMIT 1;"
        cur.execute(sqltemp)
        record_id = cur.fetchone()[0]

        for q in surv["answer_questions"]:
            sql_add_answer = "INSERT INTO answers (rid, number_question, question_number_answer, grade, comment)" \
                             " VALUES (?, ?, ?, ?, ?)"
            answer = None
            grade = None
            comment = None
            if "answer" in q["reply"]:
                answer = q["reply"]["answer"]
                grade = q["reply"]["grade"]
            if "comment" in q["reply"]:
                comment = q["reply"]["comment"]
            answers = (record_id, q["question"], answer, grade, comment)
            cur.execute(sql_add_answer, answers)
            conn.commit()


        cur.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")