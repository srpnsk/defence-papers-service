import os
import zipfile
import shutil
import subprocess
import uuid
import json
from datetime import datetime

class LatexCompiler:
    def __init__(self, temp_base="./temp_latex", project_root=None):
        self.temp_base = temp_base
        self.project_root = project_root or os.getcwd()
        os.makedirs(temp_base, exist_ok=True)
    
    def check_dependencies(self):
        try:
            subprocess.run(["pdflatex", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("pdflatex не установлен. Установите TeX Live или MiKTeX")
        
        try:
            subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def compile_pdflatex(self, tex_path, work_dir, num_runs=2):
        base_name = os.path.splitext(os.path.basename(tex_path))[0]
        pdf_path = os.path.join(work_dir, f"{base_name}.pdf")
        
        for i in range(num_runs):
            try:
                result = subprocess.run(
                    ["pdflatex", 
                     "-interaction=nonstopmode", 
                     "-halt-on-error",
                     "-output-directory", work_dir, 
                     tex_path],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode != 0:
                    return None, f"Ошибка pdflatex на проходе {i+1}:\n{result.stderr[-500:]}"
            except subprocess.TimeoutExpired:
                return None, f"Таймаут при компиляции {tex_path}"
        
        if os.path.exists(pdf_path):
            return pdf_path, None
        return None, "PDF не создан после компиляции"
    
    def compile_from_files(self, tex_files_content):
        job_id = str(uuid.uuid4())
        work_dir = os.path.join(self.temp_base, job_id)
        os.makedirs(work_dir, exist_ok=True)
        
        for filename, content in tex_files_content.items():
            full_path = os.path.join(work_dir, filename)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        
        main_files = ["01_Before_acceptance.tex", "02_Acceptance_panel.tex", "style.sty"]
        for file in main_files:
            src = os.path.join(self.project_root, file)
            if os.path.exists(src):
                shutil.copy2(src, work_dir)
            else:
                print(f"  Не найден (пропускаем): {file}")
        
        templates_src = os.path.join(self.project_root, "Templates")
        if os.path.exists(templates_src):
            dest_templates = os.path.join(work_dir, "Templates")
            if os.path.exists(dest_templates):
                shutil.rmtree(dest_templates)
            shutil.copytree(templates_src, dest_templates)
        
        sources_src = os.path.join(self.project_root, "Sources")
        if os.path.exists(sources_src):
            dest_sources = os.path.join(work_dir, "Sources")
            if not os.path.exists(dest_sources):
                shutil.copytree(sources_src, dest_sources)
        
        self.check_dependencies()
        
        results = {
            "pdf_files": [],
            "docx_files": [],
            "tex_files": [],
            "logs": []
        }
        
        for tex_file in ["01_Before_acceptance.tex", "02_Acceptance_panel.tex"]:
            tex_path = os.path.join(work_dir, tex_file)
            if not os.path.exists(tex_path):
                print(f"{tex_file} не найден")
                continue
            
            pdf_path, error = self.compile_pdflatex(tex_path, work_dir, num_runs=2)
            
            if pdf_path:
                results["pdf_files"].append(pdf_path)

                docx_path = os.path.join(work_dir, tex_file.replace(".tex", ".docx"))
                try:
                    subprocess.run(
                        ["pandoc", tex_path, "-o", docx_path],
                        capture_output=True,
                        text=True,
                        timeout=60,
                        check=True
                    )
                    if os.path.exists(docx_path):
                        results["docx_files"].append(docx_path)
                except Exception as e:
                    print(f" Конвертация в Word не удалась: {str(e)[:100]}")
            else:
                results["logs"].append(f"Ошибка в {tex_file}: {error}")
                print(f" Ошибка компиляции {tex_file}")
        
        for root, _, files in os.walk(work_dir):
            for f in files:
                if f.endswith(".tex"):
                    results["tex_files"].append(os.path.join(root, f))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if results["pdf_files"]:
            pdf_zip = os.path.join(work_dir, f"documents_pdf_{timestamp}.zip")
            with zipfile.ZipFile(pdf_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in results["pdf_files"]:
                    zipf.write(file_path, os.path.basename(file_path))
            results["pdf_zip"] = pdf_zip
        
        if results["tex_files"]:
            tex_zip = os.path.join(work_dir, f"documents_tex_{timestamp}.zip")
            with zipfile.ZipFile(tex_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in results["tex_files"]:
                    arcname = os.path.relpath(file_path, work_dir)
                    zipf.write(file_path, arcname)
            results["tex_zip"] = tex_zip
        
        if results["docx_files"]:
            docx_zip = os.path.join(work_dir, f"documents_docx_{timestamp}.zip")
            with zipfile.ZipFile(docx_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in results["docx_files"]:
                    zipf.write(file_path, os.path.basename(file_path))
            results["docx_zip"] = docx_zip
        
        results["work_dir"] = work_dir
        results["job_id"] = job_id
        
        return results
    
    def cleanup(self, work_dir):
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)