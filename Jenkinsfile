pipeline {
    agent any
    environment {
        BRANCH_NAME = "${env.BRANCH_NAME}"
    }
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(daysToKeepStr: '30', numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        ansiColor('xterm')
    }

    stages{
        stage('Build Test Image'){
            steps{
                ansiColor('xterm'){
                    script{
                        docker.build(
                            "python:3.8-slim",
                            "--pull -f baseimage/Dockerfile ."
                        )
                    }
                }
            }
        }

        stage('Run Tests'){
            steps {
                ansiColor('xterm') {
                    script{
                        docker.image("python:3.8-slim").inside(){
                            sh '''#!/usr/bin/env bash
                            pip install --user -r requirements.txt
                            pip install --user -r tests/requirements.txt
                            export PYSPARK_HOME=/usr/local/bin/python
                            export PYTHONPATH=tests:src
                            python -m pytest --cov-report=xml:coverage.xml --cov=src -vv tests'''
                        }
                    }
                }
            }
        }

        stage('SonarQube analysis') {
            steps {
                ansiColor('xterm') {
                    script{
                        def scannerHome = tool 'SonarQubeScanner';
                        withSonarQubeEnv('SonarCloud') {
                            sh '''/var/jenkins_home/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQubeScanner/bin/sonar-scanner \
                            -Dsonar.organization=mcamargo85 \
                            -Dsonar.projectKey=Mcamargo85_support_modules \
                            -Dsonar.sources=src \
                            -Dsonar.branch.name=${BRANCH_NAME} \
                            -Dsonar.python.coverage.reportPaths=coverage.xml'''
                        }
                    }
                }
            }
        }
    }
}
