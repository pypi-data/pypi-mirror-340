import requests
import json
import csv
import logging
import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from jinja2 import Environment, FileSystemLoader
from collections import Counter
import time
import getpass

# Configuration
NVD_API_BASE = "https://services.nvd.nist.gov/rest/json"
CPE_API = f"{NVD_API_BASE}/cpes/2.0"
CVE_API = f"{NVD_API_BASE}/cves/2.0"
API_KEY = os.environ.get("NVD_API_KEY")  # Try to get from environment variable

logging.basicConfig(level=logging.WARNING)

def search_cpe_from_user_input(product, version):
    global API_KEY  # Declare API_KEY as global to allow reassignment
    query = f"{product} {version}"
    headers = {"apiKey": API_KEY} if API_KEY else {}
    print(f"Using API Key: {API_KEY or 'None'}")  # Debug print
    response = requests.get(CPE_API, headers=headers, params={"keywordSearch": query})
    if response.status_code != 200:
        print(f"❌ Failed to fetch CPEs: {response.status_code} - {response.text}")
        if response.status_code == 403 and not API_KEY:
            print("⚠️ NVD API key is required. Set NVD_API_KEY environment variable or enter it below.")
            api_key_input = getpass.getpass("Enter NVD API Key: ")
            if api_key_input:
                API_KEY = api_key_input
                headers = {"apiKey": API_KEY}
                response = requests.get(CPE_API, headers=headers, params={"keywordSearch": query})
                if response.status_code != 200:
                    print(f"❌ Failed with provided key: {response.status_code} - {response.text}")
                    return []
            else:
                return []
        return []
    products = response.json().get("products", [])
    results = []
    for entry in products:
        cpe = entry.get("cpe", {}).get("cpeName")
        title = entry.get("titles", [{}])[0].get("title", cpe)
        if cpe:
            results.append((cpe, title))
    return results

def fetch_cves(cpe_uri, severity=None):
    global API_KEY  # Declare API_KEY as global to allow reassignment
    headers = {"apiKey": API_KEY} if API_KEY else {}
    #print(f"Debug: Using API Key for CVE fetch: {API_KEY or 'None'}")  # Debug print
    params = {"cpeName": cpe_uri, "resultsPerPage": 2000}
    if severity:
        params["cvssV3Severity"] = severity.upper()
    all_cves = []
    start_index = 0

    while True:
        params["startIndex"] = start_index
        response = requests.get(CVE_API, headers=headers, params=params)
        if response.status_code != 200:
            print(f"❌ Failed to fetch CVEs: {response.status_code} - {response.text}")
            if response.status_code == 403 and not API_KEY:
                print("⚠️ NVD API key is required. Set NVD_API_KEY environment variable or enter it below.")
                api_key_input = getpass.getpass("Enter NVD API Key: ")
                if api_key_input:
                    API_KEY = api_key_input
                    headers = {"apiKey": API_KEY}
                    response = requests.get(CVE_API, headers=headers, params=params)
                    if response.status_code != 200:
                        print(f"❌ Failed with provided key: {response.status_code} - {response.text}")
                        break
                else:
                    break
            break
        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])
        all_cves.extend(vulnerabilities)
        total_results = data.get("totalResults", 0)
        if start_index + len(vulnerabilities) >= total_results:
            break
        start_index += 2000
        time.sleep(0.5)  # Respect rate limits

    return all_cves

def output_results(cves, output_format="json", output_file=None):
    if not cves:
        print("⚠️ No CVEs found.")
        return

    if output_format == "json":
        # Transform cves to include id as a dictionary with url
        enriched_cves = []
        for item in cves:
            cve = item["cve"]
            product = item.get("product", "Unknown")
            cve_id = cve["id"]
            url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
            enriched_cve = {
                "product": product,
                "id": {"value": cve_id, "url": url},
                "published": cve.get("published"),
                "lastModified": cve.get("lastModified"),
                "cvssScore": cve.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseScore", "N/A"),
                "severity": cve.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseSeverity", "N/A"),
                "description": cve.get("descriptions", [{}])[0].get("value", "N/A")
            }
            enriched_cves.append({"cve": enriched_cve})
        with open(output_file or "output.json", "w", encoding="utf-8") as f:
            json.dump(enriched_cves, f, indent=2)
        print(f"✅ JSON report written to {output_file or 'output.json'}")

    elif output_format == "csv":
        keys = ["product", "id", "published", "lastModified", "cvssScore", "severity", "description"]
        with open(output_file or "output.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for item in cves:
                cve = item["cve"]
                product = item.get("product", "Unknown")
                cve_id = cve["id"]
                url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
                writer.writerow({
                    "product": product,
                    "id": f'=HYPERLINK("{url}", "{cve_id}")',
                    "published": cve.get("published"),
                    "lastModified": cve.get("lastModified"),
                    "cvssScore": cve.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseScore", "N/A"),
                    "severity": cve.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseSeverity", "N/A"),
                    "description": cve.get("descriptions", [{}])[0].get("value", "N/A")
                })
        print(f"✅ CSV report written to {output_file or 'output.csv'}")

def generate_html_report(cves, output_file="report.html"):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.html")

    rows = []
    severity_counter = Counter()
    for item in cves:
        cve = item["cve"]
        product = item.get("product", "Unknown")
        cve_id = cve["id"]
        url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
        metrics = cve.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {})
        severity = metrics.get("baseSeverity", "UNKNOWN")
        score = metrics.get("baseScore", "N/A") if metrics.get("baseScore") else "N/A"
        description = cve.get("descriptions", [{}])[0].get("value", "N/A")
        published = cve.get("published", "N/A")
        severity_counter[severity] += 1

        rows.append({
            "product": product,
            "id": cve_id,
            "url": url,
            "severity": severity,
            "score": score,
            "description": description,
            "published": published
        })

    html = template.render(cves=rows, severity_counts=severity_counter)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📄 HTML report written to {output_file}")

