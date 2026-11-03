"""Upload a local file to a Shopify staged-upload target.

1. Call Shopify stagedUploadsCreate (via the Shopify connector) and save its
   stagedTargets[0] object as target.json  ({"url":..., "resourceUrl":..., "parameters":[{name,value},...]})
2. python3 upload.py target.json path/to/file [index]   (index picks one of several stagedTargets, default 0)
3. Call fileCreate with originalSource = resourceUrl (contentType IMAGE or VIDEO), then read the CDN URL.
Prints OK + resourceUrl on success.
"""
import json, mimetypes, subprocess, sys

target = json.load(open(sys.argv[1]))
if "stagedTargets" in target:
    target = target["stagedTargets"][int(sys.argv[3]) if len(sys.argv) > 3 else 0]
path = sys.argv[2]
mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
cmd = ["curl", "-sS", "-m", "300", "-o", "/dev/null", "-w", "%{http_code}", target["url"]]
for p in target["parameters"]:
    cmd += ["-F", f"{p['name']}={p['value']}"]
cmd += ["-F", f"file=@{path};type={mime}"]
code = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
if code not in ("200", "201", "204"):
    sys.exit(f"UPLOAD FAILED http {code}")
print("OK", target["resourceUrl"])
