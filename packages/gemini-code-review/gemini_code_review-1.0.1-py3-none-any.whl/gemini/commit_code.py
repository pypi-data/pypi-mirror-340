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



def analyze_code(parsed_diff: List[Dict[str, Any]] ) -> List[Dict[str, Any]]:
    file_diffs = []
    for file_data in parsed_diff:
        file_path = file_data.get('path', '')
        if not file_path or file_path == "/dev/null":
            continue
        class FileInfo:
            def __init__(self, path):
                self.path = path

        file_info = FileInfo(file_path)
        hunks = file_data.get('hunks', [])
        for hunk_data in hunks:
            hunk_lines = hunk_data.get('lines', [])
            if not hunk_lines:
                continue
            hunk = Hunk()
            hunk.source_start = 1
            hunk.source_length = len(hunk_lines)
            hunk.target_start = 1
            hunk.target_length = len(hunk_lines)
            hunk.content = '\n'.join(hunk_lines)
            file_diffs.append(create_prompt(file_info, hunk))
    diffs = '\n'.join(file_diffs)
    prompt = f"""
    You are to act as an author of a commit message in git.Your mission is to create clean and comprehensive commit messages following the @commitlint convention and explain WHAT changes were made and WHY. 
    I will send you the output of the 'git diff --staged' command, and you need to convert it into a commit message.

    Instructions:
    * The 'scope' should be the task ID part of your current branch name. For example, if your branch is 'feature/123', then the scope should be '123'.
    * Your current branch is: {os.popen('git branch --show-current').readline().strip()}.
    * Don't add any descriptions to the commit, only commit message.

    The output of 'git diff --staged' is:
    {diffs}

    Please generate a commit message conforming to the convention based on the above information.
    """
    print(prompt)
    return get_ai_response(prompt)


def create_prompt(file: PatchedFile, hunk: Hunk) -> str:
    return f"""
    File "{file.path}" :
    {hunk.content}
    """


def get_ai_response(prompt: str) -> List[Dict[str, str]]:
    """Sends the prompt to Gemini API and retrieves the response."""
    # Use 'gemini-2.0-flash-001' as a fallback default value if the environment variable isn't set
    gemini_model = Client.GenerativeModel(os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash'))

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 0.8,
        "top_p": 0.95,
    }
    response = gemini_model.generate_content(prompt, generation_config=generation_config)
    return response.text.strip()


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
                file_a = line[6:]
                if file_a != '/dev/null':
                    current_file['path'] = file_a

        elif line.startswith('+++ b/'):
            if current_file:
                file_b = line[6:]
                if file_b != '/dev/null':
                    current_file['path'] = file_b

        elif line.startswith('@@'):
            if current_file:
                current_hunk = {'header': line, 'lines': []}
                current_file['hunks'].append(current_hunk)

        elif current_hunk is not None:
            current_hunk['lines'].append(line)

    if current_file:
        files.append(current_file)

    return files


def main(code_diff_cmd):
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

    response = analyze_code(filtered_diff)
    print(response)


def command_git_commit():
    main(code_diff_cmd='git diff --staged')


if __name__ == "__main__":
    main(code_diff_cmd='cd /Users/xuwuqiang/PycharmProjects/psed && git diff --staged')
