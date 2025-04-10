@app.route('/get-attendance', methods=['POST'])
def fetch_attendance():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400

    etlab_id = data.get('username')
    password = data.get('password')

    login_data = {
        "LoginForm[username]": etlab_id,
        "LoginForm[password]": password,
    }

    session = requests.Session()
    login = session.post(login_url, data=login_data, headers=headers)

    if login.status_code == 200:
        attendance_response = session.get(attendance_url, headers=headers)
        if attendance_response.status_code == 200:
            soup = BeautifulSoup(attendance_response.text, "html.parser")
            table = soup.find("table")

            if not table:
                return jsonify({"error": "Attendance table not found."}), 404

            headers_text = [th.text.strip() for th in table.find_all("th")]
            rows = []

            for row in table.find_all("tr")[1:]:
                cols = [td.text.strip() for td in row.find_all("td")]
                if cols:
                    rows.append(cols)

            return jsonify({
                "headers": headers_text,
                "data": rows
            })

    return jsonify({"error": "Login Failed"}), 401
