# Resume Formatter

A Python desktop application for automatically formatting resumes with customizable sections and fonts.

## Features

- **Smart Text Parsing**: Automatically detects and organizes resume sections
- **Live Preview**: See your formatted resume in real-time as you type
- **Customizable Sections**: Enable/disable sections like Contact, Summary, Experience, Education, Skills, Projects, Certifications, and Awards
- **Font Control**: Choose from multiple font families and adjust font sizes
- **Multiple Export Options**: Generate HTML files that can be easily printed or saved as PDF
- **Settings Persistence**: Your preferences are automatically saved and restored
- **Clean, Professional Output**: Modern, ATS-friendly resume formatting

## Quick Start

1. **Run the application**:
   ```bash
   python resume_formatter.py
   ```

2. **Paste your resume content** in the left text area

3. **Customize your preferences**:
   - Choose font family and size
   - Select which sections to include
   - See live preview on the right

4. **Generate your resume**:
   - Click "Generate Resume" to open in browser
   - Click "Export HTML" to save as a file
   - Print or save as PDF from your browser

## Input Format

The application is flexible with input formats. You can paste text in various ways:

### Method 1: Section Headers
```
John Doe
Software Engineer
john.doe@email.com | (555) 123-4567

SUMMARY
Experienced software engineer with 5+ years...

EXPERIENCE
Senior Software Engineer | Tech Company | 2020-2023
• Led development of customer-facing applications
• Improved system performance by 40%

EDUCATION
Bachelor of Science in Computer Science | University | 2018

SKILLS
Programming Languages: Python, JavaScript, Java
Frameworks: React, Node.js, Django
```

### Method 2: Natural Text
```
John Doe
john.doe@email.com
(555) 123-4567

I am an experienced software engineer...

I worked as a Senior Software Engineer at Tech Company from 2020 to 2023.
During this time I led development of customer-facing applications.
I also improved system performance by 40%.

I have a Bachelor of Science in Computer Science from University in 2018.

My skills include Python, JavaScript, Java, React, Node.js, and Django.
```

The application will automatically detect sections and format them appropriately.

## Customization Options

### Sections
- **Contact**: Name, email, phone, LinkedIn, etc.
- **Summary**: Professional summary or objective
- **Experience**: Work history with job titles, companies, dates, and achievements
- **Education**: Degrees, schools, graduation dates, GPA, coursework
- **Skills**: Technical skills, programming languages, tools
- **Projects**: Personal or professional projects
- **Certifications**: Professional certifications and licenses
- **Awards**: Recognition and achievements

### Fonts
- **Available Fonts**: Arial, Calibri, Times New Roman, Georgia, Verdana
- **Font Sizes**: 8pt to 16pt
- **Automatic Scaling**: Headers are automatically sized relative to body text

### Output Styling
- Clean, modern design
- Professional color scheme
- Print-optimized layout
- ATS-friendly formatting
- Consistent spacing and alignment

## File Structure

```
resume_formatter.py    # Main application file
requirements.txt       # Python dependencies (standard library only)
README.md             # This file
```

## Settings Storage

Your preferences are automatically saved to `~/.resume_formatter_settings.json` and will be restored when you restart the application.

## Tips for Best Results

1. **Use clear section headers** like "EXPERIENCE", "EDUCATION", "SKILLS"
2. **Include dates** in a consistent format (e.g., "2020-2023" or "Jan 2020 - Dec 2023")
3. **Use bullet points** (• or -) for lists of achievements or skills
4. **Keep it concise** - the formatter works best with well-organized content
5. **Preview before exporting** - use the live preview to ensure formatting looks correct

## Browser Compatibility

The generated HTML works in all modern browsers:
- Chrome/Chromium
- Firefox
- Safari
- Edge

## Printing/PDF Export

To save as PDF:
1. Click "Generate Resume" to open in browser
2. Use your browser's print function (Ctrl+P / Cmd+P)
3. Select "Save as PDF" as the destination
4. Adjust margins if needed (usually "Minimum" works best)

## Troubleshooting

**Preview not updating?**
- Make sure you have text in the input area
- Check that at least one section is enabled in settings

**Formatting looks wrong?**
- Verify section headers are clear (EXPERIENCE, EDUCATION, etc.)
- Ensure consistent formatting in your input text
- Try the sample text provided to see expected format

**Can't save settings?**
- Check that you have write permissions in your home directory
- Settings are saved to `~/.resume_formatter_settings.json`

## Requirements

- Python 3.6 or higher
- No additional packages required (uses only standard library)

## License

This project is open source and available under the MIT License.