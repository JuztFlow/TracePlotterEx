import wmi
import ipaddress
import socket
import dns.resolver
import dns.reversename
from scapy.all import IP, ICMP, sr1, get_if_addr, conf

LOCALHOST = get_if_addr(conf.iface)


def is_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def get_windows_dns_servers():
    dns_servers = set()
    for nic in wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True):
        if nic.DNSServerSearchOrder:
            dns_servers.update(nic.DNSServerSearchOrder)
    return list(dns_servers) if dns_servers else None


DNS_SERVERS = get_windows_dns_servers() or ["8.8.8.8", "1.1.1.1", "8.8.4.4", "1.0.0.1"]


def nslookup_by_ip(dns_servers, ip):
    reverse_name = dns.reversename.from_address(ip)
    resolver = dns.resolver.Resolver()
    resolver.nameservers = dns_servers
    try:
        answer = resolver.resolve(reverse_name, "PTR")
        return str(answer[0])
    except Exception:
        return "*"


def target_alive(target, timeout=5, ttl=128):
    packet = IP(dst=str(target), ttl=ttl) / ICMP()
    reply = sr1(packet, timeout=timeout, verbose=0)
    return reply is not None


def reached_target(target, reply_src):
    return (target == reply_src) if is_ip(target) else (socket.gethostbyname(target) == reply_src)


def traceroute(target, max_hops=30, timeout=1, verbose=0):

    # There shall be a hop 0 that always is the localhost
    yield {"Hop": 0, "IP": LOCALHOST, "Host": "*"}

    for hop in range(1, max_hops + 1):

        packet = IP(dst=target, ttl=hop) / ICMP()
        reply = sr1(packet, timeout=timeout, verbose=verbose)

        # If we get a timeout, we assume the hop is unreachable
        if reply is None:
            yield {"Hop": hop, "IP": "*", "Host": "*"}

        # If we get a reply and if it is the target, we are done
        elif reached_target(target, reply.src):
            yield {
                "Hop": hop,
                "IP": reply.src,
                "Host": nslookup_by_ip(DNS_SERVERS, reply.src),
            }
            break

        # If we get a reply and it is not the target, we continue
        else:
            yield {
                "Hop": hop,
                "IP": reply.src,
                "Host": nslookup_by_ip(DNS_SERVERS, reply.src),
            }

    # If we reached the maximum hops or if we reached the target, we are done
    return None


def ping(target, timeout=1, verbose=0):
    packet = IP(dst=target) / ICMP()
    reply = sr1(packet, timeout=timeout, verbose=verbose)
    return round((reply.time - packet.sent_time) * 1000, 3) if reply else None
