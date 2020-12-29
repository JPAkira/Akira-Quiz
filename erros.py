from flask import render_template, request, redirect, session, flash, url_for
from main import app

@app.route('/cpferror')
def cpferror():
    return render_template('cpferror.html')