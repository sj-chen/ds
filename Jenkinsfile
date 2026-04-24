pipeline {
    agent any
    environment {
        ALLURE_RESULTS = "allure-results"
    }
    stages {
        stage('CheckOut'){
            steps { git branch: 'master', url: 'https://github.com/sj-chen/ds.git'}
        }
//         stage('Start Environment'){
//             steps { sh "$DOCKER_COMPOSE up -d mysql redis"
//                 sh "sleep 10"
//             }
//         }
        stage('api autotest'){
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''# 进入项目目录（Jenkins 会自动拉取到工作空间）
                        cd $WORKSPACE
                        if [ ! -d "venv" ]; then
                            python3 -m venv venv
                        fi
                        . venv/bin/activate   # Linux/Mac

                        # 安装依赖
                        pip install -r requirements.txt
                        # 运行测试并生成 allure 结果
                        pytest -s -v --alluredir=allure-results --junitxml=junit.xml
                    '''
                }
            }
        }
        stage('gate'){
            steps {
                script {
                    def total = sh(script: "grep -o 'tests=\"[0-9]*\"' junit.xml | cut -d'\"' -f2 | paste -sd+ | bc", returnStdout: true).trim().toInteger()
                    def failed = sh(script: "grep -o 'failures=\"[0-9]*\"' junit.xml | cut -d'\"' -f2 | paste -sd+ | bc", returnStdout: true).trim().toInteger()
                    float passRate = (total - failed) * 100.0 / total
                    echo "自动化测试通过率: ${passRate}%"
                    if (passRate < 95) {
                        error("自动化测试通过率 ${passRate}% < 95%")
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                // 使用 Allure 插件生成报告
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }
}