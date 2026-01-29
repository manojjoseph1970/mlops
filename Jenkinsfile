pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "mlops-485220"
     }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/manojjoseph1970/mlops.git']])
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
   
    stage('testing Google enviornment before building docker image'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEYFILE')]) {
                sh '''
                    set -e

                    # Use the same venv you created earlier
                    . ${VENV_DIR}/bin/activate
                    #python -m pip install -U google-auth google-cloud-storage

                    export GOOGLE_APPLICATION_CREDENTIALS="$GCP_KEYFILE"

                    # Confirm ADC + python libs work
                    python -c "import google.auth; print(google.auth.default())"

                    # Confirm gcloud exists
                    which gcloud
                    gcloud --version
                 '''
                }
            }
    }


        stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to GCR.............'
                        sh '''
                        
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest 

                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Google cloud run'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to GCR.............'
                        sh '''
                        
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        gcloud run deploy ml-project-service --image gcr.io/${GCP_PROJECT}/ml-project:latest --platform managed --region us-east1 --allow-unauthenticated

                        '''
                    }
                }
            }
        }
        
    }
}




