class JSONReporter:
    def generate(self, results):
        import json
        return json.dumps(results.get_summary(), indent=2)
