import re
import io
import json
import logging
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from email import policy
from email.parser import Parser
import pdfplumber
import fitz  # pymupdf


logger = logging.getLogger(__name__)


def simplify_email_object(obj):

    # returns a python dictionary where all the keys are strings,
    # and all the values are strings except for the key 'content',
    # which as a value of type 'bytes'

    def __parse_email_to_dict(email_raw: str):

        # Parse raw MIME email string
        msg = Parser(policy=policy.default).parsestr(email_raw)

        result = {
            "headers": dict(msg.items()),  # dict[str, str]
            "subject": msg.get("subject"),
            "from": msg.get("from"),
            "to": msg.get("to"),
            "text": None,
            "html": None,
            "attachments": []
        }

        # Walk through MIME parts
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))

            # Plain text body
            if content_type == "text/plain" and "attachment" not in content_disposition:
                result["text"] = part.get_content()

            # HTML body
            elif content_type == "text/html" and "attachment" not in content_disposition:
                result["html"] = part.get_content()

            # Attachments
            elif "attachment" in content_disposition:
                result["attachments"].append({
                    "filename": part.get_filename(),
                    "content_type": content_type,
                    "content": part.get_payload(decode=True)  # bytes
                })

        return result
    

    if not obj:
        return None

    email = None
    for k,v in obj.items():
        if "email" == k:
            email = __parse_email_to_dict(v)

    if not email:
        return None

    keep = ["to", "from", "subject", "sender_ip", "envelope"]
    obj = {k:v for k,v in obj.items() if k in keep}

    obj["email_text"] = email["text"]
    obj["email_html"] = email["html"]
    obj["attachments"] = email["attachments"]

    for k,v in obj.items():
        if type(v) == str:
            obj[k] = v.strip()

    att = None
    for k,v in obj.items():
        if k != "attachments":
            pass
        else:
            if len(v) >= 1:
                for attachment in v:
                    att = attachment
                    break
    
    # attachment_keys = ["filename", "content_type", "content"] # The ones I want to keep
    if not att:
        att = {}
        att["filename"] = ""
        att["content_type"] = ""
        att["content"] = ""

    else:
        obj["filename"] = att["filename"]
        obj["content_type"] = att["content_type"]
        obj["content"] = att["content"]

    from_name = ""
    from_email = ""

    try:
        obj["from_name"] = from_name
        obj["from_email"] = json.loads(obj["envelope"])["from"]
    except Exception as e:
        print(e)

    if not obj["from_email"]:
        try:
            from_email = "<".split(obj["frmo"][1].split(">")[0].strip())
            obj["from_email"] = from_email
        except Exception as e:
            print(e)

    return obj


def extract_text(filename: str, file_bytes: bytes, email_from: str) -> str:

    ext = filename.rsplit(".", 1)[-1].lower()

    print("ext", ext)
    # ONLY .txt
    if ext == 'txt':
        return file_bytes.decode("utf-8", errors="replace")

    # and .pdf supported
    if ext != "pdf":
        # Only doing PDFs at the moment
        return ""
    
    extracted_text = None
    excepted = False
    error_message = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        extracted_text = "\n".join(
            page.get_text("text") or "\n[MISSING_PAGE]\n" for page in doc
        )
    except Exception as e:
        excepted = True
        error_message += str(e) + ". | \n"


    if (extracted_text == None) or (excepted == True) or ("[MISSING_PAGE]" in extracted_text):
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                extracted_text = "\n".join(
                    page.extract_text() or "\n[MISSING_PAGE]\n" for page in pdf.pages
                )
        except Exception as e:
            excepted = True
            error_message += str(e) + ". | \n"


    if extracted_text and ("[MISSING_PAGE]" in extracted_text):
        return ""
        
    if (extracted_text == None):
        return ""
           
    return extracted_text


def detect_language(text: str) -> str:
    non_ws = [c for c in text if not c.isspace()]
    if not non_ws:
        return "en"
    cjk = sum(1 for c in non_ws if '\u4e00' <= c <= '\u9fff')
    return "zh" if (cjk / len(non_ws)) > 0.10 else "en"


