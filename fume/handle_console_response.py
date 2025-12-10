import globals as g
from difflib import SequenceMatcher
import helper_functions.print_verbosity as pv
import datetime
import os

def check_similarity(line):
    for response in g.console_response_log:
        similarity = SequenceMatcher(None, line, response).ratio()
        
        # If there is another response that is similar enough, then
        # we don't want the new response
        if similarity >= g.SIMILARITY_THRESHOLD:
            return True
    return False

# Handle responses from the target's console, AKA, stdout
# We listen for new messages, and when those messages are unique enough,
# we log them
def handle_console_response(proc):
    for line in iter(proc.stdout.readline, b''):

        # Ignore lines that we have seen already
        if line not in g.console_response_log:

            # Check the similarity between this line and others we have logged
            similarity = check_similarity(line)

            # If it is unique enough, log it
            # TODO we need a way to better check if we have just sent a payload to the target
            if similarity is False and type(g.payload) is bytearray:
                g.console_response_log[line] = g.payload
                count = len(g.console_response_log)
                time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                pv.normal_print("[%s] Found new console response (%d total)" % (time_str, count))

                # NEW: Save response to folder
                try:
                    filename = f"console_response_{count}.txt"
                    filepath = os.path.join(g.SESSION_LOG_DIRECTORY, filename)
                    with open(filepath, "wb") as f:
                        f.write(line)
                except Exception as e:
                    pv.print_error(f"Failed to save console response to file: {e}")