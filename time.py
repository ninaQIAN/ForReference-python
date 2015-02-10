
import time
from datetime import datetime, date



timestamp = 1420440421742

x = time.localtime(timestamp/1000)

print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestamp/1000))
