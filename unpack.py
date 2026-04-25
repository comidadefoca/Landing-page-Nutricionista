import json
import re

bundle_file = "Dra. Marina Castro - Nutricionista.html"
template_file = "template.html"
output_file = "index.html"

# Read the bundled file
with open(bundle_file, "r", encoding="utf-8") as f:
    bundle_content = f.read()

# Extract the manifest
start_marker = "<script type=\"__bundler/manifest\">"
end_marker = "</script>"
start_idx = bundle_content.find(start_marker)
if start_idx == -1:
    print("Manifest not found!")
    exit(1)

start_idx += len(start_marker)
end_idx = bundle_content.find(end_marker, start_idx)
manifest_json = bundle_content[start_idx:end_idx].strip()

# Parse the manifest
manifest = json.loads(manifest_json)

# Read the template
with open(template_file, "r", encoding="utf-8") as f:
    template_content = f.read()

# Replace UUIDs in template with base64 data URIs from manifest
for uuid, file_info in manifest.items():
    if isinstance(file_info, dict) and "mime" in file_info and "data" in file_info:
        data_uri = "data:" + file_info["mime"] + ";base64," + file_info["data"]
        template_content = template_content.replace(uuid, data_uri)

# Also fix the script tags inside template_content that we escaped earlier
template_content = template_content.replace("<\\/script>", "</script>")

# Write the final static HTML file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(template_content)

print(f"Successfully unpacked the project to {output_file}!")
