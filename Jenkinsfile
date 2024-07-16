@Library('shared-library') _

podTemplate(yaml: '''
    apiVersion: v1
    kind: Pod
    spec:
      serviceAccountName: jenkins-sa-agent
      containers:
      - name: docker
        image: docker:dind  # Docker-in-Docker image
        command: ["dockerd", "--tls=false", "--host=unix:///var/run/docker.sock", "--host=tcp://localhost:2375"]
        securityContext:
          privileged: true  # Required for running Docker inside Docker
        volumeMounts:
          - name: docker-data
            mountPath: /var/lib/docker
        resources:
          requests:
            memory: "8192Mi"
            cpu: "2"
          limits:
            memory: "8192Mi"
            cpu: "2"
      - image: "043196765225.dkr.ecr.us-east-1.amazonaws.com/jenkins-agent:latest"
        name: "jnlp"
        resources:
          requests:
            memory: "4096Mi"
            cpu: "2"
          limits:
            memory: "4096Mi"
            cpu: "2"
        env:
        - name: "DOCKER_HOST"
          value: "tcp://localhost:2375"
        - name: "JENKINS_URL"
          value: "http://jenkins.jenkins.svc.cluster.local:8080/"
        volumeMounts:
        - mountPath: "/home/jenkins/agent"
          name: "workspace-volume"
          readOnly: false
      volumes:
      - name: docker-data
        emptyDir: {}
      - name: "workspace-volume"
        emptyDir:
          medium: ""
      restartPolicy: "Never"
      imagePullPolicy: Always
''') {
    node(POD_LABEL) {

        //## Please provide docker build arguments if applicable in the fashion --> "key1=value1, key2=value2"
        def (environment, ecrRepoURL, repoName, region, ecrCredsInJenkins, dockerFilePath, dockerBuildContent, dockerBuildArguments) = [
                env.environment,
                env.ecrRepoURL,
                env.JOB_NAME,
                env.region,
                env.jenkins_ecr_creds,
                "Dockerfile",
                ".",
                "VUE_APP_API_PORT=STATICSET_VALUE_PLACEHOLDER_API_PORT, VUE_APP_API_SUBDOMAIN=STATICSET_VALUE_PLACEHOLDER_API_SUBDOMAIN, VUE_APP_DOMAIN=STATICSET_VALUE_PLACEHOLDER_API_DOMAIN, VUE_APP_API_PROTOCOL=STATICSET_VALUE_PLACEHOLDER_API_PROTOCOL, VUE_APP_WEBSOCKET_SERVER_APP_ENDPOINT=STATICSET_VALUE_PLACEHOLDER_APP_ENDPOINT, VUE_APP_GDS_BASE_URL=STATICSET_VALUE_PLACEHOLDER_GDS_BASE_URL, VUE_APP_NECTAR_APP_ID=STATICSET_VALUE_PLACEHOLDER_NECTAR_APP_ID, VUE_APP_GDS_API_KEY=STATICSET_VALUE_PLACEHOLDER_GDS_API_KEY, VUE_APP_WALKME_URL=STATICSET_VALUE_PLACEHOLDER_WALKME_URL, VUE_APP_GDS_SUBDOMAIN=STATICSET_VALUE_PLACEHOLDER_GDS_SUBDOMAIN, VUE_APP_FILE_APP_ID=STATICSET_VALUE_PLACEHOLDER_FILE_APP_ID, VUE_APP_HELP_JUICE_URL=STATICSET_VALUE_PLACEHOLDER_HELP_JUICE_URL, VUE_APP_HUMMINGBIRD_APP_ID=STATICSET_VALUE_PLACEHOLDER_HUMMINGBIRD_APP_ID"
        ]

        def (branchName, gitCredentialsId, devOpsScmUrl, devOpsScmBranchName, subDirectoryToCheckoutTo) = [
                env.branchName,
                env.gitlab_creds,
                env.devOpsScmUrl,
                env.devOpsScmBranchName,
                "devOpsRepo"
        ]

        def (chart_version, aws_creds, aus_cluster_name, aus_cluster_region, us_cluster_name, us_cluster_region) = [
          "1.0.0",
          env.mgmt_aws_jenkins_creds,
          env.eks_cluster_name,
          env.eks_cluster_region,
          "non-prod-us-east-1-eks-cluster",
          env.region
        ]

        def imageTag = null
        def commit_hash = null

        if (environment == env.targetEnvironment) {
            try {
                stage('Clean previous builds') {
                    def buildNumber = env.BUILD_NUMBER as int
                    if (buildNumber > 1) milestone(buildNumber - 1)
                    milestone(buildNumber)
                }
                stage('SCM checkout') {
                    awsGetSecretValueCmd = "aws secretsmanager get-secret-value --region " + region + " --secret-id gitlab-urls --query SecretString --output text | jq -r '.[\"" + repoName + "\"]'"
                    scmUrl = sh(returnStdout: true, script: awsGetSecretValueCmd).toString().trim()
                    scmCheckout.scmCheckoutAtBranch(scmUrl, branchName, gitCredentialsId)
                    commit_hash = sh(returnStdout: true, script: 'git rev-parse --short HEAD').toString().trim()
                    slackSendMessages.slackSendJobTriggeredMessage('docker-image-builds-notifications', commit_hash, branchName)
                    imageTag = commit_hash
                }
                stage('Build and Push Docker Image') {
                    if ( imageTag == null ){
                        imageTag = branchName + "." + commit_hash
                    }
                    dockerOperations.dockerBuildAndPush(repoName, imageTag, dockerFilePath, dockerBuildContent,
                                    ecrRepoURL, region, ecrCredsInJenkins, dockerBuildArguments)
                }
                stage("Slack image build notification") {
                    slackSendMessages.slackSendBuildSuccessMessage(ecrRepoURL, repoName, imageTag, 'docker-image-builds-notifications', branchName)
                }
                stage('SCM checkout devOps repo') {
                    scmCheckout.scmCheckoutAtBranchToSubDirectory(devOpsScmUrl, devOpsScmBranchName, gitCredentialsId, subDirectoryToCheckoutTo)
                }
                /* stage('Helm deployment') {
                    helm.deploy(environment, repoName, imageTag, ecrRepoURL, region, ecrCredsInJenkins, chart_version, aws_creds, us_cluster_name, us_cluster_region)
                } */
                stage('Helm deployment AUS') {
                    helm.deploy(environment, repoName, imageTag, ecrRepoURL, region, ecrCredsInJenkins, chart_version, aws_creds, aus_cluster_name, aus_cluster_region)
                }
                stage("Slack helm deployment notification") {
                    slackSendMessages.slackSendDeploymentSuccessMessage(ecrRepoURL, repoName, imageTag, 'docker-image-builds-notifications', branchName)
                }
            } catch (Exception e) {
                stage("Slack Send Error") {
                    println(e)
                    slackSendMessages.slackSendFailureMessage('docker-image-builds-notifications', e, branchName)
                    //Throwing an exception with graceful exit.
                    throw new Exception("Job failed due to one of the pipeline stage is failed.")
                }
            }
        } else {
            println("Specified environment i.e. ${environment} does not match with target environment i.e. ${env.targetEnvironment}")
        }
    }
}
