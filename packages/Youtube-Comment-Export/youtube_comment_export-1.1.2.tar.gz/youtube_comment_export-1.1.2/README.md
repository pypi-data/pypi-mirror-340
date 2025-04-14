<h1 align="center">Youtube Comment Export</h1>

<h3 align="center">Export the comments of a YouTube channel in Excel files.</h3>

<div align="center">
    
  [![PyPI](https://img.shields.io/pypi/v/Youtube-Comment-Export?style=flat)](https://pypi.org/project/Youtube-Comment-Export)
  <a href="https://opensource.org/license/mit">![License](https://img.shields.io/badge/License-MIT-blue)</a>
  <a href="https://github.com/Atem83/Youtube-Comment-Export/archive/refs/heads/main.zip">![Download](https://img.shields.io/badge/Source_Code-Download-blue)</a>
  ![LOC](https://tokei.rs/b1/github/Atem83/Youtube-Comment-Export?category=lines)
  
</div>

<div align="center">
  <div style="display: flex; justify-content: space-around;">
    <img src="https://raw.githubusercontent.com/Atem83/Youtube-Comment-Export/main/images/GUI light theme.png" alt="GUI Light Theme" style="width: 35%;">
    <img src="https://raw.githubusercontent.com/Atem83/Youtube-Comment-Export/main/images/GUI dark theme.png" alt="GUI Dark Theme" style="width: 35%;">
  </div>
</div>

<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/Atem83/Youtube-Comment-Export/main/images/GUI Settings.png" alt="GUI Settings" style="width: 35%;">
</div>

<h2 align="center"> Excel Main Sheet </h2>

<div align="center">
  <img src="https://raw.githubusercontent.com/Atem83/Youtube-Comment-Export/main/images/Excel videos sheet.png" alt="Excel videos sheet" style="width: 100%;">
</div>

<h2 align="center"> Excel Comments Sheet </h2>

<div align="center">
  <img src="https://raw.githubusercontent.com/Atem83/Youtube-Comment-Export/main/images/Excel comments sheet.png" alt="Excel comments sheet" style="width: 100%;">
</div>

<h2 align="center"> Features </h2>

- Download data from a YouTube channel
- Download comments from a YouTube channel
- Export the data and comments in Excel files in a nice format
- Light ou Dark theme according to your OS theme
- Import old saves, this way :
  - you can keep a more precise date of the comments
  - you can keep comments even if they have been deleted
  - sadly, it will not be possible to save downloading time because all the comments needs to be downloaded again

<h2 align="center"> Installation </h2>

<div align="center">

```
pip install Youtube-Comment-Export
```

[<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Atem83/Youtube-Comment-Export?&color=green&label=Source%20Code&logo=Python&logoColor=yellow&style=for-the-badge"  width="300">](https://github.com/Atem83/Youtube-Comment-Export/archive/refs/heads/main.zip)

</div>

<br>

<h1 align="center"> GUI App </h1>

<h2 align="center"> From the software </h2>

Download the .exe software from [here](https://github.com/Atem83/Youtube-Comment-Export/releases/latest) and launch it.

<h2 align="center"> From a CLI </h2>

```bash
ytComments-gui
```

<h2 align="center"> From a Python script </h2>

```python
import ytComments

app = ytComments.App()
app.run()
```

<br>

<h1 align="center"> Python API </h1>

<h2 align="center"> Introduction </h2>

```python
import ytComments

# Settings
url = 'https://www.youtube.com/@GabbPiano'

# Initialize the instance
yt = ytComments.yt_manager(url)

# Needed to download the data from the url
yt.refresh()

# Export the comments in Excel
yt.export_excel()
```

<h2 align="center"> Settings </h2>

```python
import ytComments

### You can use these settings at initialization ###

# Youtube Channel URL or Youtube Video URL
url = 'https://www.youtube.com/@GabbPiano/videos'

# Directory to save the Excel files
dir = 'C:\Users\User\Desktop'

# Path of the old save files
path_save1 = r'C:\Users\User\Desktop\Save File 1.xlsx'
path_save2 = r'C:\Users\User\Desktop\Save File 2.xlsx'
path_save = [path_save1, path_save2]

# Initialize the instance
yt = ytComments.yt_manager(
  channel_url=url, 
  directory=dir,
  old_save=path_save
  )

# Needed to download the data from the url
yt.refresh()

# Merging the old save data with the new downloaded data
yt.import_excel()

# Export the comments in Excel
yt.export_excel()
```

```python
### You can also set these settings later ###

yt.old_save = path_save
yt.settings.channel_url = url
yt.settings.directory = dir

## Some additional settings are available too

# Swap color on Excel for each thread of comments
yt.settings.bg_color = ('#C5D9F1', '#FDE9D9')

# Allow or not the background color to be highlighted
yt.settings.bg_highlight = True

# Maximum number of sheets per file to export
# If the number of videos exceeds this number, the data will be split into multiple Excel files
yt.settings.max_sheets = 250

# Date format in the comments
yt.settings.date_format = 'DD/MM/YYYY'
yt.settings.date_format = 'MM-DD-YY'

# Sort comments from oldest to newest = True
# Sort comments from newest to oldest = False
yt.settings.oldest_to_newest = True
```

<h2 align="center"> Class variables </h2>

```python
# Raw data downloaded from the YouTube Channel
data = yt.channel_data

# Processed videos data of the channel 
# Format : polars.DataFrame
data = yt.channel_videos(include_comments=True)

# Processed videos data of the channel 
# Format : list of dictionaries for each row
data = yt.channel_videos(include_comments=True).to_dicts()

# You can also get the comments in a list format :
for video in data:
  video['comments'] = video['comments'].to_dicts()

# Title of the YouTube Channel
data = yt.channel_title

# ID of the YouTube Channel
data = yt.channel_id

# Total duration of the channel videos
data = yt.channel_total_duration

# Total views of the channel videos
data = yt.channel_total_views

# Number of videos of the channel
data = yt.channel_number_videos
```