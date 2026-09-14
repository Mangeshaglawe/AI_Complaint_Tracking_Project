extraction_prompt = '''
Extract the following fields from the provided customer complaint document text and return a strict JSON object with these keys exactly:

customer_name, email, phone, complaint_category, issue_description, resolution_provided, is_complaint, escalation_required, supporting_document, overall_status

Rules:
- Only output valid JSON (no extra commentary).
- Use true/false for boolean fields.
- If a field is not present, use null for strings and false for booleans.

Document Text:
"""
{text}
"""

Return the JSON now.
'''

email_prompt = '''
Using the extracted fields, write a professional customer response email. Be concise, address the customer by name when available, summarize the issue, mention the resolution/status, and avoid inventing facts not present in the data.

Data:
{customer_name}
{email}
{phone}
Category: {complaint_category}
Issue: {issue_description}
Resolution: {resolution_provided}
Status: {overall_status}

Write the email body only.
'''

summary_prompt = '''
Create an internal case summary for management. Include: Case overview, Key issue, Action taken, Current status, Recommended next action.

Data:
{customer_name}
{email}
{phone}
Category: {complaint_category}
Issue: {issue_description}
Resolution: {resolution_provided}
Status: {overall_status}

Return a short, bulleted summary.
'''
