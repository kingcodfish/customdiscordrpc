# Custom Discord RPC

A simple and customizable Discord Rich Presence client written in Python. This script allows you to display custom status, images, and buttons in your Discord profile.

## Requirements

- Python 3.6+
- `pypresence` library
- Discord desktop application

## Setup

1. Install the required dependency:
```bash
pip install pypresence
```

2. Create a Discord Application:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Copy the "Client ID" from the General Information page
   - Under "Rich Presence" > "Art Assets", upload your images (optional)

3. Configure the script:
   - Open `customdiscordrpc.py`
   - Replace `YOUR_CLIENT_ID_HERE` with your application's Client ID
   - Modify other configuration options in the `CONFIG` dictionary as needed

## Configuration Options

- `client_id`: Your Discord application's client ID
- `state`: The current state text
- `details`: Additional details text
- `large_image`: Key name of the large image asset
- `large_text`: Text shown when hovering over the large image
- `small_image`: Key name of the small image asset
- `small_text`: Text shown when hovering over the small image
- `buttons`: List of button objects with labels and URLs
- `start_time`: Timestamp for showing elapsed time

## Usage

Run the script:
```bash
python customdiscordrpc.py
```

To stop the script, press `Ctrl+C`.

## Features

- Customizable status text
- Support for large and small images
- Clickable buttons (up to 2)
- Elapsed time display
- Easy configuration
- Error handling and graceful shutdown

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to open issues or submit pull requests with improvements.
