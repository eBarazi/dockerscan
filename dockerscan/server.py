from flask import Flask, render_template, request, jsonify
import subprocess, json, docker

app = Flask(__name__)
client = docker.from_env()

@app.route("/")
def index():
    # Detect mode: 'images' (default) or 'containers'
    mode = request.args.get("mode", "images")

    if mode == "containers":
        # List running containers
        containers = [
            {
                "id": c.short_id,
                "name": c.name,
                "image": c.image.tags[0] if c.image.tags else "<none>:<none>",
                "status": c.status
            }
            for c in client.containers.list()
        ]
        return render_template("index.html", items=containers, mode=mode)
    else:
        # List available images
        images = [
            {"id": img.short_id, "tags": img.tags or ["<none>:<none>"]}
            for img in client.images.list()
        ]
        return render_template("index.html", items=images, mode=mode)

@app.route("/scan", methods=["POST"])
def scan():
    image = request.form.get("image")
    if not image:
        return jsonify({"error": "No image specified"}), 400

    try:
        cmd = ["trivy", "image", "--format", "json", image]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        # Count severities
        summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
        for res in data.get("Results", []):
            for vuln in res.get("Vulnerabilities", []):
                sev = vuln.get("Severity")
                if sev in summary:
                    summary[sev] += 1

        return jsonify({"summary": summary, "raw": data})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.stderr or str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
