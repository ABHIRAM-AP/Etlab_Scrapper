from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()
ETLAB_ID = os.getenv('ETLAB_ID')
PASSWORD = os.getenv('PASSWORD')

login_url = 'https://sctce.etlab.in/user/login'
attendance_url = 'https://sctce.etlab.in/ktuacademics/student/viewattendancesubject/88'


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
}




def fetchAttendance():
    # data = requests.get_json()
    # ETLAB_ID = data.get('username')
    # PASSWORD = data.get('password')
    

    login_data = {
    "LoginForm[username]": ETLAB_ID,
    "LoginForm[password]": PASSWORD,
}
    userSession = requests.Session()
    loginSession = userSession.post(login_url, data=login_data, headers=headers)

    if loginSession.status_code == 200:
        attendance_response = userSession.get(attendance_url, headers=headers)
        if attendance_response.status_code == 200:
            attendance_soup = BeautifulSoup(attendance_response.text, "html.parser")
            attendance_table = attendance_soup.find("table")
            if attendance_table:
            
                header_elements = attendance_table.find_all("th")
                headers_text = [header.text.strip() for header in header_elements]
                
                # print("\nHeaders:")
                print(headers_text, "\n") 

                rows = attendance_table.find_all("tr")[1:]  
                
                print("Attendance Data:")
                for row in rows:
                    columns = row.find_all("td")
                    data = [col.text.strip() for col in columns]
                    
                    if data:  
                          print(data)

            else:
                print("Attendance Data Not Found!")
            return {
    "data": data
}



sample = fetchAttendance()
print(sample)