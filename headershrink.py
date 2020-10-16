#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Usage:
#   ./shrinkheader.py <curl_syntax>

import gzip
import time
import argparse
import itertools
import urllib.request


def print_info(message):
    print('\033[92m\033[1m[INFO]\033[0m\033[0m ' + message)


def print_error(message):
    print('\033[91m\033[1m[ERROR]\033[0m\033[0m ' + message)
    exit()


def parseArgs():
    parser = argparse.ArgumentParser(
        usage='headershrink.py curl [URL] [-X REQUEST] [-H HEADER] [-d DATA]')
    parser.add_argument('-X', '--request', nargs=1, help='Request method')
    parser.add_argument('-H', '--header', nargs=1, action='append',
                        help='Request headers')
    parser.add_argument('-d', '--data', '--data-raw', nargs=1, action='append',
                        help='Request data')
    return parser.parse_known_args()


def get_url(args):
    for a in args:
        if not a.startswith('-'):
            return a
    print_error('Missing URL!')


def get_rest_options(args):
    optlist = []
    for a in args:
        if a.startswith('-'):
            optlist.append(a)
    return optlist


def get_method(args):
    if args.request is not None:
        return args.request[0]
    if args.data is not None:
        return 'POST'
    return 'GET'


def header_list_to_dict(headerlist):
    dict = {}
    if headerlist is not None:
        for h in headerlist:
            parts = h[0].split(':')
            key = parts[0]
            value = ':'.join(parts[1:]).lstrip()
            dict[key] = value
    return dict


def data_list_to_str(datalist):
    str = ''
    if datalist is not None:
        for d in datalist:
            str += '&' + d[0]
        str = str[1:]
    return bytes(str, 'utf-8')


def call(reqdict):
    request = urllib.request.Request(reqdict['url'],
                                     data=reqdict['data'],
                                     headers=reqdict['headers'])
    request.method = reqdict['method']

    try:
        response = urllib.request.urlopen(request)
        status = response.getcode()
        rawcontent = response.read()
        try:
            content = rawcontent.decode('utf-8')
        except UnicodeDecodeError:
            content = gzip.decompress(rawcontent).decode('utf-8')
        return status, content
    except urllib.error.HTTPError as error:
        return error.code, ''


def write_to_file(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()


def iterate_headers(reqdict, repdict):
    headers = reqdict['rawheaders']
    for i in range(0, len(headers) + 1):
        print_info('Checking combination ' + str(i))
        for c in list(itertools.combinations(headers, i)):
            reqdict['headers'] = header_list_to_dict(c)
            print_info('>> Header(s): ' + str(reqdict['headers']))
            status, content = call(reqdict)
            if repdict['ref']['status'] == status \
                    and repdict['ref']['length'] == len(content):

                output = 'curl -X ' + reqdict['method'] \
                    + ' "' + reqdict['url'] + '"'

                if reqdict['headers']:
                    print_info('Found min. combination: '
                               + ', '.join(reqdict['headers'].keys()))
                    for h, v in reqdict['headers'].items():
                        output += ' -H \'' + h + ': ' + v + '\''
                else:
                    print_info('Header is not needed ¯\\_(ツ)_/¯')

                if len(reqdict['data']) > 0:
                    output += ' --data \'' + reqdict['data'] + '\''

                if len(reqdict['options']) > 0:
                    for o in reqdict['options']:
                        output += ' ' + o

                return output


def main():
    requestdict = {}
    reportdict = {}

    args, rest = parseArgs()

    if args.header is None:
        print_error('Missing header!')

    try:
        rest.remove('curl')
    except ValueError:
        pass

    requestdict['url'] = get_url(rest)
    requestdict['method'] = get_method(args)
    requestdict['data'] = data_list_to_str(args.data)
    requestdict['options'] = get_rest_options(rest)
    requestdict['headers'] = header_list_to_dict(args.header)
    requestdict['rawheaders'] = args.header

    refstatus, refcontent = call(requestdict)
    reportdict['ref'] = {}
    reportdict['ref']['status'] = refstatus
    reportdict['ref']['length'] = len(refcontent)
    reportdict['ref']['content'] = refcontent
    reportdict['ref']['headers'] = requestdict['headers']

    result = iterate_headers(requestdict, reportdict)
    print(result)
    write_to_file(str(int(time.time())) + '.curl', result)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
