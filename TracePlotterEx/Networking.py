import asyncio
import ipaddress
import socket
import aiodns
import dns.reversename
from scapy.all import IP, ICMP, sr, sr1, get_if_addr, conf

loop = asyncio.get_event_loop()
resolver = aiodns.DNSResolver(loop=loop)


class Networking:
    """
    A class encapsulating common networking utilities such as ping, traceroute, checking host reachability, IP validation, and DNS lookups.
    """

    LOCALHOST = get_if_addr(conf.iface)

    @staticmethod
    def target_alive(target: str, timeout: float = 5, ttl: int = 128, verbose: int = 0) -> bool:
        """
        Invoke an ICMP echo request to determine if the target is alive.
        """
        return Networking.ping(target=target, timeout=timeout, ttl=ttl, verbose=verbose) is not None

    @staticmethod
    def ping(target: str, timeout: float = 1, ttl: int = 128, verbose: int = 0) -> float:
        """
        Send a single ICMP echo request and return round-trip time in milliseconds with 3 decimal places.
        Returns None if no response.
        """
        packet = IP(dst=str(target), ttl=ttl) / ICMP()
        reply = sr1(packet, timeout=timeout, verbose=verbose)
        if reply:
            return round((reply.time - packet.sent_time) * 1000, 3)
        return None

    @staticmethod
    def traceroute(target: str, max_hops: int = 30, timeout: float = 1, verbose: int = 0) -> list:
        """
        Invokes a traceroute to the target which is then done asynchronously.

        Returns a list of dicts with 'Hop', 'IP', and 'Host' keys, ordered by hop.
        """
        return loop.run_until_complete(Networking._traceroute_async(target, max_hops, timeout, verbose))

    @staticmethod
    async def _traceroute_async(target: str, max_hops: int = 30, timeout: float = 1, verbose: int = 0) -> list:
        """
        Actually performs the traceroute to the target asynchronously.

        Returns a list of dicts with 'Hop', 'IP', and 'Host' keys, ordered by hop.
        """
        results = []

        # Hop 0: localhost
        results.append({"Hop": 0, "IP": Networking.LOCALHOST, "Host": "*"})

        # Build all TTL packets and send them in parallel
        resolved_target_ip = Networking._resolve_hostname_to_ip(target)
        packets = [IP(dst=resolved_target_ip, ttl=hop) / ICMP() for hop in range(1, max_hops + 1)]
        answered, _ = sr(packets, timeout=timeout, verbose=verbose)

        # Map TTL → source IP
        hop_to_ip = {sent.ttl: reply.src for sent, reply in answered}

        # Prepare all async DNS lookups
        tasks = []
        for current_hop in range(1, max_hops + 1):
            current_hop_ip = hop_to_ip.get(current_hop)
            if current_hop_ip is None:
                results.append({"Hop": current_hop, "IP": "*", "Host": "*"})
            else:
                tasks.append(Networking._lookup_hostname_async(hop=current_hop, ip=current_hop_ip, results=results))
                if current_hop_ip == resolved_target_ip:
                    break

        # Wait for all DNS lookups to complete
        await asyncio.gather(*tasks)

        return results

    @staticmethod
    def _resolve_hostname_to_ip(target: str) -> str:
        """
        Resolve hostname to IP if needed.
        """
        return target if Networking._is_valid_ip(target) else socket.gethostbyname(target)

    @staticmethod
    def _is_valid_ip(address: str) -> bool:
        """
        Check if the provided string is a valid IPv4 or IPv6 address.
        """
        try:
            ipaddress.ip_address(address)
            return True
        except ValueError:
            return False

    @staticmethod
    async def _lookup_hostname_async(hop: int, ip: str, results: list) -> None:
        """
        Helper function to look up hostnames asynchronously and append to results.
        """
        hostname = await Networking._nslookup_by_ip(ip)
        results.append({"Hop": hop, "IP": ip, "Host": hostname if hostname else "*"})

    @staticmethod
    async def _nslookup_by_ip(ip: str) -> str:
        """
        Perform a reverse DNS lookup (PTR) for the given IP address using aiodns.
        """
        reverse_name = dns.reversename.from_address(ip)
        try:
            response = await resolver.query(str(reverse_name), "PTR")
            return str(response.name)
        except aiodns.error.DNSError:
            return None
