import time
import traceback

# wifi_radio_obj must implement:
# connect(ssid,passwd)
# ping(addr)
# ipv4_gateway
# ipv4_address

class NetworkBase:
    def __init__(self, secrets, wifi_radio_obj=None, wifi_state_change_cb=None, sleep_func=None, debug=False):
        self.secrets = secrets
        self.wifi = wifi_radio_obj
        if self.wifi is None:
            import wifi
            self.wifi = wifi.radio
        if wifi_state_change_cb is None:
            self.wifi_state_change_cb = lambda state: None
        else:
            self.wifi_state_change_cb = wifi_state_change_cb    
        if sleep_func is None:
            self.sleep = time.sleep
        else:
            self.sleep = sleep_func
    def _connect(self):
        self.wifi_state_change_cb(False)
        ssid = self.secrets["ssid"]
        passwd = self.secrets["password"]
        while True:
            try:
                print(f"Connecting to {ssid}")
                self.wifi.connect(ssid, passwd)
                if self._check_connection():
                    break
                else:
                    raise RuntimeError("Connected, but failed connection check!")
            except Exception as e:
                print(f"Exception when trying to connect:")
                traceback.print_exception(None, e, e.__traceback__)
                self.sleep(0.5)
        print(f"Connected with ip: {self.wifi.ipv4_address}")
        self.wifi_state_change_cb(True)
    def _check_connection(self):
        latency = None
        try:
            latency = self.wifi.ping(self.wifi.ipv4_gateway)
            if self.debug:
                print(f"Current latency: {latency}")
        except Exception as e:
            print(f"Exception when trying to ping gateway:")
            traceback.print_exception(None, e, e.__traceback__)
        if latency is not None:
            return True
        return False
