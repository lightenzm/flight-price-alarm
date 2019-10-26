node {
   stage('Checkout') {
      checkout changelog: false, poll: false, scm: [$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'CleanBeforeCheckout']], submoduleCfg: [], userRemoteConfigs: [[credentialsId: "zohar-github", url: "https://github.com/lightenzm/flight-price-alarm.git"]]]
   }
   stage('upload to s3') {
      sh "sudo apt-get -y install awscli"
      sh 'ls'
      sh "tar -czvf flight_price_alarm.tar.gz *"
        withCredentials([usernamePassword(credentialsId: 'zohar-aws', passwordVariable: 'secretkey', usernameVariable: 'accesskey')]) {
            sh "export AWS_ACCESS_KEY_ID=$secretkey"
            sh "export AWS_SECRET_ACCESS_KEY=$accesskey"
            sh "aws s3 cp flight_price_alarm.tar.gz s3://flights-jenkins-tar --region eu-west-1"
        }
    }
}​