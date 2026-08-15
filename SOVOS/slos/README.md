# SLOs-as-code — the fabric's availability contract (v1, 2026-08-15)

Pattern: Google SRE workbook / GitHub & Stripe publish availability. Three
SLOs only — the discipline is in NOT having more.

## The 3 SLOs (Sloth format, Apache-2.0)

```yaml
version: "2.0"
service: "council-of-ai"
slos:
  - name: "registry-api-availability"
    objective: 99.5
    description: "GSPC MCP + verify endpoints answer"
    sli:
      events:
        errorQuery: "rate(probe_success == 0)"
      ratioErrors: true
    alerting:
      page:
        disable: true
      ticket:
        labels: [coai-ops]
  - name: "index-on-time"
    objective: 95.0
    description: "Daily index (closing-cross value) published before 00:30 UTC"
    slo:
      events:
        errorQuery: "rate(index_late_total)"
        ratioErrors: true
  - name: "card-verification-success"
    objective: 99.9
    description: "Signed cards verify successfully when checked"
    slo:
      events:
        errorQuery: "rate(verify_failed_total)"
        ratioErrors: true
```

## The error-budget policy

- When a budget burns (30-day window over threshold), **non-essential changes
  are frozen** and we say so publicly on the status page
- The three SLOs are checked by a Upptime/Sloth combo: Upptime for reach,
  Sloth for the budget math
- Monthly availability report commits to git (GitHub monthly-report pattern —
  mixed news is the trust signal)

## The registry SLO interpretation

"99.5% registry API availability" is the honest version of an uptime promise
for an institution whose product is verification. We publish the SLOs; we
publish the misses. That candor is the moat.

## Where it runs

- Upptime (GitHub Actions + Pages) for reachability — zero infra
- Sloth YAML consumed by Prometheus/Grafana when we stand up the metrics
  stack — until then the YAML + Upptime history IS the SLO record