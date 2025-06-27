import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Connect to parser and embedder
from ai_bot.indexer.document_parser import parse_file
from ai_bot.indexer.embedder import embed_and_store

WATCH_FOLDER = "input_files"

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"📄 New file detected: {event.src_path}")
            self.process(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"✏️ File modified: {event.src_path}")
            self.process(event.src_path)

    def process(self, file_path):
        print(f"🧪 Starting to process: {file_path}")
        try:
            text_chunks = parse_file(file_path)
            print(f"🧾 Extracted {len(text_chunks)} chunks")
            embed_and_store(file_path, text_chunks)
            print(f"✅ Done processing {file_path}")
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

def start_watcher():
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"👀 Watching folder: {WATCH_FOLDER}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
