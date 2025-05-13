from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, ICMP, sr1, get_if_addr, conf

LOCALHOST = get_if_addr(conf.iface)


def nslookup_by_domain(srv, host):
    packet = IP(dst=srv) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=host))
    reply = sr1(packet, verbose=0)[DNS]
    for item in range(reply[DNS].ancount):
        yield reply[DNSRR][item].rdata


def nslookup_by_ip(srv, ip):
    ipParts = ip.split(".")
    ip = f"{ipParts[-1]}.{ipParts[-2]}.{ipParts[-3]}.{ipParts[-4]}"
    packet = (
        IP(dst=srv)
        / UDP()
        / DNS(rd=1, qd=DNSQR(qname=f"{ip}.in-addr.arpa", qtype="PTR"))
    )
    reply = sr1(packet, verbose=0)[DNS]
    for item in range(reply[DNS].ancount):
        dns = reply[DNSRR][item].rdata.decode()[:-1]
        if dns:
            return dns
        return None


def host_alive(host, timeout=1):
    packet = IP(dst=str(host), ttl=20) / ICMP()
    reply = sr1(packet, timeout=timeout, verbose=0)
    if not (reply is None):
        return True
    return False


def traceroute(ip):
    yield {"Hop": 0, "IP": LOCALHOST}
    for hop in range(1, 28):
        packet = IP(dst=ip, ttl=hop) / UDP(dport=33434)
        reply = sr1(packet, verbose=0)
        if reply is None:
            break
        elif reply.type == 3:
            yield {"Hop": hop, "IP": reply.src}
            break
        else:
            yield {"Hop": hop, "IP": reply.src}


def ping(host):
    packet = IP(dst=host) / ICMP()
    reply = sr1(packet, verbose=0)
    return round((reply.time - packet.sent_time) * 1000, 3)
