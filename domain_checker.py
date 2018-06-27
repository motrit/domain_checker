#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import click
import requests

@click.group()
@click.pass_context
@click.option('--domains', type=click.Path(exists=True), default='domains.txt', help='Domains to be checked for responsiveness')
@click.option('--proxy', default = None, type=str, help='Proxy to be used in format http|https|socks5://proxy_IP:proxy_port' )
def args_parser(ctx, domains, proxy) :
    domain_list = []
    with open(domains) as domain_reader :
        for domain_line in domain_reader :
            domain_list.append(domain_line[:-1])
    ctx.obj = {'domains' : domain_list, 'proxy' : {'http': proxy, 'https': proxy}}

@args_parser.command()
@click.pass_context
def check(ctx) :
    # Initilize variables
    proxy = ctx.obj['proxy']
    domain_list = ctx.obj['domains']
    live_domain_list = []
    counter = 0
    protocols = ['http://', 'https://']

    for domain in domain_list :
        counter += 1
        for prefix in protocols :
            try :
                if prefix+domain not in live_domain_list :
                    r = requests.get(prefix + domain, proxies=proxy, timeout=3)
                    print (counter,'/',len(domain_list), ' : ', prefix+domain, 'exists!')
                    if (('http://' + domain) in live_domain_list) or (('https://' + domain) in live_domain_list):
                        prefix = 'http(s)://'
                    live_domain_list.append(prefix+domain)
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) :
#                print (prefix+domain, 'doesn\'t respond')
                pass
            except requests.exceptions.ConnectionError :
#                print (prefix+domain, 'doesn\'t exist')
                pass
    print ('Scanning finished! Printing results...')
    print (live_domain_list)


if __name__ == '__main__' :
    args_parser()
