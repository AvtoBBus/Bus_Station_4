import requests
from bs4 import BeautifulSoup as BS
import csv


def find_schedule_session_url(num_group: str) -> str:
    with open(f"AllGroupShedule/AllGroup_course_{num_group[1]}.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if row[1] == num_group:
                result = f"{row[0][:20]}/session?groupId={row[0][29:]}"
                return result


def pars_schedule_session(num_group: str) -> str:
    url = find_schedule_session_url(num_group)
    response = requests.get(url)
    list_session = []
    soup = BS(response.content, "html.parser")
    for item in soup.find_all(class_="daily-session"):
        if not item.find(class_="caption-text meeting__type").contents[0] == " Консультация":
            list_session.append((
                item.find(class_="h3-text").contents,
                item.find(class_="caption-text meeting__type").contents,
                item.find(class_="h3-text meeting__discipline").contents,
                item.find(class_="h2-text meeting__time").contents
            ))
    result = f"Расписание сессии для группы {num_group}:\n"
    for item in list_session:
        result += f"---{item[1][0]}---\n\nДата и время: {item[0][0]} - {item[3][0]}\nПредмет: {item[2][0]}\n\n"
    return result
