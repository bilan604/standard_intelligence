from website.backend.operations import handle_standardhc_workflow


ret = handle_standardhc_workflow("form_dump.json")
print("ret:", ret)
