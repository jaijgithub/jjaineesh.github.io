#!/usr/bin/env python3
"""
PM Resume Tailoring Agent

An intelligent agent that helps prepare Product Manager resumes tailored to specific job descriptions.
Features:
- Job description analysis and keyword extraction
- Resume section optimization
- Skills matching and highlighting
- Experience relevance scoring
- ATS-friendly formatting
"""

import re
import json
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import Counter
import argparse


@dataclass
class Experience:
    """Represents a work experience entry."""
    title: str
    company: str
    duration: str
    achievements: List[str]
    skills: List[str]
    relevance_score: float = 0.0


@dataclass
class Education:
    """Represents an education entry."""
    degree: str
    institution: str
    year: str
    details: List[str] = None


@dataclass
class UserProfile:
    """User's complete profile information."""
    name: str
    email: str
    phone: str
    linkedin: str
    location: str
    summary: str
    experiences: List[Experience]
    education: List[Education]
    skills: List[str]
    certifications: List[str]
    languages: List[str]


class JobDescriptionAnalyzer:
    """Analyzes job descriptions to extract key requirements and keywords."""
    
    PM_KEYWORDS = {
        'core_skills': [
            'product management', 'product strategy', 'roadmap', 'user stories',
            'agile', 'scrum', 'kanban', 'sprint planning', 'backlog management',
            'stakeholder management', 'cross-functional', 'data analysis',
            'market research', 'competitive analysis', 'user research', 'ux/ui',
            'metrics', 'kpis', 'analytics', 'a/b testing', 'experimentation'
        ],
        'technical_skills': [
            'sql', 'python', 'jira', 'confluence', 'figma', 'sketch',
            'google analytics', 'mixpanel', 'amplitude', 'tableau',
            'api', 'sdk', 'aws', 'azure', 'gcp', 'docker', 'kubernetes'
        ],
        'soft_skills': [
            'leadership', 'communication', 'collaboration', 'problem solving',
            'critical thinking', 'decision making', 'negotiation',
            'presentation', 'mentoring', 'coaching', 'influence'
        ],
        'industries': [
            'saas', 'fintech', 'healthcare', 'e-commerce', 'mobile',
            'enterprise', 'b2b', 'b2c', 'marketplace', 'platform'
        ]
    }
    
    def __init__(self):
        self.all_keywords = []
        for category in self.PM_KEYWORDS.values():
            self.all_keywords.extend(category)
    
    def analyze(self, job_description: str) -> Dict:
        """Analyze job description and extract key information."""
        jd_lower = job_description.lower()
        
        # Extract keywords and their frequency
        found_keywords = {}
        for category, keywords in self.PM_KEYWORDS.items():
            found_keywords[category] = []
            for keyword in keywords:
                if keyword in jd_lower:
                    count = jd_lower.count(keyword)
                    found_keywords[category].append({'keyword': keyword, 'count': count})
        
        # Extract requirements sections
        requirements = self._extract_requirements(job_description)
        
        # Extract company info
        company_info = self._extract_company_info(job_description)
        
        # Calculate keyword importance scores
        keyword_scores = self._calculate_keyword_scores(found_keywords)
        
        return {
            'keywords': found_keywords,
            'keyword_scores': keyword_scores,
            'requirements': requirements,
            'company_info': company_info,
            'analysis_summary': self._generate_analysis_summary(found_keywords, requirements)
        }
    
    def _extract_requirements(self, jd: str) -> List[str]:
        """Extract requirements from job description."""
        requirements = []
        
        # Common requirement section headers
        req_patterns = [
            r'requirements?:?\s*(.*?)(?=\n\s*[A-Z][^:]*:|\n\s*$)',
            r'qualifications?:?\s*(.*?)(?=\n\s*[A-Z][^:]*:|\n\s*$)',
            r'what you.{0,20}need:?\s*(.*?)(?=\n\s*[A-Z][^:]*:|\n\s*$)',
            r'you should have:?\s*(.*?)(?=\n\s*[A-Z][^:]*:|\n\s*$)'
        ]
        
        for pattern in req_patterns:
            matches = re.finditer(pattern, jd, re.IGNORECASE | re.DOTALL)
            for match in matches:
                section = match.group(1).strip()
                # Split by bullet points or line breaks
                items = re.split(r'[•\-\*]\s*|^\s*\d+\.?\s*', section, flags=re.MULTILINE)
                requirements.extend([item.strip() for item in items if item.strip()])
        
        return requirements[:10]  # Limit to top 10 requirements
    
    def _extract_company_info(self, jd: str) -> Dict:
        """Extract company information from job description."""
        # This is a simplified version - in practice, you might use NER or other techniques
        company_info = {
            'industry': '',
            'size': '',
            'stage': '',
            'culture': []
        }
        
        jd_lower = jd.lower()
        
        # Industry detection
        for industry in self.PM_KEYWORDS['industries']:
            if industry in jd_lower:
                company_info['industry'] = industry
                break
        
        # Company stage/size indicators
        if any(term in jd_lower for term in ['startup', 'early stage', 'seed']):
            company_info['stage'] = 'startup'
        elif any(term in jd_lower for term in ['enterprise', 'fortune', 'large']):
            company_info['stage'] = 'enterprise'
        
        return company_info
    
    def _calculate_keyword_scores(self, found_keywords: Dict) -> Dict[str, float]:
        """Calculate importance scores for keywords based on frequency and category."""
        scores = {}
        category_weights = {
            'core_skills': 1.0,
            'technical_skills': 0.8,
            'soft_skills': 0.6,
            'industries': 0.7
        }
        
        for category, keywords in found_keywords.items():
            weight = category_weights.get(category, 0.5)
            for kw_data in keywords:
                keyword = kw_data['keyword']
                count = kw_data['count']
                scores[keyword] = count * weight
        
        return scores
    
    def _generate_analysis_summary(self, found_keywords: Dict, requirements: List[str]) -> str:
        """Generate a summary of the job description analysis."""
        total_keywords = sum(len(kws) for kws in found_keywords.values())
        top_categories = sorted(found_keywords.items(), 
                              key=lambda x: len(x[1]), reverse=True)[:3]
        
        summary = f"Found {total_keywords} relevant PM keywords. "
        summary += f"Top focus areas: {', '.join([cat for cat, _ in top_categories])}. "
        summary += f"Identified {len(requirements)} key requirements."
        
        return summary


