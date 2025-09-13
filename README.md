
# 🇮🇩 AbuseIPDB Indonesia Blocklist

> 🚦 **Efficient, Indonesia-focused blocklist for abusive IPs.**

---

## ✨ Description

This project provides a curated blocklist of the most reported abusive IP addresses from Indonesia, sourced from AbuseIPDB and related services. By focusing only on Indonesian IPs, the blocklist remains small, fast, and highly relevant for local security needs—perfect for firewalls, IDS, and other security systems.

---

## 🎯 Goals

- 🗜️ **Minimize blocklist size** by including only abusive IPs from Indonesia
- 🔒 **Easy integration** with local security systems
- ⏰ **Automated updates** blocklist updated every 6 hours

---

## ⚙️ How It Works

1. The Python script [`abuseipdb_id.py`](./abuseipdb_id.py) downloads blocklist data from [borestad/blocklist-abuseipdb](https://github.com/borestad/blocklist-abuseipdb).
2. Only IPs tagged with `# ID` (Indonesia) are filtered and included.
3. Filtered results are saved to output files (`abuseipdb-id-1d.txt`, `abuseipdb-id-7d.txt`, etc.) with a rich metadata header.
4. The workflow [`run-abuseipdb-id.yml`](.github/workflows/run-abuseipdb-id.yml) runs automatically every 6 hours and commits changes if any.

---

## 📦 Output Files

- `abuseipdb-id-1d.txt` — Last 1 day blocklist
- `abuseipdb-id-7d.txt` — Last 7 days blocklist
- `abuseipdb-id-14d.txt` — Last 14 days blocklist
- `abuseipdb-id-30d.txt` — Last 30 days blocklist

---

## 🙏 Credits

- Original script & data by [borestad](https://github.com/borestad/blocklist-abuseipdb)
- Abusive IP data by [AbuseIPDB](https://www.abuseipdb.com)
- IP & geolocation data by [ipinfo.io](https://ipinfo.io)
- Automation powered by [GitHub Actions](https://github.com/features/actions)

---

## 📄 License

See the LICENSE file for details on usage and distribution.

---

> If you use this blocklist, please support the original authors and the services above!
