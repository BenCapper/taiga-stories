# taiga-stories

Creates GitHub issues based off a Taiga export.
Must be a fresh repo with no prior issues created.

Enter your GitHub Personal Access Token
~~~
git = Github('TOKEN')
~~~

Enter the GitHUb repo namespace
~~~
repo = git.get_repo('USERNAME/REPO_NAME')
~~~

Enter the exported Taiga export name
~~~
t = open('JSON_FILE')
~~~

Run
