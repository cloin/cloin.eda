import os
import re

plugin_dir = "plugins/event_source/"
docs_dir = "docs/"

if not os.path.exists(docs_dir):
    os.makedirs(docs_dir)

for file in os.listdir(plugin_dir):
    if file.endswith(".py"):
        with open(os.path.join(plugin_dir, file), "r") as f:
            content = f.read()
            match = re.search(r'""".*?"""', content, re.DOTALL)

            if match:
                comment = match.group(0).strip('"""')
                lines = comment.split("\n")

                markdown = []
                table_header_created = False
                parsing_arguments = False

                for line in lines:
                    if line.startswith("## "):
                        markdown.append(f"### {line[3:]}\n")
                        if "## Arguments:" in line:
                            parsing_arguments = True
                        else:
                            parsing_arguments = False
                    elif line.startswith("    "):
                        if parsing_arguments:
                            if not table_header_created:
                                markdown.append("| Argument | Description |\n| --- | --- |\n")
                                table_header_created = True
                            arg_name, arg_desc = line[4:].split(": ", 1)
                            markdown.append(f"| {arg_name.strip()} | {arg_desc.strip()} |\n")
                        elif "## Example(s):" in markdown[-1]:
                            markdown.append("```yaml\n" + line[4:] + "\n")
                        else:
                            markdown.append(line[4:] + "\n")
                    else:
                        markdown.append(line + "\n")

                if "## Example(s):" in markdown[-1]:
                    markdown.append("```\n")

                with open(os.path.join(docs_dir, f"{file[:-3]}.md"), "w") as md_file:
                    md_file.writelines(markdown)

print("Markdown documentation generated successfully.")
