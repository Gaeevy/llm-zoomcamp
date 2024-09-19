## Description
Provide a summary of what problem the PR is solving and how the code solves it.
Include any relevant documents/screenshots. If applicable, provide examples of usage.

## Pull Request Rules & Code Standards
Make sure your PR follows our [PR Rules](https://app.clickup.com/8699887/v/dc/89fzf-833/89fzf-184947?block=block-9806a7d1-3645-49fa-a472-9ad59cabe9ee) and our [Python Coding Standards](https://app.clickup.com/8699887/v/dc/89fzf-833/89fzf-1155?block=block-d3688b6d-d5e1-4e04-a4bf-37bb565c483c).

### Go through the following list and make sure all items are addressed:
1. Title your PR like so: **Name / PR description** e.g. John / Add task for DAG Alerts.
2. Your **pre-commit hooks are active** and commits in PR have been checked by hooks.
3. Before assigning reviews **perform a self-review on the changes** to apply fixes in advance that minimize the work for your reviewers.
4. **PR passes the CI/CD checks, unit tests**, and there are no issues such as Sonar or security vulnerabilities.
5. All functions/classes are **type hinted** and contain **helpful docstrings**.

## Tests
Please go through our [Testing Best Practices](https://app.clickup.com/8699887/v/dc/89fzf-833/89fzf-102830) for a comprehensive walkthrough.

In general, take time to test as much code as possible in order to test the correctness of your implementation as well as to secure against bugs in future iterations! As a rule of thumb, definitely write tests for:
 1. Non-trivial database queries. In addition to testing correctness, it shows the reader what the resulting table looks like.
 2. Non-trivial data manipulations. Avoid long functions which are hard to read and test. Split them into pure, single-purpose functions and test each of them.
 3. All functions/tasks that are on the rec-delivery path.
