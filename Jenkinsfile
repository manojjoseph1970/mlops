pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'mlops-485220'
        GCP_CREDENTIALS = credentials('gcp-service-account-key')
        GCLOUD_PATH = '/var/jenkins_home/gcloud/google-cloud-sdk/bin'
    }
    stages {
        stage('Cloning Repository to Jenkins Workspace') {
            steps {
                 echo 'Cloning the repository...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/manojjoseph1970/mlops.git']])
            } 
        }
    
        stage('setting up virtual enviornment and installing dependencies') {
            steps {
                 echo 'setting up virtual enviornment and installing dependencies...'
                    sh '''
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
            } 
        }
        stage('Building and pushing docker image to GCR') {
            steps {
                 
                     withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_APP_CREDENTIALS')]) {
                       script{
                         echo 'sBuilding and pushing docker image to GCR...'
                        sh '''
                            export PATH=${GCLOUD_PATH}:$PATH
                            gcloud auth activate-service-account --key-file=${GCP_APP_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet    
                            IMAGE_NAME=gcr.io/${GCP_PROJECT}/mlops-image:latest
                            docker build -t $IMAGE_NAME .
                            docker push $IMAGE_NAME
                        '''
                       } 
            } 
        }
    }
}
    }
 



