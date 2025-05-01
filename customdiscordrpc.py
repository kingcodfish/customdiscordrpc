from pypresence import Presence
import time
import sys
from typing import Optional
import logging

# Configuration
CONFIG = {
    'client_id': 'YOUR_CLIENT_ID_HERE',  # Your Discord application client ID
    'state': 'Currently Active',          # Current state text
    'details': 'Custom Status',           # Details text
    'large_image': 'default',             # Large image key
    'large_text': 'Custom RPC',           # Large image hover text
    'small_image': 'status',              # Small image key
    'small_text': 'Online',               # Small image hover text
    'buttons': [
        {"label": "GitHub", "url": "https://github.com/yourusername"},
        {"label": "Website", "url": "https://yourwebsite.com"}
    ],
    'start_time': None,                   # Set to time.time() for elapsed time
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
            
    def update_presence(self, **kwargs) -> bool:
        if not self.connected:
            self.logger.warning("Not connected to Discord. Attempting to reconnect...")
            if not self.connect():
                return False
            
        try:
            presence_data = {
                'state': kwargs.get('state', CONFIG['state']),
                'details': kwargs.get('details', CONFIG['details']),
                'large_image': kwargs.get('large_image', CONFIG['large_image']),
                'large_text': kwargs.get('large_text', CONFIG['large_text']),
                'small_image': kwargs.get('small_image', CONFIG['small_image']),
                'small_text': kwargs.get('small_text', CONFIG['small_text']),
                'buttons': kwargs.get('buttons', CONFIG['buttons']),
                'start': kwargs.get('start_time', CONFIG['start_time'])
            }
            
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
            if rpc.update_presence(start_time=time.time()):
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
