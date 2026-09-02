#!/usr/bin/env python3
"""A small shipment API for the section 4 drills.

Run it from this folder:

    python depot_api.py

It listens on http://localhost:8420 and keeps everything in memory, so
stopping it and starting it again resets the data to exactly what you see
below. Stop it with Ctrl-C.

Leave it running in one terminal and send requests from a second one. The
terminal running the server prints a line for every request it receives,
which is worth watching while you work.
"""

import json
import math
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8420

# The depot's shipments, as the server holds them at startup.
SHIPMENTS = [
    {"id": 1, "destination": "north", "packing": "crated", "weight_kg": 120},
    {"id": 2, "destination": "south", "packing": "loose", "weight_kg": 40},
    {"id": 3, "destination": "east", "packing": "crated", "weight_kg": 310},
    {"id": 4, "destination": "west", "packing": "crated", "weight_kg": None},
]

AUDIT_TOKEN = "depot-key"

INDEX = """The depot shipment API.

  /shipments
  /shipments/<id>
  /shipments/bulk
  /depot/audit
  /depot/status
  /manifest.txt
"""

MANIFEST = """Depot manifest, week 32
north  crated  120
south  loose    40
east   crated  310
west   crated    -
"""


def find_shipment(shipment_id):
    """Return the shipment with this id, or None if there is no such record."""
    for shipment in SHIPMENTS:
        if shipment["id"] == shipment_id:
            return shipment
    return None


def with_billing(shipment):
    """Return a copy of the shipment with its billable unit count worked out.

    The depot bills in whole 25kg units, rounding up.
    """
    detail = dict(shipment)
    detail["billable_units"] = math.ceil(shipment["weight_kg"] / 25)
    return detail


def validate(record):
    """Return a list of problems with a submitted shipment record.

    An empty list means the record is acceptable.
    """
    problems = []
    if "destination" not in record:
        problems.append({"field": "destination", "problem": "missing"})
    if "weight_kg" not in record:
        problems.append({"field": "weight_kg", "problem": "missing"})
    elif not isinstance(record["weight_kg"], (int, float)):
        problems.append({"field": "weight_kg", "problem": "not a number"})
    return problems


class DepotHandler(BaseHTTPRequestHandler):
    # Pinned so the Server header reads the same on every machine.
    server_version = "DepotAPI/1.0"
    sys_version = ""

    protocol_version = "HTTP/1.1"

    def version_string(self):
        return self.server_version

    def send_json(self, status, payload, extra_headers=None):
        body = json.dumps(payload, indent=2).encode() + b"\n"
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def send_text(self, status, text, extra_headers=None):
        body = text.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def wants_json(self):
        """True unless the caller asked for a format this server does not serve."""
        accept = self.headers.get("Accept", "*/*")
        return "*/*" in accept or "application/json" in accept

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length else b""

    def guard(self, route):
        """Run a route, turning any unhandled failure into a response."""
        try:
            route()
        except Exception:
            traceback.print_exc()
            self.send_json(
                500,
                {"message": "The depot API failed to handle that request."},
            )

    def do_GET(self):
        self.guard(self.route_get)

    def do_HEAD(self):
        self.guard(self.route_get)

    def do_POST(self):
        self.guard(self.route_post)

    def do_DELETE(self):
        self.guard(self.route_delete)

    def route_get(self):
        if self.path == "/":
            self.send_text(200, INDEX)
            return

        if self.path == "/manifest.txt":
            self.send_text(200, MANIFEST)
            return

        if self.path == "/depot/status":
            self.send_json(
                503,
                {"message": "Stocktake in progress."},
                {"Retry-After": "120"},
            )
            return

        if self.path == "/depot/audit":
            self.handle_audit()
            return

        if self.path == "/shipments/":
            self.send_response(308)
            self.send_header("Location", "/shipments")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        if self.path == "/shipments":
            if not self.wants_json():
                self.send_json(
                    406,
                    {"message": "This endpoint serves application/json."},
                )
                return
            self.send_json(200, SHIPMENTS)
            return

        if self.path.startswith("/shipments/"):
            self.handle_shipment_detail()
            return

        self.send_json(404, {"message": "No such path."})

    def route_post(self):
        # Read the body before deciding anything. A response sent while the
        # body is still unread leaves those bytes on the connection, and the
        # next request read off it starts in the middle of them.
        body = self.read_body()

        if self.path == "/shipments/bulk":
            self.handle_bulk(body)
            return

        if self.path != "/shipments":
            self.send_json(404, {"message": "No such path."})
            return

        content_type = self.headers.get("Content-Type", "")
        if not content_type.startswith("application/json"):
            self.send_json(
                415,
                {"message": "This endpoint reads application/json."},
                {"Accept-Post": "application/json"},
            )
            return

        try:
            record = json.loads(body)
        except json.JSONDecodeError as exc:
            self.send_json(
                400,
                {"message": "Body is not valid JSON.", "detail": str(exc)},
            )
            return

        problems = validate(record)
        if problems:
            self.send_json(
                422,
                {"message": "Record could not be accepted.", "errors": problems},
            )
            return

        new_id = max(s["id"] for s in SHIPMENTS) + 1
        stored = {
            "id": new_id,
            "destination": record["destination"],
            "packing": record.get("packing", "loose"),
            "weight_kg": record["weight_kg"],
        }
        SHIPMENTS.append(stored)
        self.send_json(201, stored, {"Location": f"/shipments/{new_id}"})

    def route_delete(self):
        if self.path.startswith("/shipments/"):
            self.send_json(
                405,
                {"message": "Shipments are not removed through this API."},
                {"Allow": "GET, HEAD"},
            )
            return
        self.send_json(404, {"message": "No such path."})

    def handle_shipment_detail(self):
        raw_id = self.path[len("/shipments/"):]
        if not raw_id.isdigit():
            self.send_json(400, {"message": "Shipment id must be a number."})
            return

        shipment = find_shipment(int(raw_id))
        if shipment is None:
            self.send_json(404, {"message": "No shipment with that id."})
            return

        self.send_json(200, with_billing(shipment))

    def handle_bulk(self, body):
        try:
            records = json.loads(body)
        except json.JSONDecodeError as exc:
            self.send_json(
                400,
                {"message": "Body is not valid JSON.", "detail": str(exc)},
            )
            return

        accepted = 0
        errors = []
        for position, record in enumerate(records):
            problems = validate(record)
            if problems:
                errors.append({"index": position, "errors": problems})
            else:
                accepted += 1

        self.send_json(200, {"accepted": accepted, "errors": errors})

    def handle_audit(self):
        header = self.headers.get("Authorization")
        if header is None:
            self.send_json(
                401,
                {"message": "This endpoint needs a token."},
                {"WWW-Authenticate": 'Bearer realm="depot"'},
            )
            return

        token = header.removeprefix("Bearer ").strip()
        if token != AUDIT_TOKEN:
            self.send_json(403, {"message": "That token cannot read the audit log."})
            return

        self.send_json(200, {"entries": ["week 31 closed", "week 32 open"]})


class DepotServer(HTTPServer):
    # Refuse to start if something is already on the port, rather than
    # quietly sharing it and answering only some of the requests.
    allow_reuse_address = False


def main():
    try:
        server = DepotServer(("localhost", PORT), DepotHandler)
    except OSError:
        print(f"Nothing started: something is already using port {PORT}.")
        print("Stop the other one first, then run this again.")
        raise SystemExit(1)

    print(f"Depot API listening on http://localhost:{PORT}")
    print("Stop it with Ctrl-C.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
