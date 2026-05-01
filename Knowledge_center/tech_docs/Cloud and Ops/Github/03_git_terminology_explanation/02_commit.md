### Commit
A commit in Git is a snapshot of your changes. It represents a point in the history of your project. Each commit has a unique identifier (a hash) and contains information about the changes made, the author, and a message describing the changes.

When you make changes to your files and want to save those changes in Git, you create a commit. This allows you to track the history of your project and revert back to previous states if needed.


without commit feature , you would not be able to keep a history of your changes, collaborate effectively with others, or manage different versions of your code. Commits are fundamental to Git's version control capabilities, enabling you to maintain a clear and organized history of your project's development.

Here are some common Git commands related to commits:
- `git commit -m "commit message"`: Create a new commit with the specified message.
- `git commit -a -m "commit message"`: Stage all changes and create a new commit with the specified message.
- `git log`: View the commit history of the repository.
- `git show <commit-hash>`: Show the details of a specific commit.
- `git revert <commit-hash>`: Create a new commit that undoes the changes made in the specified commit.
- `git reset --soft <commit-hash>`: Move the HEAD to the specified commit, keeping changes in the staging area.
- `git reset --hard <commit-hash>`: Move the HEAD to the specified commit, discarding all changes in the working directory and staging area.
- `git log --oneline`: Show a condensed view of the commit history, displaying only the commit hash and message.
- `git log --pretty=format:"%h - %an, %ar : %s"`: Show a custom format of the commit history, including the commit hash, author name, relative time, and commit message.