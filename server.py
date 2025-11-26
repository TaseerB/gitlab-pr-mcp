import os
import sys
import logging
import requests
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("gitlab-mcp-server")

# Initialize FastMCP server
mcp = FastMCP("gitlab-pr-server")

@mcp.tool()
def create_merge_request(source_branch: str = "", target_branch: str = "") -> str:
    """Create a new merge request in GitLab."""
    
    # Validate inputs
    if not source_branch or not target_branch:
        return "Error: Both source_branch and target_branch are required."

    # Get configuration from environment variables
    gitlab_token = os.environ.get("GITLAB_TOKEN")
    project_id = os.environ.get("GITLAB_PROJECT_ID")
    gitlab_url = os.environ.get("GITLAB_URL", "https://gitlab.com")

    if not gitlab_token:
        return "Error: GITLAB_TOKEN environment variable is not set."
    if not project_id:
        return "Error: GITLAB_PROJECT_ID environment variable is not set."

    # Prepare API request
    api_url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests"
    headers = {
        "Private-Token": gitlab_token,
        "Content-Type": "application/json"
    }
    payload = {
        "source_branch": source_branch,
        "target_branch": target_branch,
        "title": f"Merge {source_branch} into {target_branch}",
        "remove_source_branch": True
    }

    try:
        logger.info(f"Attempting to create MR from {source_branch} to {target_branch}")
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 201:
            data = response.json()
            web_url = data.get("web_url", "URL not found")
            return f"Success! Merge Request created: {web_url}"
        else:
            logger.error(f"GitLab API Error: {response.text}")
            return f"Failed to create Merge Request. Status: {response.status_code}. Error: {response.text}"
            
    except Exception as e:
        logger.exception("Unexpected error creating merge request")
        return f"An unexpected error occurred: {str(e)}"

if __name__ == "__main__":
    mcp.run()
