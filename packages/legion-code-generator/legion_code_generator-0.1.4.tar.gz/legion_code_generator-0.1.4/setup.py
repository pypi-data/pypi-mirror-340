from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="legion-code-generator",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "openai>=0.11.5",
        "python-dotenv>=1.0.0",
        "termcolor>=2.3.0",
        "pytest>=7.4.0",
        "setuptools>=42.0.0",
        "pathlib>=1.0.1",
        "typing-extensions>=4.0.0"
    ],
    entry_points={
        "console_scripts": [
            "legion-code-generator=legion_code_generator.agent:main",
        ],
    },
    author="Legion/Chinmay Singh",
    author_email="chinmaysingh619@gmail.com",
    description="A terminal-based AI coding agent for assisting with development tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.8",
    keywords="ai, code, generator, terminal, development, gpt, openai, gemini",
) 