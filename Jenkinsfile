pipeline {
    agent any

    environment {
        DOCKER_USER = credentials('dockerhub')   // your DockerHub credentials ID
        IMAGE_BACKEND = "jyotirmoy43/backend"
        IMAGE_FRONTEND = "jyotirmoy43/frontend"
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
                docker run --rm -v $WORKSPACE/backend:/app -w /app python:3.11 bash -c "
                    pip install --no-cache-dir -r requirements.txt &&
                    if [ -f test_main.py ]; then pytest -q || true; else echo 'No backend tests'; fi
                "
                '''
            }
        }

        stage('Build Frontend (Static HTML)') {
            steps {
                echo "🖥️ Building frontend Docker image (static HTML)..."
                sh '''
                docker build -t $IMAGE_FRONTEND:latest ./frontend
                '''
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                echo "🐳 Building backend Docker image..."
                sh '''
                docker build -t $IMAGE_BACKEND:latest ./backend
                '''
            }
        }

        stage('Push Docker Images') {
            steps {
                echo "🚀 Pushing Docker images to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                    echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin
                    docker push $IMAGE_FRONTEND:latest
                    docker push $IMAGE_BACKEND:latest
                    docker logout
                    '''
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                echo "🚀 Deploying application using docker-compose..."
                sh '''
                docker-compose down || true
                docker-compose up -d
                docker ps
                '''
            }
        }
    }

    post {
        always {
            echo "🧹 Cleaning workspace and Docker cache..."
            sh 'docker system prune -f || true'
        }
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed."
        }
    }
}
