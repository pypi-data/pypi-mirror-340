# TextOps API Client (Under Construction 🚧)

> This package is currently under development. Expect changes, improvements, and possible breaking updates.

A simple Python client for the [TextOps](https://text-ops-subs.com/) transcription API.  
Easily submit audio files for transcription, check status, and retrieve results.

---

## 📦 Installation

```bash
pip install textops-api-v1
```

---

## 🧪 Quick Examples

### Example 1: Manual submission and polling

```python
from textops_api_v1 import TextOpsAPI

# Initialize the client with your API key
api_key = "your api key"
client = TextOpsAPI(api_key=api_key)

audio_url = "audio url"

try:
    # Submit audio for transcription
    response = client.submit_transcription(audio_url)
    job_id = response['textopsJobId']
    
    # Check status
    status = client.check_status(job_id)
    print(f"Current status: {status}")
    
    # Wait for completion
    result = client.wait_for_completion(job_id)
    if result and 'text' in result:
        print(f"Transcription complete! First 100 chars: {result['text'][:100]}...")
    else:
        print("Transcription failed or timed out.")
except Exception as e:
    print(f"Error: {e}")
```

---

### Example 2: All-in-one method

```python
from textops_api_v1 import TextOpsAPI

client = TextOpsAPI(api_key="your api key")
audio_url = "audio url"

try:
    result = client.transcribe(audio_url)
    print("Transcription complete!")
    print(f"First 100 chars: {result['text'][:100]}")
    print(f"Total length: {len(result['text'])} characters")
except Exception as e:
    print(f"Error: {e}")
```

---


## ⚠️ Disclaimer

This package is in **alpha**. APIs may change and documentation is still in progress.

---

## 📄 License

MIT

---

## 📬 Contact

For questions or issues, open a GitHub issue or reach out to `your@email.com`.