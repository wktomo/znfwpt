from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置一个密钥，用于加密会话数据

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 在这里添加验证逻辑
        if username == 'admin' and password == 'password':  # 示例验证
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('您已成功登出')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash('请先登录')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/feedback')
def feedback():
    return "反馈页面"

@app.route('/more')
def more():
    return "更多信息页面"

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/my_info')
def my_info():
    return render_template('my_info.html')

if __name__ == '__main__':
    app.run(debug=True)