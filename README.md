# Assignment Submission Portal

Flask web app where students submit assignment links, with automated tests and Jenkins CI that reports results to a local receiver.

## Run the application
pip install -r requirements.txt
python app.py
Open http://127.0.0.1:5000

## Run the tests
python -m pytest -v
## Start the local report receiver
python receiver/receiver.py
The receiver listens on http://127.0.0.1:5001/report and saves each report to `receiver/test-report.json`.

## CI pipeline

Jenkins Pipeline (Jenkinsfile) runs on every push / manual trigger.
It installs dependencies, runs pytest, builds a JSON report and POSTs it to the local receiver
(also when tests fail).