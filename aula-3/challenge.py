import threading
import urllib.request
import os
import time
from typing import List, Tuple

class FileDownloader:
    """A class that handles concurrent file downloads using threads."""
    
    def __init__(self, urls: List[Tuple[str, str]]):
        """
        Initialize the downloader with a list of URLs.
        
        Args:
            urls: List of tuples (url, filename) where url is the download link 
                 and filename is what the file will be saved as
        """
        self.urls = urls
        self.threads = []
    
    def download_file(self, url: str, filename: str):
        """
        Download a file from a URL and save it to the specified filename.
        
        Args:
            url: The URL to download from
            filename: The filename to save the downloaded file as
        """
        try:
            print(f"Starting download of {url} -> {filename}")
            start_time = time.time()
            urllib.request.urlretrieve(url, filename)
            elapsed_time = time.time() - start_time
            print(f"Downloaded {filename} in {elapsed_time:.2f} seconds")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
    
    def start_downloads(self):
        """Start all downloads concurrently using threads."""
        for url, filename in self.urls:
            thread = threading.Thread(target=self.download_file, args=(url, filename))
            self.threads.append(thread)
            thread.start()
    
    def wait_for_completion(self):
        """Wait for all download threads to complete."""
        for thread in self.threads:
            thread.join()
        print("All downloads completed!")

def main():
    # Create a download directory if it doesn't exist
    download_dir = "aula-3/downloads"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # Example URLs to download
    urls = [
        ("https://www.python.org/static/img/python-logo.png", f"{download_dir}/python-logo.png"),
        ("https://www.python.org/static/community_logos/python-powered-h-140x182.png", f"{download_dir}/python-powered.png"),
        ("https://www.python.org/static/community_logos/python-powered-w-200x80.png", f"{download_dir}/python-powered-w.png"),
        ("https://www.python.org/static/community_logos/python-powered-h-50x65.png", f"{download_dir}/python-powered-small.png"),
        ("https://www.python.org/static/favicon.ico", f"{download_dir}/python-favicon.ico"),
    ]
    
    # Start the downloader
    downloader = FileDownloader(urls)
    print("Starting concurrent downloads...")
    downloader.start_downloads()
    downloader.wait_for_completion()

if __name__ == "__main__":
    main()