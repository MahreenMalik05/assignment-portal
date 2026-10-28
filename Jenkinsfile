pipeline {
    agent any

    environment {
        REPO_NAME   = 'YourUsername/assignment-portal'   // apna GitHub username daalo
        BRANCH      = 'main'
        RECEIVER_URL = 'http://127.0.0.1:5001/report'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                bat 'python -m pytest -v --junitxml=ci-results.xml'
            }
        }

        stage('Build JSON Report and Send to Localhost') {
            steps {
                script {
                    // Commit SHA and Run ID
                    env.COMMIT_SHA = bat(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    env.RUN_ID = env.BUILD_NUMBER
                }
                bat '''
                    set REPO_NAME=%REPO_NAME%
                    set BRANCH=%BRANCH%
                    set COMMIT_SHA=%COMMIT_SHA%
                    set RUN_ID=%RUN_ID%
                    set RECEIVER_URL=%RECEIVER_URL%
                    python ci/build_report.py
                '''
            }
        }
    }

    post {
        always {
            // Report hamesha bhejo (pass ya fail dono)
            echo "Pipeline finished. Check receiver/test-report.json"
        }
        success {
            echo "All tests passed"
        }
        failure {
            echo "Some tests failed"
        }
    }
}