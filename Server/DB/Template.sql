CREATE TABLE IF NOT EXISTS Related (
	ID integer PRIMARY KEY AUTOINCREMENT,
	Hop integer,
	HostIp varchar,
	RelatedIp varchar,
	HostDNS varchar,
	UNIQUE(Hop, HostIp, RelatedIp) ON CONFLICT ABORT
);

CREATE TABLE IF NOT EXISTS Host (
	ID integer PRIMARY KEY AUTOINCREMENT,
	HostIp varchar,
	RTT float,
	DateTime datetime DEFAULT CURRENT_TIMESTAMP
);
