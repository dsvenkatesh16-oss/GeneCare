from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_file
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from database import (
    save_report,
    get_reports,
    get_analytics
)

app = Flask(__name__)
app.secret_key = "gencare123"


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']

        session['user'] = username

        return redirect('/dashboard')

    return render_template('login.html')


# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    return render_template('dashboard.html')


# DISEASE INFORMATION
@app.route('/disease-info')
def disease_info():
    return render_template('disease_info.html')


# ANALYTICS
@app.route('/analytics')
def analytics():

    (
        total_reports,
        low_count,
        medium_count,
        high_count
    ) = get_analytics()

    return render_template(
        'analytics.html',
        total_reports=total_reports,
        low_count=low_count,
        medium_count=medium_count,
        high_count=high_count
    )


# SYMPTOM CHECKER
@app.route('/symptom-checker', methods=['GET', 'POST'])
def symptom_checker():

    risk = None
    disease = None

    if request.method == 'POST':

        symptoms = request.form.getlist('symptoms')

        score = len(symptoms)

        if score <= 2:

            risk = "Low"
            disease = "Monitor Symptoms"

        elif score <= 4:

            risk = "Medium"
            disease = "Possible Thalassemia"

        else:

            risk = "High"
            disease = "Possible Sickle Cell Anemia"

        # Save in session
        session['risk'] = risk
        session['disease'] = disease

    return render_template(
        'symptom_checker.html',
        risk=risk,
        disease=disease
    )


# INHERITANCE CALCULATOR
@app.route('/inheritance', methods=['GET', 'POST'])
def inheritance():

    normal = None
    carrier = None
    affected = None

    if request.method == 'POST':

        father_name = request.form['father_name']
        mother_name = request.form['mother_name']

        if father_name == "Carrier" and mother_name == "Carrier":

            normal = 25
            carrier = 50
            affected = 25

        elif father_name == "Normal" and mother_name == "Normal":

            normal = 100
            carrier = 0
            affected = 0

        elif father_name == "Affected" and mother_name == "Affected":

            normal = 0
            carrier = 0
            affected = 100

        else:

            normal = 50
            carrier = 50
            affected = 0

    return render_template(
        'inheritance.html',
        normal=normal,
        carrier=carrier,
        affected=affected
    )


# AUTO PDF GENERATION
@app.route('/generate-report')
def generate_report():

    name = session.get(
        'user',
        'Unknown User'
    )

    risk = session.get(
        'risk',
        'Not Available'
    )

    disease = session.get(
        'disease',
        'Not Available'
    )

    # Save to database
    save_report(
        name,
        risk,
        disease
    )

    pdf_file = "GeneCare_Report.pdf"

    doc = SimpleDocTemplate(
        pdf_file
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "GeneCare Health Report",
            styles['Title']
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"Patient Name : {name}",
            styles['BodyText']
        )
    )

    content.append(
        Paragraph(
            f"Risk Level : {risk}",
            styles['BodyText']
        )
    )

    content.append(
        Paragraph(
            f"Disease Prediction : {disease}",
            styles['BodyText']
        )
    )

    doc.build(content)

    return send_file(
        pdf_file,
        as_attachment=True
    )


# HISTORY PAGE
@app.route('/history')
def history():

    reports = get_reports()

    return render_template(
        'history.html',
        reports=reports
    )


if __name__ == '__main__':
    app.run(debug=True)