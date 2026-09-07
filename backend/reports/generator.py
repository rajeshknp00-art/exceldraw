"""Triage report generation in PDF, HTML, and text formats."""
import os
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from fpdf import FPDF
import html

class TriageReportGenerator:
    def __init__(self):
        self.output_dir = "/tmp/triage_reports"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_pdf(self, triage_data: Dict[str, Any], language: str = "en") -> str:
        """Generate PDF report."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Healthcare AI Triage Report", ln=True, align="C")
        pdf.ln(5)
        
        # Header info
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, f"Report ID: {triage_data.get('triage_id', 'N/A')}", ln=True)
        pdf.cell(0, 6, f"Date: {triage_data.get('created_at', datetime.utcnow().isoformat())}", ln=True)
        pdf.cell(0, 6, f"Urgency Level: {triage_data.get('urgency_level', 'N/A').upper()}", ln=True)
        pdf.cell(0, 6, f"Confidence: {triage_data.get('confidence', 0)*100:.0f}%", ln=True)
        pdf.ln(5)
        
        # Possible conditions
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Possible Conditions:", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for cond in triage_data.get("possible_conditions", []):
            pdf.cell(0, 6, f"- {cond.get('name', 'N/A')} ({cond.get('probability', 0)*100:.0f}%): {cond.get('description', '')}", ln=True)
        pdf.ln(5)
        
        # Recommended action
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Recommended Action:", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, triage_data.get("recommended_action", "N/A"))
        pdf.ln(5)
        
        # Red flags
        if triage_data.get("red_flags"):
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "Red Flags:", ln=True)
            pdf.set_font("Helvetica", "", 10)
            for flag in triage_data.get("red_flags", []):
                pdf.cell(0, 6, f"- {flag}", ln=True)
            pdf.ln(5)
        
        # Disclaimer
        pdf.set_font("Helvetica", "I", 8)
        pdf.multi_cell(0, 4, triage_data.get("disclaimer", ""))
        
        # Save
        report_id = str(uuid.uuid4())[:8]
        output_path = os.path.join(self.output_dir, f"triage_report_{report_id}.pdf")
        pdf.output(output_path)
        return output_path
    
    def generate_html(self, triage_data: Dict[str, Any], language: str = "en") -> str:
        """Generate HTML report."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Triage Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ text-align: center; border-bottom: 2px solid #0ea5e9; padding-bottom: 20px; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #0ea5e9; border-bottom: 1px solid #e2e8f0; padding-bottom: 5px; }}
        .condition {{ background: #f0f9ff; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #0ea5e9; }}
        .red-flag {{ background: #fef2f2; border-left: 4px solid #ef4444; padding: 10px; margin: 10px 0; }}
        .disclaimer {{ font-style: italic; color: #64748b; font-size: 0.875rem; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; }}
        .urgency {{ display: inline-block; padding: 8px 16px; border-radius: 9999px; font-weight: bold; }}
        .emergency {{ background: #fee2e2; color: #991b1b; }}
        .urgent {{ background: #ffedd5; color: #9a3412; }}
        .routine {{ background: #fef3c7; color: #92400e; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Healthcare AI Triage Report</h1>
        <p>Report ID: {triage_data.get('triage_id', 'N/A')} | Date: {triage_data.get('created_at', '')}</p>
    </div>
    
    <div class="section">
        <h2>Triage Assessment</h2>
        <p><strong>Urgency Level:</strong> <span class="urgency {triage_data.get('urgency_level', 'routine')}">{triage_data.get('urgency_level', 'N/A').upper()}</span></p>
        <p><strong>Confidence:</strong> {triage_data.get('confidence', 0)*100:.0f}%</p>
    </div>
    
    <div class="section">
        <h2>Possible Conditions</h2>
"""
        for cond in triage_data.get("possible_conditions", []):
            html_content += f"""
        <div class="condition">
            <h3>{cond.get('name', 'N/A')} ({cond.get('probability', 0)*100:.0f}%)</h3>
            <p>{cond.get('description', '')}</p>
        </div>
"""
        
        html_content += """
    </div>
    
    <div class="section">
        <h2>Recommended Action</h2>
        <p>{recommended_action}</p>
    </div>
""".format(recommended_action=triage_data.get("recommended_action", "N/A"))
        
        if triage_data.get("red_flags"):
            html_content += """
    <div class="section">
        <h2>Red Flags</h2>
"""
            for flag in triage_data.get("red_flags", []):
                html_content += f'<div class="red-flag">{html.escape(flag)}</div>'
            html_content += "</div>"
        
        html_content += f"""
    <div class="disclaimer">
        {triage_data.get("disclaimer", "")}
    </div>
</body>
</html>
"""
        
        report_id = str(uuid.uuid4())[:8]
        output_path = os.path.join(self.output_dir, f"triage_report_{report_id}.html")
        with open(output_path, "w") as f:
            f.write(html_content)
        return output_path
    
    def generate_text(self, triage_data: Dict[str, Any], language: str = "en") -> str:
        """Generate plain text report."""
        lines = [
            "=" * 60,
            "HEALTHCARE AI TRIAGE REPORT",
            "=" * 60,
            f"Report ID: {triage_data.get('triage_id', 'N/A')}",
            f"Date: {triage_data.get('created_at', datetime.utcnow().isoformat())}",
            f"Urgency Level: {triage_data.get('urgency_level', 'N/A').upper()}",
            f"Confidence: {triage_data.get('confidence', 0)*100:.0f}%",
            "",
            "POSSIBLE CONDITIONS:",
            "-" * 40,
        ]
        
        for cond in triage_data.get("possible_conditions", []):
            lines.append(f"  - {cond.get('name', 'N/A')} ({cond.get('probability', 0)*100:.0f}%): {cond.get('description', '')}")
        
        lines.extend([
            "",
            "RECOMMENDED ACTION:",
            "-" * 40,
            triage_data.get("recommended_action", "N/A"),
            "",
            "RED FLAGS:",
            "-" * 40,
        ])
        
        for flag in triage_data.get("red_flags", []):
            lines.append(f"  ! {flag}")
        
        lines.extend([
            "",
            "DISCLAIMER:",
            "-" * 40,
            triage_data.get("disclaimer", ""),
            "",
            "=" * 60,
            f"Report generated on {datetime.utcnow().isoformat()}",
            "Healthcare AI Triage Assistant",
            "=" * 60,
        ])
        
        report_id = str(uuid.uuid4())[:8]
        output_path = os.path.join(self.output_dir, f"triage_report_{report_id}.txt")
        with open(output_path, "w") as f:
            f.write("\n".join(lines))
        return output_path

# Singleton
report_generator = None

def get_report_generator():
    global report_generator
    if report_generator is None:
        report_generator = TriageReportGenerator()
    return report_generator
