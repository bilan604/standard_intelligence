from website.backend.app import handle_standardhc_workflow


ret = handle_standardhc_workflow("form_dump.json")
print("ret:", ret)
