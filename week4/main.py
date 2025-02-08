from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

app=FastAPI()
templates = Jinja2Templates(directory="templates")
# session
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
# 提供靜態文件
app.mount("/static", StaticFiles(directory="static"), name="static")
# HomePage
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
# Verification Endpoint
@app.post("/signin")
async def login(request: Request, account:str=Form(...),password:str=Form(...)):
    if account == "test" and password == "test":
        request.session["SIGNED-IN"] = True
        return RedirectResponse(url="/member", status_code=303)
    elif account == "" or password == "":
        return RedirectResponse(url="/error?message=Please enter username and password", status_code=303)
    else:
        return RedirectResponse(url="/error?message=Username or password is not correct", status_code=303)
# Success Page
@app.get("/member")
async def success(request: Request):
    if not request.session["SIGNED-IN"]:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("member.html", {"request": request})
# Error Page
@app.get("/error")
async def error(request: Request):
    message = request.query_params.get("message") 
    return templates.TemplateResponse("error.html", {"request": request, "message":message})
# Signout Endpoint
@app.get("/signout")
async def logout(request: Request):
    request.session["SIGNED-IN"]=False
    return RedirectResponse(url="/", status_code=303)
# Squared Number Page
@app.get("/square/{number}")
async def math(request: Request,number:int):
    message=number**2
    return templates.TemplateResponse("number.html", {"request": request, "message":message})