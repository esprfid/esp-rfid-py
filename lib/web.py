# -*- coding: utf-8 -*-
# Stripped down web server, based on Picoweb by Paul Sokolovsky
# https://github.com/pfalcon/picoweb
#
# Stripped by:
# Copyright (C) 2018 Raoul Snyman https://gitlab.com/superfly
#
# This web server is part of DawnDoor
# Licensed under the MIT license, see LICENSE.txt for details


import ure as re
import uerrno
import path


def unquote_plus(string):
    string = string.replace('+', ' ')
    arr = string.split('%')
    arr2 = [chr(int(part[:2], 16)) + part[2:] for part in arr[1:]]
    return arr[0] + ''.join(arr2)


def parse_qs(string):
    params = {}
    if string:
        pairs = string.split('&')
        for pair in pairs:
            values = [unquote_plus(part) for part in pair.split('=', 1)]
            if len(values) == 1:
                values.append(True)
            if values[0] in params:
                if not isinstance(params[values[0]], list):
                    params[values[0]] = [params[values[0]]]
                params[values[0]].append(values[1])
            else:
                params[values[0]] = values[1]
    return params


def get_mime_type(fname):
    # Provide minimal detection of important file
    # types to keep browsers happy
    if fname.endswith('.html'):
        return 'text/html'
    if fname.endswith('.css'):
        return 'text/css'
    if fname.endswith('.svg'):
        return 'image/svg+xml'
    if fname.endswith('.png'):
        return 'image/png'
    if fname.endswith('.jpg'):
        return 'image/jpeg'
    if fname.endswith('.txt') or fname.endswith('.csv'):
        return 'text/plain'
    return 'application/octet-stream'


def sendstream(writer, file_):
    buf = bytearray(64)
    while True:
        line = file_.readinto(buf)
        if not line:
            break
        yield from writer.awrite(buf, 0, line)


def jsonify(writer, pydict):
    import ujson
    yield from start_response(writer, 'application/json')
    yield from writer.awrite(ujson.dumps(pydict))


def start_response(writer, content_type='text/html', status='200', headers=None):
    yield from writer.awrite('HTTP/1.0 %s NA\r\n' % status)
    yield from writer.awrite('Content-Type: ')
    yield from writer.awrite(content_type)
    if not headers:
        yield from writer.awrite('\r\n\r\n')
        return
    yield from writer.awrite('\r\n')
    if isinstance(headers, bytes) or isinstance(headers, str):
        yield from writer.awrite(headers)
    else:
        for k, v in headers.items():
            yield from writer.awrite(k)
            yield from writer.awrite(': ')
            yield from writer.awrite(v)
            yield from writer.awrite('\r\n')
    yield from writer.awrite('\r\n')


def http_error(writer, status):
    yield from start_response(writer, status=status)
    yield from writer.awrite(status)


class HTTPRequest(object):

    def read_form_data(self):
        size = int(self.headers[b'Content-Length'])
        data = yield from self.reader.read(size)
        form = parse_qs(data.decode())
        self.form = form

    def parse_qs(self):
        form = parse_qs(self.qs)
        self.form = form


class WebApp(object):

    def __init__(self):
        self.url_map = []
        self.templates_dir = '/templates'
        self.static_dir = '/static'
        self.url_map.append((re.compile('^/(static/.+)'), self.handle_static))
        self.headers_mode = 'parse'

    def parse_headers(self, reader):
        headers = {}
        while True:
            line = yield from reader.readline()
            if line == b'\r\n':
                break
            key, value = line.split(b':', 1)
            headers[key] = value.strip()
        return headers

    def handle(self, reader, writer):
        close = True
        try:
            request_line = yield from reader.readline()
            if request_line == b'':
                yield from writer.aclose()
                return
            req = HTTPRequest()
            request_line = request_line.decode()
            method, path, proto = request_line.split()
            path = path.split('?', 1)
            qs = ''
            if len(path) > 1:
                qs = path[1]
            path = path[0]

            found = False
            for e in self.url_map:
                pattern = e[0]
                handler = e[1]
                extra = {}
                if len(e) > 2:
                    extra = e[2]

                if path == pattern:
                    if extra and extra.get('method'):
                        if extra['method'] == method:
                            found = True
                            break
                    else:
                        found = True
                        break
                elif not isinstance(pattern, str):
                    m = pattern.match(path)
                    if m:
                        req.url_match = m
                        if extra and extra.get('method'):
                            if extra['method'] == method:
                                found = True
                                break
                        else:
                            found = True
                            break

            if not found:
                headers_mode = 'skip'
            else:
                headers_mode = extra.get('headers', self.headers_mode)

            if headers_mode == 'skip':
                while True:
                    line = yield from reader.readline()
                    if line == b'\r\n':
                        break
            elif headers_mode == 'parse':
                req.headers = yield from self.parse_headers(reader)
            else:
                assert headers_mode == 'leave'

            if found:
                req.method = method
                req.path = path
                req.qs = qs
                req.reader = reader
                close = yield from handler(req, writer)
            else:
                yield from self.abort(writer, '404')
        except Exception as e:
            pass

        if close is not False:
            yield from writer.aclose()

    def abort(self, writer, status):
        yield from start_response(writer, status=status)
        yield from writer.awrite(status + '\r\n')

    def route(self, url, **kwargs):
        def _route(f):
            self.url_map.append((url, f, kwargs))
            return f
        return _route

    def add_url_rule(self, url, func, **kwargs):
        self.url_map.append((url, func, kwargs))

    def render_template(self, writer, tmpl_name, **kwargs):
        print('Render template')
        with open(path.join(self.templates_dir, tmpl_name)) as tfile:
            print('File open')
            from dawndoor.pypage import pypage
            print('Imported pypage')
            contents = pypage(tfile.read(), kwargs)
            print('Parsed')
            yield from writer.awrite(contents)

    def sendfile(self, writer, fname, content_type=None, headers=None):
        if not content_type:
            content_type = get_mime_type(fname)
        try:
            with open(fname) as f:
                yield from start_response(writer, content_type, '200', headers)
                yield from sendstream(writer, f)
        except OSError as e:
            if e.args[0] == uerrno.ENOENT:
                yield from http_error(writer, '404')
            else:
                raise

    def handle_static(self, req, resp):
        fpath = req.url_match.group(1)
        if '..' in fpath:
            yield from http_error(resp, '403')
            return
        # headers = {'Cache-Control': 'max-age=2592000'}
        yield from self.sendfile(resp, fpath)
