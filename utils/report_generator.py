# utils/report_generator.py
import os
import datetime

def generate_full_pipeline_report(all_user_data, report_root="reports", timestamp_dir=None):
    """
    Generates HTML report with all users' pass/fail steps.
    """
    if timestamp_dir is None:
        timestamp_dir = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = os.path.join(report_root, timestamp_dir)
    os.makedirs(report_dir, exist_ok=True)

    total = len(all_user_data)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'><title>Full Pipeline Report</title>",
        "<style>body{font-family:Arial,sans-serif} .pass{color:green} .fail{color:red} "
        "table{border-collapse:collapse;width:100%} th,td{border:1px solid #ccc;padding:4px;text-align:left} "
        "img{max-width:150px;max-height:150px} details{margin-bottom:10px} pre{background:#f4f4f4;padding:8px;}"
        "</style></head><body>",
        f"<h1>Full Pipeline Report</h1><p>{timestamp}</p>",
        f"<p>Total Users: {total}</p>"
    ]

    for user, data in all_user_data.items():
        has_errors = bool(data.get("errors"))
        status_class = "fail" if has_errors else "pass"
        status_label = "FAILED" if has_errors else "PASSED"
        html.append(f"<details><summary class='{status_class}'>{user} — {status_label}</summary>")

        if data.get("timings"):
            html.append("<h3>Page Load Times (s)</h3><ul>")
            for page_name, timing in data["timings"].items():
                html.append(f"<li>{page_name}: {timing}</li>")
            html.append("</ul>")

        steps = data.get("steps", [])
        if steps:
            html.append("<h3>Actions</h3><table><tr><th>Action</th><th>Status</th><th>Details</th></tr>")
            for s in steps:
                status = "OK" if s.get("ok") else "FAIL"
                details = s.get("details", {}) or {}
                dstr = "; ".join(f"{k}: {v}" for k, v in details.items())
                html.append(f"<tr><td>{s.get('name')}</td><td>{status}</td><td>{dstr}</td></tr>")
            html.append("</table>")

        if data.get("screenshot"):
            p = data["screenshot"]
            if os.path.isfile(p):
                html.append("<h3>Screenshot</h3>")
                html.append(f"<img src='{p}' alt='screenshot'>")

        html.append("</details>")

    html.append("</body></html>")

    path = os.path.join(report_dir, "full_pipeline.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"HTML report generated: {path}")
    return report_dir
