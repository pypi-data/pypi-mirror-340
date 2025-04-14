import argparse
import json
import os
import random
import time
from typing import List, Dict, Any
import google.generativeai as Client
import fnmatch
from unidiff import Hunk, PatchedFile, PatchSet

gemini_client = Client.configure(api_key=os.environ.get('GEMINI_API_KEY'))


class PRDetails:
    def __init__(self, owner: str, repo: str, pull_number: int, title: str, description: str):
        self.owner = owner
        self.repo = repo
        self.pull_number = pull_number
        self.title = title
        self.description = description


def analyze_code(parsed_diff: List[Dict[str, Any]], pr_details: PRDetails) -> List[Dict[str, Any]]:
    print("Starting analyze_code...")
    print(f"Number of files to analyze: {len(parsed_diff)}")
    comments = []

    for file_data in parsed_diff:
        file_path = file_data.get('path', '')
        print()
        print()
        print(f"\nProcessing file: {file_path}")

        if not file_path or file_path == "/dev/null":
            continue

        class FileInfo:
            def __init__(self, path):
                self.path = path

        file_info = FileInfo(file_path)

        hunks = file_data.get('hunks', [])

        for hunk_data in hunks:
            # print(f"\nHunk content: {json.dumps(hunk_data, indent=2)}")
            hunk_lines = hunk_data.get('lines', [])
            # print(f"Number of lines in hunk: {len(hunk_lines)}")

            if not hunk_lines:
                continue

            hunk = Hunk()
            hunk.source_start = 1
            hunk.source_length = len(hunk_lines)
            hunk.target_start = 1
            hunk.target_length = len(hunk_lines)
            hunk.content = '\n'.join(hunk_lines)

            prompt = create_prompt(file_info, hunk, pr_details)
            # print("Sending prompt to Gemini...")
            print("```diff")
            print(hunk.content)
            print("```")
            ai_response = get_ai_response(prompt)
            # print(f"AI response received: {ai_response}")

            if ai_response:
                new_comments = create_comment(file_info, hunk, ai_response)
                if new_comments:
                    comments.extend(new_comments)
                    # print(f"Updated comments list: {comments}")

    print(f"\nFinal comments list: {json.dumps(comments)}")
    return comments


def create_prompt(file: PatchedFile, hunk: Hunk, pr_details: PRDetails) -> str:
    return f"""Your task is reviewing pull requests. Instructions:
    - Provide the response in following JSON format:  {{"reviews": [{{"lineNumber":  <line_number>, "reviewComment": "<review comment>"}}]}}
    - Provide comments and suggestions ONLY if there is something to improve, otherwise "reviews" should be an empty array
    - Use GitHub Markdown in comments
    - Focus on bugs, security issues, and performance problems
    - IMPORTANT: NEVER suggest adding comments to the code
    - IMPORTANT: The project is mainly about code refactoring, paying particular attention to the changes in the original logic during the refactoring process

Review the following code diff in the file "{file.path}" and take the pull request title and description into account when writing the response.

Pull request title: {pr_details.title}
Pull request description:

---
{pr_details.description or 'No description provided'}
---

Git diff to review:

```diff
{hunk.content}
```
"""


def get_ai_response(prompt: str) -> List[Dict[str, str]]:
    """Sends the prompt to Gemini API and retrieves the response."""
    # Use 'gemini-2.0-flash-001' as a fallback default value if the environment variable isn't set
    gemini_model = Client.GenerativeModel(os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash-001'))

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 0.8,
        "top_p": 0.95,
    }

    try:
        response = gemini_model.generate_content(prompt, generation_config=generation_config)

        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove ```
        response_text = response_text.strip()

        # print(f"Cleaned response text: {response_text}")

        try:
            data = json.loads(response_text)

            if "reviews" in data and isinstance(data["reviews"], list):
                reviews = data["reviews"]
                valid_reviews = []
                for review in reviews:
                    if "lineNumber" in review and "reviewComment" in review:
                        valid_reviews.append(review)
                    else:
                        print(f"Invalid review format: {review}")
                return valid_reviews
            else:
                print("Error: Response doesn't contain valid 'reviews' array")
                print(f"Response content: {data}")
                return []
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Raw response: {response_text}")
            return []
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        time.sleep(15)
        return []


class FileInfo:
    """Simple class to hold file information."""

    def __init__(self, path: str):
        self.path = path


def create_comment(file: FileInfo, hunk: Hunk, ai_responses: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Creates comment objects from AI responses."""
    # print("AI responses in create_comment:", ai_responses)
    # print(f"Hunk details - start: {hunk.source_start}, length: {hunk.source_length}")
    # print(f"Hunk content:\n{hunk.content}")

    comments = []
    for ai_response in ai_responses:
        try:
            line_number = int(ai_response["lineNumber"])
            print(f"Original AI suggested line: {line_number}")

            # Ensure the line number is within the hunk's range
            if line_number < 1 or line_number > hunk.source_length:
                print(f"Warning: Line number {line_number} is outside hunk range")
                continue

            comment = {
                "body": ai_response["reviewComment"],
                "path": file.path,
                "position": line_number
            }
            print()
            print(f"Created comment: {ai_response['reviewComment']}")
            comments.append(comment)

        except (KeyError, TypeError, ValueError) as e:
            print(f"Error creating comment from AI response: {e}, Response: {ai_response}")
    return comments


def parse_diff(diff_str: str) -> List[Dict[str, Any]]:
    """Parses the diff string and returns a structured format."""
    files = []
    current_file = None
    current_hunk = None

    for line in diff_str.splitlines():
        if line.startswith('diff --git'):
            if current_file:
                files.append(current_file)
            current_file = {'path': '', 'hunks': []}

        elif line.startswith('--- a/'):
            if current_file:
                current_file['path'] = line[6:]

        elif line.startswith('+++ b/'):
            if current_file:
                current_file['path'] = line[6:]

        elif line.startswith('@@'):
            if current_file:
                current_hunk = {'header': line, 'lines': []}
                current_file['hunks'].append(current_hunk)

        elif current_hunk is not None:
            current_hunk['lines'].append(line)

    if current_file:
        files.append(current_file)

    return files


def main(title, description, code_diff_cmd):
    pr_details = PRDetails('None', 'None', None, title, description=description)

    # 生成随机字符串
    tmp_file = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 8))
    os.system(f"{code_diff_cmd} > /tmp/{tmp_file}")
    with open(f"/tmp/{tmp_file}") as f:
        diff = f.read()
    parsed_diff = parse_diff(diff)

    exclude_patterns = []
    filtered_diff = []
    for file in parsed_diff:
        file_path = file.get('path', '')
        should_exclude = any(fnmatch.fnmatch(file_path, pattern) for pattern in exclude_patterns)
        if should_exclude:
            print(f"Excluding file: {file_path}")  # Debug log
            continue
        filtered_diff.append(file)

    analyze_code(filtered_diff, pr_details)


def command_review():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', '-t',
                        help='Title of your changes')
    parser.add_argument('--description', '-d', default='No description provided',
                        help='Description of your changes')
    parser.add_argument('--command', '-c', help='Command for git diff, eg: git diff production')
    args = parser.parse_args()
    main(args.title, args.description, args.command)


if __name__ == "__main__":
    main(title='钱包精度调整', description='No description provided',
         code_diff_cmd='cd /Users/xuwuqiang/Documents/workspace/game/tkl-wallet-service && git diff production')
