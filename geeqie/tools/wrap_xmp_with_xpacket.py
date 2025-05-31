import os
import sys

SCRIPT_VERSION = "1.1"

XPACKET_START = '<?xpacket begin="\uFEFF" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'
XPACKET_END = '<?xpacket end="w"?>'

def wrap_file_with_xpacket(path, in_place=True, output_dir=None):
    with open(path, encoding='utf-8') as f:
        content = f.read()

    if '<?xpacket' in content:
        print(f"⚠️  Already wrapped: {path}")
        return

    lines = content.lstrip().splitlines()

    if lines and lines[0].startswith('<?xml'):
        xml_decl = lines[0] + '\n'
        body = '\n'.join(lines[1:])
    else:
        xml_decl = '<?xml version="1.0" encoding="utf-8"?>\n'
        body = content.strip()

    wrapped_content = (
        xml_decl +
        XPACKET_START +
        body.strip() + '\n' +
        XPACKET_END
    )

    if in_place:
        output_path = path
    else:
        rel_path = os.path.relpath(path, start=os.path.commonpath([path, output_dir]))
        output_path = os.path.join(output_dir, rel_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(wrapped_content)

    print(f"✅ Wrapped: {output_path}")

def process_xmp_directory(directory, in_place=True, output_dir=None):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.xmp'):
                full_path = os.path.join(root, file)
                wrap_file_with_xpacket(full_path, in_place, output_dir)

if __name__ == "__main__":
    print(f"\n📦 wrap_xmp_with_xpacket v{SCRIPT_VERSION}")

    if len(sys.argv) not in [2, 3]:
        print("Usage:")
        print("  In-place:      python wrap_xmp_with_xpacket.py <xmp_dir>")
        print("  To other dir:  python wrap_xmp_with_xpacket.py <xmp_dir> <output_dir>")
        sys.exit(1)

    xmp_dir = sys.argv[1]
    if len(sys.argv) == 3:
        out_dir = sys.argv[2]
        process_xmp_directory(xmp_dir, in_place=False, output_dir=out_dir)
    else:
        process_xmp_directory(xmp_dir)
