from fastapi import FastAPI, Request, Form, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector
from dotenv import load_dotenv
import os
import bcrypt

app=FastAPI()
templates = Jinja2Templates(directory="templates")

# 與資料庫連線
load_dotenv()
db_user = "root"
db_password = os.getenv("MYSQL_PASSWORD")
db_host = "localhost"
db_name = "website"
def connect_to_DB(db_host : str, db_user : str, db_pwd : str, db_Name : str):
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pwd,
        database=db_Name
    )
# 密碼加密
def hash_password(plain_password : str):
    salt = bcrypt.gensalt()  
    hashed = bcrypt.hashpw(plain_password.encode(), salt)  
    return hashed.decode() 
# session
secret_key = os.getenv("secret_key")
app.add_middleware(SessionMiddleware, secret_key=secret_key)
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
    try:
        mydb = connect_to_DB(db_host, db_user, db_password, db_name)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        # 使用者名稱重複
        if (myresult):
            return RedirectResponse(url="/error?message=Repeated username", status_code=303)
        else:
            hashed_pwd = hash_password(password)
            sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
            val = (name, username, hashed_pwd)
            mycursor.execute(sql, val)
            mydb.commit()
            return RedirectResponse(url="/", status_code=303)
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return RedirectResponse(url="/error?message=資料庫錯誤", status_code=303)
    finally:
        # release the connection resources
        mycursor.close()
        mydb.close()
# Signin Endpoint
@app.post("/signin")
async def login(request: Request, account:str=Form(...),password:str=Form(...)):
    if account == "" or password=="":
        return RedirectResponse(url="/error?message=Please enter username and password", status_code=303)
    sql = "SELECT id, name, password FROM member WHERE username = %s"
    val = (account,)
    try:
        mydb = connect_to_DB(db_host, db_user, db_password, db_name)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        if (myresult):
            hashed_password = myresult[2]
            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                request.session["SIGNED-IN"] = True
                request.session["ID"] = myresult[0]
                request.session["NAME"] = myresult[1]
                return RedirectResponse(url="/member", status_code=303)
            # 密碼錯誤
            else:
                return RedirectResponse(url="/error?message=Username or password is not correct", status_code=303)
        # 使用者名稱或密碼錯誤
        else:
            return RedirectResponse(url="/error?message=Username or password is not correct", status_code=303)
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return RedirectResponse(url="/error?message=資料庫錯誤", status_code=303)
    finally:
        # release the connection resources
        mycursor.close()
        mydb.close()
# Signout Endpoint
@app.get("/signout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
# Member Page
@app.get("/member")
async def success(request: Request):
    if not request.session.get("SIGNED-IN", False):
        return RedirectResponse(url="/", status_code=303)
    sql = "SELECT MEMBER.ID, MEMBER.NAME, MESSAGE.ID, MESSAGE.content FROM MESSAGE JOIN MEMBER ON MESSAGE.MEMBER_ID = MEMBER.ID ORDER BY MESSAGE.time DESC"
    try:
        mydb = connect_to_DB(db_host, db_user, db_password, db_name)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        object=[]
        for result in myresult:
            object.append(dict([("currentUser", result[0]==request.session["ID"]),("name",result[1]),("currentMessage", result[2]),("message",result[3])]))
        return templates.TemplateResponse("member.html", {"request": request, "account":request.session["NAME"], "messages":object})
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return RedirectResponse(url="/error?message=資料庫錯誤", status_code=303)
    finally:
        # release the connection resources
        mycursor.close()
        mydb.close()
# CreateMessage Endpoint
@app.post("/createMessage")
async def createMessage(request: Request, message:str=Form(...)):
    if not request.session.get("SIGNED-IN", False):
        return RedirectResponse(url="/", status_code=303)
    if message=="":
        return RedirectResponse(url="/error?message=Please enter message", status_code=303)
    sql = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
    val = (request.session["ID"],message)
    try:
        mydb = connect_to_DB(db_host, db_user, db_password, db_name)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        return RedirectResponse(url="/member", status_code=303)
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return RedirectResponse(url="/error?message=資料庫錯誤", status_code=303)
    finally:
        # release the connection resources
        mycursor.close()
        mydb.close()
# DeleteMessage Endpoint
@app.post("/deleteMessage")
async def deleteMessage(request: Request, deleteID:str=Form(...)):
    if not request.session.get("SIGNED-IN", False):
        return RedirectResponse(url="/", status_code=303)
    try:
        sql = "SELECT member_id FROM message WHERE id = %s"
        val = (deleteID,)
        mydb = connect_to_DB(db_host, db_user, db_password, db_name)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        if not myresult or myresult[0]!=request.session["ID"]:
            return RedirectResponse(url="/error?message=Permission denied", status_code=303)
        sql = "DELETE FROM message WHERE id = %s"
        val = (deleteID,)
        mycursor.execute(sql, val)
        mydb.commit()
        return RedirectResponse(url="/member", status_code=303)
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return RedirectResponse(url="/error?message=資料庫錯誤", status_code=303)
    finally:
        # release the connection resources
        mycursor.close()
        mydb.close()
# Member Query API
@app.get("/api/member")
async def searchAccount(request: Request, username:str = Query(...)):
    if not request.session.get("SIGNED-IN", False) or not username.strip():
            return JSONResponse(content={"data": None}, status_code=404)
    sql = "SELECT id, name, username FROM member WHERE username = %s"
    val = (username,)
    try:
        mydb = connect_to_DB(db_host, db_user, db_password, db_name)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        if not myresult:
            return JSONResponse(content={"data": None}, status_code=404)
        response_data={
                "id":myresult[0],
                "name":myresult[1],
                "username":myresult[2] 
                }
        return JSONResponse(content={"data": response_data}, status_code=200)
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return JSONResponse(content={"data": None}, status_code=500)
    finally:
        # release the connection resources
        mycursor.close()
        mydb.close()
# Name Update API
@app.patch("/api/member")
async def updateName(request: Request):
    body = await request.json()
    new_name = body.get("name") 
    if not request.session.get("SIGNED-IN", False) or not new_name.strip():
        return JSONResponse(content={"error": True}, status_code=404)
    sql = "UPDATE member SET name = %s WHERE id = %s"
    val = (new_name, request.session.get("ID", ""))
    try:
        mydb = connect_to_DB(db_host, db_user, db_password, db_name)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        request.session["NAME"]=new_name
        return JSONResponse(content={"ok": True}, status_code=200)
    except mysql.connector.Error as err:
        print(f"資料庫錯誤: {err}")
        return JSONResponse(content={"error": True}, status_code=500)
    finally:
        # release the connection resources
        mycursor.close()
        mydb.close()
    