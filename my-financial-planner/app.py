#1st
# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Welcome to My Financial Planner!"

# if __name__ == "__main__":
#     app.run(debug=True)

# 2nd
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db' 
#     db.init_app(app)

#     from .routes import main_bp 
#     app.register_blueprint(main_bp) 

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)


# from flask import Flask, render_template, request, jsonify

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     try:
#         # Extracting data from the form
#         monthly_income = float(request.form.get('income'))
#         monthly_expenses = float(request.form.get('expenses'))
#         savings_goal = float(request.form.get('savings'))

#         # Perform calculations
#         remaining_income = monthly_income - monthly_expenses
#         advice = ""
#         tips = []

#         if remaining_income <= 0:
#             advice = "Your expenses exceed your income. Consider reviewing your budget to cut unnecessary costs."
#             tips = [
#                 "Track your spending to identify areas where you can reduce expenses.",
#                 "Avoid unnecessary subscriptions or memberships.",
#                 "Plan meals to avoid overspending on food."
#             ]
#         else:
#             percentage_saved = (remaining_income / monthly_income) * 100
#             advice = f"You are saving {percentage_saved:.2f}% of your income. Keep it up!"
#             if savings_goal > 0 and remaining_income < savings_goal:
#                 advice += f" However, your savings are below your goal of ${savings_goal:.2f}. Look into additional saving strategies."
#                 tips = [
#                     "Consider automating your savings to consistently save each month.",
#                     "Explore high-yield savings accounts for better returns on your savings.",
#                     "Set a specific budget for non-essential expenses."
#                 ]
#             else:
#                 tips = [
#                     "Invest a portion of your savings into diversified assets like index funds.",
#                     "Build an emergency fund equal to 3-6 months of your expenses.",
#                     "Review and optimize recurring bills like utilities or insurance."
#                 ]

#         # Return results
#         return jsonify({
#             'status': 'success',
#             'remaining_income': f"${remaining_income:.2f}",
#             'advice': advice,
#             'tips': tips
#         })
#     except Exception as e:
#         return jsonify({
#             'status': 'error',
#             'message': str(e)
#         })

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial_planner.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance
db = SQLAlchemy(app)

# Database model for storing user financial data
class UserFinancialData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    income = db.Column(db.Float, nullable=False)
    expenses = db.Column(db.Float, nullable=False)
    savings = db.Column(db.Float, nullable=False)
    remaining_income = db.Column(db.Float, nullable=False)
    advice = db.Column(db.String(500), nullable=False)
    tips = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<UserFinancialData {self.id}>'

# Route for the home page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route to view all user data
@app.route('/view_data')
def view_all_data():
    # Fetch all records from the database
    user_data = UserFinancialData.query.all()
    return render_template('view_data.html', user_data=user_data)

# Route to handle financial data analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        income = float(request.form['income'])
        expenses = float(request.form['expenses'])
        savings = float(request.form['savings'])

        # Perform the financial calculations
        remaining_income = income - expenses
        advice = f'You are saving {savings / income * 100:.2f}% of your income. Keep it up!'
        tips = "Invest a portion of your savings into diversified assets like index funds."

        # Store data in the database
        new_data = UserFinancialData(income=income, expenses=expenses, savings=savings,
                                     remaining_income=remaining_income, advice=advice, tips=tips)
        db.session.add(new_data)
        db.session.commit()

        # Redirect to view the saved data
        return redirect(f'/data/{new_data.id}')

    except Exception as e:
        return str(e)

# Route to view saved financial data (for a specific user)
@app.route('/data/<int:id>')
def view_single_data(id):
    data = UserFinancialData.query.get_or_404(id)
    return render_template('view_data.html', data=data)

if __name__ == '__main__':
    # Create the database and tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
