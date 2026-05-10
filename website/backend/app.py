import os
import json
import uvicorn
from fastapi import FastAPI, Request, HTTPException
try:
    from website.backend.operations import logger, handle_standardhc_workflow
    from website.backend.generic import get_form_dict
except:
    print("import style 2")
    from operations import logger, handle_standardhc_workflow
    from generic import get_form_dict


app = FastAPI()

@app.post("/inbound-email/")
async def shc_inbound_email(request: Request):
    logger.info("SHC: First line of code")
    try:
        logger.info(f"DEBUG: First line of SHC /inbound-email/ triggered")
        try:
            form = await request.form()
            logger.info(f"!!! success request.form():")
        except:
            raise HTTPException(status_code=500, detail="`form` could not be loaded.")    

        keys = list(form.keys())
        logger.info(f"keys: {keys}")

        try:
            form_json = get_form_dict(form)
            # Use a separate dump file for SHC to avoid conflict
            filename = "shc_form_dump.json"
            with open(filename, "w+", encoding="utf-8") as f:
                f.write(form_json)
            handle_standardhc_workflow(filename)
        except Exception as e:
            print(f"Exception: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error in handle_standardhc_workflow: {str(e)}")

        return {"message": "/inbound-email/: SHC main try block finished without triggering exception"}
        
    except Exception as e:
        logger.info("Reached exception in SHC")
        logger.info(f"ERROR in SHC /inbound-email/: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping/")
def ping():
    return {"message": "Reached"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
