import os
import yaml
import re

def parse_docstring(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        match = re.search(r"DOCUMENTATION\s*=\s*r'''(.*?)'''", content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
        else:
            return None

def generate_markdown(doc, file_name):
    markdown = f"# {doc['module']}\n\n"
    markdown += f"## {doc['short_description']}\n\n"

    for key, value in doc.items():
        if key not in ['module', 'short_description']:
            markdown += f"## {key}\n\n"
            if key == 'options':
                markdown += "| Name | Description | Required | Default |\n"
                markdown += "|------|-------------|----------|---------|\n"
                for option, details in value.items():
                    markdown += f"| {option} | {details['description'][0]} | {details.get('required', False)} | {details.get('default', 'N/A')} |\n"
            else:
                markdown += f"{value}\n\n"

    with open(f"{file_name}.md", 'w') as md_file:
        md_file.write(markdown)

def main():
    directory = "plugins/event_source/"
    for file in os.listdir(directory):
        if file.endswith(".py"):
            doc = parse_docstring(os.path.join(directory, file))
            if doc:
                file_name = os.path.splitext(file)[0]
                generate_markdown(doc, file_name)

if __name__ == "__main__":
    main()
