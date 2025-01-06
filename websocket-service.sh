#!/usr/bin/bash

# Here is where I set a bunch of environment variables that are
# used by the process invoked below...

# Now I want to invoke the process in the background and redirect
# all of the output to a log file.
/usr/bin/python3 /root/storrensteuerung/websocket.py > /home/pi/logfile-websocket.out 2>&1 &

# Finally, I record the PID of the process before the script exits.
echo $! > /root/storrensteuerung/status/www.pid
