# Endpoint Health Monitor

This tool monitors the availability of multiple HTTP endpoints as defined in a YAML configuration file. It performs periodic checks, evaluates the responses based on availability criteria, and logs aggregated availability per domain.

---

## Setup

1. Clone the repository:
   ```bash
   git clone <your_repo_url_here>
   cd <your_repo_directory>
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:

   On Mac/Linux:
   ```bash
   source .venv/bin/activate
   ```

   On Windows:
   ```powershell
   .venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

Run the monitoring script with a YAML config file:

```bash
python main.py sample.yaml
```

Each run will:
- Check all endpoints every 15 seconds
- Evaluate response status and latency
- Aggregate and log availability by domain
- Create a timestamped log file (e.g. `health_check_2025-04-20_17-11-40.log`)

The program will continue running until interrupted (`Ctrl+C`).

---

## Configuration File Format

The configuration file should be in YAML format with the following structure:

```yaml
- name: endpoint_name
  url: https://example.com/endpoint
  method: GET        # Optional, defaults to GET if not specified
  headers:           # Optional
    content-type: application/json
  body: '{"key":"value"}'  # Optional, JSON string
```

See `sample.yaml` for full examples.

---

## 🔍 Implementation Notes

<details>
  <summary>Availability Criteria</summary>

**Requirement:** Endpoint is considered “UP” if:
- HTTP response status code is in the 200 range
- Response is received in under 500 milliseconds
</details>

<details>
  <summary>Domain Aggregation</summary>

Endpoints are grouped by domain using `urllib.parse.urlparse`, ignoring port numbers.
</details>

<details>
  <summary>Timing Precision</summary>

Each check cycle duration is tracked, and `sleep()` is adjusted to ensure checks occur every 15 seconds, regardless of processing overhead.
</details>

<details>
  <summary>Log Output</summary>

Each run creates a log file with a timestamp-based filename:

```
health_check_YYYY-MM-DD_HH-MM-SS.log
```

Both console output and file output use the same format:
```
2025-04-20 17:11:40,513 - INFO - [example.com] Availability: 75%
```
</details>

<details>
  <summary>YAML Validation</summary>

On load, the script verifies:
- File exists and is valid YAML
- Top-level structure is a list
- Each item is a dictionary
- Each entry has at least `name` (str) and `url` (str)
</details>

<details>
  <summary>Graceful Interrupt</summary>

Interrupting with `Ctrl+C` exits cleanly with a final log statement.
</details>

---

## 🛠️ Issues Identified and Fixes Made

<details>
  <summary>Response Time Enforcement</summary>

**Issue:** Initial version treated any 2xx response as “UP”, without validating latency.

**Fix:** Measured request duration and enforced a 500ms upper limit on success.
</details>

<details>
  <summary>Default HTTP Method</summary>

**Issue:** Configuration required a method field explicitly.

**Fix:** Defaulted to GET if no method is provided.
</details>

<details>
  <summary>Domain Normalization</summary>

**Issue:** Full URLs were used for grouping, potentially splitting stats unnecessarily.

**Fix:** Parsed and grouped by domain only using `urlparse()`, ignoring ports and paths.
</details>

<details>
  <summary>Cycle Duration Compensation</summary>

**Issue:** Used a fixed 15-second sleep that didn’t account for request overhead.

**Fix:** Tracked elapsed time and dynamically adjusted sleep to maintain true 15s intervals.
</details>

<details>
  <summary>Body Payload Parsing</summary>

**Issue:** YAML body strings were passed raw, causing malformed JSON in some cases.

**Fix:** Added a parsing function that safely converts JSON strings to dictionaries.
</details>

<details>
  <summary>Availability % Casting</summary>

**Issue:** Percentages were rounded, sometimes displayed as floats.

**Fix:** Used integer casting to drop decimal precision for cleaner logging.
</details>

<details>
  <summary>YAML Schema Validation</summary>

**Issue:** No safety checks were done on the config structure.

**Fix:** Added validations for file presence, list type, and required fields (`name`, `url`).
</details>

<details>
  <summary>Graceful Exit Handling</summary>

**Issue:** Script crashed ungracefully on Ctrl+C.

**Fix:** Added exception handling for `KeyboardInterrupt` with log output.
</details>

<details>
  <summary>Timestamped Logging</summary>

**Issue:** Logs were only printed to console without history or rotation.

**Fix:** Introduced logging to a timestamped file in parallel with stdout.
</details>
