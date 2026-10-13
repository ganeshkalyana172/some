from pathlib import Path
import shutil

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi"},
    "Audio": {".mp3", ".wav", ".aac", ".flac"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Programs": {".py", ".java", ".c", ".cpp", ".html", ".css", ".js", ".php"},
}

def category(path):
    for name, extensions in CATEGORIES.items():
        if path.suffix.lower() in extensions:
            return name
    return "Others"

def unique_path(path):
    if not path.exists(): return path
    n = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{n}{path.suffix}")
        if not candidate.exists(): return candidate
        n += 1

def main():
    folder = Path(input("Enter folder path: ").strip().strip('"')).expanduser()
    if not folder.is_dir():
        print("Error: folder not found."); return
    files = [p for p in folder.iterdir() if p.is_file()]
    if not files:
        print("No files found."); return
    print("\nPreview:")
    for p in files: print(f"{p.name} -> {category(p)}/")
    if input("\nType YES to organize these files: ").strip() != "YES":
        print("Cancelled; no files moved."); return
    moved = 0
    for p in files:
        try:
            target_dir = folder / category(p)
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(p), str(unique_path(target_dir / p.name)))
            moved += 1
        except OSError as e: print(f"Could not move {p.name}: {e}")
    print(f"Done: organized {moved}/{len(files)} files.")

if __name__ == "__main__": main()
