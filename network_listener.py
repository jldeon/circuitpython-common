import traceback
import wifi
import socketpool


from network_base import NetworkBase

class NetworkListener(NetworkBase):

    def __init__(self, secrets, handle_data_cb, listen_port=8080, wifi_state_change_cb=None, sleep_func=None, debug=False):
        self.handle_data_cb = handle_data_cb
        self.listen_port = listen_port
        self.debug = debug
        super().__init__(secrets, wifi_state_change_cb, sleep_func)

    def run(self):
        self._connect()
        buffer = bytearray(1024)
        pool = socketpool.SocketPool(wifi.radio)
        with pool.socket(pool.AF_INET, pool.SOCK_DGRAM) as sock:
            sock.bind(("0.0.0.0", self.listen_port))
            sock.settimeout(10)
            while True:
                length = -1
                try:
                    length, _ = sock.recvfrom_into(buffer)
                except OSError as e:
                    # timeout, check to see if we're still connected
                    if not self._check_connection():
                        self._connect()
                except Exception as e:
                    print("Error reading data:")
                    traceback.print_exception(None, e, e.__traceback__)
                if length > 0:
                    try:
                        if self.debug:
                            print("Data read")
                            print(buffer[:length])
                        self.handle_data_cb(buffer[:length])
                    except Exception as e:
                        print("Error in handle_data_cb:")
                        traceback.print_exception(None, e, e.__traceback__)
                if self.debug:
                    print("Loop complete, sleeping...")
                self.sleep(0.01)
