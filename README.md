> ATP/WTA Tennis Tour Rankings

---

## Installation
```Python
chmod +x scraper.py
./scraper.py [-h] (-m | -w | -b) [-n NUM] [-r]
```

## Flags

| Flag | Description | Default
| :--- | :--- | :--- |
| **`-h` / `--help`** | Help | |
| **`-m` / `--mens`** | ATP rankings only | |
| **`-w` / `--womens`** | WTA rankings only | |
| **`-b` / `--both`** | Both ATP & WTA rankings | |
| **`-n NUM` / `--num NUM`** | Top NUM players | 10 |
| **`-r` / `--reverse`** | Sort in reverse order |

---

Examples:
    View the top 15 ATP men's players:
    ```Bash
    ./scraper.py -m -n 15
    ```

    View the top 20 WTA women's players in reverse order:
    ```Bash
    ./scraper.py -w -n 20 -r
    ```

    Display both ATP and WTA leaderboards:
    ```Bash
    ./scraper.py -b -n 10
    ```
