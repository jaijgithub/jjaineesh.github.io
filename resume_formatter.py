#!/usr/bin/env python3
"""
Resume Formatter - Desktop Application
A customizable resume formatting tool with section management and font controls.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
import os
import webbrowser
import tempfile
from datetime import datetime
import re

class ResumeFormatter:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Formatter")
        self.root.geometry("1200x800")
        
        # Default settings
        self.settings = {
            'sections': ['Contact', 'Summary', 'Experience', 'Education', 'Skills', 'Projects'],
            'fonts': {
                'header': {'family': 'Arial', 'size': 16, 'weight': 'bold'},
                'subheader': {'family': 'Arial', 'size': 14, 'weight': 'bold'},
                'body': {'family': 'Arial', 'size': 11, 'weight': 'normal'}
            },
            'spacing': {'line': 1.2, 'section': 1.5},
            'colors': {'primary': '#2c3e50', 'secondary': '#34495e', 'text': '#2c3e50'}
        }
        
        self.load_settings()
        self.create_widgets()
        
    def create_widgets(self):
        # Create main paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for input and settings
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Right panel for preview
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        self.create_left_panel(left_frame)
        self.create_right_panel(right_frame)
        
    def create_left_panel(self, parent):
        # Input text area
        input_label = ttk.Label(parent, text="Paste your resume content here:", font=('Arial', 12, 'bold'))
        input_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.text_input = scrolledtext.ScrolledText(parent, height=15, wrap=tk.WORD)
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.text_input.bind('<KeyRelease>', self.on_text_change)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(parent, text="Formatting Settings", padding=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Font settings
        font_frame = ttk.Frame(settings_frame)
        font_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(font_frame, text="Font Family:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.font_var = tk.StringVar(value=self.settings['fonts']['body']['family'])
        font_combo = ttk.Combobox(font_frame, textvariable=self.font_var, 
                                 values=['Arial', 'Calibri', 'Times New Roman', 'Georgia', 'Verdana'],
                                 state='readonly', width=15)
        font_combo.grid(row=0, column=1, padx=5)
        font_combo.bind('<<ComboboxSelected>>', self.update_preview)
        
        ttk.Label(font_frame, text="Font Size:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        self.font_size_var = tk.StringVar(value=str(self.settings['fonts']['body']['size']))
        font_size_spin = ttk.Spinbox(font_frame, from_=8, to=16, textvariable=self.font_size_var, 
                                    width=5, command=self.update_preview)
        font_size_spin.grid(row=0, column=3, padx=5)
        
        # Section management
        section_frame = ttk.Frame(settings_frame)
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(section_frame, text="Active Sections:").pack(anchor=tk.W)
        
        self.section_vars = {}
        section_checkboxes = ttk.Frame(section_frame)
        section_checkboxes.pack(fill=tk.X)
        
        available_sections = ['Contact', 'Summary', 'Experience', 'Education', 'Skills', 'Projects', 'Certifications', 'Awards']
        for i, section in enumerate(available_sections):
            var = tk.BooleanVar(value=section in self.settings['sections'])
            self.section_vars[section] = var
            cb = ttk.Checkbutton(section_checkboxes, text=section, variable=var, command=self.update_preview)
            cb.grid(row=i//4, column=i%4, sticky=tk.W, padx=5, pady=2)
        
        # Action buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(button_frame, text="Generate Resume", command=self.generate_resume).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Export HTML", command=self.export_html).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Settings", command=self.save_settings).pack(side=tk.RIGHT)
        
    def create_right_panel(self, parent):
        preview_label = ttk.Label(parent, text="Live Preview:", font=('Arial', 12, 'bold'))
        preview_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Preview text area
        self.preview_text = scrolledtext.ScrolledText(parent, height=25, wrap=tk.WORD, state=tk.DISABLED)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.preview_text.tag_configure('header', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        self.preview_text.tag_configure('subheader', font=('Arial', 14, 'bold'), foreground='#34495e')
        self.preview_text.tag_configure('body', font=('Arial', 11, 'normal'))
        self.preview_text.tag_configure('contact', font=('Arial', 10, 'normal'), foreground='#7f8c8d')
        
    def on_text_change(self, event=None):
        """Update preview when text changes"""
        self.root.after(500, self.update_preview)  # Delay to avoid too frequent updates
        
    def parse_resume_text(self, text):
        """Parse the input text into structured resume data"""
        sections = {}
        current_section = None
        lines = text.strip().split('\n')
        
        # Common section headers
        section_patterns = {
            'Contact': r'^(contact|personal|info)',
            'Summary': r'^(summary|objective|profile)',
            'Experience': r'^(experience|work|employment|career)',
            'Education': r'^(education|academic|school)',
            'Skills': r'^(skills|technical|competenc)',
            'Projects': r'^(projects|portfolio)',
            'Certifications': r'^(certification|certificate)',
            'Awards': r'^(awards|achievement|honor)'
        }
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            found_section = None
            for section, pattern in section_patterns.items():
                if re.match(pattern, line.lower()):
                    found_section = section
                    break
            
            if found_section:
                current_section = found_section
                sections[current_section] = []
            elif current_section:
                sections[current_section].append(line)
            else:
                # If no section found yet, assume it's contact info
                if 'Contact' not in sections:
                    sections['Contact'] = []
                sections['Contact'].append(line)
        
        return sections
    
    def format_section(self, section_name, content):
        """Format a section based on its type"""
        if not content:
            return ""
            
        formatted = f"\n{section_name.upper()}\n" + "="*len(section_name) + "\n\n"
        
        if section_name == 'Contact':
            formatted += '\n'.join(content) + "\n"
        elif section_name == 'Experience':
            # Try to format experience entries
            current_job = []
            for line in content:
                if re.match(r'^[A-Z].*\s+\|\s+.*\s+\|\s+\d{4}', line) or \
                   re.match(r'^.*\s+at\s+.*\s+\(\d{4}', line.lower()):
                    if current_job:
                        formatted += self.format_job_entry(current_job) + "\n"
                        current_job = []
                    current_job.append(line)
                else:
                    current_job.append(line)
            if current_job:
                formatted += self.format_job_entry(current_job)
        elif section_name == 'Skills':
            # Format skills as categories or lists
            formatted += '\n'.join(f"• {skill}" for skill in content)
        else:
            # Default formatting
            for line in content:
                if line.startswith('•') or line.startswith('-'):
                    formatted += f"  {line}\n"
                else:
                    formatted += f"{line}\n"
        
        return formatted + "\n"
    
    def format_job_entry(self, job_lines):
        """Format a job entry"""
        if not job_lines:
            return ""
            
        # First line is usually title/company/dates
        header = job_lines[0]
        details = job_lines[1:] if len(job_lines) > 1 else []
        
        formatted = f"{header}\n"
        for detail in details:
            if detail.strip():
                if not detail.startswith('•') and not detail.startswith('-'):
                    formatted += f"• {detail}\n"
                else:
                    formatted += f"  {detail}\n"
        
        return formatted
    
    def update_preview(self, event=None):
        """Update the preview pane"""
        text = self.text_input.get('1.0', tk.END).strip()
        if not text:
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', "Enter your resume content to see the preview...")
            self.preview_text.config(state=tk.DISABLED)
            return
        
        # Parse the text
        parsed_sections = self.parse_resume_text(text)
        
        # Generate formatted preview
        preview_content = ""
        active_sections = [section for section, var in self.section_vars.items() if var.get()]
        
        for section in active_sections:
            if section in parsed_sections:
                preview_content += self.format_section(section, parsed_sections[section])
        
        # Update preview
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', preview_content)
        self.preview_text.config(state=tk.DISABLED)
    
    def generate_html(self, content_sections):
        """Generate HTML version of the resume"""
        font_family = self.font_var.get()
        font_size = self.font_size_var.get()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Resume</title>
            <style>
                body {{
                    font-family: '{font_family}', Arial, sans-serif;
                    font-size: {font_size}px;
                    line-height: 1.4;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 40px;
                    color: #2c3e50;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 20px;
                }}
                .section {{
                    margin-bottom: 25px;
                }}
                .section-title {{
                    font-size: {int(font_size) + 3}px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 10px;
                    text-transform: uppercase;
                    border-bottom: 1px solid #bdc3c7;
                    padding-bottom: 5px;
                }}
                .job-title {{
                    font-weight: bold;
                    color: #34495e;
                    margin-top: 15px;
                }}
                .contact-info {{
                    text-align: center;
                    color: #7f8c8d;
                    margin-bottom: 20px;
                }}
                ul {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
                li {{
                    margin-bottom: 5px;
                }}
                @media print {{
                    body {{ padding: 20px; }}
                }}
            </style>
        </head>
        <body>
        """
        
        active_sections = [section for section, var in self.section_vars.items() if var.get()]
        
        for section in active_sections:
            if section in content_sections and content_sections[section]:
                html += f'<div class="section">'
                
                if section == 'Contact':
                    html += '<div class="contact-info">'
                    html += '<br>'.join(content_sections[section])
                    html += '</div>'
                else:
                    html += f'<div class="section-title">{section}</div>'
                    
                    if section == 'Experience':
                        html += self.format_experience_html(content_sections[section])
                    elif section == 'Skills':
                        html += '<ul>'
                        for skill in content_sections[section]:
                            html += f'<li>{skill}</li>'
                        html += '</ul>'
                    else:
                        html += '<div>'
                        for item in content_sections[section]:
                            if item.startswith('•') or item.startswith('-'):
                                html += f'<li>{item[1:].strip()}</li>'
                            else:
                                html += f'<p>{item}</p>'
                        html += '</div>'
                
                html += '</div>'
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def format_experience_html(self, experience_content):
        """Format experience section for HTML"""
        html = ""
        current_job = []
        
        for line in experience_content:
            if re.match(r'^[A-Z].*\s+\|\s+.*\s+\|\s+\d{4}', line) or \
               re.match(r'^.*\s+at\s+.*\s+\(\d{4}', line.lower()):
                if current_job:
                    html += self.format_job_html(current_job)
                    current_job = []
                current_job.append(line)
            else:
                current_job.append(line)
        
        if current_job:
            html += self.format_job_html(current_job)
        
        return html
    
    def format_job_html(self, job_lines):
        """Format a single job entry for HTML"""
        if not job_lines:
            return ""
        
        html = f'<div class="job-title">{job_lines[0]}</div>'
        
        if len(job_lines) > 1:
            html += '<ul>'
            for detail in job_lines[1:]:
                if detail.strip():
                    clean_detail = detail.lstrip('•-').strip()
                    html += f'<li>{clean_detail}</li>'
            html += '</ul>'
        
        return html
    
    def generate_resume(self):
        """Generate and preview the formatted resume"""
        text = self.text_input.get('1.0', tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter resume content first.")
            return
        
        parsed_sections = self.parse_resume_text(text)
        html_content = self.generate_html(parsed_sections)
        
        # Create temporary HTML file and open in browser
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            temp_file = f.name
        
        webbrowser.open(f'file://{temp_file}')
        messagebox.showinfo("Success", "Resume generated and opened in your browser!")
    
    def export_html(self):
        """Export the resume as HTML file"""
        text = self.text_input.get('1.0', tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter resume content first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        
        if filename:
            parsed_sections = self.parse_resume_text(text)
            html_content = self.generate_html(parsed_sections)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            messagebox.showinfo("Success", f"Resume exported to {filename}")
    
    def save_settings(self):
        """Save current settings to file"""
        self.settings['fonts']['body']['family'] = self.font_var.get()
        self.settings['fonts']['body']['size'] = int(self.font_size_var.get())
        self.settings['sections'] = [section for section, var in self.section_vars.items() if var.get()]
        
        settings_file = os.path.join(os.path.expanduser('~'), '.resume_formatter_settings.json')
        try:
            with open(settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            messagebox.showinfo("Success", "Settings saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def load_settings(self):
        """Load settings from file"""
        settings_file = os.path.join(os.path.expanduser('~'), '.resume_formatter_settings.json')
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    saved_settings = json.load(f)
                self.settings.update(saved_settings)
        except Exception as e:
            print(f"Could not load settings: {e}")

def main():
    root = tk.Tk()
    app = ResumeFormatter(root)
    
    # Add sample text for demonstration
    sample_text = """John Doe
Software Engineer
john.doe@email.com | (555) 123-4567 | LinkedIn: linkedin.com/in/johndoe

SUMMARY
Experienced software engineer with 5+ years developing web applications and mobile solutions.

EXPERIENCE
Senior Software Engineer | Tech Company | 2020-2023
• Led development of customer-facing web applications
• Improved system performance by 40%
• Mentored junior developers

Software Engineer | StartupCo | 2018-2020
• Built mobile applications using React Native
• Collaborated with cross-functional teams
• Implemented CI/CD pipelines

EDUCATION
Bachelor of Science in Computer Science | University Name | 2018
• GPA: 3.8/4.0
• Relevant Coursework: Data Structures, Algorithms, Software Engineering

SKILLS
Programming Languages: Python, JavaScript, Java, C++
Frameworks: React, Node.js, Django, Spring Boot
Tools: Git, Docker, AWS, Jenkins
"""
    
    app.text_input.insert('1.0', sample_text)
    app.update_preview()
    
    root.mainloop()

if __name__ == "__main__":
    main()