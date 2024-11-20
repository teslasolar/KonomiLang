import os
import subprocess
import requests
from datetime import datetime

def create_github_repo():
    """Create GitHub repository if it doesn't exist."""
    headers = {
        'Authorization': f'token {os.environ["GITHUB_TOKEN"]}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': 'KonomiLang',
        'description': 'A specialized programming language designed for AI model interactions',
        'private': False,
        'has_issues': True,
        'has_projects': True,
        'has_wiki': True
    }
    
    response = requests.post('https://api.github.com/user/repos', headers=headers, json=data)
    return response.status_code == 201

def backup_to_github():
    """Backup the repository to GitHub."""
    try:
        # Initialize git if not already initialized
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)
            
        # Configure git
        subprocess.run(['git', 'config', 'user.email', 'bot@konomi.ai'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Konomi Bot'], check=True)
        
        # Create repository if it doesn't exist
        create_github_repo()
        
        # Add remote if not exists
        try:
            subprocess.run(['git', 'remote', 'add', 'origin', 
                          'https://x-access-token:' + os.environ['GITHUB_TOKEN'] + 
                          '@github.com/teslasolar/KonomiLang.git'])
        except subprocess.CalledProcessError:
            # Remote might already exist
            subprocess.run(['git', 'remote', 'set-url', 'origin',
                          'https://x-access-token:' + os.environ['GITHUB_TOKEN'] + 
                          '@github.com/teslasolar/KonomiLang.git'])
            
        # Add all files
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit changes
        commit_message = f"Automated backup {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to GitHub
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
        
        return True, "Successfully backed up to GitHub"
    except subprocess.CalledProcessError as e:
        return False, f"Error during backup: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

if __name__ == "__main__":
    success, message = backup_to_github()
    print(message)
