#!/usr/bin/env python3

from pypresence import Presence
import time
import sys

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
    'start_time': None                    # Set to time.time() for elapsed time
}

class DiscordRPC:
    def __init__(self, client_id=CONFIG['client_id']):
        self.client_id = client_id
        self.rpc = None
        
    def connect(self):
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            return True
        except Exception as e:
            print(f"Failed to connect to Discord: {e}")
            return False
            
    def update_presence(self, **kwargs):
        if not self.rpc:
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
            print(f"Failed to update presence: {e}")
            return False
            
    def close(self):
        if self.rpc:
            self.rpc.close()

def main():
    rpc = DiscordRPC()
    
    if not rpc.connect():
        sys.exit(1)
    
    try:
        while True:
            rpc.update_presence(start_time=time.time())
            time.sleep(15)  # Discord has a rate limit, don't update too frequently
    except KeyboardInterrupt:
        rpc.close()
        print("\nDiscord RPC closed successfully")

if __name__ == "__main__":
    main()
