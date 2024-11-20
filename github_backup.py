import os
import subprocess
from datetime import datetime

def backup_to_github():
    """Backup the repository to GitHub."""
    try:
        # Initialize git if not already initialized
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)
            
        # Configure git
        subprocess.run(['git', 'config', 'user.email', 'bot@konomi.ai'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Konomi Bot'], check=True)
        
        # Add remote if not exists
        try:
            subprocess.run(['git', 'remote', 'add', 'origin', 
                          'https://x-access-token:' + os.environ['GITHUB_TOKEN'] + 
                          '@github.com/teslasolar/KonomiLang.git'])
        except subprocess.CalledProcessError:
            # Remote might already exist
            pass
            
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
