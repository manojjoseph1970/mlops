pipeline {
    agent any

    stages {
        stage('Cloning Repository to Jenkins Workspace') {
            steps {
                 echo 'Cloning the repository...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/manojjoseph1970/mlops.git']])
            } 
        }
    }
}



