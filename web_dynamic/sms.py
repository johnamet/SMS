#!/usr/bin/python3
"""Starts a flask web app"""
import uuid

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    cache_id = uuid.uuid4()
    return render_template('index.html', cache_id=cache_id)


@app.route('/login', strict_slashes=False)
def login():
    cache_id = uuid.uuid4()

    return render_template('pages/login.html', cache_id=cache_id)


@app.route('/admin-dashboard')
def admin_dashboard():
    cache_id = uuid.uuid4()

    return render_template('/pages/admin_dashboard.html', cache_id=cache_id)


@app.route('/attendance', strict_slashes=False)
def attendance_portal():
    cache_id = uuid.uuid4()

    return render_template('/pages/portal/attendance2.html', cache_id=cache_id)


@app.route('/announcement', strict_slashes=False)
def announcement_portal():
    cache_id = uuid.uuid4()

    return render_template('/pages/portal/announcement.html', cache_id=cache_id)


@app.route('/student', strict_slashes=False)
def student_portal():
    cache_id = uuid.uuid4()

    return render_template('/pages/portal/student.html', cache_id=cache_id)


@app.route('/staff', strict_slashes=False)
def staff_portal():
    cache_id = uuid.uuid4()

    return render_template('/pages/portal/staff.html', cache_id=cache_id)


@app.route('/classes', strict_slashes=False)
def classes_portal():
    cache_id = uuid.uuid4()

    return render_template('/pages/portal/classes.html', cache_id=cache_id)


@app.route('/courses', strict_slashes=False)
def courses_portal():
    cache_id = uuid.uuid4()

    return render_template('/pages/portal/courses.html', cache_id=cache_id)

@app.route('/class-attendance', strict_slashes=False)
def class_attendance_portal():
    cache_id = uuid.uuid4()
    return render_template('/pages/class_attendance.html', cache_id=cache_id)


if __name__ == '__main__':
    app.run("0.0.0.0", 8081, debug=True)
