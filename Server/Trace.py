import logging
from subprocess import run, PIPE
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class Trace():
    def __init__(self, host):
        self.host = host
        
    def _apple_clean_trace(self, raw):
        hops = {}
        hop = None
        for line in raw.strip().split('\n'):
            data = {}
            part = line.split(')')
            address = filter(None, part[0].strip().split(' '))
            for item in address:
                if item.isdigit():
                    hop = int(item)
                else:
                    if 'DNS' in data:
                        data['IP'] = item.replace('(', '')
                    elif not item.split('.')[-1].isnumeric() and not ':' in item:
                        data['DNS'] = item
                    else:
                        data['DNS'] = ''
            data['RTT'] = list()
            try:
                ms = part[1].split('ms')[:-1]
            except IndexError:
                logging.warning(f"Hidden Node: {part}")
                ms = "*"
            for rtt in ms:
                data['RTT'].append(rtt.strip())
            if not hop in hops:
                hops[hop] = []
            hops[hop].append(data)
        return hops

    def domain_to_ips(self, domain):
        command = ['nslookup', domain]
        result = run(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        hadYield = False
        for item in result.stdout.decode().splitlines():
            if "Address:" in item and not '#' in item:
                hadYield = True
                yield item.split(" ")[1].strip()
            elif "NXDOMAIN" in item:
                hadYield = True
                if domain.split('.')[-1].isnumeric() and not ':' in domain:
                    yield domain
                else:
                    yield None
        if not hadYield:
            yield domain

    def is_up(self, host):
        command = ['ping', '-t 1', host]
        result = run(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        ip = result.stdout.decode().strip().split(' ')
        if not result.returncode:
            return ip[1]
        else:
            return False

    def run(self):
        try:
            for host in self.domain_to_ips(self.host):
                ip = self.is_up(host)
                if ip:
                    command = ['traceroute', ip]
                    result = run(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    if not "unknown host" in result.stderr.decode():
                        return self._apple_clean_trace(result.stdout.decode())
                return {"Error": True, "Host": host, "RTT": -1}
        except TypeError:
            raise TypeError("Invalid Domain!")