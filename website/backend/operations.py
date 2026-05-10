import os
import io
import time
import json
import base64
import logging
import uuid
import secrets
from datetime import datetime

import openai
from openai import OpenAI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

import sendgrid
from sendgrid import SendGridAPIClient
from twilio.rest import Client as TwilioClient
from sendgrid.helpers.mail import (
    Mail, ReplyTo, Attachment, FileContent, FileName,
    FileType, Disposition
)

from website.backend.config import RESUME_FORMATTING_PROMPT_1, NEW_RESUME_FORMATTING_PROMPT_1_ZH, RESUME_FORMATTING_PROMPT_2
from website.backend.generic import (
    simplify_email_object, extract_text, fix_response, create_local_docx_document, create_local_docx_document_zh, detect_language
)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
print(os.path.join(os.path.dirname(__file__), ".env"))


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

openai.api_key = OPENAI_API_KEY
openai_client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)


def get_llm_info(transcript_json):
    if not transcript_json or transcript_json == "[]" or transcript_json == "None":
        return "N/A", "N/A"

    try:
        messages = json.loads(transcript_json)
        transcript_text = ""
        for m in messages:
            role = m.get('role', 'unknown')
            content = m.get('content', '')
            transcript_text += f"{role}: {content}\n"

        if not transcript_text.strip():
            return "N/A", "N/A"

        prompt = f"""You are summarizing a voice call handled by an AI receptionist on behalf of a business.

Transcript:
{transcript_text}

Extract the following and return as JSON:

1. "full_name": The caller's full name if they stated it, otherwise "N/A".

2. "summary": A detailed 3–5 sentence summary of the interaction. Include ALL of the following that were mentioned:
   - Why the caller called and what they were looking for
   - The specific service, treatment, or inquiry (e.g. haircut type, legal matter, medical question, booking request)
   - The name of any staff member, provider, lawyer, barber, doctor, etc. requested or assigned
   - Any date, time, or scheduling details (e.g. "today at 6 PM", "Thursday at 2 PM")
   - Any pricing or deposit information discussed
   - The outcome of the call (e.g. appointment booked, information provided, callback requested, issue unresolved)
   - Any next steps or follow-up actions mentioned

Write the summary in plain past-tense prose as if briefing a manager who was not on the call. Be specific - do not omit names, times, or services that were mentioned.

Return only valid JSON:
{{
    "full_name": "...",
    "summary": "..."
}}"""

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        full_name = result.get("full_name", "N/A")
        summary = result.get("summary", "N/A")

        try:
            #### Fix bug for one account specifically
            import re
            summary = re.sub("Jeffrey Horace", "Jeffrey Horrick", summary)
            summary = re.sub("Jeffrey Horak", "Jeffrey Horrick", summary)
            summary = re.sub("Jeffrey Horaquez", "Jeffrey Horrick", summary)
            ####
        except:
            pass
        return full_name, summary
        #return result.get("full_name", "N/A"), result.get("summary", "N/A")
    except Exception as e:
        logger.info(f"Error in LLM extraction: {e}")
        return "N/A", "N/A"


def ask_GPT(query: str, model="gpt-4o") -> str:
    ans = None
    try:
        response = openai_client.chat.completions.create(
            model=model,
            max_completion_tokens=12000,
            messages=[{"role": "user", "content": query}]
        )
        ans = response.choices[0].message.content.strip()
    except Exception as e:
        logger.info("\nError Occured when making request to OpenAI:")
        logger.info(e)
        logger.info("Sleeping for 10 seconds due to error")
        time.sleep(10)
    return ans


def send_email(to_email, subject, html_content):

    def __send_email(to_email, subject, html_content):
        message = Mail(
            from_email="agent@standardhc.hk",
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        message.reply_to = ReplyTo("xingyang604302@gmail.com", "Xing Yang")

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Status code: {response.status_code}")
        return response.status_code
    
    # Example execution
    status_code = __send_email(
        to_email=to_email,
        subject=subject,
        html_content=html_content
    )

    return status_code


def send_sms(from_number: str, to_number: str, body: str) -> str:
    client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(body=body, from_=from_number, to=to_number)
    return message.sid


def send_email_with_attatchment(to_emails: str, subject: str, html_content: str, filename: str, filepath: list[str] = [], from_email: str = "agent@standardhc.hk", buffer=None):
    # sends email with a file attatchment using sendgrid
    # filepath: use list of folder names, don't include the "/"'s 
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

    buffer.seek(0)
    file_data = base64.b64encode(buffer.read()).decode()
        
    attachment = Attachment(
        FileContent(file_data),
        FileName(filename),
        FileType("application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        Disposition("attachment")
    )

    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content
    )
    message.attachment = attachment

    response = sg.send(message)
    return response


def format_email_with_ai_and_send(EMAIL_OBJECT: dict, extracted_text: str):

    lang = detect_language(extracted_text)

    if lang == "zh":
        prompt_1 = NEW_RESUME_FORMATTING_PROMPT_1_ZH.replace("{{{INPUT}}}", extracted_text)
        response_1 = ask_GPT(prompt_1)
        print(f"\n\n------------->\nresponse_1 generated:\n{response_1[:min(len(response_1), 1000)]}\n")
        buffer, docx_filename = create_local_docx_document_zh(EMAIL_OBJECT["filename"], response_1)
    else:
        prompt_1 = RESUME_FORMATTING_PROMPT_1.replace("{{{INPUT}}}", extracted_text)
        response_1 = ask_GPT(prompt_1)
        print(f"\n\n------------->\nresponse_1 generated:\n{response_1[:min(len(response_1), 1000)]}\n")
        fixed_resume = fix_response(response_1)
        print(f"\n\n--------------->\nfixed_resume for ({EMAIL_OBJECT['filename']}\n{fixed_resume[:min(len(fixed_resume), 1000)]}\n")
        buffer, docx_filename = create_local_docx_document(EMAIL_OBJECT["filename"], fixed_resume)

    print(f"\n\n--------------->\nlocal_docx_filename:\n{docx_filename}\n")

    send_to_email = json.loads(EMAIL_OBJECT["envelope"])["from"]
    subject = f'Formatted Resume: {EMAIL_OBJECT["filename"]}'
    email_html_content = f"Attatchment for {EMAIL_OBJECT['filename']}. (response from agent@standardhc.hk)"

    status_code = send_email_with_attatchment(
        to_emails=send_to_email,
        subject=subject,
        html_content=email_html_content,
        filename=docx_filename,
        filepath=[],
        from_email="agent@standardhc.hk",
        buffer=buffer
    )
    print("Send email status code:", status_code)

    return {"status": "success"}


def handle_standardhc_workflow(filename):

    obj = None
    
    with open(filename, "r", encoding="utf-8") as f:
            content = f.readlines()
            content = "".join(content)
            obj = json.loads(content)
    
    obj = simplify_email_object(obj)
    print("obj keys:", list(obj.keys()))

    EMAIL_OBJECT = obj

    extracted_text = extract_text(obj["filename"], obj["content"], obj["from_email"])
    print(f"extracted_text:\n{extracted_text}")

    format_email_with_ai_and_send(EMAIL_OBJECT, extracted_text)
