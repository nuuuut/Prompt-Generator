from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import logging

app = Flask(__name__)

# Configure CORS for your domain
CORS(app, origins=[
    "https://yourdomain.com",  # Your main domain
    "http://yourdomain.com",   # HTTP version
    "https://www.yourdomain.com" # WWW version
])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptGenerator:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/chat/completions"
    
    def build_system_prompt(self, model, prompt_type, tone, complexity):
        """Build system prompt based on user preferences"""
        complexity_levels = {
            1: "very simple and basic",
            2: "simple and straightforward", 
            3: "medium complexity with good detail",
            4: "complex and detailed",
            5: "very complex and highly detailed"
        }
        
        tone_descriptions = {
            "professional": "professional and formal",
            "casual": "casual and friendly", 
            "academic": "academic and scholarly",
            "persuasive": "persuasive and convincing",
            "humorous": "humorous and witty",
            "inspiring": "inspiring and motivational"
        }
        
        prompt_type_descriptions = {
            "creative": "creative writing",
            "technical": "technical explanation",
            "business": "business and marketing",
            "educational": "educational content", 
            "conversational": "conversational dialogue",
            "analytical": "data analysis"
        }
        
        system_prompt = f"""You are a professional AI prompt engineer. Create optimized, ready-to-use prompts based on these specifications:

- Model: {model.upper()}
- Type: {prompt_type_descriptions.get(prompt_type, prompt_type)}
- Tone: {tone_descriptions.get(tone, tone)}
- Complexity: {complexity_levels.get(complexity, 'medium')}

Create a prompt that is clear, specific, and will yield high-quality results from the target AI model."""
        
        return system_prompt
    
    def build_user_prompt(self, data):
        """Build the user prompt from form data"""
        components = []
        
        # Basic information
        components.append(f"Topic: {data['topic']}")
        
        # Additional options
        if data.get('include_examples'):
            components.append("Include relevant examples")
        
        if data.get('step_by_step'):
            components.append("Use step-by-step format")
            
        if data.get('include_questions'):
            components.append("Include follow-up questions")
        
        # Custom instructions
        if data.get('custom_instructions'):
            components.append(f"Additional requirements: {data['custom_instructions']}")
        
        user_prompt = f"Create an AI prompt with these specifications:\n" + "\n".join(f"- {component}" for component in components)
        user_prompt += "\n\nProvide only the final optimized prompt, ready to be used with the specified AI model."
        
        return user_prompt
    
    def generate_with_ai(self, data):
        """Generate prompt using DeepSeek API"""
        if not self.api_key:
            raise Exception("DeepSeek API key not configured")
        
        system_prompt = self.build_system_prompt(
            data['model'], 
            data['type'], 
            data['tone'], 
            data['complexity']
        )
        
        user_prompt = self.build_user_prompt(data)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.7,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise Exception(f"AI API error: {str(e)}")
    
    def generate_fallback_prompt(self, data):
        """Generate a fallback prompt if AI API fails"""
        model = data['model']
        prompt_type = data['type']
        topic = data['topic']
        tone = data['tone']
        complexity = data['complexity']
        include_examples = data.get('include_examples', False)
        step_by_step = data.get('step_by_step', False)
        include_questions = data.get('include_questions', False)
        custom_instructions = data.get('custom_instructions', '')
        
        complexity_labels = {
            1: 'Very Simple',
            2: 'Simple', 
            3: 'Medium',
            4: 'Complex',
            5: 'Very Complex'
        }
        
        prompt = f"Create a {prompt_type} prompt about: \"{topic}\"\n\n"
        prompt += f"Tone: {tone}\n"
        prompt += f"Complexity: {complexity_labels.get(complexity, 'Medium')}\n\n"
        
        # Add specific instructions based on type
        type_instructions = {
            'creative': 'Please create engaging and imaginative content.',
            'technical': 'Focus on accuracy, clarity, and depth of explanation.',
            'business': 'Emphasize practical applications and ROI considerations.',
            'educational': 'Structure content for optimal learning and retention.',
            'conversational': 'Make it feel like a natural, engaging conversation.',
            'analytical': 'Focus on data interpretation and actionable insights.'
        }
        
        prompt += type_instructions.get(prompt_type, '') + "\n"
        
        # Add optional components
        if include_examples:
            prompt += "Include relevant examples to illustrate key points.\n"
        
        if step_by_step:
            prompt += "Present information in a clear, step-by-step format.\n"
        
        if include_questions:
            prompt += "Incorporate thought-provoking questions for engagement.\n"
        
        # Add custom instructions if provided
        if custom_instructions:
            prompt += f"\nAdditional Requirements: {custom_instructions}\n"
        
        # Model-specific formatting
        if model == 'midjourney':
            prompt += "\nFormat the response as a ready-to-use Midjourney prompt with appropriate parameters."
        elif model == 'dalle':
            prompt += "\nFormat as a detailed DALL-E prompt with specific visual descriptions."
        else:
            prompt += "\nProvide a comprehensive, well-structured prompt that will yield high-quality results."
        
        return prompt

# Initialize the prompt generator
prompt_generator = PromptGenerator()

@app.route('/api/generate-prompt', methods=['POST'])
def generate_prompt():
    """API endpoint to generate AI prompts"""
    try:
        data = request.json
        
        # Validate required fields
        if not data or not data.get('topic'):
            return jsonify({'error': 'Topic is required'}), 400
        
        # Generate prompt using AI
        try:
            ai_prompt = prompt_generator.generate_with_ai(data)
            return jsonify({
                'success': True,
                'prompt': ai_prompt,
                'source': 'ai'
            })
            
        except Exception as ai_error:
            logger.warning(f"AI generation failed, using fallback: {ai_error}")
            # Use fallback method
            fallback_prompt = prompt_generator.generate_fallback_prompt(data)
            return jsonify({
                'success': True,
                'prompt': fallback_prompt,
                'source': 'fallback',
                'warning': 'AI service unavailable, using template-based generation'
            })
            
    except Exception as e:
        logger.error(f"Error generating prompt: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'AI Prompt Generator API'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False for production