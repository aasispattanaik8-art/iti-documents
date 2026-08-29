from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)
PDF_FOLDER = '.' # Aapke folder ka naam

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Portal</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9;">
    <h2>Student Document Portal</h2>
    <div style="margin-top: 30px;">
        {% if message %} 
            <p style="color: red; font-weight: bold;">{{ message }}</p> 
        {% endif %}

        {% if files %}
            <h3 style="color: green;">Documents Found for: {{ reg_no }}</h3>
            {% for file in files %}
                <a href="/download/{{ file }}" target="_blank" 
                   style="display: inline-block; margin: 10px; padding: 15px; background: #008CBA; color: white; text-decoration: none; border-radius: 5px; font-size: 16px;">
                   📥 Download {{ file }}
                </a>
                <br>
            {% endfor %}
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/student/<reg_no>')
def student_view(reg_no):
    reg_no = reg_no.upper()
    files_found = []

    marksheet = f"{reg_no}_Marksheet.pdf"
    certificate = f"{reg_no}_Certificate.pdf"

    if os.path.exists(os.path.join(PDF_FOLDER, marksheet)):
        files_found.append(marksheet)
    if os.path.exists(os.path.join(PDF_FOLDER, certificate)):
        files_found.append(certificate)

    if not files_found:
        return render_template_string(HTML_PAGE, message=f"No documents found for Registration No: {reg_no}")

    return render_template_string(HTML_PAGE, files=files_found, reg_no=reg_no)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PDF_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
