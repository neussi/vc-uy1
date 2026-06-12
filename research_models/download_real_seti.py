import os
import urllib.request
import sys

# Target directory
target_dir = "research_models/data_boinc/raw"
os.makedirs(target_dir, exist_ok=True)

# We use the cleaned tabbed format which is the standard for Failure Trace Archive research (2.15 GB)
url = "https://web.archive.org/web/20170215193011id_/http://fta.scem.uws.edu.au/data/seti09/seti09_tab.tgz"
archive_path = os.path.join(target_dir, "seti09_tab.tgz")

print("==========================================================")
print("📥 DOWNLOADING REAL & COMPLETE SETI@home (seti09) DATASET")
print("==========================================================")
print(f"Source URL: {url}")
print(f"Destination: {archive_path}")
print("File size: ~2.15 GB (This will take time depending on your connection...)")
print("----------------------------------------------------------")

try:
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    with urllib.request.urlopen(req) as response, open(archive_path, 'wb') as out_file:
        meta = response.info()
        file_size_str = meta.get("Content-Length")
        total_size = int(file_size_str) if file_size_str else None
        
        block_size = 1024 * 1024  # 1 MB blocks
        downloaded = 0
        
        while True:
            buffer = response.read(block_size)
            if not buffer:
                break
            downloaded += len(buffer)
            out_file.write(buffer)
            if total_size:
                percent = (downloaded / total_size) * 100
                print(f"Download Progress: {percent:.2f}% ({downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB)", end='\r')
            else:
                print(f"Download Progress: {downloaded / (1024*1024):.1f} MB downloaded...", end='\r')
                
        print("\n\n🎉 Download completed successfully!")
        print(f"File saved to: {archive_path}")
        print("To extract the files, you can run:")
        print(f"tar -xzf \"{archive_path}\" -C \"{target_dir}\"")

except KeyboardInterrupt:
    print("\n\n❌ Download cancelled by user.")
except Exception as e:
    print(f"\n\n❌ Error occurred: {e}")
print("==========================================================")
