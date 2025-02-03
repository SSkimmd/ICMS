import logging
import re
import requests
import os

CRLF = '\r\n'
DEFAULT_HTTP_VERSION = 'HTTP/1.1'

class RequestParser(object):
    def __parse_request_line(self, request_line):
        request_parts = request_line.split(' ')
        self.method = request_parts[0]
        self.url = request_parts[1]
        self.protocol = request_parts[2] if len(request_parts) > 2 else DEFAULT_HTTP_VERSION

    def __init__(self, req_text):
        req_lines = req_text.split(CRLF)
        self.__parse_request_line(req_lines[0])
        ind = 1
        self.headers = dict()
        while ind < len(req_lines) and len(req_lines[ind]) > 0:
            colon_ind = req_lines[ind].find(':')
            header_key = req_lines[ind][:colon_ind]
            header_value = req_lines[ind][colon_ind + 1:]
            self.headers[header_key] = header_value
            ind += 1
        ind += 1
        self.data = req_lines[ind:] if ind < len(req_lines) else None
        self.body = CRLF.join(self.data)

    def __str__(self):
        headers = CRLF.join(f'{key}: {self.headers[key]}' for key in self.headers)
        return f'{self.method} {self.url} {self.protocol}{CRLF}' \
               f'{headers}{CRLF}{CRLF}{self.body}'

    async def to_request(self):
        req = requests.Request(method=self.method,
                               url=self.url,
                               headers=self.headers,
                               data=self.data, )
        return req


def reverse_readline(filename, buf_size=8192):
    """A generator that returns the lines of a file in reverse order"""
    with open(filename, 'rb') as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            # remove file's last "\n" if it exists, only for the first buffer
            if remaining_size == file_size and buffer[-1] == ord('\n'):
                buffer = buffer[:-1]
            remaining_size -= buf_size
            lines = buffer.split('\n'.encode())
            # append last chunk's segment to this chunk's last line
            if segment is not None:
                lines[-1] += segment
            segment = lines[0]
            lines = lines[1:]
            # yield lines in this chunk except the segment
            for line in reversed(lines):
                # only decode on a parsed line, to avoid utf-8 decode error
                yield line.decode()
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment.decode()


class NoColourFormatter(logging.Formatter):
    """Log formatter that strips terminal colour escape codes from the log message."""
    ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

    def format(self, record):
        """Return logger message with terminal escapes removed."""
        return "[%s] [%s]: %s" % (
            record.levelname,
            record.name,
            re.sub(self.ANSI_RE, "", record.msg % record.args)
        )