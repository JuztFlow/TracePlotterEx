import sqlite3

class DB():
    def __init__(self):
        self.connection = sqlite3.connect("./Server/DB/TracePlotter.db")
        cursor = self.connection.cursor()
        with open("./Server/DB/Template.sql", 'r') as file:
            for table in file.read().split('+'):
                cursor.executescript(table)
            
    def insert_related(self, hop, hostIp, hostDns, relatedIp):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"INSERT INTO Related (hop, HostIp, hostDns, RelatedIp) VALUES('{hop}', '{hostIp}', '{hostDns}', '{relatedIp}');")
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def insert_host(self, HostIp, rtt):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO Host (HostIp, rtt) VALUES('{HostIp}', '{rtt}');")
        self.connection.commit()

    def fetch_related_downstream(self, host):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT hop, HostIp FROM Related WHERE RelatedIp='{host}' ORDER BY id ASC;")
        for row in cursor:
            yield row

    def fetch_related_upstream(self, host):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT hop, RelatedIp FROM Related WHERE HostIp='{host}' ORDER BY id ASC;")
        for row in cursor:
            yield row

    def fetch_hosts(self, ip):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT DateTime, RTT FROM Host WHERE HostIp='{ip}' ORDER BY datetime ASC;")
        for row in cursor:
            yield row