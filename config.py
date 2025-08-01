#!/usr/bin/env python3
"""
Configuration settings for PM Resume Agent
"""

# Resume optimization settings
RESUME_CONFIG = {
    'max_experiences': 5,           # Maximum number of experiences to include
    'max_skills': 15,               # Maximum number of skills to highlight
    'max_achievements_per_role': 6,  # Maximum bullet points per experience
    'min_relevance_score': 0.5,     # Minimum relevance score to include experience
}

# Keyword analysis settings
KEYWORD_CONFIG = {
    'category_weights': {
        'core_skills': 1.0,
        'technical_skills': 0.8,
        'soft_skills': 0.6,
        'industries': 0.7
    },
    'pm_title_bonus': 5.0,          # Bonus score for PM titles
    'keyword_match_bonus': 2.0,     # Bonus for exact keyword matches
}

# Export settings
EXPORT_CONFIG = {
    'include_relevance_scores': True,    # Show relevance scores in output
    'include_optimization_notes': True,  # Include optimization notes
    'include_job_analysis': False,       # Include full job analysis in output
    'markdown_style': 'github',         # Markdown style (github, basic)
}

# Custom keyword categories (extend the base categories)
CUSTOM_KEYWORDS = {
    'pm_frameworks': [
        'design thinking', 'lean startup', 'jobs to be done', 'okrs',
        'product-market fit', 'mvp', 'minimum viable product',
        'customer development', 'product discovery', 'dual track agile'
    ],
    'metrics_analytics': [
        'north star metric', 'pirate metrics', 'cohort analysis',
        'funnel analysis', 'retention analysis', 'churn analysis',
        'ltv', 'customer lifetime value', 'cac', 'customer acquisition cost'
    ],
    'tools_platforms': [
        'productboard', 'aha', 'roadmunk', 'pendo', 'fullstory',
        'hotjar', 'optimizely', 'launchdarkly', 'segment', 'heap'
    ]
}

# Industry-specific keyword mappings
INDUSTRY_KEYWORDS = {
    'fintech': [
        'payments', 'banking', 'lending', 'compliance', 'kyc', 'aml',
        'pci dss', 'fraud detection', 'risk management', 'regulatory'
    ],
    'healthcare': [
        'hipaa', 'ehr', 'emr', 'clinical', 'patient', 'medical device',
        'fda', 'clinical trials', 'telemedicine', 'health records'
    ],
    'e-commerce': [
        'conversion rate', 'cart abandonment', 'checkout', 'inventory',
        'fulfillment', 'marketplace', 'seller tools', 'payment gateway'
    ],
    'enterprise': [
        'enterprise sales', 'b2b', 'saas', 'api', 'integration',
        'scalability', 'security', 'compliance', 'enterprise architecture'
    ]
}

# Resume formatting templates
FORMATTING_TEMPLATES = {
    'professional': {
        'font_family': 'Arial, sans-serif',
        'font_size': '11pt',
        'line_spacing': '1.15',
        'margins': '0.75in',
        'section_spacing': '12pt'
    },
    'modern': {
        'font_family': 'Calibri, sans-serif',
        'font_size': '10.5pt',
        'line_spacing': '1.1',
        'margins': '0.5in',
        'section_spacing': '10pt'
    },
    'compact': {
        'font_family': 'Times New Roman, serif',
        'font_size': '10pt',
        'line_spacing': '1.0',
        'margins': '0.5in',
        'section_spacing': '8pt'
    }
}

# ATS optimization settings
ATS_CONFIG = {
    'avoid_tables': True,           # Avoid table formatting for ATS compatibility
    'avoid_images': True,           # Avoid images and graphics
    'use_standard_headings': True,  # Use standard section headings
    'simple_formatting': True,     # Use simple text formatting
    'include_keywords': True,      # Optimize for keyword scanning
}

# Validation rules
VALIDATION_RULES = {
    'required_profile_fields': [
        'name', 'email', 'phone', 'summary', 'experiences', 'skills'
    ],
    'min_experiences': 2,
    'min_skills': 5,
    'max_summary_words': 100,
    'max_achievement_words': 25
}