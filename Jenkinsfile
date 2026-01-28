pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'mlops-485220'
        GCP_CREDENTIALS = credentials('gcp-key')
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
      stage('Build & Push Docker image to GCR') {
                        steps {
                            withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                            sh '''
                                set -e

                                export PATH=${GCLOUD_PATH}:$PATH
                                echo $GOOGLE_APPLICATION_CREDENTIALS
                                ls -l $GOOGLE_APPLICATION_CREDENTIALS
                                

                                # Auth for gcloud using the service account key
                                gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"
                                gcloud config set project "${GCP_PROJECT}"

                                # Configure Docker auth for GCR
                                gcloud auth configure-docker --quiet

                                IMAGE_NAME="gcr.io/${GCP_PROJECT}/mlops-image:${BUILD_NUMBER}"
                                docker build -t "$IMAGE_NAME" .
                                docker push "$IMAGE_NAME"

                                
                            '''
                            }
                        }
                    }
    }
}
 



