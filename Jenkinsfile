#! groovy

// This file is part of "Apromore Enterprise Edition".
//
// Copyright (C) 2018 - 2023 Apromore Pty Ltd. All Rights Reserved.
//
// NOTICE:  All information contained herein is, and remains the
// property of Apromore Pty Ltd and its suppliers, if any.
// The intellectual and technical concepts contained herein are
// proprietary to Apromore Pty Ltd and its suppliers and may
// be covered by U.S. and Foreign Patents, patents in process,
// and are protected by trade secret or copyright law.
// Dissemination of this information or reproduction of this
// material is strictly forbidden unless prior written permission
// is obtained from Apromore Pty Ltd.

pipeline {
    agent { label 'Docker' }

    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(daysToKeepStr: '30', numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        ansiColor('xterm')
    }

    environment {
        DESTINATION_BUCKET="apromore-emr-dev"
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
                            export PYTHONPATH=test:parquet_converters
                            python -m pytest --reruns 3 --cov=parquet_converters -vv test/'''
                        }
                    }
                }
            }
        }

        stage('buildAndPush-development'){
            when {
                anyOf {
                    branch 'development'
                }
            }
            steps {
                ansiColor('xterm') {
                    withAWS(role:'JenkinsAccessRole', roleAccount:'980945858983', duration: 900, roleSessionName: 'jenkins-session') {
                        sh('./scripts/deploy_to_s3.sh s3://$DESTINATION_BUCKET/spark_converters/dev/app')
                    }
                }
            }
        }

        stage('buildAndPush-release_v9.0'){
            when {
                anyOf {
                    branch 'release/v9.0'
                }
            }
            steps {
                ansiColor('xterm') {
                    withAWS(role:'JenkinsAccessRole', roleAccount:'980945858983', duration: 900, roleSessionName: 'jenkins-session') {
                        sh('./scripts/deploy_to_s3.sh s3://$DESTINATION_BUCKET/spark_converters/release_v9.0/app')
                    }
                }
            }
        }

        stage('buildAndPush-release_v9.1'){
            when {
                anyOf {
                    branch 'release/v9.1'
                }
            }
            steps {
                ansiColor('xterm') {
                    withAWS(role:'JenkinsAccessRole', roleAccount:'980945858983', duration: 900, roleSessionName: 'jenkins-session') {
                        sh('./scripts/deploy_to_s3.sh s3://$DESTINATION_BUCKET/spark_converters/release_v9.1/app')
                    }
                }
            }
        }
    }
}
