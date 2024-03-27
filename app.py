from flask import *
import pymysql

app=Flask(__name__)


#db connection
mydb=pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    db="nrcm"
)

cursor=mydb.cursor()

#login page
is_login=False

userId=""
rollNumber=""
userRole=""
@app.route("/",methods=["GET", "POST"])
def login():
    error=""
    if request.method=="POST":
        roll=request.form['username']
        cursor.execute("SELECT * FROM users WHERE username=%s",(roll,))
        data=cursor.fetchone()
        
        if data==None:
            error="Invalid User"
        else:
            global is_login
            global userId
            global rollNumber
            global userRole
            
            is_login=True
            userId=data[0]
            rollNumber=data[2]
            userRole=data[6]
            return redirect("dashbord")
            
    return render_template("index.html",data=error)

#dashbord page
@app.route("/dashbord")
def dashbordPage():
    if is_login:
        return render_template("index2.html")
    else:
        return redirect("/")
    
    
#registration form
@app.route("/registration",methods=["GET","POST"])
def reg():
    msg=""
    if request.method=="POST":
        username=request.form['username']
        roll=request.form['roll_number']
        email=request.form['email']
        password=request.form['password']
        
        try:
            cursor.execute("INSERT INTO users SET username=%s,roll_number=%s,email=%s,`password`=%s",(username,roll,email,password))
            mydb.commit()
            msg=1
        except:
            msg=0
            
    return render_template("form.html",msg=msg)

#retrieve data
is_login=False
@app.route("/info",methods=["GET","POST"])
def access():
    msg=""
    error=""
    if request.method=="POST":
        uname=request.form['username']
        try:
            cursor.execute("SELECT * FROM users WHERE username=%s",(uname))
            error=cursor.fetchone()
            msg=1
        except:
            msg=0
        
        if error==None:
            error="Invalid User"
        else:
            global is_login
            is_login=True
            retrieve=error
    return  render_template("form2.html",retrieve=error)

#retrieving users data
@app.route("/users")
def userslist():
    cursor.execute("SELECT * FROM users")
    data=cursor.fetchall()
    return render_template("users.html",users=data)



#retrieving data  of a particular user
@app.route("/myinfo")
def details():
    if is_login:
        cursor.execute("SELECT * FROM users WHERE roll_number=%s",(rollNumber,))
        userData=cursor.fetchone()
        return render_template("information.html",user=userData)
    else:
        return redirect("/")
    
    
#edit users  information
@app.route("/editinfo",methods = ["GET","POST"])
def editData():
    msg=""
    userId=request.args.get('id')
    if request.method == 'POST':
        uname=request.form['username']
        email=request.form['email']
        print(uname)
        try:
            cursor.execute("UPDATE users SET username=%s,email=%s WHERE id=%s",(uname,email,userId,))
            mydb.commit()
            return redirect("/users")
        except:
            return redirect("/users")
    cursor.execute("SELECT * FROM users WHERE id=%s",(userId,))
    userData=cursor.fetchone()
    return  render_template("editmyinfo.html",user=userData,msg=msg)
    
    
#delete users
@app.route("/deleteinfo")
def deleteuser():
    userId=request.args.get('id')
    try:
        cursor.execute("DELETE FROM users WHERE id=%s",(userId,))
        return redirect("/users")
    except EXCEPTION as e:
        print(str(e))
        return redirect('/users') 

    
if __name__=="__main__":
    app.run(debug=True)