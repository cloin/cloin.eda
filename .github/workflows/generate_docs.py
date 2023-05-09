import os
import re
from pathlib import Path

def parse_doc_section(doc_section):
    lines = doc_section.strip().split('\n')
    file_name = lines[0].strip()
    args_start = lines.index("Arguments:") + 1
    args_end = lines.index("Example(s):")
    args = [arg.strip().split(':', 1) for arg in lines[args_start:args_end] if arg.strip()]
    example = '\n'.join(lines[args_end+1:])

    return file_name, args, example

def generate_markdown(file_name, args, example):
    markdown = f"# {file_name}\n\n"

    if args:
        markdown += "## Arguments\n\n"
        markdown += "| Argument | Description |\n"
        markdown += "| -------- | ----------- |\n"
        for arg in args:
            markdown += f"| {arg[0].strip()} | {arg[1].strip()} |\n"
        markdown += "\n"

    markdown += "## Example(s)\n\n"
    markdown += f"```yaml\n{example}\n```\n"

    return markdown

def main():
    source_dir = Path("plugins/event_source")
    docs_dir = Path("docs")

    for python_file in source_dir.glob("*.py"):
        with open(python_file, 'r') as f:
            content = f.read()

        doc_section = re.search(r'""".*?"""', content, re.DOTALL)
        if doc_section:
            file_name, args, example = parse_doc_section(doc_section.group(0))
            markdown = generate_markdown(file_name, args, example)

            md_file_path = docs_dir / f"{python_file.stem}.md"
            with open(md_file_path, 'w') as f:
                f.write(markdown)

if __name__ == "__main__":
    main()
