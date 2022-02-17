import os
import re
from mitmproxy.net.http.http1.assemble import assemble_request, assemble_response

request_counter = 1
os.makedirs('logs', exist_ok=True)

curl_log_path = 'logs/curl.txt'
stream_log_path = 'logs/stream.txt'

# Clear files on fresh start
with open(curl_log_path, 'w') as stream_log: stream_log.close()
with open(stream_log_path, 'w') as stream_log: stream_log.close()

def h2c(stream):
    try:
        global request_counter
        tmp_stream_path = 'logs/stream_' + str(request_counter) + '.tmp.txt'
        with open(tmp_stream_path, 'w') as tmp_stream_log:
            tmp_stream_log.write(stream)
        tmp_curl_path = 'logs/curl_' + str(request_counter) + '.tmp.txt'
        os.system('scripts/h2c.pl < ' + tmp_stream_path + ' > ' + tmp_curl_path)
        with open(curl_log_path, 'a') as curl_log:
            curl_output = open(tmp_curl_path, 'r').read()
            if 'Error' not in curl_output:
                curl_log.write('-- REQUEST #' + str(request_counter) + ' --\n' + curl_output + '\n')
        os.remove(tmp_curl_path)
        os.remove(tmp_stream_path)
    except:
        pass

def backfill_host(stream):
    if 'Host:' not in stream:
        stream_lines = stream.split('\n')
        first_line = stream.split('\n', 1)[0]
        full_host = re.search(r'(https?://[^/]+)', first_line).group()
        host_protocol, host_name = full_host.split('://', 1)
        stream_lines[0] = first_line.replace(full_host, '') + '\nHost: ' + host_name
        return '\n'.join(stream_lines)
    else:
        return stream

def response(flow):
    global request_counter
    request_logged = False
    # Check if request has content to log; this can fail if byte cannot be converted to utf-8
    try:
        request_output = assemble_request(flow.request).decode('utf-8').strip()
        if len(request_output):
            request_output = backfill_host(request_output)
            h2c(request_output)
            with open(stream_log_path, 'a') as stream_log:
                stream_log.write('-- REQUEST #' + str(request_counter) + ' --\n')
                stream_log.write(request_output)
            request_logged = True
    except:
        pass
    # Check if response has content to log; this can fail if byte cannot be converted to utf-8
    try:
        response_output = assemble_response(flow.response).decode('utf-8').strip()
        if len(response_output):
            with open(stream_log_path, 'a') as stream_log:
                stream_log.write('\n\n-- RESPONSE #' + str(request_counter) + ' --\n')
                stream_log.write(response_output)
    except:
        pass
    # If either had content, separate with additional blank line
    if request_logged:
        request_counter += 1
        with open(stream_log_path, 'a') as stream_log:
            stream_log.write('\n\n\n')
