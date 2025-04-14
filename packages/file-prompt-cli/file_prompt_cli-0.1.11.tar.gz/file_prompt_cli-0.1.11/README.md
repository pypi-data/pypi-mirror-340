# Multimodal Python CLI Tool for LLM Evaluation

A command-line tool that processes various document types (text, PDFs, images) through LLMs using Google Cloud Platform (GCP) services and the Gemini API. The tool supports multimodal input and leverages GCP services like Cloud Storage (GCS) and Pub/Sub for scalable processing.

## Features

- **GCP Integration**:
  - Cloud Storage (GCS) for file storage
  - Pub/Sub for message queuing
  - Gemini API for LLM processing
  - IAM-based security

- **Multi-format Support**: Process various file types including:
  - Text files (.txt)
  - PDF documents (.pdf)
  - Word documents (.docx)
  - CSV data files (.csv)
  - PowerPoint presentations (.ppt, .pptx)
  - Images (.jpg, .png)

- **Scalable Architecture**:
  - Distributed processing
  - Message queuing
  - Parallel processing
  - Result streaming

## Installation

### System Dependencies

Before installing the package, you need to install system-level dependencies:

#### macOS
```bash
brew install libmagic
```

#### Ubuntu/Debian
```bash
sudo apt-get install libmagic1
```

#### Windows
No additional system dependencies needed.

### Package Installation

After installing the system dependencies, install the package:

```bash
pip install file-prompt-cli
```

### Option 2: Install from source

1. Clone the repository:

```bash
git clone https://github.com/yourusername/file-prompt-cli.git
cd file-prompt-cli
```

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

1. Install the package:

```bash
pip install -e .
```

1. Set up environment variables:
   Create a `.env` file in the project root with the following variables:

```bash
# GCP Configuration
GCP_PROJECT_ID=your-project-id
GCS_BUCKET_NAME=your-bucket-name

# Pub/Sub Configuration
PUBSUB_TOPIC=your-topic-name
PUBSUB_SUBSCRIPTION=your-subscription-name
PUBSUB_RESULTS_TOPIC=your-results-topic-name
PUBSUB_RESULTS_SUBSCRIPTION=your-results-subscription-name

# API Keys
GOOGLE_API_KEY=your-gemini-api-key
```

   You can also set these variables in your environment:
```bash
export GCP_PROJECT_ID="your-project-id"
export GCS_BUCKET_NAME="your-bucket-name"
export PUBSUB_TOPIC="your-topic-name"
export PUBSUB_SUBSCRIPTION="your-subscription-name"
export PUBSUB_RESULTS_TOPIC="your-results-topic-name"
export PUBSUB_RESULTS_SUBSCRIPTION="your-results-subscription-name"
export GOOGLE_API_KEY="your-gemini-api-key"
```

5. Set up GCP credentials:

   - Create a service account with appropriate permissions:
     - Cloud Storage Admin
     - Pub/Sub Publisher
     - Pub/Sub Subscriber
   - Download the JSON key file
   - Set the credentials path:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
```

## GCP Setup

1. **Create a GCS Bucket**:

```bash
gsutil mb gs://your-bucket-name
```

1. **Create Pub/Sub Topics and Subscriptions**:

```bash
# Create main processing topic and subscription
gcloud pubsub topics create your-topic-name
gcloud pubsub subscriptions create your-subscription-name --topic your-topic-name

# Create results topic and subscription
gcloud pubsub topics create your-results-topic-name
gcloud pubsub subscriptions create your-results-subscription-name --topic your-results-topic-name
```

3. **Deploy Cloud Function**:

```bash
gcloud functions deploy process_file \
  --runtime python39 \
  --trigger-topic your-topic-name \
  --entry-point process_file \
  --memory 512MB \
  --timeout 540s \
  --set-env-vars "PUBSUB_RESULTS_TOPIC=your-results-topic-name,GOOGLE_API_KEY=your-gemini-api-key"
```

## Usage

After installation, you can use the CLI tool directly:

```bash
# Basic usage
file-prompt --files "path/to/files/*" --prompt "Your prompt here"

# With specific mode and output format
file-prompt --files "*.pdf" --prompt "Summarize this document" --mode "auto" --output-format "json"

# Multiple file patterns
file-prompt --files "*.pdf" "*.docx" --prompt "Extract key points"
```

### Command Line Options

- `--files`: File path or glob pattern (can be specified multiple times)
- `--prompt`: The prompt to process files with
- `--mode`: Processing mode (text/image/auto, default: auto)
- `--output-format`: Output format (json/text/markdown, default: text)

### Processing Flow

1. **File Upload**:
   - Files are uploaded to GCS
   - Unique job IDs are generated
   - Metadata is extracted

2. **Message Publishing**:

   - Pub/Sub messages include:

```json
{
  "file_path": "gs://bucket/abc.pdf",
  "mime_type": "application/pdf",
  "prompt": "Summarize the content",
  "mode": "auto",
  "job_id": "uuid123"
}
```

1. **Cloud Processing**:
   - Cloud Function triggered by Pub/Sub
   - File downloaded from GCS
   - Processed based on type
   - Results stored in GCS

2. **Result Retrieval**:
   - CLI polls for results
   - Results streamed as available
   - Output formatted as specified

## Output Format

The tool returns structured JSON responses with the following format:

```json
{
    "status": "success",
    "job_id": "uuid123",
    "file_path": "gs://bucket/abc.pdf",
    "content": "processed_content",
    "analysis": "AI_analysis_result",
    "gcs_result_path": "gs://bucket/results/uuid123.json"
}
```

Error responses follow this format:
```json
{
    "status": "error",
    "job_id": "uuid123",
    "error": "error_message",
    "file_type": "detected_file_type"
}
```

## Testing

The project includes a comprehensive test suite. To run tests:

```bash
# Unit tests
pytest tests/ -v

# Integration tests (requires GCP setup)
pytest tests/integration/ -v

# Coverage report
pytest tests/ --cov=src
```

## GCP Dependencies

- google-cloud-storage - GCS operations
- google-cloud-pubsub - Pub/Sub messaging
- google-cloud-functions - Cloud Function deployment
- google-generativeai - Gemini API integration
- google-auth - Authentication

## Security

- IAM-based access control
- Service account authentication
- Encrypted data in transit
- Secure credential management

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Cloud Platform services
- Gemini API for LLM capabilities
- All open-source libraries used in this project
