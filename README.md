# PromptPilot API - AI Prompt Generator

A full-stack web application for generating professional AI prompts for various AI models including ChatGPT, Midjourney, DALL-E, and more.

## 🚀 Features

- **Multi-Model Support**: Generate prompts for ChatGPT, Midjourney, DALL-E, Stable Diffusion, Claude
- **Customizable Parameters**: Control tone, complexity, type, and additional options
- **Smart Generation**: Uses DeepSeek AI API for intelligent prompt generation
- **Fallback System**: Template-based fallback when AI service is unavailable
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Example Templates**: Pre-built templates for common use cases
- **Export Options**: Copy to clipboard or save as text file

## 📁 Project Structure

```
promptpilot-api/
├── backend/
│   ├── app.py                 # Flask API server
│   └── requirements.txt       # Python dependencies
└── frontend/
    └── index.html            # Frontend interface
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- Flask
- DeepSeek API account (for AI generation)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:
   ```bash
   export DEEPSEEK_API_KEY="your_deepseek_api_key_here"
   export PORT=5000  # Optional, defaults to 5000
   ```

5. **Run the server**:
   ```bash
   python app.py
   ```

### Frontend Setup

1. **Update API URL**:
   - Open `frontend/index.html`
   - Find the `API_BASE_URL` configuration in the JavaScript section
   - Update with your actual domain for production:
   ```javascript
   const API_BASE_URL = 'https://your-actual-domain.com/api';
   ```

2. **Deploy frontend**:
   - Serve `index.html` from your web server
   - Ensure CORS is properly configured for your domain

## 🌐 Deployment

### Backend Deployment (PythonAnywhere, Heroku, Railway)

1. **Upload backend files** to your hosting service
2. **Set environment variables**:
   - `DEEPSEEK_API_KEY`: Your DeepSeek API key
   - `PORT`: Server port (usually set automatically by hosting provider)

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Deployment (Netlify, Vercel, GitHub Pages)

1. **Upload frontend files** to your static hosting service
2. **Update API endpoint URL** in `index.html`
3. **Configure proper CORS headers** if needed

## 🔧 Configuration

### Environment Variables

- `DEEPSEEK_API_KEY`: Required for AI-powered prompt generation
- `PORT`: Server port (default: 5000)

### CORS Configuration

Update the allowed origins in `app.py`:
```python
CORS(app, origins=[
    "https://yourdomain.com",
    "http://yourdomain.com", 
    "https://www.yourdomain.com"
])
```

## 📚 API Endpoints

### `POST /api/generate-prompt`
Generate an AI prompt based on user parameters.

**Request Body**:
```json
{
  "model": "chatgpt",
  "type": "creative",
  "topic": "Artificial Intelligence",
  "tone": "professional",
  "complexity": 3,
  "include_examples": true,
  "step_by_step": false,
  "include_questions": true,
  "custom_instructions": "Focus on practical applications"
}
```

**Response**:
```json
{
  "success": true,
  "prompt": "Generated prompt text...",
  "source": "ai"
}
```

### `GET /api/health`
Health check endpoint.

## 🎨 Customization

### Adding New AI Models
1. Update the `model` dropdown in `index.html`
2. Add model-specific formatting in the `build_fallback_prompt` method in `app.py`

### Adding Prompt Types
1. Update the `prompt-type` dropdown in `index.html`
2. Add type descriptions in the `build_system_prompt` method in `app.py`

## 🔒 Security Notes

- Keep your DeepSeek API key secure and never commit it to version control
- Use environment variables for all sensitive configuration
- Implement rate limiting in production
- Validate all user inputs on the backend

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Update the allowed origins in the Flask CORS configuration
2. **API Key Issues**: Verify your DeepSeek API key is correctly set as an environment variable
3. **Generation Failures**: The system will automatically fall back to template-based generation

### Logs

Check the application logs for detailed error information:
```bash
# View logs in production
heroku logs --tail  # For Heroku
```

## 📄 License

This project is licensed under the GNU GENERAL PUBLIC LICENSE.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation at [PromptPilot](https://promptpilot.opensystems.co.ke)

---

**Note**: Remember to replace placeholder domains and API keys with your actual production values before deployment.
