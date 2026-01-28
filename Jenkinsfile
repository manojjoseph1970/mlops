pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Cloning Repository to Jenkins Workspace') {
            steps {
                 echo 'Cloning the repository...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/manojjoseph1970/mlops.git']])
            } 
        }
    }
    stages {
        stage('setting up virtual enviornment and installing dependencies') {
            steps {
                 echo 'setting up virtual enviornment and installing dependencies...'
                    sh '''
                        python3 -m venv ${VENV_DIR}
                        source ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
            } 
        }
    }
}



