from flask import render_template, jsonify, request
from flask_login import login_required, current_user

from api.users import get_available_profiles, get_current_profile
from app import app
from reports import get_available_report_units, get_report_html, get_report_pdf


@app.route('/tpreport')
@login_required
def tpreport():
    return render_template('generateReport.html', title='Отчёт', user=get_current_profile(),
                           available_users=get_available_profiles(current_user))


@app.route('/reportunits')
@login_required
def reportunits():
    return jsonify({'ok': True, 'units': get_available_report_units()})


@app.route('/report', methods=['POST'])
@login_required
def report():
    req_data = request.get_json()
    return jsonify({'ok': True, 'html': get_report_html(req_data)})


@app.route('/reportToPdf', methods=['POST'])
@login_required
def reportToPdf():
    req_data = request.get_json()
    html = get_report_html(req_data)
    url = get_report_pdf(html)
    return jsonify({'ok': True, 'url': url})
