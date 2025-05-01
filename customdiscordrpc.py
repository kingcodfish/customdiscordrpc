from pypresence import Presence
import time
import sys
from typing import Optional, Dict, Any
import logging

# Configuration
CONFIG = {
    # Required
    'client_id': 'YOUR_CLIENT_ID_HERE',  # Your Discord application client ID
    
    # Text Status (set to None to disable)
    'state': 'Currently Active',          # Current state text
    'details': 'Custom Status',           # Details text
    
    # Images (set to None to disable either image)
    'large_image': {
        'enabled': True,                  # Set to False to disable large image
        'key': 'default',                 # Large image key
        'text': 'Custom RPC'              # Large image hover text
    },
    'small_image': {
        'enabled': True,                  # Set to False to disable small image
        'key': 'status',                  # Small image key
        'text': 'Online'                  # Small image hover text
    },
    
    # Buttons (set to None or empty list to disable)
    'buttons': [
        {"label": "GitHub", "url": "https://github.com/yourusername"},
        {"label": "Website", "url": "https://yourwebsite.com"}
    ],
    
    # Timestamps
    'show_time': True,                    # Set to False to disable elapsed time
    'start_time': None,                   # Don't modify this - it's set automatically
    
    # Connection settings
    'max_retries': 3,                     # Maximum number of connection retries
    'retry_delay': 5                      # Delay between retries in seconds
}

# Set up root logger
logger = logging.getLogger('DiscordRPC')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class DiscordRPCError(Exception):
    """Custom exception for Discord RPC errors"""
    pass

class DiscordRPC:
    def __init__(self, client_id: str = CONFIG['client_id']):
        self.client_id = client_id
        self.rpc: Optional[Presence] = None
        self.connected = False
        self.logger = logger
        
    def connect(self, retries: int = CONFIG['max_retries']) -> bool:
        attempt = 0
        while attempt < retries:
            try:
                if not self.connected:
                    self.logger.info("Attempting to connect to Discord...")
                    self.rpc = Presence(self.client_id)
                    self.rpc.connect()
                    self.connected = True
                    self.logger.info("Successfully connected to Discord!")
                    return True
                return True  # Already connected
            except Exception as e:
                attempt += 1
                if attempt < retries:
                    self.logger.warning(f"Connection attempt {attempt} failed: {str(e)}")
                    self.logger.info(f"Retrying in {CONFIG['retry_delay']} seconds...")
                    time.sleep(CONFIG['retry_delay'])
                else:
                    self.logger.error(f"Failed to connect after {retries} attempts: {str(e)}")
                    self.logger.error("Please check:")
                    self.logger.error("1. Discord application is running")
                    self.logger.error("2. Client ID is correct")
                    self.logger.error("3. Internet connection is stable")
                    return False
            
    def _build_presence_data(self, **kwargs) -> Dict[str, Any]:
        """Build presence data dictionary based on enabled features"""
        presence_data = {}
        
        # Add state and details if enabled
        if CONFIG['state']:
            presence_data['state'] = kwargs.get('state', CONFIG['state'])
        if CONFIG['details']:
            presence_data['details'] = kwargs.get('details', CONFIG['details'])
            
        # Add large image if enabled
        if CONFIG['large_image'] and CONFIG['large_image']['enabled']:
            presence_data['large_image'] = kwargs.get('large_image', CONFIG['large_image']['key'])
            presence_data['large_text'] = kwargs.get('large_text', CONFIG['large_image']['text'])
            
        # Add small image if enabled
        if CONFIG['small_image'] and CONFIG['small_image']['enabled']:
            presence_data['small_image'] = kwargs.get('small_image', CONFIG['small_image']['key'])
            presence_data['small_text'] = kwargs.get('small_text', CONFIG['small_image']['text'])
            
        # Add buttons if enabled and not empty
        if CONFIG['buttons'] and len(CONFIG['buttons']) > 0:
            presence_data['buttons'] = kwargs.get('buttons', CONFIG['buttons'])
            
        # Add timestamp if enabled
        if CONFIG['show_time']:
            presence_data['start'] = kwargs.get('start_time', CONFIG['start_time'])
            
        return presence_data
            
    def update_presence(self, **kwargs) -> bool:
        if not self.connected:
            self.logger.warning("Not connected to Discord. Attempting to reconnect...")
            if not self.connect():
                return False
            
        try:
            presence_data = self._build_presence_data(**kwargs)
            self.rpc.update(**presence_data)
            return True
        except Exception as e:
            self.logger.error(f"Failed to update presence: {str(e)}")
            self.connected = False
            return False
            
    def close(self):
        try:
            if self.rpc and self.connected:
                self.rpc.close()
                self.connected = False
                self.logger.info("Discord RPC connection closed successfully")
        except Exception as e:
            self.logger.error(f"Error while closing connection: {str(e)}")

def main():
    try:
        rpc = DiscordRPC()
        
        if not rpc.connect():
            logger.error("Initial connection failed. Please check your configuration and try again.")
            return
        
        update_count = 0
        while True:
            if rpc.update_presence(start_time=time.time() if CONFIG['show_time'] else None):
                if update_count == 0:
                    logger.info("Discord Rich Presence is now active. Press Ctrl+C to exit.")
                update_count += 1
            else:
                logger.warning("Lost connection. Attempting to reconnect...")
                if not rpc.connect():
                    logger.error("Reconnection failed. Waiting before next attempt...")
                    time.sleep(CONFIG['retry_delay'])
            time.sleep(15)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
    finally:
        if 'rpc' in locals():
            rpc.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        sys.exit(1)
