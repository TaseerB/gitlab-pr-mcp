# GitLab PR MCP Server

An MCP server to easily raise Merge Requests in GitLab.

## Configuration

You need the following environment variables:

- `GITLAB_TOKEN`: Your GitLab Personal Access Token.
    1.  Go to **User Settings** (click your avatar) > **Access Tokens**.
    2.  Create a new token.
    3.  Give it a name and check the **`api`** scope.
    4.  Copy the token (starts with `glpat-`).
- `GITLAB_PROJECT_ID`: The ID of the GitLab project.
    1.  Go to your project's homepage in GitLab.
    2.  Look under the project name for **"Project ID: 123456"**.
    3.  **Alternative:** You can use the **URL-encoded path** of the project (e.g., `group%2Fproject`).
        *   If your URL is `gitlab.com/my-group/my-project`, the ID is `my-group%2Fmy-project`.
- `GITLAB_URL`: (Optional) Base URL for GitLab instance. Defaults to `https://gitlab.com`.

## Installation & Usage

### 1. Build the Docker Image

```bash
docker build -t gitlab-pr-mcp .
```

### 2. Configure Your MCP Client (Antigravity / Claude Desktop)

Add the following configuration to your MCP settings file (e.g., `claude_desktop_config.json` or Antigravity's MCP config):

```json
{
  "mcpServers": {
    "gitlab-pr": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "GITLAB_TOKEN=your_token_here",
        "-e", "GITLAB_PROJECT_ID=your_project_id_here",
        "gitlab-pr-mcp"
      ]
    }
  }
}
```

Replace `your_token_here` and `your_project_id_here` with your actual values.

### 3. Configure Cursor

1.  Open **Cursor Settings** (`Cmd + ,` or `Ctrl + ,`).
2.  Navigate to **Features** > **MCP**.
3.  Click **+ Add New MCP Server**.
4.  Fill in the details:
    *   **Name:** `gitlab-pr`
    *   **Type:** `command` (or `stdio`)
    *   **Command:** `docker`
    *   **Args:**
        ```text
        run
        -i
        --rm
        -e
        GITLAB_TOKEN=your_token_here
        -e
        GITLAB_PROJECT_ID=your_project_id_here
        gitlab-pr-mcp
        ```
    *(Note: Add each argument as a separate line/item in the args list)*

### 3. Usage

Ask Claude: "Create a merge request from feature-branch to main"
