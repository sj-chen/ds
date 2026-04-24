pipeline {
    agent any
    enviroment = {
        ALLURE_RESULTS = "allure-results"
    }
    stages {
        stage('CheckOut'){
            steps { git branch: 'main', url: 'https://github.com/sj-chen/ds.git'}
        }
        stage('Start Envirement'){
            steps { sh "$DOCKER_COMPOSE up -d mysql redis"
                sh "sleep 10"
            }
        }
        stage('api autotest'){
            steps { sh 'pytest $WORKSPACE/ --allure-dir = ALLURE_RESULTS'}
        }
        stage('gate'){
            steps {
                script {
                    def total = sh(script: "grep -o 'tests=\"[0-9]*\"' junit.xml | cut -d'\"' -f2 | paste -sd+ | bc", returnStdout: true).trim().toInteger()
                    def failed = ... // 同理提取 failures 数量
                    float passRate = (total - failed) * 100.0 / total
                    if (passRate < 95) {
                        error("自动化测试通过率 ${passRate}% < 95%")
                    }
                }

            }
        }
    }
}