# bike_point_project

This python script extrcats data from TFL's bike point API. The Transport for London BikePoint API provides real-time information about London's Santander Cycles docking stations (often called "Boris Bikes").

How it works:

Initialization: Generates a consistent timestamp to bind the log file and data file together.

API Request: Attempts to fetch data from https://api.tfl.gov.uk/BikePoint/.

Condition Check:

Success (2xx): Parses JSON, confirms it's not empty, writes to disk, logs success, and prints yippee.

Server Error (5xx / Network): Waits 10 seconds, logs the attempt, and retries.

Client Error (4xx): Stops immediately, tells end user to fix something, and logs the specific bad status code so you don't waste API quota.

├── data/
│ └── 2026-07-08 16-43-22.json # Live BikePoint snapshot
└── logs/
└── 2026-07-08 16-43-22.log # Detailed execution audit trail
