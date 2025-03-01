# AutoLinker 🔗

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)

Automate personalized LinkedIn networking at scale with intelligent connection management.

**👉 Important:** Use responsibly and comply with [LinkedIn's User Agreement](https://www.linkedin.com/legal/user-agreement).  
**⚠️ Warning:** Always maintain human-like interaction patterns to avoid account restrictions.

## Table of Contents
- [Key Features](#key-features)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [Usage](#usage)
- [LinkedIn Account Limitations](#linkedin-account-limitations)
- [Output Structure](#output-structure)
- [Contributing](#contributing)
- [License](#license)

## Key Features ✨

| Feature                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| 🚀 Bulk Processing     | Handle hundreds of profiles across multiple companies simultaneously       |
| 🎯 Smart Filtering     | Target specific roles using LinkedIn search query parameters               |
| 📊 Progress Tracking   | Real-time CSV logging with automatic resume capabilities                   |
| 🔒 Chrome Profile Sync | Maintain persistent LinkedIn session using your existing Chrome profile    |

## Installation Guide 🛠️

### Prerequisites
- Google Chrome (latest stable version)
- Active LinkedIn account
- Python 3.8+ with pip

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/baderanaas/AutoLinker.git
   cd AutoLinker
   ```

2. **Install Dependencies**
   ```bash
   # Using Makefile (recommended)
   make install

   # Manual installation
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```ini
   PROFILE_PATH=C:/Users/<YourUsername>/AppData/Local/Google/Chrome/User Data/Default
   ```

## Configuration ⚙️

### 1. Create `companies.csv`
Example (`data/companies.csv`):
```csv
Link,Message,Note,Done
https://www.linkedin.com/company/<company-name>/people/?param=4512,"Hi, How are you?","Let's collaborate!",No
```

| Column   | Format                                  | Example                              |
|----------|-----------------------------------------|--------------------------------------|
| Link     | URL-encoded LinkedIn people search      | `/company/<company-name>/people/?param=4512` |
| Message  | Connection message                      | `Hi, How are you?`           |
| Note     | Optional connection note                | `Let's collaborate!`                 |
| Done     | Auto-updated completion status          | `No`/`Yes`                           |

### 2. Configure Account Type
Edit `main.py`:
```python
autoLinker(link, message, note, premium=True)  # Set False for basic accounts
```

## Usage 🚀

This will run headless:
```bash
# Using Makefile (recommended)
make run

# Run Manually
python main.py
```

### Display Chrome Window
If you want to see the browser instead of running headless, comment out the following line in `autoLinker.py`:
```python
options.add_argument("--headless=new")
```

### Execution Flow:
1. Reads `companies.csv` input
2. Processes 5-7 profiles/minute (human-like pacing)
3. Generates individual company reports
4. Updates master CSV with completion status

## LinkedIn Account Limitations 🔒

AutoLinker is 100% open-source and free to use. The following limitations are imposed by LinkedIn:

| Capability               | LinkedIn Premium | LinkedIn Basic |
|--------------------------|------------------|----------------|
| Connection Notes         | ✅ Unlimited    | ❌ 3/month     |
| Daily Connection Limit    | 100             | 40             |
| Search Rate              | ✅ Unlimited     | ❌ Limited     |
| API Rate Limits          | Higher          | Standard       |

**Important Notes:**
- 🚀 AutoLinker has no premium version - all features are free.
- 🔓 These limitations are set by LinkedIn, not by AutoLinker.
- ⚠️ Free users can send connection notes but are limited by LinkedIn.
- 📈 Actual limits may vary based on LinkedIn's policies.

## Output Structure 📂

```
📦 Companies
 ┣ 📜 Google.csv
 ┣ 📜 Microsoft.csv
 ┗ 📜 StartupXYZ.csv
```

### Sample CSV Output:
```csv
Company,Profile Name,Profile Link,Company Link,Send Message, Date
Google,John Doe,https://linkedin.com/in/johndoe,https://linkedin.com/company/google,True,2025-03-01T11:46:48
```

### Advanced Debugging
```bash
# Generate detailed logs
tail -f auto_linker.log
```

## Contributing 🤝

We welcome contributions! Follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License 📄

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.

---

**Ethical Note:** This tool is designed to enhance professional networking, not spam. Maintain genuine interaction patterns and respect connection recipients' privacy.
