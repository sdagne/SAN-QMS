# Portal Overview Notice

This document summarizes how each of the four UI files works in the Queue Management Standard project.

## 1. `kiosk_portal.html`
- Citizen-facing kiosk for ticket creation.
- Collects ID, name, service, optional phone number and posts to `/api/tickets`.
- Shows the generated ticket number, QR code, wait estimate, and handles errors such as duplicate active tickets.
- Communicates directly with the backend ticket-creation API; no counter-level features are present.

## 2. `counter_portal.html`
- Counter-facing dashboard for staff (one instance per counter).
- Displays queue statistics, current ticket, and a waiting list of tickets that have not yet been assigned.
- Each waiting ticket shows an "Assign to Counter X" button that hits `/api/counters/{id}/assign-ticket` with the selected ticket number; assignment marks the ticket as `CALLED` with that counter number but does not start verification yet.
- Staff verify the citizen ID via `/api/counters/{id}/verify` and complete service via `/api/counters/{id}/complete`, while the page polls `/api/display/waiting-tickets` and `/api/statistics` every 5 seconds.

## 3. `display_portal.html`
- Public waiting-room see-through display for customers.
- Polls `/api/display/queue-status` and `/api/statistics` at short intervals and shows the date/time.
- "Now Serving" cards highlight tickets with assigned counters and show `Awaiting counter` until a counter claims them.
- Automatically updates whenever the backend assigns a counter, creating a live view of who to go to.

## 4. `demo_dashboard.html`
- Operations/control dashboard combining ticket creation, counter management, ticket management, and a read-only waiting list.
- Allows admins to create tickets (mirroring kiosk behavior), cancel tickets, call next ticket per counter, and inspect the `/display/queue-status`/`/statistics` payloads.
- Includes a read-only table built from `/api/display/waiting-tickets`, showing ticket position, masked ID, and created time; refreshes every 10 seconds.
- Provides links to API documentation and shows server health status.

## How they work together
Each portal interacts with FastAPI endpoints:
- Ticket creation and status: `/api/tickets` and `/api/tickets/{ticket_number}`.
- Staff actions: `/api/counters/{id}/assign-ticket`, `/api/counters/{id}/verify`, `/api/counters/{id}/complete`, and `/api/counters/{id}/call-next` for fallback.
- Display data: `/api/display/queue-status` and `/api/display/waiting-tickets` used by both the public display and the dashboard.
- Stats/health: `/api/statistics` and `/health` for monitoring.

The flow ensures tickets stay in `WAITING` until a staff member explicitly assigns them, and the display only shows counter numbers when the backend records them, preserving fairness and clarity for waiting citizens.

