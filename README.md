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

## facebook web
archive all chats
```
function getElementsByText(str, tag = 'a') {
  return Array.prototype.slice.call(document.getElementsByTagName(tag)).filter(el => el.textContent.trim() === str.trim());
}
function getElementByXpath(path) {
  return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function doIt(){
console.log("1");
    getElementsByText = function getElementsByText(str, tag = 'a') {
      return Array.prototype.slice.call(document.getElementsByTagName(tag)).filter(el => el.textContent.trim() === str.trim());
    }
getElementByXpath = function getElementByXpath(path) {
  return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

    document.querySelectorAll('[aria-label="Menu"]')[1].click();

    setTimeout(function(){
      getElementByXpath('//span[text()="Archive Chat" or text()="Archive chat"]').click();
    },1500);

    setTimeout(function(){
      getElementByXpath('//div[(@aria-label="Archive Chat" and @tabindex="0")or(@aria-label="Archive chat" and @tabindex="0")]').click();
    },1000);

}

var myInt = setInterval(function(){ doIt() }, 2000);
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

## ytdlp
download protected hsl / ts videos
```
yt-dlp -o filename.extension –referer {url} {inspect->network->filter(m3u8)->master…->copy->copy link address}
```
download audio with thumbnail
```
yt-dlp url --embed-thumbnail -f bestaudio -x --audio-format mp3 --audio-quality 320k
```
