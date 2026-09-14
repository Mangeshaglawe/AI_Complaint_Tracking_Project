# AI Customer Complaint & Case Processing System

This project demonstrates a batch-oriented GenAI document processing workflow.

## CLI usage

1. Set `OPENAI_API_KEY` in your environment.
2. Place documents under the `data/` folder (supported: `.txt`, `.pdf`, `.docx`).
3. Run the processor:

```bash
python -m src.main
```

## Streamlit dashboard

Launch the real-time dashboard to monitor requests, results analytics, and pipeline execution:

```bash
streamlit run app.py
```

The dashboard shows:
- live batch status
- processed vs total documents
- per-file result tables
- error tracking
- analytics summary of success/error counts
- generated output file paths

Outputs are written to `output/` with structured JSON, customer emails, case summaries, and `final_report.csv`.


"""
Build a GenAI-powered document
processing workflow that automatically processes a collection of business
documents and performs multiple AI-powered tasks on each document.

The objective is to demonstrate your
ability to build a batch-oriented LLM workflow with structured outputs,
parallel/sequential processing and automated content generation.

[Suggested Business
Scenario]()

Build an AI Customer Complaint & Case Processing System.

The system receives customer complaint documents from a local data/ folder and processes each document automatically.

Example input documents may contain:

·
Customer name

·
Contact information

·
Complaint description

·
Product/service involved

·
Issue details

·
Resolution provided

·
Escalation information

·
Supporting information

The documents can be .txt, .pdf or .docx files.

Functional Requirements
1. Document Ingestion
The application should:

·
Read documents from a
designated data/ folder.

·
Support at least two
document formats.

·
Process multiple documents in a
batch.

·
Extract the textual content
from each document.

·
Handle basic file-level errors
gracefully.

[2. Structured
Information Extraction]()

For every document, the LLM should extract structured information
such as:

·
Customer Name

·
Email

·
Phone Number

·
Complaint Category

·
Issue Description

·
Resolution Provided

·
Complaint: Yes/No

·
Escalation Required: Yes/No

·
Supporting Document Available:
Yes/No

·
Overall Case Status

The output should follow a defined schema using Pydantic or
another structured-output mechanism.

The application should not simply save the raw LLM response.

[3. Automated
Response Generation]()

For each complaint, generate a professional customer response
email based on the extracted information.

The email should:

·
Address the customer
appropriately.

·
Summarize the issue.

·
Mention the resolution/status.

·
Maintain a professional tone.

·
Avoid inventing information
that is not present in the source document.

4. Management Case Summary
For each document, generate a concise internal case summary
containing:

·
Case overview

·
Key issue

·
Action taken

·
Current status

·
Recommended next action

5. Workflow Design
The workflow should execute the three AI tasks:

Document → Structured Extraction

Document/Extracted Data → Customer Email

Document/Extracted Data → Internal Case Summary

The learner may implement the workflow sequentially or use parallel
execution where appropriate.

The implementation should clearly demonstrate workflow
orchestration rather than placing the entire application inside one large
LLM call.

6. Batch Processing
The application should be capable of processing multiple documents
automatically.

For example:

data/

├── complaint_001.pdf

├── complaint_002.pdf

├── complaint_003.txt

├── complaint_004.docx

└── complaint_005.pdf

The system should process all eligible files and produce
corresponding outputs.

Expected Output
A recommended output structure:

output/

├── structured_data/

├── customer_emails/

├── case_summaries/

└── final_report.csv

The final report should provide a consolidated view of the processed
documents.

Expected Technical Skills Demonstrated
The project should demonstrate:

·
Python

·
LLM API integration

·
Prompt Engineering

·
Structured Outputs

·
Pydantic

·
Batch Processing

·
Sequential/Parallel Workflow

·
Error Handling

·
Modular Code

·
File Processing

·
Git/GitHub

·
Basic loggingBuild a GenAI-powered document
processing workflow that automatically processes a collection of business
documents and performs multiple AI-powered tasks on each document.

The objective is to demonstrate your
ability to build a batch-oriented LLM workflow with structured outputs,
parallel/sequential processing and automated content generation.

[Suggested Business
Scenario]()

Build an AI Customer Complaint & Case Processing System.

The system receives customer complaint documents from a local data/ folder and processes each document automatically.

Example input documents may contain:

·
Customer name

·
Contact information

·
Complaint description

·
Product/service involved

·
Issue details

·
Resolution provided

·
Escalation information

·
Supporting information

The documents can be .txt, .pdf or .docx files.

Functional Requirements
1. Document Ingestion
The application should:

·
Read documents from a
designated data/ folder.

·
Support at least two
document formats.

·
Process multiple documents in a
batch.

·
Extract the textual content
from each document.

·
Handle basic file-level errors
gracefully.

[2. Structured
Information Extraction]()

For every document, the LLM should extract structured information
such as:

·
Customer Name

·
Email

·
Phone Number

·
Complaint Category

·
Issue Description

·
Resolution Provided

·
Complaint: Yes/No

·
Escalation Required: Yes/No

·
Supporting Document Available:
Yes/No

·
Overall Case Status

The output should follow a defined schema using Pydantic or
another structured-output mechanism.

The application should not simply save the raw LLM response.

[3. Automated
Response Generation]()

For each complaint, generate a professional customer response
email based on the extracted information.

The email should:

·
Address the customer
appropriately.

·
Summarize the issue.

·
Mention the resolution/status.

·
Maintain a professional tone.

·
Avoid inventing information
that is not present in the source document.

4. Management Case Summary
For each document, generate a concise internal case summary
containing:

·
Case overview

·
Key issue

·
Action taken

·
Current status

·
Recommended next action

5. Workflow Design
The workflow should execute the three AI tasks:

Document → Structured Extraction

Document/Extracted Data → Customer Email

Document/Extracted Data → Internal Case Summary

The learner may implement the workflow sequentially or use parallel
execution where appropriate.

The implementation should clearly demonstrate workflow
orchestration rather than placing the entire application inside one large
LLM call.

6. Batch Processing
The application should be capable of processing multiple documents
automatically.

For example:

data/

├── complaint_001.pdf

├── complaint_002.pdf

├── complaint_003.txt

├── complaint_004.docx

└── complaint_005.pdf

The system should process all eligible files and produce
corresponding outputs.

Expected Output
A recommended output structure:

output/

├── structured_data/

├── customer_emails/

├── case_summaries/

└── final_report.csv

The final report should provide a consolidated view of the processed
documents.

Expected Technical Skills Demonstrated
The project should demonstrate:

·
Python

·
LLM API integration

·
Prompt Engineering

·
Structured Outputs

·
Pydantic

·
Batch Processing

·
Sequential/Parallel Workflow

·
Error Handling

·
Modular Code

·
File Processing

·
Git/GitHub

·
Basic logging
"""