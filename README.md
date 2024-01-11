# IMMUNIZE

[![patch](https://github.com/R3DRUN3/immunize/actions/workflows/patch.yaml/badge.svg)](https://github.com/R3DRUN3/immunize/actions/workflows/patch.yaml)

Pipeline for patching vulnerable container images 📦🛡️

## Abstract
The present is a repository containing a [Github action](https://github.com/features/actions) to patch vulnerable container images with [copacetic](https://github.com/project-copacetic/copacetic).  

> [!Note]
> The pateched images can be found [here](https://github.com/R3DRUN3?tab=packages&repo_name=immunize).  

## Instructions

The pipeline is triggered upon a push to the repo (any branch).   
The corresponding action is configured in the `.github/workflows/patch.yaml` file.  
Specifically, the list of container images to patch is specified within the strategy as follows:

```yaml
images: ['docker.io/library/nginx:1.21.6', 'docker.io/openpolicyagent/opa:0.46.0']
```  
Following is an high-level description of the pipeline jobs and steps:  
## Immunize Job
### Overview:

This job is triggered on every push event (excluding changes to README.md) and focuses on scanning and immunizing Docker images for security vulnerabilities.
### Steps: 
1. **Set up Docker Buildx:**  
   - Uses the `docker/setup-buildx-action` to set up Docker Buildx for multi-platform builds. 
2. **Generate Trivy Report:**  
   - Utilizes the `aquasecurity/trivy-action` to scan specified Docker images for OS vulnerabilities and generates a JSON report. 
3. **Check Vuln Count:**  
   - Parses the Trivy report using `jq` to count the number of vulnerabilities and outputs the count to the GitHub environment. 
4. **Set Tag:** 
   - Extracts the tag from the Docker image reference and appends "-immunized" to create a new tag. Sets this new tag in the GitHub environment. 
5. **Copa Action:**  
   - Conditionally executes the `project-copacetic/copa-action` if vulnerabilities are found.
   - Utilizes Copa to apply security patches to the Docker image, generating a patched image and a detailed report.  
6. **Log into ghcr:**  
   - Logs into GitHub Container Registry (ghcr.io) using the `docker/login-action` with the GitHub token. 
7. **Tag Image for GHCR:** 
   - Tags the patched Docker image and prepares it for pushing to GitHub Container Registry. 
8. **Docker Push Patched Image:** 
   - Pushes the patched Docker image to GitHub Container Registry for storage and distribution.  

## Send-Mail-Report Job
### Overview:

This job is dependent on the completion of the `Immunize` job and is responsible for sending an email report.  
If you dont need this job you can comment it out in the pipeline manifest.  
### Steps: 
1. **Checkout Repository:** 
   - Checks out the repository to access necessary files and scripts. 
2. **Send Mail Report:**  
   - Executes a Python script (`send_mail_report.py`) located in the repository, sending a report via email.  
   - Configures email recipient addresses, sender address, and password using github action secrets.  
3. **Report Example**:  
   - ![report](images/report.png)

<br />



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
> Please be aware that *Copacetic* focuses on rectifying vulnerabilities within the operating system's libraries in the relative container layer, rather than addressing application dependencies.  

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
docker pull ghcr.io/r3drun3/immunize/docker.io/openpolicyagent/opa:0.46.0-immunized \
&& trivy image ghcr.io/r3drun3/immunize/docker.io/openpolicyagent/opa:0.46.0-immunized
```  

Output for OS CVEs:  
```console   
Total: 18 (UNKNOWN: 0, LOW: 11, MEDIUM: 7, HIGH: 0, CRITICAL: 0)
```  

As you can see the latest has way less CVEs than the former!  






