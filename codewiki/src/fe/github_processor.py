#!/usr/bin/env python3
"""
GitHub repository processing utilities.
"""

import os
import subprocess
from typing import Dict, Optional
from urllib.parse import urlparse

from .config import WebAppConfig


class GitHubRepoProcessor:
    """Handles GitHub repository processing."""
    
    @staticmethod
    def is_valid_github_url(url: str) -> bool:
        """Validate if the URL is a valid Git repository URL (GitHub, GitLab, or any Git repo)."""
        try:
            url = url.strip()
            
            # Handle SSH URLs (ssh://git@domain.com:port/owner/repo.git)
            if url.startswith('ssh://'):
                parsed = urlparse(url)
                path = parsed.path.strip('/')
                # Remove .git suffix if present
                if path.endswith('.git'):
                    path = path[:-4]
                path_parts = path.split('/')
                # Check if we have at least owner/repo
                return len(path_parts) >= 2 and all(part for part in path_parts[:2])
            
            # Handle SSH SCP-like syntax (git@domain.com:owner/repo.git)
            if '@' in url and ':' in url and not url.startswith('http'):
                parts = url.split(':')
                if len(parts) == 2:
                    path = parts[1]
                    # Remove .git suffix if present
                    if path.endswith('.git'):
                        path = path[:-4]
                    path_parts = path.split('/')
                    # Check if we have at least owner/repo
                    return len(path_parts) >= 2 and all(part for part in path_parts[:2])
            
            # Handle HTTP/HTTPS URLs
            parsed = urlparse(url)
            # Accept any domain (GitHub, GitLab, or others)
            path = parsed.path.strip('/')
            # Remove .git suffix if present
            if path.endswith('.git'):
                path = path[:-4]
            path_parts = path.split('/')
            # Check if we have at least owner/repo
            return len(path_parts) >= 2 and all(part for part in path_parts[:2])
        except Exception:
            return False
    
    @staticmethod
    def get_repo_info(url: str) -> Dict[str, str]:
        """Extract repository information from Git repository URL."""
        url = url.strip()
        path = None
        domain = None
        
        # Handle SSH URLs (ssh://git@domain.com:port/owner/repo.git)
        if url.startswith('ssh://'):
            parsed = urlparse(url)
            path = parsed.path.strip('/')
            # Extract domain, handle potential port
            netloc = parsed.netloc
            if '@' in netloc:
                domain = netloc.split('@')[1]
            else:
                domain = netloc
            # Remove port if present
            if ':' in domain:
                domain = domain.split(':')[0]
        
        # Handle SSH SCP-like syntax (git@domain.com:owner/repo.git)
        elif '@' in url and ':' in url and not url.startswith('http'):
            parts = url.split(':')
            path = parts[1]
            # Extract domain from the first part
            first_part = parts[0]
            if '@' in first_part:
                domain = first_part.split('@')[1]
            else:
                domain = first_part
        
        # Handle HTTP/HTTPS URLs
        else:
            parsed = urlparse(url)
            path = parsed.path.strip('/')
            domain = parsed.netloc
        
        # Remove .git suffix if present
        if path and path.endswith('.git'):
            path = path[:-4]
        
        if not path:
            raise ValueError("Could not extract repository path from URL")
        
        path_parts = path.split('/')
        
        if len(path_parts) < 2:
            raise ValueError("Invalid repository path")
        
        owner = path_parts[0]
        repo = path_parts[1]
        
        return {
            'owner': owner,
            'repo': repo,
            'full_name': f"{owner}/{repo}",
            'clone_url': url,
            'domain': domain if domain else 'unknown'
        }
    
    @staticmethod
    def generate_title(url: str) -> str:
        """
        Generate a title from Git repository URL in the format: <host>/<group>/<repo>
        Examples:
            - https://github.com/owner/repo -> github.com/owner/repo
            - ssh://git@szgit.gs.com:36001/gsbase/gsdr.git -> szgit.gs.com/gsbase/gsdr
            - git@gitlab.com:group/subgroup/repo.git -> gitlab.com/group/subgroup/repo
        """
        try:
            repo_info = GitHubRepoProcessor.get_repo_info(url)
            domain = repo_info.get('domain', 'unknown')
            full_name = repo_info.get('full_name', '')
            return f"{domain}/{full_name}"
        except Exception:
            return url
    
    @staticmethod
    def clone_repository(clone_url: str, target_dir: str, commit_id: Optional[str] = None) -> bool:
        """Clone a GitHub repository to the target directory, optionally checking out a specific commit."""
        try:
            # Ensure target directory exists
            os.makedirs(os.path.dirname(target_dir), exist_ok=True)
            
            # If specific commit is requested, don't use shallow clone
            if commit_id:
                # Clone full repository to access specific commit
                result = subprocess.run([
                    'git', 'clone', clone_url, target_dir
                ], capture_output=True, text=True, timeout=WebAppConfig.CLONE_TIMEOUT)
                
                if result.returncode != 0:
                    print(f"Error cloning repository: {result.stderr}")
                    return False
                
                # Checkout specific commit
                result = subprocess.run([
                    'git', 'checkout', commit_id
                ], cwd=target_dir, capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    print(f"Error checking out commit {commit_id}: {result.stderr}")
                    return False
            else:
                # Clone repository with shallow depth (default behavior)
                result = subprocess.run([
                    'git', 'clone', '--depth', str(WebAppConfig.CLONE_DEPTH), clone_url, target_dir
                ], capture_output=True, text=True, timeout=WebAppConfig.CLONE_TIMEOUT)
                
                if result.returncode != 0:
                    print(f"Error cloning repository: {result.stderr}")
                    return False
            
            return True
        except Exception as e:
            print(f"Error cloning repository: {e}")
            return False