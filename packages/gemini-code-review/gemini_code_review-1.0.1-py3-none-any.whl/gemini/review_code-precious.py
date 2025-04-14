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
            get_ai_response(prompt)



def create_prompt(file: PatchedFile, hunk: Hunk, pr_details: PRDetails) -> str:
    return  f"""
        你是一位资深Java编程专家，gitlab的分支代码变更将以git diff 字符串的形式提供，请你帮忙review本段代码。然后你review内>容的返回内容必须严格遵守下面的格式，包括标题内容。
        模板中的变量内容解释：
        变量5为: 代码中的优点。
        变量1:给review打分，分数区间为0~100分。
        变量2：code review发现的问题点。
        变量3：具体的修改>建议。
        Instructions:
        1. 以精炼的语言、严厉的语气指出存在的问题。
        2. 你的反馈内容必须使用严谨的markdown格式 
        3. 不要携带变量内容解释信息。
        4. 有清晰的标题结构。有清晰的标题结构。有清晰的标题结构。
        5. IMPORTANT：本次代码主要是对原有逻辑的重构，请确保逻辑没有变化。
        6. IMPORTANT: 请确保代码中跟钱有关的如balance，如果有setBalance(a) 的地方都会有 setPrecisionBalance(b),eg.
            如果看到setWalletEvent(amount) 则需要有 setPrecisionWalletEvent(amount).如果没有找到，在变量6 中体现,找到了则在变量6中展示为NULL
        7. IMPORTANT: 请确保代码中是否存在赋值错误的地方，如果存在，在变量7 中体现，否则变量7展示为NULL,例如：
            a.setX(b.getX) 错误的写成了 a.setX(b.getY)，
            a.setX(b.getSomeX) 错误的写成了 a.setX(b.getSomeY)
        
        返回格式严格如下：

        ### 😀代码评分：
        [变量1]

        #### ✅代码优点：
        [变量5]

        #### 🤔问题点：
        [变量2]

        #### 🎯修改建议：
        [变量3]

        ### 逻辑缺失
        [变量6]

        ### 赋值错误
        [变量7]
        
        Code diff in the file "{file.path}" to review:
        Pull request title: {pr_details.title}
        Pull request description: {pr_details.description or 'No description provided'}

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
        print(response_text)
    except Exception as e:
        time.sleep(15)


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
    # main(title='钱包精度调整', description='No description provided',
         # code_diff_cmd='cd /Users/xuwuqiang/Documents/workspace/game/tkl-wallet-service && git diff production')
     main(title='多维度数据统计', description='No description provided',
    code_diff_cmd='cd /Users/xuwuqiang/Documents/workspace/game/tkl-riskctl-service && git show 743076dbe324288a41b58fd9769793feeb4a7257')
