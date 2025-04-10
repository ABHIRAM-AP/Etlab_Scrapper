from flask import Flask,request,jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

login_url = 'https://sctce.etlab.in/user/login'
attendance_url = 'https://sctce.etlab.in/ktuacademics/student/viewattendancesubject/88'


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
}

@app.route('/get-attendance',methods=['POST'])
def fetch_attendance():
    data = request.get_json()
    etlab_id = data.get('username')
    password = data.get('password')

    login_data = {
    "LoginForm[username]": etlab_id,
    "LoginForm[password]": password,
    }
    session = requests.Session()
    login = session.post(login_url,data=login_data,headers=headers)


    if login.status_code == 200:
        attendance_response = session.get(attendance_url,headers=headers)
        if attendance_response.status_code == 200:
            soup = BeautifulSoup(attendance_response.text,"html_parser")
            table = soup.find("table")

            if not table:
                return jsonify({"error":"Attendance table not found."}),404
            headers_text = [th.text.strip() for th in table.find_all("th")]
            rows=[]

            for row in table.find_all("tr")[1:]:
                cols = [td.text.strip() for td in row.find_all("td")]
                if cols:
                    rows.append(cols)
            return jsonify({
                "headers":headers_text,
                "data":rows
            })
    return jsonify({"Error":"Login Failed"}),401

if __name__ == "__main__":
    app.run(debug=True)