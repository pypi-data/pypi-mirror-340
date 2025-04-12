from flask import Flask, render_template_string
import os
import socket

app = Flask(__name__)

# Dummy employee data
employee_data = {
    "sbb925582": "Shyam Bhat",
    "gss921715": "Gayathri Senthilkumar",
    "vpp922312": "Vipin Patel",
    "nss930303": "Nithin S",
    "arg930049": "Atul Gunjal",
    "crr928745": "Chandrasekaran Rangasamy",
    "tss930030": "Thennarasu Sivan",
    "ass929820": "Ajakrishna S",
    "vkb927000": "Vamsi Basireddy",
    "akj926523": "Amit Kumar Jha",
    "rbp927239": "Roshani Patil",
    "agg929000": "Apeksha Ganeshwar",
    "ajj922550": "Akhil Kumar Jha",
    "kbb924775": "Karan Barman",
    "sss922509": "Suchitra Shastri",
    "ses926552": "Sandip Shipekar",
    "mbb926223": "Maroti Belge",
    "aww925212": "Afaque Wajid",
    "sss927909": "Shabas S",
    "akc928430": "Amit Cheepepi",
    "pss926952": "Priyanka Sathish",
    "pbr926866": "Praveen Ronad",
    "skk928067": "Sathiskumar Kalimuthu",
    "abb930860": "Akshatha B V",
    "shh927546": "Sreelatha HS",
    "ass926167": "Adity Shree",
    "mjj922930": "Malavika J",
    "ass930085": "Aruthra Srinivasan",
    "aps929784": "Aparna",
    "pds930304": "Poorani Devi",
    "dpp921730": "Deepika T",
    "dtt927633": "Samuel M",
    "svv931258": "Pavithra Dabbara",
    "sirv": "Siri V",
    "mgm931265": "Shashiprakash Singh",
    "bkk928218": "Mohini Mahalle",
    "sdd928523": "Balakumar Krishnan",
    "kss926601": "Komal Sonukale",
    "kkk931360": "Karthikeyan V",
    "bcc929456": "Bhavya Challa",
    "css931257": "Chanda Singh",
    "kbb931496": "Keerthi Bhanu"
}

def get_employee_name(ttl_login_id):
    return employee_data.get(ttl_login_id, "Employee not found")

def check_application_status():
    try:
        ttl_login_id = os.getlogin()
        employee_name = get_employee_name(ttl_login_id)
        host_name = socket.gethostname()
        status = "Blocked" if ttl_login_id else "Free"

        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Garrett Remote Desktop</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Inter', sans-serif;
                    background-color: #f0f2f5;
                    margin: 0;
                    padding: 60px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                .table-container {
                    background-color: #ffffff;
                    padding: 40px 50px;
                    border-radius: 16px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    width: 100%;
                }
                h1 {
                    text-align: center;
                    color: #2c3e50;
                    font-size: 28px;
                    margin-bottom: 30px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 16px;
                }
                th, td {
                    text-align: left;
                    padding: 14px 18px;
                    border-bottom: 1px solid #e0e0e0;
                }
                th {
                    background-color: #007BFF;
                    color: white;
                    font-weight: 600;
                }
                tr:hover td {
                    background-color: #f9f9f9;
                }
                td:first-child {
                    font-weight: 500;
                    color: #333;
                }
                td:last-child {
                    color: #555;
                }
            </style>
        </head>
        <body>
            <div class="table-container">
                <h1>Welcome Garrett Remote Desktop User</h1>
                <table>
                    <tr><th>Field</th><th>Details</th></tr>
                    <tr><td>User Name</td><td>{{ employee_name }}</td></tr>
                    <tr><td>User ID</td><td>{{ user_id }}</td></tr>
                    <tr><td>Host Name</td><td>{{ host_name }}</td></tr>
                    <tr><td>Status of the System</td><td>{{ system_status }}</td></tr>
                </table>
            </div>
        </body>
        </html>
        """

        context = {
            'employee_name': employee_name,
            'user_id': ttl_login_id,
            'host_name': host_name,
            'system_status': status
        }

        return render_template_string(html_template, **context)

    except Exception as e:
        return f"<h2 style='color:red;'>An error occurred: {e}</h2>"

@app.route('/')
def home():
    return "Welcome to the Application Status Page"

@app.route('/stat', methods=['GET'])
def status():
    return check_application_status()

# ✅ Added this function so the module can be run via `garrett_status`
def run():
    app.run(host='0.0.0.0', port=9090)

if __name__ == '__main__':
    run()
