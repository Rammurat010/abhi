from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data structures to simulate a database
users = []
loans = []
payments = []

# Define roles
ROLES = ['admin', 'borrower', 'lender']

# Define loan statuses
LOAN_STATUSES = ['pending', 'approved', 'paid']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        role = request.form['role']
        if role not in ROLES:
            return 'Invalid role'
        users.append({'email': email, 'role': role})
        return redirect(url_for('dashboard', email=email))
    return render_template('register.html', roles=ROLES)

@app.route('/dashboard/<email>')
def dashboard(email):
    user = next((user for user in users if user['email'] == email), None)
    if user:
        if user['role'] == 'admin':
            transactions = loans + payments
            return render_template('admin_dashboard.html', transactions=transactions)
        elif user['role'] == 'borrower':
            user_loans = [loan for loan in loans if loan['borrower'] == email]
            return render_template('borrower_dashboard.html', loans=user_loans)
        elif user['role'] == 'lender':
            user_payments = [payment for payment in payments if payment['lender'] == email]
            return render_template('lender_dashboard.html', payments=user_payments)
    return 'User not found'

@app.route('/request_loan', methods=['POST'])
def request_loan():
    if request.method == 'POST':
        borrower = request.form['borrower']
        amount = float(request.form['amount'])
        loans.append({'borrower': borrower, 'amount': amount, 'status': 'pending'})
        return redirect(url_for('dashboard', email=borrower))

@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    if request.method == 'POST':
        lender = request.form['lender']
        amount = float(request.form['amount'])
        payments.append({'lender': lender, 'amount': amount})
        return redirect(url_for('dashboard', email=lender))

if __name__ == '__main__':
    app.run(debug=True,port=5002)
