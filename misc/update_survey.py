import json


def main():
    with open("../static/json/survey.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    copy = {"title_en": "Survey", "title_ru": "Опросник", "version": 2, "data": {"directions": []}}
    directs = data["data"]["directions"]
    i = 0
    total_weight = 0
    for direct in directs:
        c = copy["data"]["directions"]
        c.append(dict())
        c[i]["title"] = direct["title"]
        c[i]["criterions"] = list()
        j = 0
        for crit in direct['criterions']:
            ct = c[i]["criterions"]
            ct.append(dict())
            c1 = ct[j]
            c1["title"] = crit["title"]
            c1["number"] = crit["number"]
            c1["subcriterions"] = list()
            if "question_number" in crit:
                c1["question_number"] = crit["question_number"]
                c1["weight"] = crit["weight"]
                total_weight += crit["weight"]
                if "question" in crit:
                    c1["question"] = crit["question"]
                else:
                    c1["question"] = None
                c1["detailed_response"] = crit["detailed_response"]
                c1["is_interview"] = crit["is_interview"]
            t = 0
            for sub in crit["subcriterions"]:
                total_weight += sub["weight"]
                c1["subcriterions"].append(dict())
                c2 = c1["subcriterions"][t]
                c2["question_number"] = sub["question_number"]
                c2["title"] = sub["title"]
                c2["weight"] = sub["weight"]
                c2["puncts"] = list()

                cp = c2["puncts"]
                for d in range(0, 4):
                    cp.append(dict)
                cp[0], cp[1], cp[2], cp[3] = dict(), dict(), dict(), dict()
                cp[0]["title"] = sub["01"]
                cp[0]["range_max"] = 1
                cp[0]["range_min"] = 0
                cp[1]["title"] = sub["12"]
                cp[1]["range_max"] = 2
                cp[1]["range_min"] = 1
                cp[2]["title"] = sub["23"]
                cp[2]["range_max"] = 3
                cp[2]["range_min"] = 2
                cp[3]["title"] = sub["34"]
                cp[3]["range_max"] = 4
                cp[3]["range_min"] = 3
                cp[0]["prompt"], cp[1]["prompt"], cp[2]["prompt"], cp[3]["prompt"], \
                    cp[0]["comment"], cp[1]["comment"], cp[2]["comment"], cp[3]["comment"], = None, None, None, None, None, None, None, None

                if "note" in sub:
                    c2["note"] = sub["note"]
                else:
                    c2["note"] = None
                if "needed_answer" in sub:
                    c2["needed_answer"] = sub["needed_answer"]
                else:
                    c2["needed_answer"] = False
                t += 1
            j += 1
            t = 0
        # if total_weight != 1.json:
        #     print(crit["title"], " не соответствует весу: ", total_weight)
        total_weight = 0
        j = 0
        i += 1
    with open("templatejson.json", "w", encoding='utf8') as f:
        json.dump(copy, f, ensure_ascii=False)



if __name__ == "__main__":
    main()