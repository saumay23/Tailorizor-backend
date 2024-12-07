# main.py
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from ClassTypes.type import HTMLData, ResumeType

from pyppeteer import launch
import io
import os
from google.ai.generativelanguage_v1beta.types import content

import google.generativeai as genai 
import json 


load_dotenv()


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


@app.post("/resume-tailor")
async def resume_tailor(resume:object,jd:str):
    try:
        
        AI_KEY=os.getenv('AI_KEY')

        if not AI_KEY:
            return {"error":"AI_KEY could not be parsed"}
        genai.configure(api_key=AI_KEY)

        schema = content.Schema(
    type = content.Type.OBJECT,
    enum = [],
    required = ["user_id", "resumeName", "personalDetails", "roleDetails", "Education", "WorkExperience", "Skills", "CustomField"],
    properties = {
      "user_id": content.Schema(
        type = content.Type.STRING,
      ),
      "resumeName": content.Schema(
        type = content.Type.STRING,
      ),
      "personalDetails": content.Schema(
        type = content.Type.OBJECT,
        enum = [],
        required = ["name", "email"],
        properties = {
          "name": content.Schema(
            type = content.Type.STRING,
          ),
          "email": content.Schema(
            type = content.Type.STRING,
          ),
          "contact_no": content.Schema(
            type = content.Type.STRING,
          ),
          "country": content.Schema(
            type = content.Type.STRING,
          ),
          "city": content.Schema(
            type = content.Type.STRING,
          ),
        },
      ),
      "roleDetails": content.Schema(
        type = content.Type.OBJECT,
        enum = [],
        required = ["role", "linkedIn"],
        properties = {
          "role": content.Schema(
            type = content.Type.STRING,
          ),
          "linkedIn": content.Schema(
            type = content.Type.STRING,
          ),
          "summary": content.Schema(
            type = content.Type.STRING,
          ),
        },
      ),
      "Education": content.Schema(
        type = content.Type.ARRAY,
        items = content.Schema(
          type = content.Type.OBJECT,
          enum = [],
          required = ["data"],
          properties = {
            "data": content.Schema(
              type = content.Type.ARRAY,
              items = content.Schema(
                type = content.Type.OBJECT,
                enum = [],
                required = ["Institute", "degree", "location", "description"],
                properties = {
                  "Institute": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "degree": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "start_date": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "end_date": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "location": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "description": content.Schema(
                    type = content.Type.STRING,
                  ),
                },
              ),
            ),
            "fieldName": content.Schema(
              type = content.Type.STRING,
            ),
          },
        ),
      ),
      "WorkExperience": content.Schema(
        type = content.Type.ARRAY,
        items = content.Schema(
          type = content.Type.OBJECT,
          enum = [],
          required = ["data"],
          properties = {
            "data": content.Schema(
              type = content.Type.ARRAY,
              items = content.Schema(
                type = content.Type.OBJECT,
                enum = [],
                required = ["company_name", "role", "description", "location"],
                properties = {
                  "company_name": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "start_date": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "end_date": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "role": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "description": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "location": content.Schema(
                    type = content.Type.STRING,
                  ),
                },
              ),
            ),
            "fieldName": content.Schema(
              type = content.Type.STRING,
            ),
          },
        ),
      ),
      "Skills": content.Schema(
        type = content.Type.OBJECT,
        enum = [],
        required = ["data"],
        properties = {
          "fieldName": content.Schema(
            type = content.Type.STRING,
          ),
          "data": content.Schema(
            type = content.Type.STRING,
          ),
        },
      ),
      "CustomField": content.Schema(
        type = content.Type.ARRAY,
        items = content.Schema(
          type = content.Type.OBJECT,
          properties = {
            "fieldName": content.Schema(
              type = content.Type.STRING,
            ),
            "fields": content.Schema(
              type = content.Type.ARRAY,
              items = content.Schema(
                type = content.Type.OBJECT,
                properties = {
                  "header": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "subHeader": content.Schema(
                    type = content.Type.STRING,
                  ),
                  "description": content.Schema(
                    type = content.Type.STRING,
                  ),
                },
              ),
            ),
          },
        ),
      ),
    },
  ),        
        generationConfig ={
          "temperature": 1,
          "responseMimeType":"application/json",
          "responseSchema":schema,
        }
        prompt = f'''
                     You are an AI assistant tasked with tailoring resumes for job applications. 
      **Objective:**
      1. Extract key skills, qualifications, and relevant keywords from the provided job description.
      2. Incorporate these keywords into the given resume JSON while maintaining its structure and format.
      3. Modify specific sections like "Education," "WorkExperience," "Skills," and "CustomField" to align with the job description's requirements.
      
      **Instructions:**
      - Update the "resumeName" field to include the company or role name if mentioned in the job description.
      - Ensure the "WorkExperience" and "Education" descriptions reflect the job description’s priorities.
      - Do not introduce extraneous information; only refine or rephrase the existing content to better match the job description.
      - Preserve the JSON schema provided below and return a complete JSON object with the modified resume.
      
      **Job Description:** 
      {jd}
      
      **Resume JSON:** 
      {json.dumps(resume)}
      
      **Expected Output:**
      Return the modified resume as a JSON object adhering to the schema, with all updates seamlessly integrated.

'''
        model = genai.GenerativeModel( model_name="gemini-1.5-pro",generation_config=generationConfig)

        chatSession= model.start_chat(history=[])
        modifiedResume =await chatSession.send_message(prompt)
        if not modifiedResume:
            return {"error":"Modified Resume did not generated"}
        
        return modifiedResume

    except Exception as e:
        return {"error":f"Failed to fetch AI results : {str(e)}"}

