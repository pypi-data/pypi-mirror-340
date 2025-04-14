import json
from pathlib import Path
from screeninfo import get_monitors

class Settings():
    """Settings Manager to save and apply settings to the software."""
    def __init__(self):
        self._channel_url = 'https://www.youtube.com/@GabbPiano'
        self._directory = Path.home() / 'Desktop'
        self._bg_color = ('#C5D9F1', '#FDE9D9')
        self._bg_highlight = True
        self._max_sheets = 250
        self._date_format = 'DD/MM/YYYY'
        self._oldest_to_newest = True
        self._auto_update = True
        self._window_size = (100, 100, 320, 170)
    
    @property
    def channel_url(self):
        """URL of the YouTube channel."""
        return self._channel_url
    
    @channel_url.setter
    def channel_url(self, value):
        if value is None:
            self._channel_url = 'https://www.youtube.com/@GabbPiano'
            return
        elif not isinstance(value, str):
            raise TypeError(
                f"The channel URL must be a string, not {type(value)}"
                )
        self._channel_url = str(value)

    @property
    def directory(self):
        """Directory where the files will be saved."""
        return self._directory
    
    @directory.setter
    def directory(self, value):
        if value is None:
            return
        else:
            path = Path(value)
        
        if path.exists() and path.is_dir():
            self._directory = path
        else:
            raise ValueError(
                f"The directory {value} does not exist"
                )

    @property
    def bg_color(self):
        """Hex color code for the background of the comments on Excel."""
        return self._bg_color

    @bg_color.setter
    def bg_color(self, value):
        if (len(value) != 2
            or not isinstance(value, tuple)
            or not isinstance(value[0], str)
            or not isinstance(value[1], str)
            ):
            raise ValueError(
                "The value must be a tuple of two strings"
                )
        elif not (value[0].startswith('#') and len(value[0]) == 7):
            raise ValueError(
                "The first value must be a valid hex color code"
                )
        elif not (value[1].startswith('#') and len(value[1]) == 7):
            raise ValueError(
                "The second value must be a valid hex color code"
                )
        self._bg_color = value

    @property
    def bg_highlight(self):
        """Allow or not the background color to be highlighted."""
        return self._bg_highlight

    @bg_highlight.setter
    def bg_highlight(self, value):
        if not isinstance(value, bool):
            print("bg highlight value must be a boolean, default value will be used")
            return
        self._bg_highlight = value

    @property
    def max_sheets(self):
        """Maximum number of sheets per file to export."""
        return self._max_sheets

    @max_sheets.setter
    def max_sheets(self, value):
        if not isinstance(value, int):
            raise ValueError(
                "The maximum number of sheets must be an integer"
                )
        elif value < 2:
            raise ValueError(
                "The maximum number of sheets must be at least 2"
                )
        self._max_sheets = value

    @property
    def date_format(self):
        """Format of the date in the comments."""
        return self._date_format

    @date_format.setter
    def date_format(self, value):
        if not isinstance(value, str):
            raise ValueError(
                "the date format must be a string. E.g: 'DD/MM/YY' ; 'YYYY-MM-DD'"
                )
        self._date_format = value

    @property
    def oldest_to_newest(self):
        """Sort comments from oldest to newest."""
        return self._oldest_to_newest

    @oldest_to_newest.setter
    def oldest_to_newest(self, value):
        if not isinstance(value, bool):
            print("oldest to newest value must be a boolean, default value will be used")
            return
        self._oldest_to_newest = value

    @property
    def auto_update(self):
        """Allow or not the GUI to search for software updates at startup."""
        return self._auto_update

    @auto_update.setter
    def auto_update(self, value):
        if not isinstance(value, bool):
            print("auto update value must be a boolean, default value will be used")
            return
        self._auto_update = value

    @property
    def window_size(self):
        """Size of the GUI window."""
        return self._window_size

    @window_size.setter
    def window_size(self, value):
        if not isinstance(value, tuple):
            return
        elif len(value) != 4:
            return
        
        # Check if the coordinates are within monitors coordinates
        monitors = get_monitors()
        x_min = 0
        y_min = 0
        x_max = 0
        y_max = 0
        for monitor in monitors:
            if monitor.x < x_min:
                x_min = monitor.x
            if monitor.y < y_min:
                y_min = monitor.y
            if monitor.x + monitor.width > x_max:
                x_max = monitor.x + monitor.width
            if monitor.y + monitor.height > y_max:
                y_max = monitor.y + monitor.height
        
        x_margin = 0
        y_margin = 0
        if value[0] < x_min + x_margin or value[0] + value[2] > x_max - x_margin:
            self._window_size = (100, 100, 320, 170)
            return
        if value[1] < y_min + y_margin or value[1] + value[3] > y_max - y_margin:
            self._window_size = (100, 100, 320, 170)
            return
        
        self._window_size = value

    def path_save(self):
        """Path to the saved parameters file."""
        file = "yt_parameters.json"
        folder = "Atem83"
        path_file = Path.home() / "Documents" / folder / file
        return path_file

    def save(self):
        """Save the parameters in a configuration file."""
        settings = {
            'channel_url': self.channel_url,
            'directory': str(self.directory),
            'bg_color': self.bg_color,
            'bg_highlight': self.bg_highlight,
            'max_sheets': self.max_sheets,
            'date_format': self.date_format,
            'oldest_to_newest': self.oldest_to_newest,
            'auto_update': self.auto_update,
            'window_size': self.window_size
            }
        path_file = self.path_save()

        try:
            # Create the folder if it doesn't exist
            path_folder = Path(path_file).parent
            path_folder.mkdir(parents=True, exist_ok=True)

            # Write my backup
            with open(path_file, 'w', encoding='utf-8') as file:
                json.dump(settings, file, indent=4, ensure_ascii=False)
        except:
            print("Save failed.")
            return

    def load(self):
        """Load the parameters from the configuration file."""
        path_file = self.path_save()
        try:
            with open(path_file, "r", encoding='utf-8') as file:
                settings = json.load(file)
                self.channel_url = settings["channel_url"]
                self.directory = settings["directory"]
                self.bg_color = tuple(settings["bg_color"])
                self.bg_highlight = settings["bg_highlight"]
                self.max_sheets = settings["max_sheets"]
                self.date_format = settings["date_format"]
                self.oldest_to_newest = settings["oldest_to_newest"]
                self.auto_update = settings["auto_update"]
                self.window_size = tuple(settings["window_size"])
        except:
            print("Load failed, the parameters by default will be used.")
            return
