# IMMUNIZE

[![patch](https://github.com/R3DRUN3/immunize/actions/workflows/patch.yaml/badge.svg)](https://github.com/R3DRUN3/immunize/actions/workflows/patch.yaml)

Pipeline for patching vulnerable container images 📦🛡️

## Abstract
The present is a repository containing a [Github action](https://github.com/features/actions) to patch vulnerable container images with [copacetic](https://github.com/project-copacetic/copacetic).  

## Instructions

The pipeline is triggered upon a push to the *main* branch.  
The corresponding action is configured in the `.github/workflows/patch.yaml` file.  
Specifically, the list of container images to patch is specified within the strategy as follows:

```yaml
images: ['docker.io/library/nginx:1.21.6', 'docker.io/openpolicyagent/opa:0.46.0']
```  
Following are the steps in the pipeline:  
1. **Set up Docker Buildx**
   - Action: `docker/setup-buildx-action`
   - Description: Sets up Docker Buildx for building multi-platform Docker images.

2. **Generate Trivy Report**
   - Action: `aquasecurity/trivy-action`
   - Description: Scans Docker images for vulnerabilities using Trivy, generates a JSON report, and ignores unfixed vulnerabilities.

3. **Check Vuln Count**
   - Description: Uses *jq* to count the number of vulnerabilities in the Trivy report and outputs the count to `$GITHUB_OUTPUT`.

4. **Copa Action**
   - Action: `project-copacetic/copa-action`
   - Description: Runs Copa Action to handle vulnerabilities based on the Trivy report.  
   If vulnerabilities are present, it immunizes the image.

1. **Log into ghcr**
   - Action: `docker/login-action`
   - Description: Logs into GitHub Container Registry (ghcr.io) using the GitHub token if the Copa Action was successful.

2. **Tag Image for GHCR**
   - Description: Tags the immunized Docker image for GitHub Container Registry (*GHCR*) using the patched image from the Copa Action.

3. **Docker Push Patched Image**
   - Description: Pushes the tagged immunized Docker image to GitHub Container Registry (GHCR) if the login was successful.

The pateched images can be found [here](https://github.com/R3DRUN3?tab=packages&repo_name=immunize).  


To perform image pulls, authentication is not required; however, GitHub may prompt for a token if the API call limit is exceeded.  
In such instances, please refer to the instructions provided [here](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic) to configure an access token.  
Subsequently, proceed to log in as follows:

```console
export CR_PAT=YOUR_TOKEN \
&& echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin

Login Succeeded
```   

## Verify Patching

>[!Note]
> Please be aware that *Copacetic* focuses on rectifying vulnerabilities within the operating system's libraries, rather than addressing application dependencies.  

To assess the effectiveness of patching, you may conduct a scan using [Trivy](https://github.com/aquasecurity/trivy) initially on one of the original images:  
```console
trivy image docker.io/openpolicyagent/opa:0.46.0
```  

Output for OS CVEs:  
```console   
Total: 41 (UNKNOWN: 0, LOW: 11, MEDIUM: 21, HIGH: 9, CRITICAL: 0)
```  

And then on the immunized version of that same image:  
```console
docker pull ghcr.io/r3drun3/immunize/docker.io/openpolicyagent/opa:immunized \
&& trivy image ghcr.io/r3drun3/immunize/docker.io/openpolicyagent/opa:immunized
```  

Output for OS CVEs:  
```console   
Total: 18 (UNKNOWN: 0, LOW: 11, MEDIUM: 7, HIGH: 0, CRITICAL: 0)
```  

As you can see the latest has way more CVEs than the former!  






