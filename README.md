# Prompt Engineering Workshop App

This Streamlit application is designed for workshop attendees to learn about prompt engineering with Azure OpenAI models.

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd PromptLab
```

2. **Run the setup script**
```bash
python scripts/setup.py
```

3. **Configure your environment**
   - Copy `.env.example` to `.env`
   - Add your Azure OpenAI credentials:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key-here
ADMIN_PASSWORD=your-secure-admin-password
```

4. **Start the application**
```bash
streamlit run app.py
```

## 📁 Project Structure

```
PromptLab/
├── app.py                      # Main routing application
├── requirements.txt            # Python dependencies
├── config/                     # Configuration files
├── src/                       # Source code
│   ├── core/                  # Core functionality
│   ├── models/                # Model definitions
│   ├── services/              # External service integrations
│   ├── ui/                    # UI components
│   └── views/                 # Application views
│       ├── main_view.py       # Main user interface
│       └── admin_view.py      # Admin interface
├── tests/                     # Test files
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
└── logs/                      # Application logs
```

## ✨ Features

- **Interactive Prompt Testing**: Test system and user prompts with various models
- **Model Comparison**: Side-by-side comparison of responses from multiple models
- **Cost Tracking**: Real-time cost calculation and projections
- **URL-Based Admin Access**: Hidden admin interface accessible only via URL parameter
- **Admin Controls**: Manage visible models, pricing visibility, and token limits
- **Modern Architecture**: Clean, maintainable code with proper separation of concerns

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/ -v
```

### Code Structure
- **`src/core/`**: Configuration management and constants
- **`src/models/`**: Model registry and pricing calculations
- **`src/services/`**: Azure AI service integration
- **`src/ui/`**: Reusable UI components

### Adding New Models
1. Add model information to `src/models/models.py`
2. Include pricing information
3. The model will automatically appear in the admin interface

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Refactoring Guide](docs/REFACTORING.md)

## 🔧 Configuration

The application uses a JSON configuration file (`config/model_config.json`) and environment variables for settings. All configuration can be managed through the admin interface.

## 🚀 Deployment

See [Deployment Guide](docs/DEPLOYMENT.md) for production deployment instructions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.