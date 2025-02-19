from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector

app=FastAPI()
templates = Jinja2Templates(directory="templates")

# 與資料庫連線
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345678",
  database="website"
)
mycursor = mydb.cursor()
# session
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
# 提供靜態文件
app.mount("/static", StaticFiles(directory="static"), name="static")
# HomePage
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
# Error Page
@app.get("/error")
async def error(request: Request):
    message = request.query_params.get("message") 
    return templates.TemplateResponse("error.html", {"request": request, "message":message})
# Signup Endpoint
@app.post("/signup")
async def signup(request: Request, name:str=Form(...),username:str=Form(...),password:str=Form(...)):
    if name == "" or username == "" or password=="":
        return RedirectResponse(url="/error?message=Please enter name, username and password", status_code=303)
    sql = "SELECT * FROM member WHERE username = %s"
    # must be of type list, tuple or dict
    val = (username,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if (myresult):
        return RedirectResponse(url="/error?message=Repeated username", status_code=303)
    else:
        sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
        val = (name, username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        return RedirectResponse(url="/", status_code=303)
# Signin Endpoint
@app.post("/signin")
async def login(request: Request, account:str=Form(...),password:str=Form(...)):
    if account == "" or password=="":
        return RedirectResponse(url="/error?message=Please enter username and password", status_code=303)
    sql = "SELECT id, name FROM member WHERE username = %s AND password = %s"
    val = (account, password)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if (myresult):
        request.session["SIGNED-IN"] = True
        request.session["ID"] = myresult[0][0]
        request.session["NAME"] = myresult[0][1]
        return RedirectResponse(url="/member", status_code=303)
    else:
        return RedirectResponse(url="/error?message=Username or password is not correct", status_code=303)
# Signout Endpoint
@app.get("/signout")
async def logout(request: Request):
    request.session["SIGNED-IN"]=False
    request.session["ID"]=""
    request.session["NAME"]=""
    return RedirectResponse(url="/", status_code=303)
# Member Page
@app.get("/member")
async def success(request: Request):
    if not request.session["SIGNED-IN"]:
        return RedirectResponse(url="/", status_code=303)
    sql = "SELECT MEMBER.ID, MEMBER.NAME, MESSAGE.ID, MESSAGE.content FROM MESSAGE JOIN MEMBER ON MESSAGE.MEMBER_ID = MEMBER.ID ORDER BY MESSAGE.time DESC"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    object=[]
    for result in myresult:
        object.append(dict([("currentUser", result[0]==request.session["ID"]),("name",result[1]),("currentMessage", result[2]),("message",result[3])]))
    return templates.TemplateResponse("member.html", {"request": request, "account":request.session["NAME"], "messages":object})
# CreateMessage Endpoint
@app.post("/createMessage")
async def createMessage(request: Request, message:str=Form(...)):
    if message=="":
        return RedirectResponse(url="/error?message=Please enter message", status_code=303)
    sql = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
    val = (request.session["ID"],message)
    mycursor.execute(sql, val)
    mydb.commit()
    return RedirectResponse(url="/member", status_code=303)
# DeleteMessage Endpoint
@app.post("/deleteMessage")
async def deleteMessage(request: Request, deleteID:str=Form(...)):
    sql = "SELECT member_id FROM message WHERE id = %s"
    val = (deleteID,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if(myresult[0][0]!=request.session["ID"]):
        return RedirectResponse(url="/error?message=Incorrect ID", status_code=303)
    sql = "DELETE FROM message WHERE id = %s"
    val = (deleteID,)
    mycursor.execute(sql, val)
    mydb.commit()
    return RedirectResponse(url="/member", status_code=303)