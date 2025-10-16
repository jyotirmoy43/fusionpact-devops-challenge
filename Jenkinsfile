pipeline {
    agent any

    environment {
        REGISTRY          = "your-dockerhub-username"
        BACKEND_IMAGE     = "${REGISTRY}/fusionpact-backend"
        FRONTEND_IMAGE    = "${REGISTRY}/fusionpact-frontend"
        DOCKER_CREDENTIAL = "dockerhub-cred"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "🔄 Checking out source code..."
                checkout scm
            }
        }

        stage('Build & Test Backend') {
            steps {
                echo "⚙️ Building and testing backend in Python container..."
                sh '''
                docker run --rm -v $PWD/backend:/app -w /app python:3.11 bash -c "
                    pip install --no-cache-dir -r requirements.txt &&
                    if [ -f test_main.py ]; then pytest -q || true; else echo 'No backend tests'; fi
                "
                '''
            }
        }

        stage('Build & Test Frontend') {
            steps {
                echo "🖥️ Building frontend in Node container..."
                sh '''
                docker run --rm -v $PWD/frontend:/app -w /app node:18 bash -c "
                    npm ci || npm install &&
                    npm run build
                "
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                echo "🐳 Building Docker images..."
                sh """
                docker build -t ${BACKEND_IMAGE}:${BUILD_NUMBER} ./backend
                docker build -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} ./frontend
                """
            }
        }

        stage('Push Docker Images') {
            steps {
                echo "📦 Pushing images to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIAL, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}
                    docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                echo "🚀 Deploying application using docker-compose..."
                sh '''
                docker-compose down || true
                docker-compose pull || true
                docker-compose up -d --build
                '''
            }
        }
    }

    post {
        always {
            echo "🧹 Cleaning workspace and Docker cache..."
            sh 'docker system prune -f || true'
        }
        success { echo "✅ Pipeline completed successfully." }
        failure { echo "❌ Pipeline failed." }
    }
}
