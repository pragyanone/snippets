# snippets

## android
automatically delete old files by matching filename
```
names="
contact1,
contact2,
"

# Initialize the find command
find_command="find /storage/emulated/0/Call -type f -mtime +6"

# Set IFS to comma and loop over each name
IFS=','  # Treat comma and space as delimiters
first=true
for name in $names; do
  # Trim leading/trailing whitespace from each name
  name=$(echo $name | xargs)

  # For the first name, add the opening parenthesis and start the condition
  if $first; then
    find_command="$find_command \( -name '*_${name}.oga'"
    first=false
  else
    find_command="$find_command -o -name '*_${name}.oga'"
  fi
done

# Close the parentheses and add the delete action
find_command="$find_command \) -exec rm {} \;"

# Echo the final command
echo $find_command

# Uncomment below to actually execute the command after testing
eval $find_command
```

## autodesk
fix Licence issue due to updating of Current link

syntax:
```
mklink /d <link> <target>
```
example:
```
mklink /d “C:\Program Files (x86)\Common Files\Autodesk Shared\AdskLicensing\Current” “C:\Program Files (x86)\Common Files\Autodesk Shared\AdskLicensing\13.0.0.8122”
```

## messenger web
archive all chats
```
function getElementsByText(str, tag = 'a') {
  return Array.prototype.slice.call(document.getElementsByTagName(tag)).filter(el => el.textContent.trim() === str.trim());
}

function getElementByXpath(path) {
  return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function doIt() {
  console.log("1");
  
  // Find menu button that starts with "More options for"
  const menuButtons = Array.from(document.querySelectorAll('[aria-label^="More options for"]'));
  
  if (menuButtons.length > 0) {
    menuButtons[0].click();

    setTimeout(function() {
      getElementByXpath('//span[text()="Archive Chat" or text()="Archive chat"]')?.click();
    }, 1500);

    setTimeout(function() {
      getElementByXpath('//div[(@aria-label="Archive Chat" and @tabindex="0") or (@aria-label="Archive chat" and @tabindex="0")]')?.click();
    }, 1000);
  }
}

var myInt = setInterval(doIt, 2000);
```


## ffmpeg
compress (sequential)
```
for %f in (*.mp4) do ffmpeg_cuda -n -i "%f" -c:v libx264 -preset ultrafast -crf 30 -c:a aac -b:a 128k -movflags +faststart -an "compressed\_%~nf.mp4"
```
compress (parallel)
```
for %f in (*.mp4) do start /B ffmpeg_cuda -n -i "%f" -c:v libx264 -preset ultrafast -crf 30 -c:a aac -b:a 128k -movflags +faststart -an "compressed\_%~nf.mp4"
```

embed thumbnail in mp3
```
ffmpeg -i in.mp3 -i test.png -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" out.mp3
```

## windows
safely remove hardware
```
RunDll32.exe shell32.dll,Control_RunDLL hotplug.dll
```

delete duplicates from a subdirectory like Downloads
```
import os
import hashlib
from send2trash import send2trash

# Define paths
target_folder = os.path.abspath(r"E:/dir1/dir2")
search_root = os.path.abspath(r"E:/")
excluded_dirs = {
    os.path.abspath(r"E:/$RECYCLE.BIN"),
    target_folder,
}

# Function to calculate SHA-256 hash of a file
def get_file_hash(file_path, chunk_size=8192):
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# Step 1: Scan entire search_root excluding selected dirs
existing_hashes = set()
print("\n--- Scanning Files for Hashing ---")
for root, _, files in os.walk(search_root):
    if any(
        root.startswith(excluded) for excluded in excluded_dirs
    ):  # Skip excluded directories
        continue
    for file in files:
        file_path = os.path.join(root, file)
        file_hash = get_file_hash(file_path)
        if file_hash:
            existing_hashes.add(file_hash)
            file_size = os.path.getsize(file_path)
            print(f"Scanned: {file_path} ({file_size / (1024**2):.2f} MB)")

# Step 2: Scan target folder, move duplicates to recycle bin, and calculate total size
total_size = 0  # Track total size of trashed files
print("\n--- Checking for Duplicates & Moving to Recycle Bin ---")

for root, _, files in os.walk(target_folder):
    for file in files:
        file_path = os.path.join(root, file)
        file_hash = get_file_hash(file_path)
        if file_hash in existing_hashes:
            file_size = os.path.getsize(file_path)  # Get file size
            total_size += file_size  # Add to total size
            print(
                f"Moving to Recycle Bin: {file_path} ({file_size / (1024**2):.2f} MB)"
            )
            send2trash(file_path)  # Move to Recycle Bin

# Print total size of trashed files
print(f"\nTotal size of trashed files: {total_size / (1024**2):.2f} MB")

```


## web
paste using javascript
```
document.addEventListener("click", function(event) {
    let inputBox = document.activeElement; // Get the currently focused input field
    if (inputBox && (inputBox.tagName === "INPUT" || inputBox.tagName === "TEXTAREA")) {
        let text = `Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Nam ante justo, dictum vitae enim quis, consequat tincidunt ipsum.`;
        inputBox.value = text; // Insert text into the input box
    }
});
```

## ytdlp
download protected hsl / ts videos
```
yt-dlp -o filename.extension –referer {url} {inspect->network->filter(m3u8)->master…->copy->copy link address}
```
download audio with thumbnail
```
yt-dlp url --embed-thumbnail -f bestaudio -x --audio-format mp3 --audio-quality 320k
```
