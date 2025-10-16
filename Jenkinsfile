pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub')  // Jenkins credentials ID
        BACKEND_IMAGE = "jyotirmoy43/backend-app"
        FRONTEND_IMAGE = "jyotirmoy43/frontend-app"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "🔄 Checking out source code"
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/jyotirmoy43/fusionpact-devops-challenge.git',
                        credentialsId: 'dockerhub'
                    ]]
                ])
            }
        }

        stage('Build & Test Backend') {
            steps {
                dir('backend') {
                    echo "📦 Building backend"
                    sh '''
                        sudo apt update -y
                        sudo apt install -y python3-venv python3-pip
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        echo "✅ Backend dependencies installed"
                    '''
                }
            }
        }

        stage('Build & Test Frontend') {
            steps {
                dir('frontend') {
                    echo "🌐 Building frontend"
                    sh '''
                        sudo apt update -y
                        sudo apt install -y npm
                        npm install
                        npm run build
                        echo "✅ Frontend built successfully"
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                echo "🐳 Building Docker images"
                sh '''
                    docker build -t $BACKEND_IMAGE:latest ./backend
                    docker build -t $FRONTEND_IMAGE:latest ./frontend
                '''
            }
        }

        stage('Push Images') {
            steps {
                echo "📤 Pushing images to Docker Hub"
                sh '''
                    echo $DOCKER_HUB_CREDENTIALS_PSW | docker login -u $DOCKER_HUB_CREDENTIALS_USR --password-stdin
                    docker push $BACKEND_IMAGE:latest
                    docker push $FRONTEND_IMAGE:latest
                    docker logout
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Deploying using Docker Compose"
                sh '''
                    docker-compose down || true
                    docker-compose up -d
                '''
            }
        }
    }

    post {
        always {
            echo "🧹 Post actions: cleanup"
            sh '''
                docker system prune -f || true
            '''
        }
        failure {
            echo "❌ Pipeline failed"
        }
        success {
            echo "✅ Pipeline completed successfully!"
        }
    }
}
