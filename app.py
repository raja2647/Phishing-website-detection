from flask import Flask, render_template, request
import os
from utils.phishing_checker import check_url
from utils.malware_checker import is_malware
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ScanResult
from flask import jsonify

app = Flask(__name__)

engine = create_engine('sqlite:///scan_results.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    session = Session()
    reports = session.query(ScanResult).order_by(ScanResult.id.desc()).all()
    return render_template('index.html', reports=reports)


@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    session = Session()
    results = session.query(ScanResult).filter(ScanResult.url.contains(query)).limit(5).all()
    session.close()
    
    suggestions = [{'id': r.id, 'url': r.url} for r in results]
    return jsonify(suggestions)

@app.route('/report/<int:report_id>')
def show_report(report_id):
    session = Session()
    report = session.query(ScanResult).get(report_id)
    session.close()
    return render_template('single_report.html', report=report)

@app.route('/check', methods=['POST'])
def check():
    url_result = None
    file_result = None
    file_name = None
    file_path = None


    url = request.form.get('url')

    if url:
        url_result = check_url(url)
    else:
        url_result = None
     

    uploaded_file = request.files.get('file')

    if uploaded_file and uploaded_file.filename != '':
        filename = secure_filename(uploaded_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(filepath)
        
        scan_data = is_malware(filepath)
        file_result = scan_data['result']
        file_name = scan_data['file_name']
        file_path = scan_data['file_path']


    if url_result:
       session = Session()
       new_result = ScanResult(
            url=url_result['url'],
            url_length=url_result['url_length'],
            sha_hash=url_result['sha_hash'],
            is_https=url_result['is_https'],
            domain=url_result['domain'],
            contains_keywords=url_result['contains_keywords'],
            phishing_status=url_result['phishing_status']
        )
       session.add(new_result)
       session.commit()
       session.close()

    return render_template('result.html', url_result=url_result, file_result=file_result, file_name=file_name,
                           file_path=file_path)

     

if __name__ == '__main__':
    app.run(debug=True)