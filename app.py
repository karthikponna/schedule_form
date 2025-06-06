import os
from datetime import datetime
from urllib.parse import quote_plus 
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from ai_model import classify_business
from sheets import add_contact, add_user_input_status
from fastapi.staticfiles import StaticFiles     

app = FastAPI()
BASE_DIR = os.path.dirname(__file__)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def post_about(
    request: Request,
    about: str = Form(...),
    previous: str = Form(None),
):
    
    if previous:  # if this is a follow-up (second) attempt
        combined_input = (
            f"First user message: {previous}\n"
            f"Second user message: {about}\n"
            "Note: This is a follow-up. Do not request more info again—make a final classification."
        )  
        result = classify_business(combined_input)  
        status = result.get("status")
    else:
        result = classify_business(about)
        status = result.get("status")
    now = datetime.now().isoformat()
    add_user_input_status({
        "Date/Time": now,
        "User Input": about,
        "Status": status
    })
        
    if status == "qualified":
        
        return templates.TemplateResponse("qualified.html", {"request": request})
    
    elif status == "more info":
        
        return templates.TemplateResponse("about.html", {
            "request": request,
            "warning": result.get("message"),
            "about": about
        })
    elif status == "spam":
        safe_about = quote_plus(about)
        safe_status = quote_plus(status)
        return RedirectResponse(
            url=f"/contact?about={safe_about}&status={safe_status}",
            status_code=302
        )
    
    elif status == "not qualified":
        
        return RedirectResponse(
            url="https://app.secondbrainlabs.com/signup",
            status_code=302,
        )
    
    else:
        return RedirectResponse(url="/contact", status_code=302)


@app.get("/contact", response_class=HTMLResponse)
async def get_contact(request: Request):
    about = request.query_params.get("about")
    status = request.query_params.get("status")
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "about": about,
        "status": status
    })


@app.post("/contact")
async def post_contact(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    linkedin: str = Form(...),
    about: str = Form(None),
    status: str = Form(None),
):
    now = datetime.now().isoformat()
    add_contact({
        "Date/Time": now,
        "Name": name,
        "Phone Number": phone,
        "Email": email,
        "Linkedin Profile": linkedin
    })
    return RedirectResponse(url="/thankyou", status_code=302)


@app.get("/thankyou", response_class=HTMLResponse)
async def thank_you(request: Request):
    return templates.TemplateResponse("thankyou.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8011, reload=True)

# uvicorn app:app --host 0.0.0.0 --port 8000
