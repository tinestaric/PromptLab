# Prompt Engineering Workshop App

This Streamlit application is designed for workshop attendees to learn about prompt engineering with Azure OpenAI models.

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd PromptLab
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create environment file**
   - Copy `.env.example` to `.env` and add your Azure AI Foundry credentials:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.services.ai.azure.com/models
AZURE_OPENAI_KEY=your-api-key-here
ADMIN_PASSWORD=your-secure-admin-password
```
   - Note: Use Azure AI inference endpoint, not the standard OpenAI endpoint

4. **Configure models**
   - Edit `config/models.json` with your Azure deployment details
   - Example structure:
```json
{
  "models": {
    "YourModelName": {
      "api_name": "your-deployment-name",
      "input_price": 0.002,
      "output_price": 0.006,
      "description": "Your model description"
    }
  }
}
```
   - Required: `api_name` must match your Azure deployment name exactly
   - Optional: `input_price`/`output_price` for cost tracking, `description` for display
   - Get deployment names from Azure OpenAI Studio → Deployments

5. **Run the application**
```bash
streamlit run app.py
```

## 📁 Project Structure

```
PromptLab/
├── app.py                      # Main routing application
├── requirements.txt            # Python dependencies
├── config/                     # Configuration files
│   ├── models.json            # Model definitions and pricing
│   ├── logging.yaml           # Logging configuration
│   └── model_config.json      # Runtime model settings
├── src/                       # Source code
│   ├── core/                  # Core functionality
│   ├── models/                # Model definitions
│   ├── services/              # External service integrations
│   ├── ui/                    # UI components
│   └── views/                 # Application views
│       ├── main_view.py       # Main user interface
│       └── admin_view.py      # Admin interface
```

## ✨ Features

- **Interactive Prompt Testing**: Test prompts with various Azure OpenAI models
- **Model Comparison**: Compare responses from multiple models side-by-side
- **Cost Tracking**: Real-time cost calculation and projections
- **Admin Interface**: Access via `?view=admin` using password from `.env` file
- **Chain View**: Access prompt chaining via `?view=chain`

## 🛠️ Development

### Code Structure
- **`src/core/`**: Configuration management and constants
- **`src/models/`**: Model registry and pricing calculations
- **`src/services/`**: Azure AI service integration
- **`src/ui/`**: Reusable UI components

## 🔧 Configuration

Configure models in `config/models.json` and settings in `.env`. Admin interface available via `?view=admin`.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.