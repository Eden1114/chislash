#coding: utf-8
import yaml
import sys
import os
from collections.abc import Mapping
ext_template = r"""
redir-port: 0
port: %s
socks-port: %s
tproxy-port: %s
mixed-port: %s
bind-address: '*'
allow-lan: true
log-level: %s
ipv6: %s
dns:
  enable: true
  listen: 0.0.0.0:1053
  enhanced-mode: fake-ip
  default-nameserver:
    - 180.76.76.76
    - 223.5.5.5
    - 119.29.29.29
  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query
 
  fallback:
    - 'tls://1.1.1.1:853'
    - 'tcp://1.1.1.1:53'
    - 'tcp://208.67.222.222:443'
    - 'tls://dns.google'
"""

def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.items():
        if isinstance(value, Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source

def override(user_config, required_config, ext):
    user = yaml.load(open(user_config, 'r', encoding="utf-8").read(), Loader=yaml.FullLoader)
    for dnskey in ['default-nameserver', 'nameserver', 'fallback']:
      if 'dns' in user and dnskey in user['dns'] and user['dns'][dnskey]:
        ed = ext['dns']
        del ed[dnskey]
        ext['dns'] = ed
    deep_update(user, ext)
    if required_config:
      must = yaml.load(open(required_config, 'r', encoding="utf-8").read(), Loader=yaml.FullLoader)
      deep_update(user, must)
    user_file = open(user_config, 'w', encoding="utf-8")
    yaml.dump(user, user_file)
    user_file.close()

_,user_config,required_config,port,socks_port,tproxy_port,mixed_port,log_level,ipv6_proxy = sys.argv
override(
  user_config, required_config,
  yaml.load(ext_template%(
    port,
    socks_port,
    tproxy_port,
    mixed_port,
    log_level,
    ipv6_proxy=="1",
    ), Loader=yaml.FullLoader))

