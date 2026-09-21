import os
import sys
import subprocess
import requests
from google import genai

print("--- AI Code Reviewer Starting ---")

def get_git_diff() -> str:
    base_ref = os.getenv("GITHUB_BASE_REF", "main")
    print(f"Base branch: {base_ref}")

    try:
        subprocess.run(["git", "fetch", "origin", base_ref], check=True)
    except Exception as e:
        print(f"Git fetch error: {e}")

    cmd = ["git", "diff", f"origin/{base_ref}...HEAD"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    diff = result.stdout.strip()
    return diff

def analyze_diff_with_gemini(diff_text: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[Error] GEMINI_API_KEY is not set.")
        sys.exit(1)

    print("Sending diff to Gemini...")
    client = genai.Client(api_key=api_key)
    prompt = f"""
You are an expert Principal Software Engineer performing a PR review.
Carefully review the following git diff and output markdown feedback:

1. 🚨 **Critical Bugs & Security Flaws**
2. ⚡ **Performance & Optimization**
3. 💡 **Code Quality Suggestions**
4. 🛠️ **Recommended Fixes**

Git Diff:
```diff
{diff_text}
"""
response = client.models.generate_content(
model="gemini-2.5-flash",
contents=prompt
)
return response.text

def post_github_comment(review_body: str):
token = os.getenv("GITHUB_TOKEN")
repo = os.getenv("GITHUB_REPOSITORY")
pr_num = os.getenv("PR_NUMBER")
print(f"Posting comment to PR #{pr_num} on {repo}...")
url = f"https://api.github.com/repos/{repo}/issues/{pr_num}/comments"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {
    "body": f"## 🤖 Gemini AI Code Review\n\n{review_body}\n\n---\n*Automated review run by Gemini.*"
}
resp = requests.post(url, json=payload, headers=headers)
if resp.status_code == 201:
    print("[Success] Review posted successfully!")
else:
    print(f"[Error] Failed to post comment ({resp.status_code}): {resp.text}")
    sys.exit(1)
def main():
diff = get_git_diff()
print(f"Diff character length: {len(diff)}")

if not diff:
    print("[Notice] No diff found between branches. Skipping review.")
    return

if len(diff) > 40000:
    diff = diff[:40000] + "\n\n[Diff truncated]"

review = analyze_diff_with_gemini(diff)
post_github_comment(review)
if name == "main":
main()
