# PM Resume Tailoring Agent

An intelligent agent that helps prepare Product Manager resumes tailored to specific job descriptions. This tool analyzes job postings, extracts key requirements, and optimizes your resume to match what employers are looking for.

## 🎯 Features

- **Job Description Analysis**: Automatically extracts keywords, requirements, and company information
- **Intelligent Resume Tailoring**: Reorders experiences and skills based on relevance to the job
- **ATS Optimization**: Ensures your resume passes Applicant Tracking Systems
- **Multiple Export Formats**: Supports Markdown and JSON output
- **Keyword Scoring**: Prioritizes content based on job requirements
- **Experience Relevance Scoring**: Ranks your experiences by how well they match the role
- **Professional Summary Optimization**: Tailors your summary to include relevant keywords

## 🚀 Quick Start

### 1. Set Up Your Profile

Copy the template and fill in your information:

```bash
cp examples/user_profile_template.json my_profile.json
```

Edit `my_profile.json` with your actual information, experiences, and skills.

### 2. Prepare Job Description

Save the job description you're targeting as a text file:

```bash
# Copy the job posting text into a file
echo "Senior Product Manager - SaaS Platform..." > job_description.txt
```

### 3. Generate Tailored Resume

```bash
python pm_resume_agent.py \
    --profile my_profile.json \
    --job-description job_description.txt \
    --output tailored_resume.md
```

## 📁 Project Structure

```
pm-resume-agent/
├── pm_resume_agent.py          # Main application
├── config.py                   # Configuration settings
├── utils.py                    # Utility functions
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── examples/
    ├── user_profile_template.json
    └── sample_job_description.txt
```

## 🔧 Installation

### Basic Installation (No Dependencies)

The agent works with Python's standard library only:

```bash
git clone <repository-url>
cd pm-resume-agent
python pm_resume_agent.py --help
```

### Enhanced Installation (Optional Dependencies)

For additional features like URL parsing and advanced text processing:

```bash
pip install -r requirements.txt
```

## 📖 Usage Guide

### Command Line Interface

```bash
python pm_resume_agent.py [OPTIONS]

Options:
  --profile PATH              Path to user profile JSON (required)
  --job-description PATH      Path to job description text file (required)
  --output PATH              Output file path (default: tailored_resume.md)
  --format {markdown,json}   Output format (default: markdown)
  --focus TEXT [TEXT ...]    Additional focus areas
```

### Example Usage

```bash
# Basic usage
python pm_resume_agent.py \
    --profile examples/user_profile_template.json \
    --job-description examples/sample_job_description.txt

# Specify output format and location
python pm_resume_agent.py \
    --profile my_profile.json \
    --job-description fintech_pm_role.txt \
    --output fintech_resume.md \
    --format markdown

# Add specific focus areas
python pm_resume_agent.py \
    --profile my_profile.json \
    --job-description startup_role.txt \
    --focus "agile methodologies" "data analysis" \
    --output startup_tailored_resume.md
```

## 📝 User Profile Format

Your profile should be a JSON file with the following structure:

```json
{
  "name": "Your Name",
  "email": "your.email@example.com",
  "phone": "+1 (555) 123-4567",
  "linkedin": "https://linkedin.com/in/yourprofile",
  "location": "City, State",
  "summary": "Your professional summary...",
  "experiences": [
    {
      "title": "Product Manager",
      "company": "Company Name",
      "duration": "Jan 2022 - Present",
      "achievements": [
        "Achievement 1 with metrics",
        "Achievement 2 with impact"
      ],
      "skills": ["skill1", "skill2"]
    }
  ],
  "education": [
    {
      "degree": "MBA",
      "institution": "University",
      "year": "2020",
      "details": ["Relevant details"]
    }
  ],
  "skills": ["Product Strategy", "Agile", "Data Analysis"],
  "certifications": ["CSPO", "Google Analytics"],
  "languages": ["English", "Spanish"]
}
```

See `examples/user_profile_template.json` for a complete template.

## ⚙️ Configuration

The agent can be customized through `config.py`:

### Resume Settings
- `max_experiences`: Maximum experiences to include (default: 5)
- `max_skills`: Maximum skills to highlight (default: 15)
- `min_relevance_score`: Minimum score to include experience (default: 0.5)

### Keyword Categories
- **Core Skills**: Product management fundamentals
- **Technical Skills**: Tools and technologies
- **Soft Skills**: Leadership and communication
- **Industries**: Sector-specific terms

### Export Options
- Include relevance scores
- Show optimization notes
- Multiple output formats

## 🎯 How It Works

### 1. Job Description Analysis
- Extracts keywords from predefined PM categories
- Identifies requirements and qualifications
- Analyzes company information and culture

### 2. Experience Scoring
- Matches your experiences against job requirements
- Calculates relevance scores based on keyword frequency
- Applies bonus scoring for PM titles and exact matches

### 3. Resume Optimization
- Reorders experiences by relevance score
- Prioritizes skills mentioned in job description
- Optimizes professional summary with key terms
- Generates tailored content while maintaining authenticity

### 4. Output Generation
- Creates ATS-friendly formatted resume
- Includes optimization notes and analysis
- Supports multiple export formats

## 📊 Sample Output

The agent generates a tailored resume with sections like:

```markdown
# John Smith
**Email:** john.smith@email.com | **Phone:** +1 (555) 123-4567
**LinkedIn:** https://linkedin.com/in/johnsmith | **Location:** San Francisco, CA

## Professional Summary
Experienced Product Manager with 6+ years driving product strategy and execution for SaaS platforms...

## Professional Experience
### Senior Product Manager | TechCorp
*Jan 2022 - Present* | Relevance Score: 8.5
- Led product strategy for enterprise platform, resulting in 40% increase in user engagement
- Managed cross-functional team of 8 engineers, designers, and analysts
...

## Resume Optimization Notes
- Optimized for 23 relevant PM keywords from job description
- Emphasized core_skills based on job requirements
- Reordered experiences by relevance score
- Prioritized skills matching job description
```

## 🔍 Advanced Features

### Custom Keywords
Add industry-specific terms in `config.py`:

```python
CUSTOM_KEYWORDS = {
    'fintech': ['payments', 'compliance', 'kyc'],
    'healthcare': ['hipaa', 'clinical', 'fda']
}
```

### URL Support
Load job descriptions from URLs (requires optional dependencies):

```python
from utils import load_job_description_from_url
jd_text = load_job_description_from_url('https://company.com/jobs/pm-role')
```

### Validation
The agent validates your profile for completeness:

```python
from utils import validate_user_profile
is_valid, errors = validate_user_profile(profile_data)
```

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Structure
- `pm_resume_agent.py`: Main application logic
- `config.py`: Configuration and settings
- `utils.py`: Utility functions and helpers
- `examples/`: Sample files and templates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

**Profile validation errors**: Check that all required fields are filled in your JSON profile.

**Low relevance scores**: Ensure your experiences include relevant keywords and skills.

**Import errors**: Install optional dependencies if using advanced features.

### Getting Help

1. Check the examples in the `examples/` directory
2. Review configuration options in `config.py`
3. Open an issue on GitHub for bugs or feature requests

## 🔮 Roadmap

- [ ] PDF export support
- [ ] Web interface
- [ ] Integration with job boards
- [ ] AI-powered content suggestions
- [ ] Multiple resume templates
- [ ] Cover letter generation
- [ ] Interview preparation insights

---

**Made for Product Managers, by Product Managers** 🚀

Transform your resume from generic to targeted in minutes, not hours.