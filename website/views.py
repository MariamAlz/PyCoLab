from flask import Blueprint,render_template ,request,flash,jsonify,redirect,url_for,session 
from flask_socketio import SocketIO,send,join_room,leave_room,emit
from flask_login import login_user,login_required ,logout_user,current_user
from .models import Note , Code ,Task ,user_task ,Admin ,User ,Request, Room,Logs, Approved
from . import db
from . import socketio
import json 
import io
import sys
from . import app
views = Blueprint('views',__name__)

@views.route('/' ,methods=['GET','POST'])       
@login_required
def home():
    session.clear()
    # return render_template("index.html",user=current_user)
    return redirect(url_for('views.index'))
    if request.method == 'POST':
        note = request.form.get('note') 
        print(note)

        if len(note) < 1:
            flash('Note is too short' ,category='error')
        else:
            new_note =Note(data=note ,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully !',category='success')

    return render_template("index.html",user=current_user)




@views.route('/delete-note', methods=['POST'])
def delete_note():
    task = json.loads(request.data)
    taskId=  task['taskId']
    task = Task.query.get(taskId)

    if task:
        # if note.user_id == current_user.id:
        current_user.Tasks.remove(task)
        db.session.delete(task)
        db.session.commit()
        flash('Note added successfully !',category='success')
    
    return jsonify({})   

from operator import itemgetter
from datetime import datetime

@views.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        name = request.form['name']
        data = request.form['Description']
        request_limit = request.form['request_limit']
        print(name)
        admin = None

        if len(name) < 1:
            flash('Name is short', category='error')
        else:
            if current_user.is_admin:
                admin = Admin.query.filter_by(email=current_user.email).first()
                new_task = Task(name=name, data=data, request_limit=request_limit)
                db.session.add(new_task)
                db.session.commit()
                for student in admin.students:
                    print(student.first_name)
                    student.Tasks.append(new_task)
                current_user.Tasks.append(new_task)
                db.session.commit()
                flash('Note added successfully!', category='success')

    if current_user.is_admin:
        admin = Admin.query.filter_by(email=current_user.email).first()
        students = admin.students
        last_run_times = {
            student.id: Code.query.filter_by(user_id=student.id).order_by(Code.date.desc()).first().date
            for student in students
        }
        return render_template("index.html", user=current_user, admin=admin, students=students, last_run_times=last_run_times)
    
    return render_template("index.html", user=current_user)

    
    # return render_template("index_3.html" , user=current_user)

    # if request.method == 'POST':
    #     name= request.form.get('name')
    #     data = request.form.get('Description')
    #     print(name)

    #     if len(name) < 1:
    #         flash('Name is short' ,category='error')
    #     else:
    #         new_task = Task(name=name , data = data)
    #         db.session.add(new_task)
    #         db.session.commit()
    #         current_user.Tasks.append(new_task)
    #         db.session.commit()
    #         flash('Note added successfully !',category='success')

    # return render_template("index.html",user=current_user)

@views.route('/populate', methods=['GET', 'POST'])
@login_required
def populate():
    
    # return render_template("index_3.html" , user=current_user)
    global Data
    global task
    global code
 
    if request.method == 'POST':
        
        code = json.loads(request.data)
        # print(task)
        codeId =  code['codeId']
        code = Code.query.get(codeId)
        Data = code.data
        print(Code.data)
        return jsonify({}) 
    
    if current_user.is_admin:
         admin = Admin.query.filter_by(email=current_user.email).first()
         return render_template("index_3.html",task=task ,data = Data, current_code=None,user=current_user ,admin=admin)
    admin = Admin.query.filter_by(id=current_user.admin_id).first()

    return render_template("index_3.html", task=task , data = Data , current_code = code, user=current_user,admin=admin)
    

@views.route('/updatedata', methods=['GET', 'POST'])
@login_required
def updatedata():
    global Data
    global task
    global code
    print("inside")
    if request.method == 'POST':
        data = request.form.get('note') 
        # code = json.loads(request.data)
        # # print(task)
        # codeId =  code['codeId']
        # data = code['data']
        # print(data)
        codeId = code.id
        code = Code.query.get(codeId)
        code.data = data
        db.session.commit()
        Data = data
        output = io.StringIO()
        sys.stdout = output
        try:
            exec(data, globals())
        except Exception as e:
            print(str(e))
        sys.stdout = sys.__stdout__
        code.output = output.getvalue()
        db.session.commit()

        # return jsonify({}) 
    
    if current_user.is_admin:
         admin = Admin.query.filter_by(email=current_user.email).first()
         return render_template("index_3.html",task=task ,data = Data, current_code=code,user=current_user ,admin=admin)
    admin = Admin.query.filter_by(id=current_user.admin_id).first()
        

    return render_template("index_3.html", task=task , data = Data , current_code = code,output=output.getvalue(), user=current_user,admin = admin)
    
    



@views.route('/index_3', methods=['GET', 'POST'])
@login_required
def index_3():
    return redirect(url_for('views.action'))




@views.route('/run', methods=['GET', 'POST'])
@login_required
def run():
    if request.method == 'POST':
        data = request.form.get('code_editor') 
        
        
        code = Code.query.get(int(session['code_name']))
        code.data = data
        db.session.commit()
        Data = data
        output = io.StringIO()
        sys.stdout = output
        try:
            exec(data, globals())
        except Exception as e:
            print(str(e))
        sys.stdout = sys.__stdout__

        session['output'] = output.getvalue()
        code.output =  output.getvalue()
        session['data'] = data
        return render_template('room.html', user= current_user,session=session)

    # redirect (url_for('views.change'))
    return render_template('room.html', user= current_user,session=session)
    







@views.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.args:
        pass
        session['request_id'] = request.args.get('request_id')
        session['data'] = request.args.get('data')
        session['room'] = request.args.get('room')
    
    if request.method == 'POST':
        recievied_data = json.loads(request.data)
        print(recievied_data)
        username =  recievied_data['username']
        room =  recievied_data['room']
        code_id = recievied_data['code_id']
        task_id =  recievied_data['task_id']
        student_id = recievied_data['student_id']
        print(student_id)
        
        
        session['username']= username
        session['task_name'] = task_id
        session['code_name'] = code_id
        code = Code.query.get(int(code_id))
        # print(code)
        # print(code.name)

        new_request = Request(requester_id = current_user.id, requester_name = current_user.first_name ,requestee_id = int(student_id ) ,type = room ,code_id = int(code_id) , task_id = int(task_id))
        db.session.add(new_request)
        db.session.commit()

        
        session['data'] = code.data
        session['room']= room
        print('we are in chatt route')

        return jsonify({"request_id": new_request.id}) 
    print(session)
    if current_user.is_admin:
         admin = Admin.query.filter_by(email=current_user.email).first()
         return render_template('room.html', user= current_user,session=session ,admin=admin)


    return render_template('room.html', user= current_user,session=session )




@views.route('/checkstudentwork', methods=['GET', 'POST'])
@login_required
def checkstudentwork():
    # session.clear()
    global task
    global student 
    global Data
    global logs


    
    if request.method == 'POST':
        recievied_data = json.loads(request.data)
        print(recievied_data)
        username =  recievied_data['studentid']
        task_id =  recievied_data['task_id']
        
        task= Task.query.get(int(task_id))
        student = User.query.get(username)
        Data = None
        logs = None
        for code in student.codes:
            if code.task_id == task.id:
                Data =code.data
                log_code = Code.query.get(code.id)
                print(log_code.name)
                logs = Logs.query.filter_by(code_id= code.id).all()
               
                
                
        


        return jsonify({}) 
    return render_template('student_work.html', user= current_user,session=session , task=task,student=student,admin=current_user,data= Data, current_logs= logs)


@views.route('/sniffRoom' , methods=['GET', 'POST'])
@login_required
def sniffRoom():
    if request.method == 'POST':
        data = json.loads(request.data)
        request_id = data['request_id']
        return jsonify({"request_id": request_id}) 
        
    

    return 

@views.route('/studentCode', methods=['GET', 'POST'])
@login_required
def studentCode():
    global Data
    if request.method == 'POST':
        code = json.loads(request.data)
        # print(task)
        codeId =  code['codeId']
        code = Code.query.get(codeId)
        Data = code.data
        print(Code.data)
        return jsonify({}) 
    return 

    

@views.route('/change', methods=['GET', 'POST'])
@login_required
def change():
    
    if request.method == 'POST':
        recievied_data = json.loads(request.data)
        
        print(recievied_data)
        
        
        session['data']= recievied_data['data']
        
        session['code_name']
        code = Code.query.get(int(session['code_name'] ))
        print(recievied_data)
        
        code.data = recievied_data['data']
        db.session.commit()
        
        print(code.data)
        

        return jsonify({}) 
        
    return render_template('room.html', user= current_user,session=session)

@socketio.on('join' )
def join(data):
    # session.clear()
    print('data:', data)
    request_id = data['request_id']
    request = Request.query.get(int(request_id))
    session['request_id'] = request_id
    code = Code.query.get(request.code_id)
    print(code.data)
    

    

    room =Room.query.filter_by(request_id =request.id).first()
    
    if room :
        pass
    else :
        temp_requestor = User.query.get(request.requester_id)
        temp_helper =  User.query.get(request.requestee_id)
        room_name = temp_requestor.first_name + '-' +  temp_helper.first_name + "-" + str(request.id)
        new_room = Room(name= room_name , requester_name = temp_requestor.first_name,helper_name = temp_helper.first_name , creator_id = request.requester_id ,helper_id = request.requestee_id ,request_id= request.id , admin_id = temp_requestor.admin_id)

        db.session.add(new_room )
        db.session.commit()

        new_log = Logs(before = code.data , code_id= code.id ,output=code.output, request_id = request.id, error_type = request.type,helper_name= temp_helper.first_name)
        db.session.add(new_log )
        db.session.commit()
        print("new log created")

    
    room = request.type
    # session['data'] = code.data
    session['data'] = code.data
    session['room'] = room
    
    join_room(room)

  

    print(f"{current_user.first_name} joined room {room}")
    # emit('chat',{'username':session},room=room)
    # return redirect(url_for('views.checkstudentwork'))
    # return render_template('room.html', user= current_user,session=session)
    print('session',session)
    data = session.get('data')
     
    # emit('redirect', {'url':  url_for('views.chat', data=data , request_id = request_id , room= session['room'])})
    emit('redirect', {'url':  url_for('views.requestForm', data=data , request_id = request_id , room= session['room'])})
    # redirect(url_for('views.chat'))


@socketio.on('text')
def text(message): 
    room = session.get('room')
    print('room' , room)
    print("message" , message)
    # session['data'] = message
    request_id  = session.get('request_id')
    print("request_id" , request_id)
   
    request = Request.query.get(int(request_id))
    code = Code.query.get(request.code_id)
    temp_helper = User.query.get(request.requestee_id)
    log = Logs.query.filter_by(code_id= request.code_id ,request_id =request.id, helper_name = temp_helper.first_name).first()
    
    code.data = message
    log.after = message
    db.session.commit()
    session['data']= message

    print("session", message)
    # join_room(room)
    # send({"data": session['data']} ,room=room)
    emit( "message",{"data": session['data']},broadcast=True )
    # emit('redirect', {'url':  url_for('views.chat', data=session['data'] , request_id = request_id , room= session['room'] )})

    # emit('message',{'msg:' + session.get('username')  + ': ' + message['msg']},room = room)




# @socketio.on("connect")
# def connect(auth):
#     room = session.get("room")
#     # name = session.get("name")
#     # if not room or not name:
#     #     return
#     # if room not in rooms:
#     #     leave_room(room)
#     #     return
    
#     join_room(room)
#     # send({"name": name, "message": "has entered the room"}, to=room)
#     # rooms[room]["members"] += 1
#     print("ab connect")
#     print(f"{current_user.first_name} joined room {room}")


@socketio.on('left')
def left(data):
    room = data['room']
    print("roooooooom", data)
    # username = session.get('username')
    leave_room(room)
    session.clear()

    # emit('sta',{'msg': session.get('username') + 'has left the room'},room = room)
    # emit('redirect', {'url':  url_for('views.chat')})
    emit('redirect', {'url':  url_for('views.requestForm')})





@views.route('/add_files', methods=['GET', 'POST'])
@login_required
def add_files():
    # name= request.form['name']
    # data = request.form['Description']
    print("jjjj")
    if request.method == 'POST':
        # name= request.form.get('name')
        # data = request.form.get('Description')
        name= request.form['name']
        data = request.form['language']
        print(name)

        if len(name) < 1:
            flash('Name is short' ,category='error')
        
        else:
            global task
            new_code = Code(name=name ,user_id =current_user.id,task_id = task.id ,request_limit =0)
            db.session.add(new_code)
            db.session.commit()
            # current_user.Tasks.append(new_task)
            # db.session.commit()
            flash('Code successfully !',category='success')
    
    return redirect(url_for('views.index_3'))




@views.route('/leave',methods=['GET', 'POST'])
@login_required
def leave():
    if request.method == 'POST':
        data = json.loads(request.data)
        print("jdjjdjjdjjdj")
        room = data['room']
        
        return jsonify({"room": room}) 
    return 


@views.route('/requestForm',methods=['GET', 'POST'])
@login_required
def requestForm():
    if request.args:
        pass
        session['request_id'] = request.args.get('request_id')
        session['data'] = request.args.get('data')
        session['room'] = request.args.get('room')

    if request.method == 'POST':
        data = request.form.get('student')
        data = json.loads(data)
        print('dataaaaaaaa',data)
        print(data['student_id'])
        student = User.query.get(int(data['student_id']))
        type = request.form.get('type')
        room = type + '' + current_user.first_name + '-' + student.first_name
        code_id = data['code_id']
        task_id = data['task_id']

       
        
        # room =  recievied_data['room']
        # code_id = recievied_data['code_id']
        # task_id =  recievied_data['task_id']
        # student_id = recievied_data['student_id']
        # print(student_id)
        
        
        session['username']= student.first_name
        session['task_name'] = task_id
        session['code_name'] = code_id
        code = Code.query.get(int(code_id))
        task = Task.query.get(int(task_id))
        session['data'] = code.data
        
        if code.request_limit <= task.request_limit:
            new_request = Request(requester_id = current_user.id, requester_name = current_user.first_name ,requestee_id = student.id  ,type = type ,code_id = int(code_id) , task_id = int(task_id))
            db.session.add(new_request)
            code.request_limit = code.request_limit + 1
            db.session.commit()
        else:
            
            code.request_limit_is_reached = True
            db.session.commit()

    
        return render_template('room.html', user= current_user,session=session )

    

    if current_user.is_admin:
         admin = Admin.query.filter_by(email=current_user.email).first()
         return render_template('room.html', user= current_user,session=session ,admin=admin)
    
    return render_template('room.html', user= current_user,session=session )

@views.route('/viewDash', methods=['GET', 'POST'])
@login_required
def viewDash():

    jsondata = []
    admin = Admin.query.filter_by(email=current_user.email).first()
    num_students = len(admin.students)
    num_tasks = Task.query.count()
    num_collaborations = len(admin.rooms)
    num_executions = Logs.query.count()
    #num_requests = Request.query.count()
    num_requests = Request.query.join(User, User.id == Request.requester_id).filter(User.is_admin == False).count()

    
    if request.method == 'POST':
        jsondata = []
        admin = Admin.query.filter_by(email=current_user.email).first()
        
        for student in admin.students:
            for task in student.Tasks:
                code = Code.query.filter_by(task_id=task.id).first()
                temp_task = Task.query.filter_by(id=task.id).first()
                                
                jsondata.append({"name": student.first_name, "task": temp_task.name, "Done": 1})
            
        print(jsondata)
        return jsonify(jsondata)
    
    if current_user.is_admin:
        admin = Admin.query.filter_by(email=current_user.email).first()
        return render_template('charts.html', user=current_user, session=session, admin=admin, num_students=num_students, num_tasks=num_tasks, num_collaborations=num_collaborations, num_executions=num_executions, num_requests=num_requests)
    
    return render_template('charts.html', user=current_user, session=session, num_students=num_students, num_tasks=num_tasks, num_collaborations=num_collaborations, num_executions=num_executions, num_requests=num_requests)


@views.route('/getJson',methods=['GET', 'POST'])
@login_required
def getJson():
    # if request.method == 'POST':
    jsondata = []
    admin = Admin.query.filter_by(email=current_user.email).first()
    for student in admin.students:
        for task in student.Tasks:
            code = Code.query.filter_by(task_id = task.id).first()
            temp_task = Task.query.filter_by(id= task.id).first()
            
            jsondata.append({"name":student.first_name,"task":temp_task.name , "Done":1})
        
    print(jsondata)

    return jsonify(jsondata) 
    
    return
    # if current_user.is_admin:
    #     admin = Admin.query.filter_by(email=current_user.email).first()
    #     return render_template('charts.html', user= current_user,session=session,admin= admin)
    # return render_template('charts.html', user= current_user,session=session)


@views.route('/getSecondJson',methods=['GET', 'POST'])
@login_required
def getSecondJson():
    # if request.method == 'POST':
    jsondata = []
    admin = Admin.query.filter_by(email=current_user.email).first()
    for student in admin.students:
        for task in student.Tasks:
            code = Code.query.filter_by(task_id = task.id).first()
            temp_task = Task.query.filter_by(id= task.id).first()
            for request in student.requests:
                if request.task_id == temp_task.id:
                    jsondata.append({"name":student.first_name,"task":temp_task.name , "ID":student.id, "help":request.type})
        
    print(jsondata)

    return jsonify(jsondata) 
    
    return

from flask import render_template

@views.route('/list_students_last_code_run', methods=['GET'])
def list_students_last_code_run():
    students = User.query.filter_by(is_admin=False).all()
    students_data = []

    for student in students:
        last_code = Code.query.filter_by(user_id=student.id).order_by(Code.date.desc()).first()
        last_code_run = last_code.date if last_code else None
        students_data.append({
            'student_id': student.id,
            'student_name': student.first_name,
            'last_code_run': last_code_run.strftime('%Y-%m-%d %H:%M:%S') if last_code_run else None
        })

    return render_template('index.html', students_d=students_data)


@views.route('/list_tasks_last_code_run', methods=['GET'])
def list_tasks_last_code_run():
    tasks = Task.query.all()
    tasks_data = []

    for task in tasks:
        last_code = Code.query.filter_by(task_id=task.id).order_by(Code.date.desc()).first()
        last_code_run = last_code.date if last_code else None
        tasks_data.append({
            'task_id': task.id,
            'task_name': task.name,
            'last_code_run': last_code_run
        })

    return jsonify(tasks_data)