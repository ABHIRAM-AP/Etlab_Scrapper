import requests
import re
from bs4 import BeautifulSoup
from flask import jsonify

login_url = "https://sctce.etlab.in/user/login"
attendance_url = "https://sctce.etlab.in/ktuacademics/student/viewattendancesubject/88"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_data(userID, password):
    session = requests.Session()
    
    login_data = {
        "LoginForm[username]": userID,
        "LoginForm[password]": password,
    }

    login_response = session.post(login_url, data=login_data, headers=headers)
    if login_response.status_code != 200:
        return jsonify({"error": "Login Failed"}), 401

    # Attendance 
    attendance_data = {
        "title": [],
        "data": [],
    }
    subject_data = fetch_subjects(session)
    attendance_response = session.get(attendance_url, headers=headers)
    if attendance_response.status_code == 200:
        attend_soup = BeautifulSoup(attendance_response.text, "html.parser")
        table = attend_soup.find("table")
        if table:
            attendance_data["title"] = [th.text.strip() for th in table.find_all("th")]
            for row in table.find_all("tr")[1:]:
                cols = [td.text.strip() for td in row.find_all("td")]
                if cols:
                    attendance_data["data"] = cols


    
    #  Final JSON 
    return jsonify({
        "attendance": attendance_data,
        "subjects":subject_data["subjects"],
    })


def fetch_subjects(session):
    subject_url =  "https://sctce.etlab.in/ktuacademics/student/teacher"
    response = session.get(subject_url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch subjects"}

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    if not tables:
        return {"error": "No tables found"}

    last_table = tables[-1]
    t_body = last_table.find("tbody")
    rows = t_body.find_all("tr")

    subjects_dict = {}
    for row in rows:
        tds = row.find_all("td")
        if len(tds) >= 3:
            second_td = tds[2].get_text(strip=True)
            regex_match = re.match(r"([A-Z]{3}\d{3})\s*-\s*(.+)", second_td)
            if regex_match:
                sub_code = regex_match.group(1).strip()
                sub_name = regex_match.group(2).strip().upper()

                if sub_code not in subjects_dict:
                    subjects_dict[sub_code] =sub_name
                

    print(subjects_dict)
    return {"subjects": subjects_dict}
