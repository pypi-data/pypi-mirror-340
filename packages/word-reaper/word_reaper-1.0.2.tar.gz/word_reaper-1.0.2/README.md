

<h1 align="left">WordReaper v1.0.2 <img src="assets/scythe.png" width="64"/></h1>




⚠️ **NOTICE: This project is in early development and not yet ready for production use. Features may change, break, or be incomplete. Use at your own risk.**


> Reap & Forge Wordlists for Password Cracking  
> By `d4rkfl4m3z`

![wordreaper help menu](https://raw.githubusercontent.com/Nemorous/word-reaper/main/screenshots/banner.jpg)

---

## 💡 What is Word Reaper?

**WordReaper** is a powerful, modular tool for generating, mutating, and combining wordlists — ideal for use in redteaming and CTFs.

It supports:

- 🕸️ HTML scraping (with tag/class/id filtering)
- 🐙 GitHub/Gist wordlist pulling (`raw.githubusercontent.com` and `gist.githubusercontent.com`)
- 📁 Local file loading and mentalist-style mutations
- 🔄 Hashcat-style mask-based permutations
- ⚔️ Merging and combining wordlists like a pro

---

## 🚀 Install

### 🔧 Clone & Install Locally

```bash
git clone https://github.com/Nemorous/word-reaper.git
cd word-reaper
pip install .
```

### 📦 Install via PyPI (Optional)
```bash
pip install word-reaper
```

---

## ⚙️ Usage

### 📥 HTML Scraping with Tag/Class/ID Filtering
```bash
wordreaper --method html --url https://example.com --tag a --class content
```

### 🐙 GitHub Scraping
Supports both GitHub raw and Gist raw URLs:
```bash
wordreaper --method github --url https://raw.githubusercontent.com/username/repo/main/file.txt
wordreaper --method github --url https://gist.githubusercontent.com/username/gistid/raw/commitid/file.txt
```

### 📁 Local File Loading
```bash
wordreaper --method file --input wordlist.txt
```

---

## 🧠 Wordlist Mutations & Permutations

```bash
wordreaper --mentalize --input input.txt --output mutated.txt \
--leet --toggle --underscores --append-mask ?d?d --increment
```

Supports:
- ✅ Leetspeak (`--leet`)
- ✅ Case toggling (`--toggle`)
- ✅ Separators: `--underscores`, `--spaces`, `--hyphens`)
- ✅ Permutations: `--append-mask`, `--prepend-mask`, `--synchronize`, `--increment`

---

## 🧰 Other Features

### 🪓 Reaper ASCII Art
```bash
wordreaper --ascii-art
```

### 📦 Merge Multiple Wordlists
```bash
wordreaper --merge file1.txt file2.txt file3.txt ... -o merged.txt
```

### ⚔️ Combinator
```bash
wordreaper --combinator adjectives.txt nouns.txt -o combos.txt
```

---

## 📝 Changelog

See [`CHANGELOG.md`](CHANGELOG.md)

---

## 📁 License

MIT

---

## 🤝 Contributions

PRs and issues welcome! Add new scrapers, modules, or mutation strategies.

Made with ☕ and 🔥 By d4rkfl4m3z

