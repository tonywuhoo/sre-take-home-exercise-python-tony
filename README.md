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

## Usage

Run the monitoring script with a YAML config file:

```bash
python main.py sample.yaml
```

Each run will:
- Check all endpoints every 15 seconds
- Evaluate response status and latency
- Aggregate and log availability by domain
- Create a timestamped log file (e.g. health_check_2025-04-20_17-11-40.log)

The program will continue running until interrupted (Ctrl+C).

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

See sample.yaml for full examples.

---

## Changelog

<details>
  <summary>Availability Criteria</summary>
  <br>

  **Issue:** Did not enforce 500ms response latency.

  **Fix:** Measured duration and included latency in success criteria.
</details>

<details>
  <summary>Domain Grouping</summary>
  <br>

  **Issue:** Used full URL instead of normalized domain.

  **Fix:** Parsed domain using urlparse and stripped port/path.
</details>

<details>
  <summary>Cycle Accuracy</summary>
  <br>

  **Issue:** Fixed sleep timing didn’t account for overhead.

  **Fix:** Tracked cycle duration and adjusted sleep to stay aligned.
</details>

<details>
  <summary>Config Parsing</summary>
  <br>

  **Issue:** No error handling or schema validation for YAML.

  **Fix:** Validated file, type, and required keys (name, url).
</details>

<details>
  <summary>Graceful Shutdown</summary>
  <br>

  **Issue:** Script exited uncleanly on Ctrl+C.

  **Fix:** Added KeyboardInterrupt handling with clean log.
</details>

<details>
  <summary>Logging Format</summary>
  <br>

  **Issue:** No file logs, no timestamps.

  **Fix:** Used logging.FileHandler with timestamped log file and stdout mirror.
</details>
