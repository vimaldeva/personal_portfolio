### Squash
Squash is a Git technique used to combine multiple commits into a single commit. This is often done to clean up a commit history before merging a feature branch into the main branch. Squashing can help make the commit history more concise and easier to understand, especially when a feature branch has many small commits that may not be meaningful on their own.

When you squash commits, you take a series of commits and combine them into one commit that represents the overall changes made in those commits. This can be done using an interactive rebase, where you can choose which commits to squash together.

The advantage of squashing commits is that it can help to create a cleaner and more organized commit history. It allows you to group related changes together and remove unnecessary commits that may have been made during the development process. This can make it easier for others to understand the changes being made when they review the commit history.

In summary, squash is a useful technique in Git for combining multiple commits into a single commit to create a cleaner and more organized commit history. It can help to group related changes together and remove unnecessary commits, making it easier for others to understand the changes being made in a feature branch before merging it into the main branch.


---
**Scenario** : But this is the same thing that rebase does right ?

While both squash and rebase can be used to clean up commit history, they serve different purposes. Rebase is primarily used to move or combine commits onto a new base commit, while squash is specifically focused on combining multiple commits into a single commit.