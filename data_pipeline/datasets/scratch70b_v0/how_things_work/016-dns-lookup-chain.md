---
id: how-016
category: how_things_work
subcategory: computing
difficulty: medium
source_model: opus-5
skills:
  - causal-explanation
  - general-knowledge
title: How DNS turns a name into an address, at a lookup-chain level
approx_words: 800
---

# How DNS turns a name into an address, at a lookup-chain level

Type a hostname into a browser and something must convert that string
into an IP address, because routers forward packets by address and know
nothing about names. The Domain Name System does that conversion. It
solves a hard problem — a global directory that no single organisation
owns, that updates constantly, and that answers enormous query volumes —
by never storing the whole thing anywhere.

## Names are read right to left

A name like `shop.example.com` is a path through a tree whose root is on
the right. There is even a silent trailing dot: the fully qualified name
is `shop.example.com.`, and that final dot is the root.

- `.` is the root zone.
- `com` is a top-level domain.
- `example.com` is a zone delegated by the `com` operator to whoever
  registered it.
- `shop` is a record inside that zone.

Each level does one job: it knows the answers it is authoritative for,
and it knows who to ask about the level below. Nobody holds the whole
tree. That *delegation* is what makes the system scale, and it lets an
organisation change its own records without permission from above.

## The chain, one query at a time

Your device does almost none of this work. It runs a *stub resolver* that
forwards the question to a configured *recursive resolver* — run by your
ISP, your company, or a public service — and waits. The recursive
resolver does the walking. Assume every cache is empty, the worst case:

1. **Resolver to a root server.** "What is the address of
   `shop.example.com`?" A root server does not know. It replies with a
   *referral*: the servers authoritative for `com`. Root server addresses
   are the one thing hard-coded into every resolver, which is how the
   process bootstraps.

2. **Resolver to a `com` server.** Same question. The `com` servers do
   not know either; they only track delegations. They refer the resolver
   to the nameservers listed for `example.com`.

3. **Resolver to `example.com`'s nameserver.** This server *is*
   authoritative for the zone. It reads its zone file and returns the
   actual record: an A record with an IPv4 address, or an AAAA record
   with an IPv6 one.

4. **Resolver to your device.** The resolver returns the address.

Only now does the browser open a TCP connection to that address; DNS is a
prerequisite step and carries no web traffic itself.

Along the way the resolver may hit a CNAME record — "this name is an
alias for that one" — and must restart the lookup for the target. CNAME
chains are common with content delivery networks and are a frequent
source of surprising latency.

## Caching is what makes it fast

Three or four round trips per name would be intolerable, so every record
carries a *time to live* in seconds. The recursive resolver caches the
answer for that long, and so does your operating system and often your
browser. The full chain above therefore almost never happens. Root and
TLD referrals have very long TTLs and are effectively permanent in a busy
resolver's cache, so a typical lookup for a new name under a known domain
is a single query, and a popular name is answered from cache in under a
millisecond.

TTL is a direct trade between speed and agility. A one-day TTL means
excellent cache hit rates and a full day before a changed address is
universally visible. A sixty-second TTL means fast failover and far more
query traffic.

Two other details matter. DNS traditionally runs over UDP on port 53 with
no encryption, so queries are visible to the network path — the
motivation for DNS over HTTPS and DNS over TLS. Separately, DNSSEC adds
signatures so a resolver can verify an answer came from the zone's owner,
since plain DNS cannot tell a real answer from a forged one.

## Limiting case: what if you change your server's IP address?

You migrate to a new host and update the A record for `shop.example.com`.
What happens next is governed entirely by TTL, and it explains the
phenomenon people describe vaguely as "DNS propagation."

Nothing propagates. Nobody is pushed anything. Every cache holding the
old answer keeps serving it until its own countdown expires, and only
then asks again. If the TTL was 86,400 seconds, a resolver that cached
the record one minute before your change hands out the old address for
nearly 24 more hours.

So during the transition your users split. Some resolvers have expired
and fetched the new address; others have not. Two people on different
networks reach different servers, and one person may flip between them as
caches expire. Shut the old server down immediately and those users see
connection failures — not because DNS is broken, but because it is doing
precisely what it was told to do.

The correct procedure follows from the mechanism. Well before the move,
lower the TTL to something like 300 seconds and wait out the *old* TTL so
every cache picks up the short one. Then change the record; worst-case
staleness is now five minutes. Keep the old server answering, ideally
proxying to the new one, until its traffic drops to zero, then raise the
TTL again. There is no button to flush the world's caches, so the only
lever you have is one you must pull in advance.
