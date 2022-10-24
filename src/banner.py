import pyfiglet
import time

def banner():
    ascii_banner = pyfiglet.figlet_format("Kathara Net Creator")
    ascii_banner_segments = str(ascii_banner).split('\n')
    for segment in ascii_banner_segments:
        print(segment)
        time.sleep(0.02)

