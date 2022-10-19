from .DB import Commands
from Server.Trace import Trace, get_local_ip

def trace_to_db(host):
    db = Commands.DB()
    trace = Trace(host).run()
    if not "Error" in trace.keys():
        localhost = get_local_ip()
        relatedIp = localhost
        for hop, index in enumerate(trace):
            for host in trace[index]:
                for rtt in host["RTT"]:
                    if not host["IP"] == relatedIp:
                        db.insert_related(hop, host["IP"], host["DNS"], relatedIp)
                        db.insert_host(host["IP"], rtt)
            relatedIp = host["IP"]
    else:
        db.insert_host(trace["Host"], trace["RTT"])

def build_nodes_up(host):
    db = Commands.DB()
    addresses = []
    for item in db.fetch_related_upstream(host):
        data = {
            "Hop": item[0],
            "IP": item[1],
            "RTTs": db.fetch_hosts(item[1]),
            "Nodes": [build_nodes_up(item[1])]
        }
        addresses.append(data)
    return addresses

def build_nodes_down(host):
    db = Commands.DB()
    addresses = []
    for item in db.fetch_related_downstream(host):
        data = {
            "Hop": item[0],
            "IP": item[1],
            "RTTs": db.fetch_hosts(item[1]),
            "Nodes": [build_nodes_down(item[1])]
        }
        addresses.append(data)
    return addresses

def domain_to_db(domain, times=1):
    for index in range(times):
        print(f"Running Trace { index+1 } of { times } on { domain }...")
        trace_to_db(domain)
    print("Trace Done!")