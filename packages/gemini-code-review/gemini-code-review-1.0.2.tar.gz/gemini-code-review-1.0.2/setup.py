from setuptools import setup, find_packages

setup(
    name="gemini-code-review",
    version="1.0.2",
    keywords=("gitlab", "ai", "code review"),
    description="code review via diff",
    long_description="code review via diff with ai model",
    license="MIT Licence",

    url="https://xxx.com",
    author="xuwuqiang",
    author_email="xwqiang2008@outlook.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "google-ai-generativelanguage==0.6.10",
        "google-generativeai",
        "github3.py==1.3.0",
        "unidiff",
        "setuptools==65.6.3"
    ],

    scripts=[],
    # 如果出现 ModuleNotFoundError: No module named,用 py_modules
    py_modules=[],
    entry_points={
        'console_scripts': [
            'review = gemini.review_code:command_review',
            'commit = gemini.commit_code:command_git_commit'
        ]
    }
)
