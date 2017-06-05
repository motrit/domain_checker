#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import click
import requests
import progressbar

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
    protocols = ['http://', 'https://']
    progress_iter = 0
    bar = progressbar.ProgressBar(
            widgets=[   'Processing...', 
                        progressbar.Bar(), 
                        progressbar.Percentage(),
                        progressbar.ETA()
                    ], 
            max_value = len(domain_list) * len(protocols),
            redirect_stdout = True)
    bar.start()

    for prefix in protocols :
        for domain in domain_list :
            try :
                if prefix+domain not in live_domain_list :
                    r = requests.get(prefix + domain, proxies=proxy, timeout=3)
                    live_domain_list.append(prefix+domain)
                    print (prefix+domain, 'exists!')
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) :
#                print (prefix+domain, 'doesn\'t respond')
                pass
            except requests.exceptions.ConnectionError :
#                print (prefix+domain, 'doesn\'t exist')
                pass
            progress_iter += 1
            bar.update(progress_iter)
    bar.finish()
    print(live_domain_list)


if __name__ == '__main__' :
    args_parser()
