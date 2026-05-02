### Branch Protection
Branch protection is a feature in GitHub that allows repository administrators to enforce certain rules and restrictions on specific branches. This is particularly useful for maintaining the integrity of important branches, such as `main` or `master`, by preventing unauthorized changes and ensuring that code reviews are conducted before any modifications are made.

Branch protection rules can include requirements such as:
- Requiring pull request reviews before merging
- Requiring status checks to pass before merging
- Restricting who can push to the branch
- Enabling signed commits
- Requiring linear history (no merge commits)

By implementing branch protection, teams can ensure that their codebase remains stable and that all changes are properly reviewed and tested before being integrated into critical branches. This is an essential practice for maintaining code quality and fostering collaboration in a team environment.

Branch protection is typically configured in the repository settings under the "Branches" section, where administrators can specify which branches to protect and what rules to apply. It is a crucial tool for teams that want to enforce best practices and maintain a high standard of code quality in their projects.

---
List of Branch protection rules avaialble (in addition to above)

- Restrict creations :Only allow users with bypass permission to create matching refs.
- Restrict updates : Only allow users with bypass permission to update matching refs.
- Restrict deletions :Only allow users with bypass permissions to delete matching refs.
- Require linear history :Prevent merge commits from being pushed to matching refs.
- Require code quality results :Choose which severity levels of code quality results should block pull request merges. When configured, a code quality analysis must be done on the pull request before the changes can be merged.
- Automatically request Copilot code review :Request Copilot code review for new pull requests automatically if the author has access to Copilot code review and their premium requests quota has not reached the limit.