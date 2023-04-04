pipeline {
    agent any
    environment {
        BRANCH_NAME = "${env.BRANCH_NAME}"
        CHANGE_ID = "${env.CHANGE_ID}"
        CHANGE_TARGET = "${env.CHANGE_TARGET}"
        CHANGE_BRANCH = "${env.CHANGE_BRANCH}"
        MAIN_BRANCH = 'master'
        LONG_LIVED_PATTERN = "release\\."
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

        stage('PR SonarQube analysis') {
            when { changeRequest() }
            steps {
                ansiColor('xterm') {
                    script {
                        def scannerHome = tool 'SonarQubeScanner';
                        withSonarQubeEnv('SonarCloud')
                        {
                            sh "git fetch origin ${CHANGE_TARGET}:refs/remotes/origin/${CHANGE_TARGET}"
                            sh '''/var/jenkins_home/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQubeScanner/bin/sonar-scanner \
                                -Dsonar.organization=mcamargo85 \
                                -Dsonar.projectKey=Mcamargo85_support_modules \
                                -Dsonar.sources=src \
                                -Dsonar.pullrequest.key=${CHANGE_ID} \
                                -Dsonar.pullrequest.branch=${CHANGE_BRANCH} \
                                -Dsonar.pullrequest.base=${CHANGE_TARGET} \
                                -Dsonar.python.coverage.reportPaths=coverage.xml'''
                        }
                    }
                }
            }
        }

        stage('Main branch SonarQube analysis') {
            when { allOf { not { changeRequest() }; branch MAIN_BRANCH} }
            steps {
                ansiColor('xterm') {
                    script {
                        def scannerHome = tool 'SonarQubeScanner';
                        withSonarQubeEnv('SonarCloud')
                        {
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

        stage('Long-lived branch SonarQube analysis') {
            when { allOf { not { changeRequest() }; branch pattern: LONG_LIVED_PATTERN, comparator: "REGEXP" } }
            steps {
                ansiColor('xterm') {
                    script {
                        def scannerHome = tool 'SonarQubeScanner';
                        withSonarQubeEnv('SonarCloud')
                        {
                            sh '''/var/jenkins_home/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQubeScanner/bin/sonar-scanner \
                                -Dsonar.organization=mcamargo85 \
                                -Dsonar.projectKey=Mcamargo85_support_modules \
                                -Dsonar.sources=src \
                                -Dsonar.branch.name=${BRANCH_NAME} \
                                -Dsonar.branch.target=${MAIN_BRANCH} \
                                -Dsonar.python.coverage.reportPaths=coverage.xml'''
                        }
                    }
                }
            }
        }

        stage('Short-lived branch SonarQube analysis') {
            when { allOf { not { changeRequest() }; not { branch pattern: LONG_LIVED_PATTERN, comparator: "REGEXP" } } }
            steps {
                ansiColor('xterm') {
                    script {
                        def scannerHome = tool 'SonarQubeScanner';
                        withSonarQubeEnv('SonarCloud')
                        {
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
