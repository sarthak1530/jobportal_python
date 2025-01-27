# Import required modules
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define database models
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

# Routes
@app.route('/')
def home():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = Job.query.filter(Job.title.contains(query) | Job.location.contains(query) | Job.company.contains(query)).all()
    return render_template('search_results.html', jobs=results)

@app.route('/apply/<int:job_id>', methods=['POST'])
def apply(job_id):
    user_id = request.form.get('user_id')
    application = Application(user_id=user_id, job_id=job_id)
    db.session.add(application)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/applications', methods=['GET'])
def view_applications():
    user_id = request.args.get('user_id')
    applications = Application.query.filter_by(user_id=user_id).all()
    return render_template('applications.html', applications=applications)

@app.route('/delete_application/<int:application_id>', methods=['POST'])
def delete_application(application_id):
    application = Application.query.get_or_404(application_id)
    db.session.delete(application)
    db.session.commit()
    return redirect(url_for('view_applications'))

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
