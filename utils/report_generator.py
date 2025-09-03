# utils/report_generator.py
import os
import datetime

def generate_full_pipeline_report(all_user_data, report_root="reports", timestamp_dir=None):
    """
    Generates HTML report with per-test steps and screenshots.
    """
    if timestamp_dir is None:
        timestamp_dir = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    report_dir = os.path.join(report_root, timestamp_dir)
    os.makedirs(report_dir, exist_ok=True)

    total = len(all_user_data)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'><title>Full Pipeline Report</title>",
        "<style>body{font-family:Arial,sans-serif} .pass{color:green} .fail{color:red} "
        "table{border-collapse:collapse;width:100%} th,td{border:1px solid #ccc;padding:4px;text-align:left} "
        "img{max-width:250px;max-height:200px;display:block;margin:4px 0} details{margin-bottom:10px} pre{background:#f4f4f4;padding:8px;}"
        "</style></head><body>",
        f"<h1>Full Pipeline Report</h1><p>{timestamp}</p>",
        f"<p>Total Users: {total}</p>"
    ]

    for user, data in all_user_data.items():
        has_errors = bool(data.get("errors")) or any(not s.get("ok") for s in data.get("steps", []))
        status_class = "fail" if has_errors else "pass"
        status_label = "FAILED" if has_errors else "PASSED"
        html.append(f"<details open><summary class='{status_class}'>{user} — {status_label}</summary>")

        # Split steps per test if 'test_name' present
        test_groups = {}
        for step in data.get("steps", []):
            test_name = step.get("test_name", "General")
            test_groups.setdefault(test_name, []).append(step)

        for test_name, steps in test_groups.items():
            html.append(f"<details open><summary>{test_name}</summary>")
            html.append("<table><tr><th>Action</th><th>Status</th><th>Details</th><th>Screenshot</th></tr>")
            for s in steps:
                status = "OK" if s.get("ok") else "FAIL"
                details = s.get("details", {}) or {}
                dstr = "; ".join(f"{k}: {v}" for k, v in details.items())
                screenshot_html = ""
                if s.get("screenshot") and os.path.isfile(s["screenshot"]):
                    screenshot_html = f"<img src='{s['screenshot']}' alt='screenshot'>"
                html.append(f"<tr><td>{s.get('name')}</td><td class='{status_class}'>{status}</td><td>{dstr}</td><td>{screenshot_html}</td></tr>")
            html.append("</table></details>")

        html.append("</details>")

    html.append("</body></html>")

    path = os.path.join(report_dir, "full_pipeline.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"HTML report generated: {path}")
    return report_dir
