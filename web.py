import requests
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

    attendance_response = session.get(attendance_url, headers=headers)
    if attendance_response.status_code == 200:
        attend_soup = BeautifulSoup(attendance_response.text, "html.parser")
        table = attend_soup.find("table")
        if table:
            attendance_data["title"] = [th.text.strip() for th in table.find_all("th")]
            for row in table.find_all("tr")[1:]:
                cols = [td.text.strip() for td in row.find_all("td")]
                print(cols)
                if cols:
                    attendance_data["data"] = cols

    #  Final JSON 
    return jsonify({
        "attendance": attendance_data,
    })



