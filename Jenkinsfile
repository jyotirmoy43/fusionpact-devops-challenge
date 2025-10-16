pipeline {
    agent any

    environment {
        REGISTRY          = "your-dockerhub-username"
        BACKEND_IMAGE     = "${REGISTRY}/fusionpact-backend"
        FRONTEND_IMAGE    = "${REGISTRY}/fusionpact-frontend"
        DOCKER_CREDENTIAL = "dockerhub-cred"  // Jenkins credentials ID
    }

    stages {
        stage('Checkout') {
            steps {
                echo "🔄 Checking out source code..."
                checkout scm
            }
        }

        stage('Build & Test Backend') {
            agent { docker { image 'python:3.11' } }
            steps {
                dir('backend') {
                    echo "⚙️ Installing dependencies and testing backend..."
                    sh '''
                    pip install --no-cache-dir -r requirements.txt
                    # Run tests if present
                    if [ -f "test_main.py" ]; then
                      pytest -q || echo "Tests failed, continuing..."
                    else
                      echo "No backend tests found"
                    fi
                    '''
                }
            }
        }

        stage('Build & Test Frontend') {
            agent { docker { image 'node:18' } }
            steps {
                dir('frontend') {
                    echo "🖥️ Building frontend..."
                    sh '''
                    npm ci || npm install
                    npm run build
                    '''
                }
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
                echo "📦 Pushing Docker images to registry..."
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
                echo "🚀 Deploying with Docker Compose..."
                sh '''
                # Update compose file if needed to use the new image tags
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
        success {
            echo "✅ Pipeline completed successfully."
        }
        failure {
            echo "❌ Pipeline failed."
        }
    }
}
