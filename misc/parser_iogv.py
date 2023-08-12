import json
import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

gov = "https://iss.gov.spb.ru"


def parse_iogv():
    iogv = parse(gov + "/hierarchy/27402f41-fb36-41d9-9052-617905d97f3b/")
    parse(gov + "/hierarchy/27402f41-fb36-41d9-9052-617905d97f3b/")
    with open("temp.json", "w", encoding="utf-8") as file:
        json.dump(iogv, file)
    print(iogv)


def parse(url):
    try:
        r = requests.get(url, verify=False)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        current_page_data = []
        links = soup.find('ul', {'id': 'children_list'})

        if links:
            li_items = links.find_all("li")
            persons = soup.find("table") # find('div', {'id': 'persons'}).
            persons_list = []

            if persons is not None:
                table_body = persons.find("tbody")
                rows = table_body.find_all("tr")
                t = 0;
                for row in rows:
                    print(row)
                    cols = row.find_all("td")
                    fullname = cols[0]
                    post = cols[1]
                    persons_list.append({"fullname": fullname, "post": post})
                    t += 1
            print(persons)
            for li in li_items:
                link = li.find('a', href=True)
                if link:
                    link_name = link.text.strip()
                    link_href = link.get('href')
                    next_url = gov + link['href']
                    child_pages = parse(next_url)
                    current_page_data.append({
                        'link_name': link_name,
                        'link_href': link_href,
                        'persons': persons_list,
                        'child_pages': child_pages
                    })
    except requests.exceptions.RequestException as ex:
        print(f"Ошибка при обращении к {url}: {ex}")
    return current_page_data


def get_people(dict):
    try:
        if dict["link_href"] is not None:
            uuid = dict["link_href"].split("/")[2]
            r = requests.get(f"https://iss.gov.spb.ru/person/c/?rnd=AIqp7ITUvO&uuid={uuid}&limit=100&order_by=&offset=0", verify=False)
            r.raise_for_status()
            answer = r.json()
            if answer["count"] != 0:
                for res in answer["results"]:
                    # print(f"ФИО: {name} | Должность: {position}")
                    dict["persons"].append({
                        "name": res["name"],
                        "position": res["position"],
                        "position_uuid": res["position_uuid"],
                        "uuid": res["uuid"],
                        "url": res["url"],
                        "addresses": res["addresses"]
                    })
            if 'child_pages' in dict and dict['child_pages']:
                for child in dict["child_pages"]:
                    get_people(child)
    except requests.exceptions.RequestException as ex:
        print(f"Ошибка при обращении к : {ex}")


def parse_people():
    with open("temp.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for com in data:
        get_people(com)
    with open("tempv2.json", "w", encoding="utf-8") as file:
        json.dump(data, file)
    print(data)





def get_child(d):
    childs = dict()
    if d["link_name"] is not None:
        for c in d["child_pages"]:
            childs[c["link_name"]] = get_child(c)
            # childs[-1] = get_child(c)
    return childs



def create_list_iogv():
    with open("tempv2.json", "r", encoding="utf8") as file:
        data = json.load(file)
    iogv_list = list()
    for iogv in data:
        iogv_list.append({iogv["link_name"]: get_child(iogv)})
    with open("../static/json/list_iogv.json", "w", encoding="utf8") as file:
        json.dump(iogv_list, file)
    # print(iogv_list)
        # get_child(iogv)
        # print(iogv["link_name"])




def write_iogv_db():
    with open("C:\Edu\Survey\static\json\iogvv2.json", "r", encoding="utf8") as file:
        iogv_list = json.load(file)
    for iogv in iogv_list:
        print()
        title = iogv["link_name"]
        hierarchy_id = iogv["link_href"].split("/")[2]
        print(iogv["link_href"].split("/")[2])



def main():
    # parse_people()
    # create_list_peoples()
    # create_list_iogv()
    write_iogv_db()


if __name__ == "__main__":
    main()
