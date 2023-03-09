import time
import microcontroller
import traceback

from adafruit_requests import OutOfRetries

from network_base import NetworkBase

class NetworkFetcher(NetworkBase):
    def __init__(self, network, secrets, wifi_radio_obj=None, wifi_state_change_cb=None, sleep_func=None, debug=False):
        """
        Create a NetworkFetcher object to wrap the `network` object.
        :param network: The Adafruit Network object to wrap
        :param sleep_func: If you want to ie, feed a watchdog, pass this function
            and it will be called instead of time.sleep
        :param debug: If True, emit additional debug logging information.
        """
        
        self.debug = debug
        self.network = network
        super().__init__(secrets, wifi_radio_obj=wifi_radio_obj, wifi_state_change_cb=wifi_state_change_cb, sleep_func=sleep_func)
        self._connect()

    def fetch(self, url):
        """ Wrap the adafruit_matrixportal.network.Network.fetch() routine,
            add error retries. """
        retries = 0
        response = None
        while True:
            try:
                response = self.network.fetch(url)
                print("\n")
                break
            except Exception as e:
                print("\n")
                print("Error while fetching:")
                traceback.print_exception(None, e, e.__traceback__)
                if not self._check_connection():
                    self._connect()
                retries += 1
                if retries > 5:
                    print("Retries exceeded max, resetting system...\n\n")
                    microcontroller.reset()
                self.sleep(0.5)
        return response

    def fetch_and_parse(self, url):
        """
        Fetch a URL, and then parse the result into a list of lines.
        """
        while True:
            response = self.fetch(url)
            try:
                parsed_response = response.content.decode('utf-8').split("\n")
                break
            except Exception as e:
                print("Error while parsing response.")
                traceback.print_exception(None, e, e.__traceback__)
                self.sleep(0.5)

        return parsed_response
