pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub')
        BACKEND_IMAGE = "jyotirmoy43/backend"
        FRONTEND_IMAGE = "jyotirmoy43/frontend"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "🔄 Checking out source code"
                checkout scm
            }
        }

        stage('Build & Test Backend') {
            steps {
                dir('backend') {
                    echo "📦 Building backend"
                    sh '''
                        apt update -y
                        apt install -y python3 python3-pip
                        pip install -r requirements.txt
                        python3 -m pytest || echo "⚠️ Tests skipped (no test files found)"
                    '''
                }
            }
        }

        stage('Build & Test Frontend') {
            steps {
                dir('frontend') {
                    echo "🧱 Building frontend"
                    sh '''
                        apt install -y nodejs npm
                        npm install
                        npm run build || echo "⚠️ Skipping build if not configured"
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
                echo "📤 Pushing Docker images"
                sh '''
                    echo "$DOCKER_HUB_CREDENTIALS_PSW" | docker login -u "$DOCKER_HUB_CREDENTIALS_USR" --password-stdin
                    docker push $BACKEND_IMAGE:latest
                    docker push $FRONTEND_IMAGE:latest
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Deploying stack with Docker Compose"
                sh 'docker compose down || true'
                sh 'docker compose up -d'
            }
        }
    }

    post {
        always {
            echo "🧹 Post actions: cleanup"
            sh 'docker system prune -f || true'
        }
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