class ResumeTailor:
    """Tailors resumes based on job description analysis."""
    
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.analyzer = JobDescriptionAnalyzer()
    
    def tailor_resume(self, job_description: str, 
                     focus_areas: List[str] = None) -> Dict:
        """Generate a tailored resume based on job description."""
        
        # Analyze job description
        jd_analysis = self.analyzer.analyze(job_description)
        
        # Score and rank experiences
        scored_experiences = self._score_experiences(jd_analysis)
        
        # Optimize summary
        tailored_summary = self._optimize_summary(jd_analysis, focus_areas)
        
        # Select and order skills
        prioritized_skills = self._prioritize_skills(jd_analysis)
        
        # Generate tailored resume
        tailored_resume = {
            'personal_info': {
                'name': self.user_profile.name,
                'email': self.user_profile.email,
                'phone': self.user_profile.phone,
                'linkedin': self.user_profile.linkedin,
                'location': self.user_profile.location
            },
            'summary': tailored_summary,
            'experiences': scored_experiences[:5],  # Top 5 most relevant
            'skills': prioritized_skills[:15],  # Top 15 skills
            'education': self.user_profile.education,
            'certifications': self.user_profile.certifications,
            'job_analysis': jd_analysis,
            'optimization_notes': self._generate_optimization_notes(jd_analysis)
        }
        
        return tailored_resume
    
    def _score_experiences(self, jd_analysis: Dict) -> List[Experience]:
        """Score experiences based on relevance to job description."""
        keyword_scores = jd_analysis['keyword_scores']
        scored_experiences = []
        
        for exp in self.user_profile.experiences:
            score = 0.0
            exp_text = f"{exp.title} {exp.company} {' '.join(exp.achievements)} {' '.join(exp.skills)}".lower()
            
            # Score based on keyword matches
            for keyword, kw_score in keyword_scores.items():
                if keyword in exp_text:
                    score += kw_score
            
            # Bonus for PM titles
            if any(title in exp.title.lower() for title in ['product manager', 'product owner', 'pm']):
                score += 5.0
            
            exp.relevance_score = score
            scored_experiences.append(exp)
        
        return sorted(scored_experiences, key=lambda x: x.relevance_score, reverse=True)
    
    def _optimize_summary(self, jd_analysis: Dict, focus_areas: List[str] = None) -> str:
        """Create an optimized summary targeting the job requirements."""
        keyword_scores = jd_analysis['keyword_scores']
        top_keywords = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)[:8]
        
        # Extract key themes
        themes = []
        if any('agile' in kw[0] or 'scrum' in kw[0] for kw in top_keywords):
            themes.append('agile methodologies')
        if any('data' in kw[0] or 'analytics' in kw[0] for kw in top_keywords):
            themes.append('data-driven decision making')
        if any('stakeholder' in kw[0] or 'cross-functional' in kw[0] for kw in top_keywords):
            themes.append('stakeholder management')
        
        # Build optimized summary
        base_summary = self.user_profile.summary
        
        # Add keyword-rich enhancements
        keyword_phrase = ", ".join([kw[0] for kw in top_keywords[:5]])
        
        optimized = f"{base_summary} Specialized in {keyword_phrase}"
        if themes:
            optimized += f" with proven expertise in {', '.join(themes)}"
        optimized += "."
        
        return optimized
    
    def _prioritize_skills(self, jd_analysis: Dict) -> List[str]:
        """Prioritize skills based on job description requirements."""
        keyword_scores = jd_analysis['keyword_scores']
        user_skills_lower = [skill.lower() for skill in self.user_profile.skills]
        
        # Score user skills based on job requirements
        skill_scores = []
        for skill in self.user_profile.skills:
            score = keyword_scores.get(skill.lower(), 0)
            # Bonus for exact matches
            if skill.lower() in keyword_scores:
                score += 2.0
            skill_scores.append((skill, score))
        
        # Sort by score and return
        prioritized = sorted(skill_scores, key=lambda x: x[1], reverse=True)
        return [skill for skill, _ in prioritized]
    
    def _generate_optimization_notes(self, jd_analysis: Dict) -> List[str]:
        """Generate notes about how the resume was optimized."""
        notes = []
        
        total_keywords = sum(len(kws) for kws in jd_analysis['keywords'].values())
        notes.append(f"Optimized for {total_keywords} relevant PM keywords from job description")
        
        top_category = max(jd_analysis['keywords'].items(), 
                          key=lambda x: len(x[1]))[0]
        notes.append(f"Emphasized {top_category.replace('_', ' ')} based on job requirements")
        
        notes.append("Reordered experiences by relevance score")
        notes.append("Prioritized skills matching job description")
        
        return notes


