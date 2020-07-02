from github import Github

class GitManager:
    def __init__(self, access_key):
        self.git = Github(access_key)
        self.repo = self.git.get_repo("AVEGame/AVE-usergames")
    
    def create_branch(self, branch):
        master = self.repo.get_branch("master")
        self.repo.create_git_ref("refs/heads/" + branch, sha=master.commit.sha)
    
    def add_file_to_branch(self, branch, filename, content):
        message = "Add game " + filename
        self.repo.create_file(filename, message, content, branch=branch)
