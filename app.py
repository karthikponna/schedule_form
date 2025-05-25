from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# If you like, you can add a POST endpoint to handle the form:
#
# @app.post("/", response_class=HTMLResponse)
# async def submit_about(request: Request):
#     form = await request.form()
#     about_text = form.get("about")
#     return templates.TemplateResponse("about.html", {
#         "request": request,
#         "submitted": about_text
#     })
#
# and then display `{{ submitted }}` somewhere in the template.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
