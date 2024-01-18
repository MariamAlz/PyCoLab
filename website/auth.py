from flask import Blueprint ,render_template,request, flash ,redirect,url_for
from .models import User,Admin
from . import db
from werkzeug.security import generate_password_hash ,check_password_hash
from flask_login import login_user,login_required ,logout_user,current_user


auth = Blueprint('auth',__name__)

@auth.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user =User.query.filter_by(email=email).first()
        #print(user.email)
        if user :
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password, try again.',category ='error')
        else:
            flash('Email is invalid!',category ='error')
        
    return render_template("login.html",user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign-up",methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_type = request.form.get('user-type')
        print(user_type)
        if user_type == 'admin':
            user = Admin.query.filter_by(email=email).first()
        else:
            user = User.query.filter_by(email=email).first()
        if user :
            flash('Email is already in use.',category='error')

        elif len(email) <4 :
            flash('Email must be greater than 4 characters.', category='error')

        elif len(first_name)< 2:
            flash('Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        elif len(password1)< 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            if user_type =='admin':

                new_user = User(email = email,first_name=first_name ,is_admin=True,password = generate_password_hash(password1,method= 'sha256'))
                new_admin = Admin(email = email,first_name=first_name ,password = generate_password_hash(password1,method= 'sha256'))
                db.session.add(new_admin)
                db.session.add(new_user)
                db.session.commit()
                users = User.query.all()
                for student in users:
                    print(student.first_name)

                    if not student.is_admin:
                        student.admin_id = new_admin.id
                    db.session.commit()
                
            else:
                 new_user = User(email = email,first_name=first_name ,is_admin=False,password = generate_password_hash(password1,method= 'sha256'))
                 print("I am here!")
                 db.session.add(new_user)
            
                 db.session.commit()
            flash('Acount created!', category='success')
            login_user(new_user ,remember=True)
            return redirect(url_for('views.home'))
            #add user to database

    return render_template("sign_up.html" ,user=current_user)



