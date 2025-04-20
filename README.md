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
  <summary>Response Time Check</summary>
  <br>

  **Issue:** Only HTTP status was considered for success.

  **Fix:** Response time is measured; success requires < 500ms.
</details>

<details>
  <summary>Default HTTP Method</summary>
  <br>

  **Issue:** Missing method in YAML would cause failure.

  **Fix:** If method is not specified, it defaults to GET.
</details>

<details>
  <summary>Port Number Handling</summary>
  <br>

  **Issue:** Availability was tracked per URL, not domain.

  **Fix:** Used urllib.parse to extract and normalize the domain.
</details>

<details>
  <summary>Timing Compensation</summary>
  <br>

  **Issue:** Sleep interval didn't account for processing time.

  **Fix:** Cycle duration is measured, and sleep is adjusted to maintain 15s total.
</details>

<details>
  <summary>Body Payload Parsing</summary>
  <br>

  **Issue:** JSON in body field caused errors if passed as string.

  **Fix:** Body string is parsed into a dictionary if needed.
</details>

<details>
  <summary>YAML Validation</summary>
  <br>

  **Issue:** Invalid or missing fields could crash the script.

  **Fix:** Added validation for file existence, structure, and endpoint existence.
</details>

<details>
  <summary>Logging Format</summary>
  <br>

  **Issue:** No persistent logging.

  **Fix:** Output is logged both to stdout and a timestamped file, and marked appropriately using INFO and WARNING
</details>
