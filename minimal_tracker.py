#IMPORTS
import argparse
import time

# SET UP THE COUNTER (ARGPARSE)
parser = argparse.ArgumentParser(description="Terminal Focus Timer")
parser.add_argument("minutes", type=int, nargs="?", default=20, help="Session length in minutes")
args = parser.parse_args()

# VARIABLES
duration_secs = args.minutes * 60
start_time = time.time()
end_time = start_time + duration_secs

#CODE
try:
    while time.time() < end_time:
          remaining = end_time - time.time()
    #UI
          mins = int(remaining // 60)
          secs = int(remaining % 60)
          print(f"\rTime Left: {mins:02d}:{secs:02d}", end="")
          time.sleep(0.2)
    print("\nTime's up bro! GGS!! see you later.")
except KeyboardInterrupt:
     print("\nWhat happened bro wanna pause?")
