"""
DataRoom Enterprise - Web Application with Security Vulnerabilities
Student Project - Directory Traversal & Command Injection
"""

from flask import Flask, render_template, request, redirect, session, flash
import os
import subprocess

app = Flask(__name__)
app.secret_key = "enterprise_secret_2024"



def setup_files():
    """Create necessary files for the application"""
    # Create directories
    for folder in ['documents', 'config', 'logs', 'templates']:
        os.makedirs(folder, exist_ok=True)
    
    # Create sensitive files
    files_to_create = {
        'config/api_keys.txt': '''STRIPE_PRODUCTION_KEY=sk_live_51MnBgLKuGqT4p7yV8wX9zAaBcDeFgHiJkLmNoPqRsTuVwXyZ0
AWS_ACCESS_KEY=AKIAIOSFODNN7ENTERPRISE
GOOGLE_MAPS_API=AIzaSyB_dQ4vE7fGhIjKlMnOpQrStUvWxYzA1B3C''',
        
        'config/database.conf': '''DB_HOST=prod-db.corporate.internal
DB_USER=admin
DB_PASSWORD=P@ssw0rdPr0d2024!
DB_NAME=enterprise_data''',
        
        'documents/report.txt': '''CONFIDENTIAL - Q4 FINANCIAL REPORT
Revenue: $45,820,000
Profit: $12,750,000
Merger Talks: TechSolutions Inc. ($850M valuation)''',
        
        'documents/handbook.txt': '''EMPLOYEE HANDBOOK
Security Policies:
1. Passwords must be changed every 90 days
2. Report security incidents immediately
3. Encrypt sensitive documents''',
        
        'logs/application.log': '''[2024-01-15 09:00:01] INFO - Application started
[2024-01-15 09:15:22] INFO - User admin logged in
[2024-01-15 10:30:45] ERROR - Database connection failed
[2024-01-15 11:45:33] INFO - Backup completed''',
        
        'logs/security.log': '''[2024-01-15 09:15:22] AUTH - Successful login: admin
[2024-01-15 10:22:33] WARNING - Failed login attempt
[2024-01-15 11:45:09] INFO - Security audit completed'''
    }
    
    for filepath, content in files_to_create.items():
        with open(filepath, 'w') as f:
            f.write(content)
    
    print("✅ Files created successfully!")



@app.route('/', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['user'] = username
            session['role'] = 'admin'
            return redirect('/dashboard')
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard"""
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect('/')


@app.route('/documents')
def documents():
    """
    VULNERABLE: Directory Traversal
    Attack via URL: /documents?file=../../../etc/passwd
    """
    if 'user' not in session:
        return redirect('/')
    
    filename = request.args.get('file', '')
    content = ""
    
    if filename:
        try:
           
            with open(filename, 'r') as f:
                content = f.read()
        except:
            content = "Error: File not found or cannot be read"
    
    return render_template('documents.html', 
                         content=content, 
                         filename=filename,
                         user=session['user'])



@app.route('/system', methods=['GET', 'POST'])
def system_admin():
    """
    VULNERABLE: Command Injection
    Attack via form: ;cat /etc/passwd
    """
    if 'user' not in session:
        return redirect('/')
    
    output = ""
    command = ""
    
    if request.method == 'POST':
  
        command = request.form.get('command', '')
        
        if command:
            try:
                
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                output = result.stdout
                if result.stderr:
                    output += f"\nError: {result.stderr}"
            except Exception as e:
                output = f"Error: {str(e)}"
    
    return render_template('system_admin.html',
                         output=output,
                         command=command,
                         user=session['user'])



@app.route('/logs')
def logs():
    """Log analysis page"""
    if 'user' not in session:
        return redirect('/')
    
   
    log_content = ""
    try:
        with open('logs/application.log', 'r') as f:
            log_content = f.read()
    except:
        log_content = "No logs found"
    
    return render_template('logs.html', 
                         log_content=log_content,
                         user=session['user'])

@app.route('/users')
def users():
    """User management page"""
    if 'user' not in session:
        return redirect('/')
    
   
    users_list = [
        {'id': 1, 'name': 'Admin', 'role': 'Administrator', 'status': 'Active'},
        {'id': 2, 'name': 'John Doe', 'role': 'Manager', 'status': 'Active'},
        {'id': 3, 'name': 'Soufian', 'role': 'Employee', 'status': 'Active'}
    ]
    
    return render_template('users.html', 
                         users=users_list,
                         user=session['user'])

@app.route('/audit')
def audit():
    """Security audit page"""
    if 'user' not in session:
        return redirect('/')
    
   
    audit_logs = [
        {'time': '2024-01-15 09:15', 'event': 'User login', 'user': 'admin', 'ip': '192.168.1.100'},
        {'time': '2024-01-15 10:30', 'event': 'Document accessed', 'user': 'admin', 'ip': '192.168.1.100'},
        {'time': '2024-01-15 11:45', 'event': 'System command', 'user': 'admin', 'ip': '192.168.1.100'}
    ]
    
    return render_template('audit.html',
                         audit_logs=audit_logs,
                         user=session['user'])



if __name__ == '__main__':
   
    setup_files()
    
    print("\n" + "="*60)
    print("       DATAROOM ENTERPRISE - WEB APPLICATION")
    print("="*60)
    print(f"\n🌐 Server: http://localhost:5000")

   
    print("="*60)
    
    # Run app
    app.run(debug=True, port=5000)