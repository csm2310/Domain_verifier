from flask import Flask, render_template, request, jsonify
import socket
import whois
import dns.resolver
import requests

app = Flask(__name__)

def check_domain(domain):
    result = {"domain": domain, "status": "unknown"}
    
    # Check if domain resolves to an IP
    try:
        ip = socket.gethostbyname(domain)
        result["resolved_ip"] = ip
        result["status"] = "active"
    except socket.gaierror:
        result["status"] = "inactive"
    
    # Fetch WHOIS details
    try:
        domain_info = whois.whois(domain)
        result["whois"] = domain_info.domain_name
    except Exception:
        result["whois"] = "Not Found"

    # Check MX records (email server records)
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        result["mx_records"] = [str(record.exchange) for record in mx_records]
    except Exception:
        result["mx_records"] = "No MX records found"

    # Check if the domain is accessible via HTTP
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        result["http_status"] = response.status_code
    except requests.RequestException:
        result["http_status"] = "No response"

    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    domain = data.get("domain")
    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    result = check_domain(domain)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
