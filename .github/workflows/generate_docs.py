import os
import re
from pathlib import Path

def parse_doc_section(doc_section):
    lines = doc_section.strip().split('\n')[1:-1]  # Remove the """ lines
    headings = [i for i, line in enumerate(lines) if line.strip().startswith('## ')]

    sections = {}
    for i, start in enumerate(headings):
        end = headings[i + 1] if i + 1 < len(headings) else len(lines)
        key = lines[start].strip()[3:]  # Remove '## ' from the heading
        value = '\n'.join(lines[start + 1:end]).strip()
        sections[key] = value

    return sections

def generate_markdown(sections):
    markdown = ""
    for key, value in sections.items():
        markdown += f"## {key}\n\n"
        if key == "Arguments":
            markdown += "| Argument | Description |\n"
            markdown += "| -------- | ----------- |\n"
            for arg in value.split('\n'):
                arg_name, arg_desc = arg.split(':', 1)
                markdown += f"| {arg_name.strip()} | {arg_desc.strip()} |\n"
        elif key == "Example(s)":
            markdown += f"```yaml\n{value}\n```\n"
        else:
            markdown += f"{value}\n"
        markdown += "\n"
    return markdown

def main():
    source_dir = Path("plugins/event_source")
    docs_dir = Path("docs")

    for python_file in source_dir.glob("*.py"):
        with open(python_file, 'r') as f:
            content = f.read()

        doc_section = re.search(r'""".*?"""', content, re.DOTALL)
        if doc_section:
            sections = parse_doc_section(doc_section.group(0))
            markdown = generate_markdown(sections)

            md_file_path = docs_dir / f"{python_file.stem}.md"
            with open(md_file_path, 'w') as f:
                f.write(markdown)

if __name__ == "__main__":
    main()
