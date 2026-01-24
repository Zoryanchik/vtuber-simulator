from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder
import time
from config import Config

class NetworkSender:
    def __init__(self):
        print("Initializing Network Sender...")
        try:
            self.client = udp_client.SimpleUDPClient(Config.UnityIp, Config.UnityPort)
            self.connected = True # Just a flag
            print("Network sender is ready")
        except Exception as e:
            print(f"Failed to initialize Network Sender: {e}")
            self.connected = False
        
        self.packet_sent = 0
        self.last_send_time = 0
        self.send_interval = 1 / 60  # Send at 60 packets per s
   
    def send_face_data(self,data):
        if not self.connected:
            return

        current_time = time.time()
        if current_time - self.last_send_time < self.send_interval:
            return 

        try:
            # here we send the face data
            self.client.send_message("/face/mouth", float(data['mouth_open']))

            self.client.send_message("/face/eye_left", float(data['eye_left']))
            self.client.send_message("/face/eye_right", float(data['eye_right']))

            self.client.send_message("/face/head_x", float(data['head_x']))
            self.client.send_message("/face/head_y", float(data['head_y']))
            self.client.send_message("/face/happy", float(data['happy']))

            self.packet_sent += 1
            self.last_send_time = current_time
        except Exception as e:
            print(f"Error sending face data: {e}")
            self.connected = False

    def get_stats(self):
        return {
            'packets_sent': self.packet_sent,
            'connected': self.connected,
            'target_ip': Config.UnityIp,
            'target_port': Config.UnityPort         
        }
    
    def reconnect(self):
        try:
            self.client = udp_client.SimpleUDPClient(Config.UnityIp, Config.UnityPort)
            self.connected = True
            print("Reconnected to Unity.")
        except Exception as e:
            print(f"Reconnection failed: {e}")
            self.connected = False

if __name__ == "__main__":
    print("Testing NetworkSender...")
    sender = NetworkSender()

    if sender.connected:
        print("Sending test data...")
        test_data = {
            'mouth_open': 0.5,
            'eye_left': 0.2,
            'eye_right': 0.3,
            'head_x': 0.1,
            'head_y': -0.1
        }

        for i in range(10):
            sender.send_face_data(test_data)
            print(f"  Packet {i+1} sent")
            time.sleep(0.1)  # Send data every 100 ms

        stats = sender.get_stats()
        print(f"  Packets sent: {stats['packets_sent']}")
        print(f"  Target: {stats['target_ip']}:{stats['target_port']}")
        print("\nTest complete!")
    else:
        print("\nSender not connected")
