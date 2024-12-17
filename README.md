# Karuta Auto Drop Bot

This project is a bot designed to automate the process of dropping and reacting to Karuta cards in a Discord channel. The bot uses `requests` library to interact with the Discord API.

## Features

- Drop Karuta cards in a specified Discord channel.
- React to the last dropped card with specified emojis.
- Add and manage multiple Discord accounts.
- Configure the channel ID and time interval between drops.

## Requirements

- Python 3.x
- PySide6
- requests

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Karuta-Auto-Drop-Botz.git
    cd Karuta-Auto-Drop-Botz
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirement.txt
    ```

## Usage

1. Run the bot:
    ```sh
    python main.py
    ```

2. Use the GUI to add Discord accounts and configure the bot settings.

## Files

- `main.py`: The main script that runs the bot and the GUI.
- `accounts.data`: Stores the Discord account names and tokens.
- `otherdata.data`: Stores the channel ID and time interval between drops.

## GUI Components

- **Name**: Input field for the custom account name.
- **Discord Account Token**: Input field for the Discord account token.
- **Add Bot**: Button to add the account to the list.
- **Start Bot**: Button to start the bot.
- **Channel ID**: Input field for the Discord channel ID.
- **Time Between Drops (s)**: Input field for the time interval between drops.
- **Confirm**: Button to save the drop settings.

## Contributing

Feel free to submit issues or pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License.
