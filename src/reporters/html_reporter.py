class HTMLReporter:
    def generate(self, results):
        return f"<html><body><h1>Scan Report</h1><p>Findings: {len(results.findings)}</p></body></html>"
