from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from ai_model import classify_business   
from sheets import add_contact          

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def post_about(
    request: Request,
    about: str = Form(...)
):
    
    result = classify_business(about)
    status = result.get("status")       
    if status == "qualified":
        
        return templates.TemplateResponse("about.html", {
            "request": request,
            "qualified_link": "https://calendar.app.google/h7YFgGZbysv83Bkc7"
        })
    
    elif status == "more info":
        
        return templates.TemplateResponse("about.html", {
            "request": request,
            "warning": "More information is required. Please tell us both what your business is **and** the scale you’re operating at."
        })
    else:
        
        response = RedirectResponse(url="/contact", status_code=302)
        return response


@app.get("/contact", response_class=HTMLResponse)
async def get_contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.post("/contact")
async def post_contact(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    linkedin: str = Form(...),
):
    # store in Google Sheets
    add_contact({
        "name": name,
        "phone": phone,
        "email": email,
        "linkedin": linkedin
    })
    return RedirectResponse(url="/thankyou", status_code=302)


@app.get("/thankyou", response_class=HTMLResponse)
async def thank_you(request: Request):
    return templates.TemplateResponse("thankyou.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8011, reload=True)

# uvicorn app:app --host 0.0.0.0 --port 8000
