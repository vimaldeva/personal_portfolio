### Fetch

**Definition**: `git fetch` is a command that retrieves updates from a remote repository without merging them into your local branch. It allows you to see changes made by others before deciding to integrate them.
**Usage**: When you run `git fetch`, Git contacts the remote repository and downloads any new commits, branches, or tags that have been added since your last fetch. However, it does not automatically merge these changes into your current branch. Instead, it updates your remote tracking branches, allowing you to review the changes before incorporating them.

```bash
git fetch <remote-name>
```
**Key Points**:
- `git fetch` updates your local copy of the remote repository without altering your working directory or current branch.
- It allows you to review changes from the remote repository before merging them into your local branch.

While both `git fetch` and `git pull` are used to update your local repository with changes from a remote repository, they serve different purposes:
- `git fetch` retrieves updates from the remote repository but does not merge them into your current branch. This allows you to review the changes before deciding to integrate them.
- `git pull` is a combination of `git fetch` followed by `git merge`. It retrieves updates from the remote repository and immediately merges them into your current branch. This can lead to merge conflicts if there are changes that conflict with your local work.

In summary, `git fetch` is useful when you want to see what changes have been made in the remote repository without affecting your current work, while `git pull` is a more direct way to update your local branch with changes from the remote repository.