class ResumeExporter:
    """Exports tailored resumes in various formats."""
    
    @staticmethod
    def to_markdown(resume_data: Dict) -> str:
        """Export resume as markdown."""
        md = []
        
        # Header
        personal = resume_data['personal_info']
        md.append(f"# {personal['name']}")
        md.append(f"**Email:** {personal['email']} | **Phone:** {personal['phone']}")
        md.append(f"**LinkedIn:** {personal['linkedin']} | **Location:** {personal['location']}")
        md.append("")
        
        # Summary
        md.append("## Professional Summary")
        md.append(resume_data['summary'])
        md.append("")
        
        # Experience
        md.append("## Professional Experience")
        for exp in resume_data['experiences']:
            md.append(f"### {exp.title} | {exp.company}")
            md.append(f"*{exp.duration}* | Relevance Score: {exp.relevance_score:.1f}")
            for achievement in exp.achievements:
                md.append(f"- {achievement}")
            md.append("")
        
        # Skills
        md.append("## Core Skills")
        skills_text = " • ".join(resume_data['skills'])
        md.append(skills_text)
        md.append("")
        
        # Education
        md.append("## Education")
        for edu in resume_data['education']:
            md.append(f"**{edu.degree}** | {edu.institution} | {edu.year}")
            if edu.details:
                for detail in edu.details:
                    md.append(f"- {detail}")
        md.append("")
        
        # Optimization notes
        md.append("## Resume Optimization Notes")
        for note in resume_data['optimization_notes']:
            md.append(f"- {note}")
        
        return "\n".join(md)
    
    @staticmethod
    def to_json(resume_data: Dict, filename: str = None) -> str:
        """Export resume as JSON."""
        json_str = json.dumps(resume_data, indent=2, default=str)
        
        if filename:
            with open(filename, 'w') as f:
                f.write(json_str)
        
        return json_str


def load_user_profile(profile_path: str) -> UserProfile:
    """Load user profile from JSON file."""
    with open(profile_path, 'r') as f:
        data = json.load(f)
    
    # Convert experiences
    experiences = []
    for exp_data in data.get('experiences', []):
        experiences.append(Experience(**exp_data))
    
    # Convert education
    education = []
    for edu_data in data.get('education', []):
        education.append(Education(**edu_data))
    
    # Create profile
    profile_data = data.copy()
    profile_data['experiences'] = experiences
    profile_data['education'] = education
    
    return UserProfile(**profile_data)


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="PM Resume Tailoring Agent")
    parser.add_argument('--profile', required=True, help='Path to user profile JSON')
    parser.add_argument('--job-description', required=True, help='Path to job description text file')
    parser.add_argument('--output', default='tailored_resume.md', help='Output file path')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Output format')
    parser.add_argument('--focus', nargs='*', help='Additional focus areas')
    
    args = parser.parse_args()
    
    # Load user profile
    try:
        user_profile = load_user_profile(args.profile)
        print(f"✓ Loaded user profile for {user_profile.name}")
    except Exception as e:
        print(f"✗ Error loading profile: {e}")
        return
    
    # Load job description
    try:
        with open(args.job_description, 'r') as f:
            job_description = f.read()
        print(f"✓ Loaded job description ({len(job_description)} characters)")
    except Exception as e:
        print(f"✗ Error loading job description: {e}")
        return
    
    # Create tailor and generate resume
    tailor = ResumeTailor(user_profile)
    print("🔄 Analyzing job description and tailoring resume...")
    
    tailored_resume = tailor.tailor_resume(job_description, args.focus)
    
    # Export resume
    if args.format == 'markdown':
        output = ResumeExporter.to_markdown(tailored_resume)
    else:
        output = ResumeExporter.to_json(tailored_resume)
    
    with open(args.output, 'w') as f:
        f.write(output)
    
    print(f"✓ Tailored resume saved to {args.output}")
    
    # Print summary
    analysis = tailored_resume['job_analysis']
    print(f"\n📊 Analysis Summary:")
    print(f"   {analysis['analysis_summary']}")
    print(f"\n🎯 Optimization Notes:")
    for note in tailored_resume['optimization_notes']:
        print(f"   • {note}")


if __name__ == "__main__":
    main()