from github import Github
import base64
import time

# GitHub credentials
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
OWNER = "YOUR_USERNAME"
REPO_NAME = "YOUR_REPO_NAME"

BASE_BRANCH = "main"
NUM_PRS = 100
COMMIT_MESSAGE = "Fake commit for PR test"

g = Github(GITHUB_TOKEN)
repo = g.get_repo(f"{OWNER}/{REPO_NAME}")

for i in range(1, NUM_PRS + 1):
    try:
        branch_name = f"fake-branch-{i}"
        print(f"Creating branch: {branch_name}")

        # Always use the latest commit from main
        main_sha = repo.get_branch(BASE_BRANCH).commit.sha
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_sha)

        # Create a unique file for each PR
        file_path = f"fake_file_PR{i}.txt"
        file_content = f"This is fake PR #{i}.\n"

        repo.create_file(file_path, COMMIT_MESSAGE, file_content, branch=branch_name)
        print(f"✅ Committed {file_path} in {branch_name}")

        # Create pull request
        pr_title = f"Fake PR #{i}"
        pr_body = f"This is an auto-generated fake PR number {i}."
        pr = repo.create_pull(title=pr_title, body=pr_body, head=branch_name, base=BASE_BRANCH, draft=False)

        print(f"Created PR: {pr.html_url}")

        # Wait for GitHub to process mergeability
        time.sleep(2)
        pr.update()

        if pr.mergeable:
            pr.merge(commit_message="Auto-merging fake PR", merge_method="squash")
            print(f"✅ Merged PR #{i}")
        else:
            print(f"⚠️ PR #{i} has merge conflicts. Skipping auto-merge.")

        # Delete the branch
        repo.get_git_ref(f"heads/{branch_name}").delete()
        print(f"🗑️ Deleted branch {branch_name}")
        time.sleep(1)

    except Exception as e:
        print(f"❌ Error in PR #{i}: {e}")

print("✅ Finished processing all PRs!")