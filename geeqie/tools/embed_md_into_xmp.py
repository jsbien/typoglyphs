import os
import sys
import re
import xml.etree.ElementTree as ET

SCRIPT_VERSION = "3.3"

def extract_keywords_from_md(md_path):
    with open(md_path, encoding='utf-8') as f:
        lines = f.readlines()

    description = "".join(lines).strip()
    keywords = []

    for line in lines:
        match = re.match(r'^\s*([a-zA-Z0-9\-\s]+)="([^"]+)"', line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            keywords.append(f'{key}={value}')

    return description, keywords

def embed_metadata(xmp_path, md_path, output_path):
    description, keywords = extract_keywords_from_md(md_path)

    tree = ET.parse(xmp_path)
    root = tree.getroot()
    ns = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }

    desc_elem = root.find(".//dc:description/rdf:Alt", ns)
    if desc_elem is None:
        dc_desc = ET.SubElement(root.find(".//rdf:Description", ns), '{http://purl.org/dc/elements/1.1/}description')
        desc_elem = ET.SubElement(dc_desc, '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Alt')
    else:
        desc_elem.clear()

    ET.SubElement(desc_elem, '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li', {'xml:lang': 'x-default'}).text = description

    subj_elem = root.find(".//dc:subject/rdf:Bag", ns)
    if subj_elem is None:
        dc_subj = ET.SubElement(root.find(".//rdf:Description", ns), '{http://purl.org/dc/elements/1.1/}subject')
        subj_elem = ET.SubElement(dc_subj, '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Bag')
    else:
        subj_elem.clear()

    for kw in keywords:
        ET.SubElement(subj_elem, '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li').text = kw

    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"✅ Updated: {output_path}")

def find_matching_xmp(xmp_root_dir, base_name):
    expected_filename = f"{base_name}.png.gq.xmp"
    for dirpath, _, files in os.walk(xmp_root_dir, followlinks=True):
        for filename in files:
            if filename == expected_filename:
                return os.path.join(dirpath, filename)
    print(f"⚠️  No XMP found for {base_name} — expected: {expected_filename}")
    return None

def main(md_dir, xmp_root_dir, output_dir):
    print(f"\n🛠️ embed_md_into_xmp version {SCRIPT_VERSION}")
    print(f"📂 Markdown directory: {md_dir}")
    print(f"🔍 XMP root directory: {xmp_root_dir}")
    print(f"💾 Output directory:    {output_dir}\n")

    os.makedirs(output_dir, exist_ok=True)
    md_files = sorted(f for f in os.listdir(md_dir) if f.endswith('.md'))

    if not md_files:
        print("⚠️  No .md files found!")
        return

    for md_file in md_files:
        md_path = os.path.join(md_dir, md_file)
        base_name = os.path.splitext(md_file)[0]

        xmp_path = find_matching_xmp(xmp_root_dir, base_name)
        if xmp_path:
            output_path = os.path.join(output_dir, os.path.basename(xmp_path))
            print(f"🔗 Found match: {md_file} → {os.path.basename(xmp_path)}")
            embed_metadata(xmp_path, md_path, output_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: python {os.path.basename(__file__)} <md_dir> <xmp_root_dir> <output_dir>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
