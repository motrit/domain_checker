# domain_checker
Python script, which checks domains listed in file, to be responsive for HTTP(S) requests
- - - -
# Usage
```domain_checker.py [OPTIONS] COMMAND [ARGS]...```

Options:
*  --domains PATH  Domains to be checked for responsiveness
*  --proxy TEXT    Proxy to be used in format http|https|socks5://proxy_IP:proxy_port
*  --help          Show this message and exit.

Commands:
*  check
- - - -
# Sample usage:
```./domain_checker.py --domains ~/Downloads/subdomains.txt --proxy="socks5://127.0.0.1:XXXX" check```
