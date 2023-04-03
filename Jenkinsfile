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
                        if (BRANCH_NAME == 'master') {
                            withSonarQubeEnv('SonarCloud') {
                                sh '''/var/jenkins_home/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQubeScanner/bin/sonar-scanner \
                                    -Dsonar.organization=mcamargo85 \
                                    -Dsonar.projectKey=Mcamargo85_support_modules \
                                    -Dsonar.sources=src \
                                    -Dsonar.branch.name=${BRANCH_NAME} \
                                    -Dsonar.python.coverage.reportPaths=coverage.xml'''
                                }
                        } else {
                             withSonarQubeEnv('SonarCloud') {
                                 sh '''/var/jenkins_home/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQubeScanner/bin/sonar-scanner \
                                    -Dsonar.organization=mcamargo85 \
                                    -Dsonar.projectKey=Mcamargo85_support_modules \
                                    -Dsonar.sources=src \
                                    -Dsonar.branch.name=${BRANCH_NAME} \
                                    -Dsonar.branch.target=${BRANCH_NAME} \
                                    -Dsonar.python.coverage.reportPaths=coverage.xml'''
                                 }
                        }
                    }
                }
            }
        }
    }
    post{
        success{
            setBuildStatus("Build succeeded", "SUCCESS");
        }

        failure {
            setBuildStatus("Build failed", "FAILURE");
        }
    }
}

void setBuildStatus(String message, String state) {
    step([
        $class: "GitHubCommitStatusSetter",
        reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/Mcamargo85/support_modules"],
        contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
        errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
        statusResultSource: [$class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]]]
    ]);
