from flask import Flask,render_template,request,url_for,redirect,flash,session
import hashlib
import ibm_db
import ibm_boto3
from ibm_botocore.client import Config, ClientError


import requests

app=Flask(__name__)
app.secret_key = "abc"  



#cloud
connection = ibm_db.connect("DATABASE=bludb;HOSTNAME=815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30367;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ltk79172;PWD=lyUb0CFg1tQd1MDu;",'','')

news_api_key="f71565537970409cbe006afcbac30c33"

@app.route("/")
def index():
    return  render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")
    

@app.route("/register",methods=['GET','POST'])
def register():
    error = None
    if request.method=='POST':
        username= request.form['username']
        email=request.form['email']
        password=request.form['password']
        cpass=request.form['cpassword']
        if password != cpass:
            error = "Password and Confirm password should be same!!"
        else:
            hashed_password=hashlib.sha256(password.encode()).hexdigest()
           
            sql="SELECT * FROM newstracker WHERE username=?"
            stat =ibm_db.prepare(connection,sql)
            ibm_db.bind_param(stat,1,username)
            ibm_db.execute(stat)
            res=ibm_db.fetch_assoc(stat)
            if res:
                error="Username is already exits user different username"
                 
            else:
                 
                sql1="INSERT INTO newstracker VALUES (?,?,?)"
                pre_stat =ibm_db.prepare(connection,sql1)
                ibm_db.bind_param(pre_stat,1,username)
                ibm_db.bind_param(pre_stat,2,email)
                ibm_db.bind_param(pre_stat,3,hashed_password)
                ibm_db.execute(pre_stat)
                
                flash('Account created successfully')
                return redirect(url_for('index'))
    return render_template('signup.html', error = error)


@app.route('/login',methods=["GET","POST"])
def login():
    error = None
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        hashed=hashlib.sha256(password.encode()).hexdigest()
        
         
        sql="SELECT * FROM newstracker WHERE username=?"
        con =ibm_db.prepare(connection,sql)
        ibm_db.bind_param(con,1,username)
        ibm_db.execute(con)
        res=ibm_db.fetch_assoc(con)
         
        if res:
            if hashed == res['HASHED_PASSWORD']:
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            else:
                error = "Login Failed!!"
                return render_template('index.html',error=error)
        else:
            error = "Login Failed!!"
            return render_template('index.html',error=error)

 
 
         
@app.route('/home')
def home():
    error=None
    if 'username' in session:
        username = session['username']
        main_url="https://newsapi.org/v2/top-headlines?country=in&apiKey="+news_api_key
        news=requests.get(main_url).json()
        articles=news["articles"]
        news_articles_title=[]
        for a in articles:
            news_articles_title.append(a["title"])

        news_articles_description=[]
        for a in articles:
            news_articles_description.append(a["description"])

        news_articles_url=[]
        for a in articles:
            news_articles_url.append(a["url"])

        news_articles_urlToImage=[]
        for a in articles:
            news_articles_urlToImage.append(a["urlToImage"])

        news_articles_publishedAt=[]
        for a in articles:
            news_articles_publishedAt.append(a["publishedAt"])

        news_articles_content=[]
        for a in articles:
            news_articles_content.append(a["content"])


        return render_template("home.html",user=username,articles=articles)
    else:
        error="Pleasr Login to access"
        return render_template('index.html',error=error)
          
@app.route('/sports')
def sports():
     error=None
     if 'username' in session:
        username = session['username']
        main_url="https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey="+news_api_key
        news=requests.get(main_url).json()
        articles=news["articles"]
        return render_template("home.html",user=username,articles=articles)
     else:
        error="Pleasr Login to access"
        return render_template('index.html',error=error)

@app.route('/entertainment')
def entertainment():
     error=None
     if 'username' in session:
        username = session['username']
        main_url="https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey="+news_api_key
        news=requests.get(main_url).json()
        articles=news["articles"]
        return render_template("home.html",user=username,articles=articles)
     else:
        error="Pleasr Login to access"
        return render_template('index.html',error=error)


@app.route('/technology')
def technology():
     error=None
     if 'username' in session:
        username = session['username']
        main_url="https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey="+news_api_key
        news=requests.get(main_url).json()
        articles=news["articles"]
        return render_template("home.html",user=username,articles=articles)
     else:
        error="Pleasr Login to access"
        return render_template('index.html',error=error)

@app.route('/science')
def science():
     error=None
     if 'username' in session:
        username = session['username']
        main_url="https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey="+news_api_key
        news=requests.get(main_url).json()
        articles=news["articles"]
        return render_template("home.html",user=username,articles=articles)
     else:
        error="Pleasr Login to access"
        return render_template('index.html',error=error)

@app.route('/business')
def business():
     error=None
     if 'username' in session:
        username = session['username']
        main_url="https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey="+news_api_key
        news=requests.get(main_url).json()
        articles=news["articles"]
        return render_template("home.html",user=username,articles=articles)
     else:
        error="Please Login to access"
        return render_template('index.html',error=error)

@app.route('/world')
def world():
     error=None
     if 'username' in session:
        username = session['username']
        main_url="https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey="+news_api_key
        news=requests.get(main_url).json()
        articles=news["articles"]
        return render_template("home.html",user=username,articles=articles)
     else:
        error="Pleasr Login to access"
        return render_template('index.html',error=error)

@app.route("/search",methods=["GET","POST"])
def search():
     if 'username' in session:
        username = session['username']
        if request.method=="POST":
            search=request.form["search"] 
            news_data = requests.get(f'https://newsapi.org/v2/everything?q={search}&apiKey='+news_api_key).json()
            articles=news_data['articles']
            return render_template("home.html",user=username,articles=articles)
        
     

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))


@app.route('/forgot_password')
def forgot_password():
    return render_template("resetpassword.html")

@app.route("/verify_email",methods=["GET","POST"])
def verify_email():
    error=None
    if request.method=="POST":
        email=request.form["email"]
        sql="SELECT * FROM newstracker WHERE email=?"
        stat =ibm_db.prepare(connection,sql)
        ibm_db.bind_param(stat,1,email)
        ibm_db.execute(stat)
        res=ibm_db.fetch_assoc(stat)
         
         
        if res:
            return render_template("resetpassword.html",result="200",email=email)
        else:
            error="No such email is available"
            return render_template("resetpassword.html",result="404",error=error)
            

@app.route("/update_password",methods=["GET",'POST'])
def update_password():
    error=None
    if request.method=="POST":
         password=request.form["newp"]
         cpass=request.form["cp"]
         email=request.form["email"]
         if cpass==password:
             
            hashed=hashlib.sha256(password.encode()).hexdigest()
            sql="UPDATE newstracker SET password=? WHERE email=?"
            stat =ibm_db.prepare(connection,sql)
            ibm_db.bind_param(stat,1,hashed)
            ibm_db.bind_param(stat,2,email)
            ibm_db.execute(stat)
             
            error="Password reset successful"
            return render_template("index.html",error=error)
         else:
            error="Password and confirm password must be same"
            return render_template("resetpassword.html",error=error)
 



if __name__=="__main__":
    app.run(debug=True)
    
