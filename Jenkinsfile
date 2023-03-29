pipeline {
    agent { label 'Docker' }

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
                            "python:3.7.13-slim-buster-jre",
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
                        docker.image("python:3.7.13-slim-buster-jre").inside(){
                            sh '''#!/usr/bin/env bash
                            pip install --user -r requirements.txt
                            pip install --user -r test/requirements.txt
                            export PYSPARK_HOME=/usr/local/bin/python
                            export PYTHONPATH=test:src
                            python -m pytest --cov=parquet_converters -vv test/'''
                        }
                    }
                }
            }
        }
    }
}
