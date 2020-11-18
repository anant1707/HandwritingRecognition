# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 20:35:51 2020

@author: Anant
"""


#import keras
import matplotlib.pyplot as plt
from builtins import str
from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL
import mail
import numpy as np
from forms import ResetForm,RegistrationForm,LoginForm,EmptyForm,ForgotForm,NewPassForm,ChangePassword
import os
from flask_wtf.file import FileField,FileAllowed
from passlib.hash import pbkdf2_sha256
import sms
import random
from datetime import date

#model=keras.models.load_model("DL-part/Model/model_char74k.h5")
app = Flask(__name__)
#=============================================================================
#MYSQL CONFIGURATION
app.config['SECRET_KEY'] = 'AjJ0lXaX5K9tai8QsUhwwQ'
app.secret_key='Nottobetold'
# app.config['UPLOAD_FOLDER']=PEOPLE_FOLDER
# app.config['CROP_IMG']=CROP_FOLDER
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Anant@1707'
app.config['MYSQL_DB'] = 'hwr'
mysql=MySQL(app)
#HOMEPAGE

@app.route('/',methods=['GET','POST'])
def home():
    if(request.method=='POST'):
        res=request.get_json(force=True)
        #print(res)
        lst=[]
        for stroke in res:
            for c in stroke:
                lst.append((float(c['x']),float(c['y'])))
        
        #print(lst)

        StrokeSet=np.array(lst)
        #print(StrokeSet)
        minx = min(StrokeSet[:, 0])
        miny = min(StrokeSet[:, 1])
        maxx = max(StrokeSet[:, 0])
        maxy = max(StrokeSet[:, 1])

        #print(minx,miny,maxx,maxy)

        StrokeSet[:, 0] = StrokeSet[:, 0] - minx
        StrokeSet[:, 1] = StrokeSet[:, 1] - miny

        StrokeSet[:, 0] = StrokeSet[:, 0] / (maxx-minx)
        StrokeSet[:, 1] = StrokeSet[:, 1] / (maxy-miny)


        if(len(StrokeSet)<365):
            StrokeSet=np.vstack((StrokeSet,(np.zeros((365-len(StrokeSet),2)))))

        #print(StrokeSet.shape)
        StrokeSet=np.reshape(StrokeSet,(1,365,2))


        char_map=[i for i in range(10)]

        AtoZ=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        atoz=list("abcdefghijklmnopqrstuvwxyz")
        char_map.extend(AtoZ)
        char_map.extend(atoz)

        #print(StrokeSet)
        y=model.predict(StrokeSet)

        y=np.array(y)
        y=np.reshape(y,(62,))
        #print(y[np.argmax(y)]*100)
        return (str(char_map[np.argmax(y)])+str(y[np.argmax(y)]*100)), 200
        
        
    return render_template('index.html',title='Home',character='default')

@app.route('/plot',methods=['GET','POST'])
def plot():
    if(request.method=='POST'):
        res=request.get_json(force=True)
        
        points=[]
        for stroke in res:
            for c in stroke:
                points.append((float(c['x']),float(c['y'])))

        StrokeSet=np.array(points)
        #print(StrokeSet)
        minx = min(StrokeSet[:, 0])
        miny = min(StrokeSet[:, 1])
        maxx = max(StrokeSet[:, 0])
        maxy = max(StrokeSet[:, 1])

        #print(minx,miny,maxx,maxy)

        points=sorted(points)
        # print(points)
        x=[]
        y=[]
        dictionary={}
        for c in points:
            if(c[0] in dictionary):
                dictionary[c[0]]=min(dictionary[c[0]],c[1])
            else:
                dictionary[c[0]]=c[1]

        for i in sorted(dictionary.keys()):
            x.append((i-minx)/(maxx-minx))
            y.append(0.5)
        #print(x,y)

        plt.scatter(x,y)
        plt.axis([0,1,1,0])
        plt.savefig('plot.png')
        plt.close()

    return render_template('index.html',title='Home',character='default')

@app.route('/register',methods=['GET','POST'])
def register():
    session.pop('logged-in',False)
    form=RegistrationForm()
    if request.method=='POST':
        if form.validate_on_submit():
            cursor=mysql.connection.cursor()
            result=request.form.to_dict()
            result['email']=form.data['email'].lower()

            regdata=[]

            for key,value in result.items():
                if(key=='submit' or key=='cpassword' or key=='csrf_token'):
                    continue
                elif (key=='password'):
                    regdata.append(pbkdf2_sha256.hash(value))
                elif(key!='type'):
                    regdata.append(value)
            #fname,lname,phone,email,password
            #print(f"INSERT INTO USERINFO VALUES {tuple(regdata)}")

            try:
                #print(f"INSERT INTO USERINFO VALUES {tuple(regdata)}")
                cursor.execute(f"INSERT INTO USERINFO VALUES {tuple(regdata)}")

            except:
                return redirect(url_for('register'))

            else:

                session['log-in']='reg'
                flash("Verify Otp!","info")
                return redirect(url_for('resetpass'))
            mysql.connection.commit()
            cursor.close()
        else:
            return render_template('register.html',form=form)
    else:
        return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    session.pop('logged-in',False)
    form=LoginForm()
    if(request.method == 'POST'):
        cursor=mysql.connection.cursor()
        result=form.data
        cursor.execute(f"Select passwordd from userinfo where lower(email)='{result['email'].lower()}'")
        a=cursor.fetchone()
        if a is None:
            flash(f"NO ACCOUNT EXISTS WITH THIS USERNAME",'danger')
            return redirect(url_for('register'))
        else:
            dict1 = dataret(result['email'].lower())
            if pbkdf2_sha256.verify(result['password'], a[0]):
                session['logged-in']=True
                session['email']=result['email']
                return redirect(url_for('userhome'))

            else:
                flash("Incorrect Password!","danger")
                return render_template("login.html",form=form)
    else:

        return render_template('login.html',form=form)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    session.pop('logged-in', False)
    form=ForgotForm()
    cur = conn.cursor()
    if request.method == 'POST':
        phone=form.data['phone']
        cur.execute(f"select email from userinfo where phone = '{phone}' ")
        a=cur.fetchone()
        if(a == None):
            flash("You are not registered!!,REGISTER NOW", 'danger')
            return redirect(url_for('register'))
        else:
            session['phone'] = phone
            session['logged-in']=False
            return redirect(url_for('resetpass'))

    return render_template('forgot.html',form=form)

@app.route('/reset', methods=['GET', 'POST'])
def resetpass():
    if(not session.get('phone')):
        return redirect(url_for('login'))

    form= ResetForm()
    if request.method == 'POST':
        ootp = form.data['otp']
        if ootp == session['otp']:
            if(session.get('log-in')=='reg'):

                conn.commit()
                session.pop('log-in', None)
                session.pop('phone', None)

                return redirect(url_for('login'))




            return redirect(url_for('newpass'))
        else:

            flash('INVALID OTP', 'danger')
            return redirect(url_for('resetpass'))


    otp1 = str(random.randrange(100000, 999999))
    print(otp1)
    URL = 'https://www.way2sms.com/api/v1/sendCampaign'
    session['otp']=otp1
    phone=session['phone']

    #resp=sms.sendPostRequest(URL, 'C23FTIDPYUYZVP7UV238S0QC1POBFWMR', 'N1AY9Q2S52NHUADE', 'stage', phone, '9781396442', f"Your OTP (One Time Password) to change your password is: {otp1} Do not share this with anyone!   Team college+")
    #print(resp.text)
    return render_template('verifyotp.html',form=form)

@app.route('/changepass',methods=['GET','POST'])
def changepass():
    if (not session.get('logged-in')):
        flash('LOGIN TO CONTINUE', 'danger')
        return redirect(url_for('logout'))

    form=ChangePassword()
    if request.method=='POST':
        if form.is_submitted():
            oldp=form.oldpassword.data
            dict1=dataret(session['email'])
            if pbkdf2_sha256.verify(oldp,dict1['passwordd']):
                cursor=mysql.connection.cursor()
                newpassworda=pbkdf2_sha256.hash(form.password.data)
                cursor.execute(f" UPDATE  userinfo  set passwordd = '{newpassworda}' where email='{session['email']}' ")
                conn.commit()
                flash('Update successfull', 'success')
                return redirect(url_for('userhome'))
            else:
                flash('Enter Correct old password', 'danger')
                return redirect(url_for('changepass'))

    return render_template('newpass.html',form=form,title="Change Password")

@app.route('/newpass', methods=['GET', 'POST'])
def newpass():
    form=NewPassForm()
    cur = conn.cursor()
    if request.method == 'POST':
        newpassword = form.data['password']
        confirmnewpassword = form.data['cpassword']

        if (newpassword == confirmnewpassword):
            newpassworda = pbkdf2_sha256.hash(newpassword)

            cur.execute(f" UPDATE  userinfo  set passwordd = '{newpassworda}' where email =  '{session['email']}' ")
            conn.commit()
            session['logged-in']=True
            return redirect(url_for('userhome'))
        else:
            flash("passwords didnt match", 'danger')
            return redirect(url_for('newpass'))
    return render_template('newpass.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    session.pop('logged-in', False)
    session.pop('phone', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)