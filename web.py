import requests
from bs4 import BeautifulSoup
from flask import jsonify

login_url = "https://sctce.etlab.in/user/login"
attendance_url = "https://sctce.etlab.in/ktuacademics/student/viewattendancesubject/88"
result_url = "https://sctce.etlab.in/ktuacademics/student/results"

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

    # Internal Marks 
    internal_marks = []
    result_response = session.get(result_url, headers=headers)
    if result_response.status_code == 200:
        result_soup = BeautifulSoup(result_response.text, "html.parser")  
        h5_headings = result_soup.find_all('h5')
        for heading in h5_headings:
            if "Internal marks" in heading.text.strip():
                widget_box = heading.find_parent('div', class_='widget-box')
                if widget_box:
                    marks_table = widget_box.find('table', class_='items')
                    if marks_table:
                        rows = marks_table.find_all('tr')[1:]
                        for row in rows:
                            columns = [td.text.strip() for td in row.find_all('td')]
                            if len(columns) >= 4:
                                subject_code, subject_name = columns[0].split(' - ')
                                semester = columns[1]
                                max_marks = columns[2]
                                marks_obtained = columns[3]
                                internal_marks.append({
                                    'subject_code': subject_code,
                                    'subject_name': subject_name,
                                    'semester': semester,
                                    'marks_obtained': marks_obtained,
                                    'max_marks': max_marks,
                                })

    # Attendance 
    attendance_data = {
        "headers": [],
        "data": [],
    }

    attendance_response = session.get(attendance_url, headers=headers)
    if attendance_response.status_code == 200:
        attend_soup = BeautifulSoup(attendance_response.text, "html.parser")
        table = attend_soup.find("table")
        if table:
            attendance_data["headers"] = [th.text.strip() for th in table.find_all("th")]
            for row in table.find_all("tr")[1:]:
                cols = [td.text.strip() for td in row.find_all("td")]
                if cols:
                    attendance_data["data"].append(cols)

    #  Final JSON 
    return jsonify({
        "internal_marks": internal_marks,
        "attendance": attendance_data,
    })



