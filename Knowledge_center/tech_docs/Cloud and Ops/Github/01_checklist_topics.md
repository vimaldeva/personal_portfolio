## Github

### Git Basics

- The Three States: Working Directory, Staging Area (Index), and Repository.
- Branching Strategy: Mastering main vs. feature vs. develop branches.
- Merging vs. Rebasing: Knowing when to use a "Merge Commit" (to keep history) vs. a "Rebase" (to keep a clean, linear history).
- Resolving Merge Conflicts: Learning how to read conflict markers and fix them without losing code.

---
### Collaboration & Code Quality (GitHub Specific)
In a professional DE team, you never push directly to main.

- Pull Requests (PRs): How to write a good PR description, link issues, and use "Draft PRs."
- Code Reviews: Using GitHub’s review tools to leave comments, suggest changes, and approve code.
- Branch Protection Rules: Setting up rules so no one can merge code without an approval or a passing test.
- GitHub Issues & Projects: Using Kanban boards to track data engineering tasks (e.g., "Fixing broken Airflow DAG").

---
### Automation (GitHub Actions for DE)
This is the most important skill for a modern Data Engineer.

- CI/CD Pipelines: Automatically testing your Python scripts or SQL code whenever you push.
- Automated Testing: Running pytest for your transformation logic or sqlfluff to lint your SQL.
- Deployment: Automatically deploying your code to AWS Lambda, Snowflake, or an Airflow environment.
- Secrets Management: Using GitHub Secrets to store API keys and database credentials securely (never hardcode them!).

---
### Summary Checklist for You:
- Can I resolve a merge conflict confidently?
- Do I know how to set up a GitHub Action to run a Python test?
- Do I understand the difference between a Squash Merge and a Regular Merge?
-  Am I keeping my credentials out of my repo using Secrets?