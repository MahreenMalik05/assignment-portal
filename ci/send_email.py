import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def main():
    with open("report.json", encoding="utf-8") as f:
        report = json.load(f)

    status = report.get("overall_status", "unknown").upper()
    summary = report.get("summary", {})
    commit = report.get("commit_sha", "unknown")[:7]
    run_id = report.get("run_id", "")

    subject = f"[Assignment Portal CI] {status} - {commit}"
    body = f"""CI Test Report

Repository : {report.get('repository')}
Branch     : {report.get('branch')}
Commit     : {report.get('commit_sha')}
Run ID     : {run_id}
Timestamp  : {report.get('timestamp')}

Overall Status : {status}
Total  : {summary.get('total')}
Passed : {summary.get('passed')}
Failed : {summary.get('failed')}

Individual Tests:
"""
    for t in report.get("tests", []):
        line = f"- {t['name']}: {t['result']}"
        if t.get("failure_message"):
            line += f" → {t['failure_message']}"
        body += line + "\n"

    msg = MIMEMultipart()
    msg["From"] = os.environ["EMAIL_USERNAME"]
    msg["To"] = os.environ["EMAIL_TO"]
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach JSON
    part = MIMEBase("application", "octet-stream")
    part.set_payload(json.dumps(report, indent=2).encode())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", 'attachment; filename="test-report.json"')
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ["EMAIL_USERNAME"], os.environ["EMAIL_PASSWORD"])
        server.send_message(msg)
    print("Email sent successfully")

if __name__ == "__main__":
    main()
