from parsers.parse_initializer import ParseInitializer
import helper_functions.determine_protocol_version as hpv
import helper_functions.print_verbosity as pv
import globals as g
import datetime
import os

# Handle the network response -- log the request if 
# the response was unique.
# A response is unique if its G field has never been seen before.
def handle_network_response(recv):
    if len(recv) == 0:
        return

    if g.protocol_version == 0:
        g.protocol_version = hpv.determine_protocol_version(recv.hex())
        
    index = 0
    while index < len(recv.hex()):
        try:
            parser = ParseInitializer(recv.hex()[index:], g.protocol_version)

            # Log G fields
            G_fields = str(parser.parser.G_fields)
            # G_fields = str(parser.parser.G_fields) + str(parser.parser.H_fields)
            if G_fields not in g.network_response_log.keys():
                g.network_response_log[G_fields] = g.payload

                count = len(g.network_response_log)
                time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                pv.normal_print("[%s] Found new network response (%d total)" % (time_str, count))

                try:
                    filename = f"network_response_{count}.bin"
                    filepath = os.path.join(g.SESSION_LOG_DIRECTORY, filename)
                    with open(filepath, "wb") as f:
                        f.write(recv)
                except Exception as e:
                    pv.print_error(f"Failed to save network response to file: {e}")

            index +=  2 * (parser.parser.remainingLengthToInteger()) + 2 + len(parser.parser.remaining_length)

        # If the parser throws a ValueError, chances are that the payload
        # is malformed. In that case, we skip the current byte and hope for 
        # the best.
        except ValueError:
            index += 2