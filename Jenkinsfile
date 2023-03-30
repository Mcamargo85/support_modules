pipeline {
    agent any
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
                        docker.image("python:3.8-slim").inside('-v /var/jenkins_home/workspace/coverage_results:/coverage_results'){
                            sh '''#!/usr/bin/env bash
                            pip install --user -r requirements.txt
                            pip install --user -r tests/requirements.txt
                            export PYSPARK_HOME=/usr/local/bin/python
                            export PYTHONPATH=tests:src
                            python -m pytest --cov-report=xml:/coverage_results/coverage.xml --cov=src -vv tests'''
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
                            -Dsonar.branch.name=ci_cd \
                            -Dsonar.branch.target=ci_cd \
                            -Dsonar.python.coverage.reportPaths=/var/jenkins_home/workspace/coverage_results/coverage.xml'''
                        }
                    }
                }
            }
        }
    }
}
