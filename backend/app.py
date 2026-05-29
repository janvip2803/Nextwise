from flask import Flask, request, jsonify, render_template
from email.message import EmailMessage
import ssl, smtplib, logging

# Pointing to the root path where your HTML files live
app = Flask(__name__, template_folder='../')
logging.basicConfig(level=logging.INFO)

GMAIL_USER     = 'info.nextwise501@gmail.com'
GMAIL_PASSWORD = 'kqfbzdofgrwczujp'
RECEIVER_EMAIL = 'Nextwise.finserv@gmail.com'

# CORS
@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin']  = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    return response

# ==========================================
# FRONTEND ROUTES (Serving Your HTML Pages)
# ==========================================

@app.route('/', methods=['GET'])
def home():
    # This automatically opens your index.html file on the homepage
    return render_template('index.html')

@app.route('/balance-transfer', methods=['GET'])
def balance_transfer():
    return render_template('balance-transfer.html')

@app.route('/business-loan-unsecured', methods=['GET'])
def business_loan_unsecured():
    return render_template('business-loan-unsecured.html')

@app.route('/cgtmse', methods=['GET'])
def cgtmse():
    return render_template('cgtmse.html')

@app.route('/expansion-funding', methods=['GET'])
def expansion_funding():
    return render_template('expansion-funding.html')

@app.route('/home-loan', methods=['GET'])
def home_loan():
    return render_template('home-loan.html')

@app.route('/insurance', methods=['GET'])
def insurance():
    return render_template('insurance.html')

@app.route('/loan-by-profession', methods=['GET'])
def loan_by_profession():
    return render_template('loan-by-profession.html')

@app.route('/machinery-funding', methods=['GET'])
def machinery_funding():
    return render_template('machinery-funding.html')

@app.route('/mortgage-loan', methods=['GET'])
def mortgage_loan():
    return render_template('mortgage-loan.html')

@app.route('/msme-loan', methods=['GET'])
def msme-loan():
    return render_template('msme-loan.html')

@app.route('/od-cc-limit', methods=['GET'])
def od_cc_limit():
    return render_template('od-cc-limit.html')

@app.route('/project-loan', methods=['GET'])
def project_loan():
    return render_template('project-loan.html')

@app.route('/solar-funding', methods=['GET'])
def solar_funding():
    return render_template('solar-funding.html')

@app.route('/working-capital', methods=['GET'])
def working_capital():
    return render_template('working-capital.html')


# ==========================================
# BACKEND API ROUTES (Lead Form Submission)
# ==========================================

@app.route('/send-application', methods=['OPTIONS'])
def options():
    return '', 200

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "NextWise backend is running"}), 200

@app.route('/send-application', methods=['POST'])
def send_application():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    full_name     = str(data.get('full_name', '')).strip()
    mobile        = str(data.get('mobile', '')).strip()
    city          = str(data.get('city', '')).strip()
    loan_type     = str(data.get('loan_type', 'Not specified'))
    loan_amount   = str(data.get('loan_amount', 'Not specified'))
    business_name = str(data.get('business_name', 'Not provided'))
    page          = str(data.get('page', 'Unknown'))

    if not full_name or not city:
        return jsonify({"error": "Name and city are required"}), 422

    body = (
        'New Loan Lead - NextWise Finserv\n'
        '---------------------------------------------\n'
        'Name          : ' + full_name + '\n'
        'Mobile        : ' + mobile + '\n'
        'City          : ' + city + '\n'
        'Business Name : ' + business_name + '\n'
        'Loan Type     : ' + loan_type + '\n'
        'Loan Amount   : ' + loan_amount + '\n'
        'Source Page   : ' + page + '\n'
        '---------------------------------------------\n'
        'Respond within 30 minutes!\n'
    )

    try:
        em = EmailMessage()
        em['From']    = GMAIL_USER
        em['To']      = RECEIVER_EMAIL
        em['Subject'] = '[New Lead] ' + loan_type + ' - ' + full_name + ' (' + city + ')'
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.sendmail(GMAIL_USER, RECEIVER_EMAIL, em.as_string())

        logging.info('Lead sent: ' + full_name + ' | ' + mobile)
        return jsonify({"message": "Application submitted successfully!"}), 200

    except Exception as e:
        import traceback
        err = traceback.format_exc()
        logging.error('Error: ' + err)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
