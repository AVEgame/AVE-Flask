from github import Github
from datetime import datetime

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
    
    def create_pull_request(self, branch, filename):
        message = "Add game " + filename
        return self.repo.create_pull(title=message, body=message, head=branch, base="master").html_url

    def add_file(self, filename, content):
        branch = f"{filename}-{int(datetime.now().timestamp())}"
        self.create_branch(branch)
        self.add_file_to_branch(branch, filename, content)
        return self.create_pull_request(branch, filename)