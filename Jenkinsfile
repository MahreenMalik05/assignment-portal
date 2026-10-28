pipeline {
    agent any

    environment {
        REPO_NAME    = 'YourUsername/assignment-portal'   // apna username daalo
        BRANCH       = 'main'
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
                // Tests fail hone pe bhi pipeline continue kare
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    bat 'python -m pytest -v --junitxml=ci-results.xml'
                }
            }
        }

        stage('Build JSON Report and Send to Localhost') {
            steps {
                script {
                    env.COMMIT_SHA = bat(
                        script: '@echo off & git rev-parse HEAD',
                        returnStdout: true
                    ).trim()
                    env.RUN_ID = "${env.BUILD_NUMBER}"
                }

                // Environment variables set karke report bhejo
                bat """
                    set REPO_NAME=${env.REPO_NAME}
                    set BRANCH=${env.BRANCH}
                    set COMMIT_SHA=${env.COMMIT_SHA}
                    set RUN_ID=${env.RUN_ID}
                    set RECEIVER_URL=${env.RECEIVER_URL}
                    python ci\\build_report.py
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Check receiver/test-report.json for the latest report."
        }
    }
}