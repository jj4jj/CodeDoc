# GitHub 处理器

GitHub 处理器负责处理 Web 应用程序的代码仓库克隆和 URL 解析。

## 概述

GitHub 处理器提供以下实用工具：
- 验证 Git 仓库 URL
- 提取仓库信息
- 克隆仓库

## 类定义

```python
class GitHubRepoProcessor:
    @staticmethod
    def is_valid_github_url(url: str) -> bool:
        """Validate if the URL is a valid Git repository URL."""

    @staticmethod
    def get_repo_info(url: str) -> Dict[str, str]:
        """Extract repository information from URL."""

    @staticmethod
    def generate_title(url: str) -> str:
        """Generate a title from repository URL."""

    @staticmethod
    def clone_repository(clone_url: str, target_dir: str, commit_id: Optional[str] = None) -> bool:
        """Clone a GitHub repository."""
```

## URL 验证

### is_valid_github_url()

支持多种 URL 格式：

```python
@staticmethod
def is_valid_github_url(url: str) -> bool:
    """Validate if the URL is a valid Git repository URL."""

    # SSH format: git@github.com:owner/repo.git
    if '@' in url and ':' in url and not url.startswith('http'):
        parts = url.split(':')
        path = parts[1].replace('.git', '')
        return len(path.split('/')) >= 2

    # HTTP/HTTPS format
    parsed = urlparse(url)
    path = parsed.path.strip('/').replace('.git', '')
    path_parts = path.split('/')

    return len(path_parts) >= 2
```

## 仓库信息

### get_repo_info()

提取仓库元数据：

```python
@staticmethod
def get_repo_info(url: str) -> Dict[str, str]:
    """Extract repository information from Git repository URL."""

    # Handle SSH format
    if url.startswith('ssh://'):
        parsed = urlparse(url)
        path = parsed.path.strip('/').replace('.git', '')
        domain = parsed.netloc.split('@')[-1]

    # Handle HTTP format
    else:
        parsed = urlparse(url)
        path = parsed.path.strip('/').replace('.git', '')
        domain = parsed.netloc

    path_parts = path.split('/')
    owner = path_parts[0]
    repo = path_parts[1]

    return {
        'owner': owner,
        'repo': repo,
        'full_name': f"{owner}/{repo}",
        'clone_url': url,
        'domain': domain
    }
```

### generate_title()

创建显示标题：

```python
@staticmethod
def generate_title(url: str) -> str:
    """Generate a title from Git repository URL."""
    repo_info = GitHubRepoProcessor.get_repo_info(url)
    domain = repo_info.get('domain', 'unknown')
    full_name = repo_info.get('full_name', '')
    return f"{domain}/{full_name}"
```

## 仓库克隆

### clone_repository()

执行克隆，支持可选的浅克隆深度：

```python
@staticmethod
def clone_repository(clone_url: str, target_dir: str, commit_id: Optional[str] = None) -> bool:
    """Clone a GitHub repository to the target directory."""

    # Create target directory
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)

    if commit_id:
        # Clone full repo for specific commit
        result = subprocess.run([
            'git', 'clone', clone_url, target_dir
        ], capture_output=True)

        if result.returncode != 0:
            return False

        # Checkout specific commit
        result = subprocess.run([
            'git', 'checkout', commit_id
        ], cwd=target_dir, capture_output=True)

        return result.returncode == 0

    else:
        # Shallow clone
        result = subprocess.run([
            'git', 'clone', '--depth', '1', clone_url, target_dir
        ], capture_output=True)

        return result.returncode == 0
```

## 支持的 URL 格式

| 格式 | 示例 |
|--------|---------|
| HTTPS | `https://github.com/owner/repo.git` |
| SSH | `git@github.com:owner/repo.git` |
| SSH 协议 | `ssh://git@github.com/owner/repo.git` |
| GitLab | `https://gitlab.com/owner/repo.git` |
| 自定义 | `ssh://git@custom.com:36001/owner/repo.git` |

## 相关文档

- [后台 Worker](background_worker.md)
- [路由](routes.md)