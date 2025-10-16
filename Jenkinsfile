pipeline {
    agent any

    environment {
        // Docker registry (adjust to your real registry)
        DOCKER_REGISTRY = "your-dockerhub-username"
        BACKEND_IMAGE   = "${DOCKER_REGISTRY}/fusionpact-backend"
        FRONTEND_IMAGE  = "${DOCKER_REGISTRY}/fusionpact-frontend"
        // Credentials IDs in Jenkins (you must configure these)
        DOCKER_CREDENTIALS = "dockerhub-cred"
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
                    // Adjust based on your backend (looks like FastAPI / Python)
                    sh '''
                    # Assuming Python project
                    pip install -r requirements.txt
                    # run tests if any (you may add pytest etc.)
                    # Example: pytest --maxfail=1 --disable-warnings -q
                    '''
                }
            }
        }

        stage('Build & Test Frontend') {
            steps {
                dir('frontend') {
                    echo "🖥️ Building frontend"
                    // Adjust for your frontend (e.g. React/Vue/Static HTML)
                    sh '''
                    # Example if using Node-based frontend
                    # npm install
                    # npm run build
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                echo "🐳 Building Docker images"
                // build backend image
                sh """
                docker build -t ${BACKEND_IMAGE}:${env.BUILD_NUMBER} ./backend
                """
                // build frontend image
                sh """
                docker build -t ${FRONTEND_IMAGE}:${env.BUILD_NUMBER} ./frontend
                """
            }
        }

        stage('Push Images') {
            steps {
                echo "🚀 Pushing images to registry"
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push ${BACKEND_IMAGE}:${env.BUILD_NUMBER}
                    docker push ${FRONTEND_IMAGE}:${env.BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "🛠️ Deploying via Docker Compose"
                // Assuming your root has docker-compose.yml wired to use images with tags
                sh '''
                # Optionally pull latest images
                docker-compose down || true
                docker-compose pull || true
                # Start up
                docker-compose up -d
                '''
            }
        }
    }

    post {
        always {
            echo "🧹 Post actions: cleanup"
            sh 'docker system prune -f || true'
        }
        success {
            echo "✅ Pipeline succeeded"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
