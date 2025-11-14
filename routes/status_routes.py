"""
Patron Status Routes - Patron Information viewing endpoints, including late fees, borrow history, etc
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.library_service import get_patron_status_report

status_bp = Blueprint('status', __name__)
@status_bp.route('/patron_status', methods=['GET', 'POST'])
def patron_status():
    if request.method == 'POST':
        patron_id = request.form.get('patron_id')
        if not patron_id:
            flash('Patron ID is required', 'error')
            return redirect(url_for('status.patron_status'))

        report = get_patron_status_report(patron_id)
        return render_template('patron_status.html', report=report)

    return render_template('patron_status.html')