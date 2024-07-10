@Library('jenkins-shared-library') _

//## Please provide docker build arguments if applicable in the fashion --> "key1=value1, key2=value2"
def (ecrRepoURL, repoName, region, ecrCredsInJenkins, dockerFilePath, dockerBuildContent, dockerBuildArguments) = [
        "https://043196765225.dkr.ecr.us-east-1.amazonaws.com",
        "hummingbird-admin-server",
        "us-east-1",
        "jenkins-ecr-creds",
        "Dockerfile",
        "."
    ]
def (scmUrl, branchName, gitCredentialsId) = [
        "https://gitlab.com/storageapi/hummingbird/admin-portal.git",
        env.BRANCH_NAME,
        "ramesh-gitlab-creds"
    ]

//import org.tenant.jenkinsCI  //For future use
//def object = new jenkinsCI()  //For future use
runPipeline.runCommonPipeline(ecrRepoURL, repoName, region, ecrCredsInJenkins, dockerFilePath,
                              dockerBuildContent, dockerBuildArguments,
                              scmUrl, branchName, gitCredentialsId)
