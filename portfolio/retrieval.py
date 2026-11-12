import json, re, urllib.request
M = "https://tony-isaac-portfolio.mintlify.site/mcp"
H = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
def rpc(body, sid=None):
    h = dict(H)
    if sid: h["Mcp-Session-Id"] = sid
    r = urllib.request.urlopen(urllib.request.Request(M, json.dumps(body).encode(), h), timeout=30)
    raw = r.read().decode()
    data = [l[5:].strip() for l in raw.splitlines() if l.startswith("data:")]
    return r.headers.get("mcp-session-id"), json.loads(data[-1] if data else raw)
sid, _ = rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"t","version":"1"}}})
tests = [
 ("My Express webhook handler returns 401 for every event Hookferry forwards", "troubleshooting/signature-errors"),
 ("I stopped hookferry listen overnight, will missed webhooks show up", "concepts/retries-and-replay|guides/replay-failed-events|troubleshooting/missing-events|resources/faq"),
 ("How many times does Hookferry retry an HTTPS destination and over how long", "concepts/retries-and-replay"),
 ("forward only events whose type starts with invoice. to port 8080 path /hooks", "cli/listen|guides/filter-events"),
 ("use Hookferry in GitHub Actions without hookferry login", "guides/use-hookferry-in-ci"),
 ("Free plan replay an event from 10 days ago", "concepts/events-and-attempts|resources/faq|guides/replay-failed-events"),
 ("app runs in Docker and listen says connection refused", "troubleshooting/connection-refused"),
 ("what happens when I hit the API rate limit", "api-reference/rate-limits"),
 ("how do I delete a source using the CLI", "concepts/sources-routes-destinations|resources/faq"),
 ("can my teammate and I both receive events from the same source", "cli/listen|resources/faq"),
]
hits = 0
for i, (q, want) in enumerate(tests, 1):
    _, res = rpc({"jsonrpc":"2.0","id":10+i,"method":"tools/call","params":{"name":"search_hookferry","arguments":{"query":q}}}, sid)
    text = " ".join(c.get("text","") for c in res.get("result",{}).get("content",[]))
    paths = []
    for p in re.findall(r"mintlify\.(?:site|app)/([a-z0-9/\-]+)", text):
        if p not in paths: paths.append(p)
    rank = next((n for n, p in enumerate(paths, 1) if re.fullmatch(want, p)), None)
    ok = rank is not None and rank <= 3
    hits += ok
    print(f"{i:>2}. {'PASS' if ok else 'MISS'} rank={rank} top3={paths[:3]}")
print(f"\n{hits}/10 questions had the answer page in the top 3 results")
