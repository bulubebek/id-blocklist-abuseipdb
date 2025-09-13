import requests
import re
import os
from datetime import datetime

# Daftar pasangan URL dan nama file output
url_file_pairs = {
    'https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/refs/heads/main/abuseipdb-s100-30d.ipv4': 'abuseipdb-id-30d.txt',
    'https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/refs/heads/main/abuseipdb-s100-14d.ipv4': 'abuseipdb-id-14d.txt',
    'https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/refs/heads/main/abuseipdb-s100-7d.ipv4': 'abuseipdb-id-7d.txt',
    'https://raw.githubusercontent.com/borestad/blocklist-abuseipdb/refs/heads/main/abuseipdb-s100-1d.ipv4': 'abuseipdb-id-1d.txt'
}

# Template header
header_template = """#
# Aggregated Blocklist for AbuseIPDB: Indonesia most reported IP addresses.
#
# Number of ips:          {num_ips}
# Last updated:           {last_update}
#
# Source:                 https://github.com/borestad/blocklist-abuseipdb
# Stats:                  https://github.com/borestad/blocklist-abuseipdb/tree/main/stats
# Credits 1:              https://www.abuseipdb.com - please support them!
# Credits 2:              https://ipinfo.io - The Trusted Source For IP Address Data
#
"""

def get_lines_from_url(url):
    """Mengambil dan mem-parsing baris dari URL."""
    print(f'Mengunduh konten dari: {url}...')
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()
        
        valid_lines = []
        ipv4_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        
        for line in lines:
            line = line.strip()
            if '# ID' in line and ipv4_pattern.match(line):
                valid_lines.append(line)
                
        return sorted(valid_lines)
        
    except requests.exceptions.RequestException as e:
        print(f'Gagal mengunduh konten dari {url}: {e}')
        return None

def write_blocklist_file(lines, file_path):
    """Menulis header dan daftar baris IP ke file output."""
    if not lines:
        print(f"Tidak ada IP yang valid ditemukan untuk file {file_path}. Tidak membuat file.")
        return False

    num_ips = len(lines)
    last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = header_template.format(num_ips=num_ips, last_update=last_update)

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'File lama "{os.path.basename(file_path)}" berhasil dihapus.')

        with open(file_path, 'w') as f:
            f.write(header)
            for line in lines:
                f.write(f'{line}\n')
        print(f'File baru berhasil dibuat: {file_path}')
        print(f'Jumlah IP yang disimpan: {num_ips}')
        return True
    except IOError as e:
        print(f'Gagal menulis file: {e}')
        return False


def update_readme_stats(file_stats, timestamp):
    """Update blocklist statistics section in README.md."""
    readme_path = "README.md"
    stats_start = "<!-- blocklist-stats-start -->"
    stats_end = "<!-- blocklist-stats-end -->"
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read README.md: {e}")
        return

    stats_lines = [stats_start]
    stats_lines.append(f"Last check: {timestamp} (UTC)")
    for fname, count in file_stats.items():
        stats_lines.append(f"❯ {fname} ({count} ips)")
    stats_lines.append(stats_end)
    stats_block = "\n".join(stats_lines)

    # Replace or insert stats block
    if stats_start in content and stats_end in content:
        new_content = re.sub(f"{stats_start}.*?{stats_end}", stats_block, content, flags=re.DOTALL)
    else:
        # Insert after Output Files section
        marker = "## \U0001F4E6 Output Files"  # 📦
        idx = content.find(marker)
        if idx != -1:
            idx = content.find("---", idx)
            if idx != -1:
                idx += 3
                new_content = content[:idx] + "\n" + stats_block + "\n" + content[idx:]
            else:
                new_content = content + "\n" + stats_block
        else:
            new_content = content + "\n" + stats_block

    try:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md statistics updated.")
    except Exception as e:
        print(f"Failed to write README.md: {e}")


if __name__ == '__main__':
    file_stats = {}
    for url, filename in url_file_pairs.items():
        valid_lines = get_lines_from_url(url)
        if valid_lines:
            write_blocklist_file(valid_lines, filename)
            file_stats[filename] = len(valid_lines)
    # Update README.md stats
    timestamp = datetime.utcnow().strftime('%Y-%m-%d - %H:%M:%S')
    update_readme_stats(file_stats, timestamp)