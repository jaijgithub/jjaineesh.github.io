#!/usr/bin/env python3
"""
Utility functions for PM Resume Agent
"""

import re
import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import config


def validate_user_profile(profile_data: Dict) -> Tuple[bool, List[str]]:
    """Validate user profile data and return validation results."""
    errors = []
    
    # Check required fields
    for field in config.VALIDATION_RULES['required_profile_fields']:
        if field not in profile_data or not profile_data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate experiences
    experiences = profile_data.get('experiences', [])
    if len(experiences) < config.VALIDATION_RULES['min_experiences']:
        errors.append(f"At least {config.VALIDATION_RULES['min_experiences']} experiences required")
    
    # Validate skills
    skills = profile_data.get('skills', [])
    if len(skills) < config.VALIDATION_RULES['min_skills']:
        errors.append(f"At least {config.VALIDATION_RULES['min_skills']} skills required")
    
    # Validate summary length
    summary = profile_data.get('summary', '')
    word_count = len(summary.split())
    if word_count > config.VALIDATION_RULES['max_summary_words']:
        errors.append(f"Summary too long: {word_count} words (max: {config.VALIDATION_RULES['max_summary_words']})")
    
    # Validate experience achievements
    for i, exp in enumerate(experiences):
        achievements = exp.get('achievements', [])
        for j, achievement in enumerate(achievements):
            word_count = len(achievement.split())
            if word_count > config.VALIDATION_RULES['max_achievement_words']:
                errors.append(f"Experience {i+1}, achievement {j+1} too long: {word_count} words")
    
    return len(errors) == 0, errors


def clean_text(text: str) -> str:
    """Clean and normalize text for processing."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters that might interfere with parsing
    text = re.sub(r'[^\w\s\-\.\,\(\)\[\]\/\&\+\%\$\#\@\!\?]', '', text)
    
    return text


def extract_years_of_experience(text: str) -> Optional[int]:
    """Extract years of experience from text."""
    patterns = [
        r'(\d+)\+?\s*years?\s*of\s*experience',
        r'(\d+)\+?\s*years?\s*experience',
        r'(\d+)\+?\s*yrs?\s*experience',
        r'experience.*?(\d+)\+?\s*years?',
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return int(match.group(1))
    
    return None


def extract_salary_range(text: str) -> Optional[Tuple[int, int]]:
    """Extract salary range from job description."""
    patterns = [
        r'\$(\d{1,3}(?:,\d{3})*)\s*-\s*\$(\d{1,3}(?:,\d{3})*)',
        r'(\d{1,3}(?:,\d{3})*)\s*-\s*(\d{1,3}(?:,\d{3})*)\s*k',
        r'\$(\d{1,3})k\s*-\s*\$(\d{1,3})k',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            min_sal = int(match.group(1).replace(',', ''))
            max_sal = int(match.group(2).replace(',', ''))
            
            # Convert k notation to full numbers
            if 'k' in pattern:
                min_sal *= 1000
                max_sal *= 1000
            
            return (min_sal, max_sal)
    
    return None


def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using simple word overlap."""
    if not text1 or not text2:
        return 0.0
    
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    if not union:
        return 0.0
    
    return len(intersection) / len(union)


def format_duration(start_date: str, end_date: str = None) -> str:
    """Format duration string for experience entries."""
    if not end_date or end_date.lower() == 'present':
        return f"{start_date} - Present"
    return f"{start_date} - {end_date}"


def generate_filename(base_name: str, job_title: str = None, company: str = None) -> str:
    """Generate a descriptive filename for the tailored resume."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    filename_parts = [base_name]
    
    if job_title:
        # Clean job title for filename
        clean_title = re.sub(r'[^\w\s\-]', '', job_title)
        clean_title = re.sub(r'\s+', '_', clean_title.strip())
        filename_parts.append(clean_title)
    
    if company:
        # Clean company name for filename
        clean_company = re.sub(r'[^\w\s\-]', '', company)
        clean_company = re.sub(r'\s+', '_', clean_company.strip())
        filename_parts.append(clean_company)
    
    filename_parts.append(timestamp)
    
    return '_'.join(filename_parts).lower()


def extract_contact_info(text: str) -> Dict[str, str]:
    """Extract contact information from text."""
    contact_info = {}
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact_info['email'] = email_match.group()
    
    # Phone pattern (US format)
    phone_patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\+1[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    ]
    for pattern in phone_patterns:
        phone_match = re.search(pattern, text)
        if phone_match:
            contact_info['phone'] = phone_match.group()
            break
    
    # LinkedIn pattern
    linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
    linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
    if linkedin_match:
        contact_info['linkedin'] = f"https://{linkedin_match.group()}"
    
    return contact_info


def merge_keyword_categories(base_keywords: Dict, custom_keywords: Dict) -> Dict:
    """Merge base keywords with custom keyword categories."""
    merged = base_keywords.copy()
    
    for category, keywords in custom_keywords.items():
        if category in merged:
            # Extend existing category
            merged[category].extend(keywords)
        else:
            # Add new category
            merged[category] = keywords
    
    # Remove duplicates
    for category in merged:
        merged[category] = list(set(merged[category]))
    
    return merged


def export_analysis_report(analysis_data: Dict, output_path: str) -> None:
    """Export detailed analysis report to JSON file."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'analysis': analysis_data,
        'config_used': {
            'resume_config': config.RESUME_CONFIG,
            'keyword_config': config.KEYWORD_CONFIG,
            'export_config': config.EXPORT_CONFIG
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)


def load_job_description_from_url(url: str) -> str:
    """Load job description from URL (requires requests and beautifulsoup4)."""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text()
        text = clean_text(text)
        
        return text
        
    except ImportError:
        raise ImportError("requests and beautifulsoup4 are required for URL loading")
    except Exception as e:
        raise Exception(f"Failed to load job description from URL: {e}")


def create_backup_profile(profile_path: str) -> str:
    """Create a backup of the user profile."""
    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"Profile file not found: {profile_path}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{profile_path}.backup_{timestamp}"
    
    with open(profile_path, 'r') as src, open(backup_path, 'w') as dst:
        dst.write(src.read())
    
    return backup_path


def get_file_stats(file_path: str) -> Dict:
    """Get file statistics."""
    if not os.path.exists(file_path):
        return {}
    
    stat = os.stat(file_path)
    return {
        'size_bytes': stat.st_size,
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'size_human': format_file_size(stat.st_size)
    }


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"