def fix_response(resp: str) -> str:
    lines = resp.split("\n")
    lines = [line for line in lines if line.strip() != "```"]
    new_lines = []
    for i in range(len(lines)):
        date = False
        if lines[i].find("- ") == 0:
            temp = "- ".join(lines[i].split("- ")[1:])
            if temp and temp[0] in "0123456789" and temp[1] in "0123456789":
                if " | " in temp:
                    datee = temp.split(" | ")[0].strip()
                    if " - " in datee:                        
                        date = True
                

        if date == True:
            fixed = "- ".join(lines[i].split("- ")[1:])
            if fixed and fixed[0] == " ":
                fixed = fixed[1:]
            if fixed and fixed[0] == " ":
                fixed = fixed[1:]
            new_lines.append(fixed)
        else:
            if lines[i].find(" | ") == 0:
                new_lines.append(" | ".join(lines[i].split(" | ")[1:]))
            elif lines[i].find(" ") == 0:
                space_count = 0
                for j in range(len(lines[i])):
                    if lines[i][j] != " ":
                        break
                    else:
                        space_count += 1

                if space_count >= 4:
                    #intentional spaces
                    new_lines.append(lines[i])
                else:

                    #new_lines.append(lines[i][space_count:])
                    new_lines.append(lines[i]) ####

            else:
                new_lines.append(lines[i])


    return "\n".join(new_lines)


def create_local_docx_document(filename, extracted_text):
    
        
    doc = Document()

    def edit_distance(word1: str, word2: str) -> int:
        word1 = "-" + word1
        word2 = "-" + word2
        m = len(word1)
        n = len(word2)

        # Initialize the dp table
        dp = [[0] * (n) for _ in range(m)]

        # Base cases
        for i in range(m):
            dp[i][0] = i
        for j in range(n):
            dp[0][j] = j

        # Fill in the dp table
        for i in range(1, m):
            for j in range(1, n):
                if word1[i] == word2[j]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j-1], dp[i][j-1], dp[i-1][j])
        return dp[m-1][n-1]


    def __is_section_title(line):
        words = line.strip().split(" ")
        words = [word.strip() for word in  words if word.strip()]
        if len(words) > 3:
            return False
        if len(words) < 1:
            return False
        line = " ".join(words)
        titles = ["Position Recommended:", "Personal Information:", "Educational Background:", "Education Background:", "Personal Information:", "Assessment on Candidate:", "Professional Experience:", "Compensation:"]
        
        for title in titles:
            if line == title:
                return True
        
        return False


    for line in extracted_text.split("\n"):
        if line.strip().lower() == "end of profile":
            end_paragraph = doc.add_paragraph()
            end_run = end_paragraph.add_run(line)
            end_run.font.name = "Arial"
            end_run.font.size = Pt(12)
            end_run.bold = True
            end_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            break

        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        run = paragraph.add_run(line)
        run.font.name = "Arial"
        if __is_section_title(line):
            run.font.size = Pt(12)
            run.bold = True
            run.underline = True
        else:
            run.font.size = Pt(10)
            if line.strip().lower() in ["current salary:", "salary expectation:"]:
                run.bold = False
            else:
                run.bold = not line.startswith("- ")

    docx_filename = ".".join(filename.split(".")[:-1]) + ".docx"
    docx_filename = re.sub(" ", "_", docx_filename)
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer, docx_filename


def create_local_docx_document_zh(filename, text):
    doc = Document()

    for line in text.split("\n"):
        is_bold = "[BOLD]" in line
        is_underline = "[UNDERLINE]" in line
        clean_line = line.replace("[BOLD]", "").replace("[UNDERLINE]", "")

        if clean_line.strip().lower() == "end of profile":
            end_paragraph = doc.add_paragraph()
            end_run = end_paragraph.add_run(clean_line.strip())
            end_run.font.name = "Arial"
            end_run.font.size = Pt(12)
            end_run.bold = True
            end_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            break

        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        run = paragraph.add_run(clean_line)
        run.font.name = "Arial"
        run.font.size = Pt(10)
        run.bold = is_bold
        run.underline = is_underline

    docx_filename = ".".join(filename.split(".")[:-1]) + ".docx"
    docx_filename = re.sub(" ", "_", docx_filename)
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer, docx_filename


def get_form_dict(form):
    """
    Convert FastAPI / Starlette FormData → JSON string
    """

    form_dict = {}

    for key in form.keys():
        values = form.getlist(key)

        if len(values) == 1:
            value = values[0]
        else:
            value = values

        if hasattr(value, "filename"):
            value = {
                "filename": value.filename,
                "content_type": value.content_type,
            }

        elif isinstance(value, list):
            new_list = []

            for v in value:
                if hasattr(v, "filename"):
                    new_list.append({
                        "filename": v.filename,
                        "content_type": v.content_type,
                    })
                else:
                    new_list.append(v)

            value = new_list

        form_dict[key] = value

    form_json = json.dumps(form_dict, indent=2)

    return form_json
