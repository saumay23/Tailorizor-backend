# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from ClassTypes.type import HTMLData
from pyppeteer import launch
import io


app = FastAPI()

# Allow CORS for frontend running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://tailorizor.vercel.app/"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)



async def generate_pdf_from_html(html: str) -> bytes:
    executable_path = '/usr/bin/google-chrome-stable'
    browser = await launch(headless=True, args=['--no-sandbox'],executablePath=executable_path)
    page = await browser.newPage()
    await page.setContent(html)
    pdf_buffer = await page.pdf(format='A4',margin={
            'top': '0.7in',
            'right': '0.5in',
            'bottom': '0.5in',
            'left': '0.5in'
        })
    await browser.close()
    return pdf_buffer

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/generate-pdf")
async def generate_pdf(data: HTMLData):
    try:
        pdf_buffer = await generate_pdf_from_html(data.html)
        return StreamingResponse(
            io.BytesIO(pdf_buffer),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=document.pdf"}
        )
    except Exception as e:
        return {"error": f"Failed to generate PDF: {str(e)}"}