import json, os, urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

KEY = open(os.path.expanduser("~/.runpod/api_key")).read().strip()
print("key:", KEY[:8] + "..." + KEY[-4:], "len", len(KEY))

def gql(query, variables=None):
    body = {"query": query}
    if variables: body["variables"] = variables
    req = urllib.request.Request(
        "https://api.runpod.io/graphql",
        data=json.dumps(body).encode(),
        headers={"api-key": KEY, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"http_error": e.code, "body": e.read().decode()[:300]}

# 1. who am I - account tier
r = gql("query { myself { id email } }")
print("myself:", r)

# 2. account balance + credit info
r2 = gql("query { myself { id } }")
print("balance query attempted")

# 3. current pods (all)
r3 = gql("""query {
  myself { pods {
    id name desiredStatus
    runtime { uptimeInSeconds gpus { id gpuUtilPercent memoryUtilPercent } }
    machine { gpuDisplayName gpuCount }
  } }
}""")
print("pods:", json.dumps(r3, indent=1)[:800])

# 4. serverless endpoints
r4 = gql("""query {
  myself { serverlessEndpoints { id name status gpus } }
}""")
print("serverless:", json.dumps(r4, indent=1)[:500])