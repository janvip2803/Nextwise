from flask import Flask, request, jsonify
from email.message import EmailMessage
import ssl, smtplib, logging

app = Flask(__name__)
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

@app.route('/send-application', methods=['OPTIONS'])
def options():
    return '', 200

@app.route('/', methods=['GET'])
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