def main():
    parser = ArgumentParser(
        description="""\
🔍 vuln-checker: Search CVEs by CPE product/version

Pre-requisite:
Check the: https://github.com/skm248/vuln-checker/blob/main/README.md for the NVD_API_KEY section for more information.

Features:
- Fetch matching CPEs using product & version
- Batch mode to scan multiple products via CSV
- Interactive selection if multiple CPEs found
- Pull CVEs from NVD (filter by severity)
- Export results in JSON, CSV, or HTML
- Auto-download & manage official CPE dictionary

Examples:
  vuln-checker --input-csv products.csv --format html --output report.html
  vuln-checker --products "jquery:1.11.3,lodash:3.5.0" --format csv --output output.csv
""",
        formatter_class=RawDescriptionHelpFormatter
    )

    # Mutually exclusive group requiring one of input-csv or products
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input-csv", help="Path to CSV file with 'product' and 'version' columns")
    group.add_argument("--products", help="Comma-separated list of product:version pairs (e.g. tomcat:9.0.46,mysql:8.0.35)")

    parser.add_argument("--severity", help="Filter by severity (LOW, MEDIUM, HIGH, CRITICAL)")
    parser.add_argument("--format", choices=["json", "csv", "html"], default="json", help="Output format")
    parser.add_argument("--output", help="Output file name")

    args = parser.parse_args()

    all_cves = []

    # Process input based on availability
    if args.input_csv:
        # Read from CSV
        try:
            with open(args.input_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                if not {'product', 'version'}.issubset(reader.fieldnames):
                    print("❌ CSV must contain 'product' and 'version' columns.")
                    return
                for row in reader:
                    product = row['product'].strip()
                    version = row['version'].strip()
                    if not product or not version:
                        print(f"⚠️ Skipping invalid row: {row}")
                        continue

                    print(f"🔍 Searching CPE for {product} {version}")
                    cpes = search_cpe_from_user_input(product, version)

                    if not cpes:
                        print(f"❌ No CPEs found for {product} {version}")
                        continue

                    if len(cpes) == 1:
                        cpe_uri = cpes[0][0]
                    else:
                        print(f"Multiple CPEs found for {product} {version}:")
                        for idx, (uri, title) in enumerate(cpes):
                            print(f"  [{idx+1}] {title} → {uri}")
                        choice = int(input(f"Select CPE [1-{len(cpes)}]: "))
                        cpe_uri = cpes[choice - 1][0]

                    print(f"🛡️ Fetching CVEs for {cpe_uri}")
                    cves = fetch_cves(cpe_uri, severity=args.severity)
                    for cve in cves:
                        cve["product"] = f"{product}:{version}"
                    all_cves.extend(cves)
        except FileNotFoundError:
            print(f"❌ CSV file '{args.input_csv}' not found.")
            return
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            return
    else:
        # Process from command-line argument
        product_version_pairs = [p.strip() for p in args.products.split(",")]
        for pair in product_version_pairs:
            try:
                product, version = pair.split(":")
            except ValueError:
                print(f"❌ Invalid format: {pair}. Use product:version.")
                continue

            print(f"🔍 Searching CPE for {product} {version}")
            cpes = search_cpe_from_user_input(product, version)

            if not cpes:
                print(f"❌ No CPEs found for {product} {version}")
                continue

            if len(cpes) == 1:
                cpe_uri = cpes[0][0]
            else:
                print(f"Multiple CPEs found for {product} {version}:")
                for idx, (uri, title) in enumerate(cpes):
                    print(f"  [{idx+1}] {title} → {uri}")
                choice = int(input(f"Select CPE [1-{len(cpes)}]: "))
                cpe_uri = cpes[choice - 1][0]

            print(f"🛡️ Fetching CVEs for {cpe_uri}")
            cves = fetch_cves(cpe_uri, severity=args.severity)
            for cve in cves:
                cve["product"] = f"{product}:{version}"
            all_cves.extend(cves)

    if args.format == "html":
        generate_html_report(all_cves, args.output or "report.html")
    else:
        output_results(all_cves, args.format, args.output)

if __name__ == "__main__":
    main()