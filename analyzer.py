import pdfplumber
import json
import re
from typing import Dict, List, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class ResumeAnalyzer:
    def __init__(self):
        # Initialize Google Gemini
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        try:
            genai.configure(api_key=api_key)
            
            # List available models and pick the first text generation model
            models = genai.list_models()
            text_models = [m for m in models if 'generateContent' in m.supported_generation_methods]
            
            if not text_models:
                raise ValueError("No text generation models available")
            
            # Use the first available model
            model_name = text_models[0].name
            print(f"Using model: {model_name}")
            self.model = genai.GenerativeModel(model_name)
            
        except Exception as e:
            print(f"Error initializing Gemini client: {e}")
            raise
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # Clean up the text
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            if not text:
                raise ValueError("No text could be extracted from the PDF")
            
            return text
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def analyze_resume(self, resume_text: str, job_role: str = "General") -> Dict[str, Any]:
        """Analyze resume using Google Gemini API"""
        
        # Truncate text if too long
        if len(resume_text) > 12000:
            resume_text = resume_text[:12000] + "..."
        
        prompt = f"""You are an expert resume analyzer. Analyze the following resume for a {job_role} position.

Resume Text:
{resume_text}

Provide your analysis in the following JSON format ONLY (no other text, no markdown):
{{
    "score": <integer 0-100>,
    "skills_found": [<list of skills found in resume>],
    "missing_skills": [<list of important skills missing for {job_role}>],
    "suggestions": [<list of 3-5 actionable suggestions to improve the resume>],
    "strengths": [<list of 2-3 key strengths>],
    "summary": "<brief 1-2 sentence summary of resume quality>"
}}

Requirements:
- Score should be based on format, content relevance, completeness, and skills match
- Skills should be specific technical and soft skills
- Suggestions should be practical and specific
- Be honest but constructive in feedback
- Return ONLY valid JSON, no explanation text"""

        try:
            # Gemini API call
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found in response")
            
            # Validate required fields
            required_fields = ['score', 'skills_found', 'missing_skills', 'suggestions']
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = [] if field != 'score' else 0
            
            return analysis
            
        except json.JSONDecodeError as e:
            return {
                "score": 50,
                "skills_found": [],
                "missing_skills": [],
                "suggestions": ["Could not parse AI response. Please try again."],
                "strengths": [],
                "summary": "Analysis encountered an error",
                "error": str(e)
            }
        except Exception as e:
            return {
                "score": 0,
                "skills_found": [],
                "missing_skills": [],
                "suggestions": [f"Error during analysis: {str(e)}"],
                "strengths": [],
                "summary": "Analysis failed"
            }
    
    def get_role_specific_analysis(self, resume_text: str, job_role: str) -> Dict[str, Any]:
        """Get role-specific resume analysis"""
        return self.analyze_resume(resume_text, job_role)