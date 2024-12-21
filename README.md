# League-Of-Legends-Overlay
 Simple Overlay for League of Legends with custom functions

## Installation

To run this project, you'll need to install the following Python libraries. You can do this by running the following command:

```bash
pip install requests python-dotenv pygetwindow psutil
```

### Explanation of Required Libraries:
- **`requests`**: For making HTTP requests.
- **`python-dotenv`**: To manage environment variables stored in `.env` files.
- **`pygetwindow`**: For window manipulation.
- **`psutil`**: To retrieve information on system utilization (CPU, memory, etc.).

These dependencies are necessary to ensure all functionalities of the project work correctly.

You also need to change the target in the shortcut to League of Legends in order to make sure it is initalized whenever league is booted up.
To do this right click the shortcut, click on Properties and paste the following command in the target section:
```bash
C:\Windows\System32\cmd.exe /K title Overlay && start "" "C:\Riot Games\Riot Client\RiotClientServices.exe" --launch-product=league_of_legends --launch-patchline=live & python "C:\Path\To\Project\main.py"
```

Finally, set up the requiered enviroment variables(recommended as a .env file):
DIRECTORY: Path to the League of Legends .exe
PROGRAM_DIRECTORY: Path to this github repo