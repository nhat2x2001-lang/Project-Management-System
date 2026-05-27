"""
CSV Data Audit Script
Analyzes CSV files in docs/ directory for data quality and consistency issues
Generates a detailed audit report for PROJECT_AUDIT.md
"""

import os
import csv
from collections import defaultdict, Counter
from datetime import datetime

class CSVAuditor:
    def __init__(self, docs_dir='docs'):
        self.docs_dir = docs_dir
        self.issues = []
        self.statistics = {}
        
    def audit_file(self, filename):
        """Read and audit a CSV file"""
        filepath = os.path.join(self.docs_dir, filename)
        if not os.path.exists(filepath):
            self.issues.append(f"FILE_NOT_FOUND: {filename}")
            return None
        
        data = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            return data
        except Exception as e:
            self.issues.append(f"ERROR_READING_{filename}: {str(e)}")
            return None
    
    def audit_task_csv(self):
        """Audit Task.csv"""
        print("\n=== AUDITING Task.csv ===")
        data = self.audit_file('Task.csv')
        if not data:
            return
        
        print(f"Total records: {len(data)}")
        self.statistics['Task.csv'] = {'total_records': len(data)}
        
        # Check for data issues
        empty_wbs = sum(1 for row in data if not row.get('WBS Code', '').strip())
        empty_description = sum(1 for row in data if not row.get('Task Discription', '').strip())
        
        print(f"  - Empty WBS Code: {empty_wbs}")
        print(f"  - Empty Task Description: {empty_description}")
        
        if empty_description > 0:
            self.issues.append(f"TASK_CSV: {empty_description} records with empty task description")
        
        # Check for typos
        print(f"  - Column 'Task Discription' (note: typo 'Discription' instead of 'Description')")
        self.issues.append("TASK_CSV: Column name typo 'Task Discription' should be 'Task Description'")
        
        # Check date formats
        date_format_issues = 0
        for idx, row in enumerate(data, 1):
            start = row.get('Start', '').strip()
            finish = row.get('Finish', '').strip()
            # Expected format: "Tue 10/07/25" or similar
            if start and not any(day in start for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
                date_format_issues += 1
        
        if date_format_issues > 0:
            print(f"  - Date format issues: {date_format_issues} records")
            self.issues.append(f"TASK_CSV: {date_format_issues} records with non-standard date format (expected 'Day MM/DD/YY')")
        
        # Check Duration format
        duration_issues = 0
        for row in data:
            duration = row.get('Duration', '').strip()
            if duration and ' day' not in duration.lower() and 'days' not in duration.lower():
                duration_issues += 1
        
        if duration_issues > 0:
            print(f"  - Duration format issues: {duration_issues}")
            self.issues.append(f"TASK_CSV: {duration_issues} records with non-standard duration format")
        
        # Predecessor references
        predecessors = [row.get('Predecessors', '').strip() for row in data if row.get('Predecessors', '').strip()]
        print(f"  - Records with predecessors: {len(predecessors)}")
        
        return data
    
    def audit_workers_csv(self):
        """Audit Workers.csv"""
        print("\n=== AUDITING Workers.csv ===")
        data = self.audit_file('Workers.csv')
        if not data:
            return
        
        print(f"Total records: {len(data)}")
        self.statistics['Workers.csv'] = {'total_records': len(data)}
        
        # Check column names
        first_row = data[0] if data else {}
        print(f"Columns: {list(first_row.keys())}")
        
        # Check for duplicates
        worker_ids = [row.get('Worker ID', '') for row in data]
        duplicate_ids = [id for id, count in Counter(worker_ids).items() if count > 1 and id]
        
        if duplicate_ids:
            print(f"  - Duplicate Worker IDs: {duplicate_ids}")
            for dup_id in duplicate_ids:
                count = worker_ids.count(dup_id)
                self.issues.append(f"WORKERS_CSV: Worker ID '{dup_id}' appears {count} times (duplicate)")
        
        # Check for empty values
        for col in ['Worker ID', 'Name', 'Resource Names']:
            empty_count = sum(1 for row in data if not row.get(col, '').strip())
            if empty_count > 0:
                print(f"  - Empty {col}: {empty_count}")
                self.issues.append(f"WORKERS_CSV: {empty_count} records with empty '{col}'")
        
        # Check for leading/trailing spaces
        spacing_issues = 0
        for row in data:
            for col in ['Name', 'Resource Names']:
                val = row.get(col, '')
                if val != val.strip():
                    spacing_issues += 1
                    break
        
        if spacing_issues > 0:
            print(f"  - Leading/trailing spaces: {spacing_issues} records")
            self.issues.append(f"WORKERS_CSV: {spacing_issues} records with leading/trailing spaces in values")
        
        # Check for misspellings
        if any('Safey' in row.get('Resource Names', '') for row in data):
            print(f"  - Misspelling detected: 'Safey' should be 'Safety'")
            self.issues.append("WORKERS_CSV: Misspelling 'Safey Practitioner' should be 'Safety Practitioner'")
        
        return data
    
    def audit_materials_csv(self):
        """Audit Materials.csv"""
        print("\n=== AUDITING Materials.csv ===")
        data = self.audit_file('Materials.csv')
        if not data:
            return
        
        print(f"Total records: {len(data)}")
        self.statistics['Materials.csv'] = {'total_records': len(data)}
        
        # Check for empty values
        for col in ['MATERIAL ID', 'MATERIALS', 'QUANTITY']:
            empty_count = sum(1 for row in data if not row.get(col, '').strip())
            if empty_count > 0:
                print(f"  - Empty {col}: {empty_count}")
                self.issues.append(f"MATERIALS_CSV: {empty_count} records with empty '{col}'")
        
        # Check cost format (contains commas)
        cost_format_issues = 0
        for row in data:
            cost = row.get('Cost', '').strip()
            if cost and ',' in cost:
                cost_format_issues += 1
        
        if cost_format_issues > 0:
            print(f"  - Cost format with commas: {cost_format_issues}")
            self.issues.append(f"MATERIALS_CSV: {cost_format_issues} cost values contain commas (should be numeric)")
        
        return data
    
    def audit_material_assignment_cost_csv(self):
        """Audit Material Assignment and Cost.csv"""
        print("\n=== AUDITING Material Assignment and Cost.csv ===")
        data = self.audit_file('Material Assignment and Cost.csv')
        if not data:
            return
        
        print(f"Total records: {len(data)}")
        self.statistics['Material Assignment and Cost.csv'] = {'total_records': len(data)}
        
        # Check for empty values
        for col in ['ForemanID', 'Task Description', 'Materials']:
            empty_count = sum(1 for row in data if not row.get(col, '').strip())
            if empty_count > 0:
                print(f"  - Empty {col}: {empty_count}")
                self.issues.append(f"MAT_ASSIGN_CSV: {empty_count} records with empty '{col}'")
        
        # Check cost format
        cost_issues = 0
        for row in data:
            for col in ['Unit Price', 'Budget Cost']:
                cost = row.get(col, '').strip()
                if cost and ',' in cost:
                    cost_issues += 1
        
        if cost_issues > 0:
            print(f"  - Cost format with commas: {cost_issues}")
        
        return data
    
    def audit_materials_usage_csv(self):
        """Audit Materials Usage.csv"""
        print("\n=== AUDITING Materials Usage.csv ===")
        data = self.audit_file('Materials Usage.csv')
        if not data:
            return
        
        print(f"Total records: {len(data)}")
        self.statistics['Materials Usage.csv'] = {'total_records': len(data)}
        
        # Check for empty values
        for col in ['USAGE ID', 'TASK ID', 'MATERIAL ID']:
            empty_count = sum(1 for row in data if not row.get(col, '').strip())
            if empty_count > 0:
                print(f"  - Empty {col}: {empty_count}")
                self.issues.append(f"MAT_USAGE_CSV: {empty_count} records with empty '{col}'")
        
        return data
    
    def audit_task_assignment_csv(self):
        """Audit Task_Assignment.csv (appears to be different from Task Assignment.csv)"""
        print("\n=== AUDITING Task_Assignment.csv ===")
        data = self.audit_file('Task_Assignment.csv')
        if not data:
            return
        
        print(f"Total records: {len(data)}")
        self.statistics['Task_Assignment.csv'] = {'total_records': len(data)}
        
        # Check for formatting issues
        header_row = data[0] if data else {}
        print(f"Columns: {list(header_row.keys())}")
        
        # Check for empty/header-like records
        empty_records = sum(1 for row in data if not row.get('TASK DESCRIPTION', '').strip() and 
                          all(not row.get(k, '').strip() for k in ['Worker ID', 'Name']))
        
        if empty_records > 0:
            print(f"  - Empty task description records: {empty_records}")
            self.issues.append(f"TASK_ASSIGN_CSV: {empty_records} records with empty task descriptions (possible formatting issues)")
        
        return data
    
    def audit_task_description_csv(self):
        """Audit Task_Description.csv"""
        print("\n=== AUDITING Task_Description.csv ===")
        data = self.audit_file('Task_Description.csv')
        if not data:
            return
        
        print(f"Total records: {len(data)}")
        self.statistics['Task_Description.csv'] = {'total_records': len(data)}
        
        return data
    
    def generate_report(self):
        """Generate comprehensive audit report"""
        print("\n" + "="*70)
        print("CSV DATA AUDIT REPORT")
        print(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}")
        print("="*70)
        
        # Run all audits
        self.audit_task_csv()
        self.audit_workers_csv()
        self.audit_materials_csv()
        self.audit_material_assignment_cost_csv()
        self.audit_materials_usage_csv()
        self.audit_task_assignment_csv()
        self.audit_task_description_csv()
        
        # Summary
        print("\n" + "="*70)
        print("AUDIT SUMMARY")
        print("="*70)
        print(f"Total Issues Found: {len(self.issues)}")
        print("\nIssue Categories:")
        
        categories = defaultdict(list)
        for issue in self.issues:
            cat = issue.split(':')[0]
            categories[cat].append(issue)
        
        for cat, issues in sorted(categories.items()):
            print(f"\n{cat}: {len(issues)} issue(s)")
            for issue in issues:
                print(f"  - {issue}")
        
        return self.issues, self.statistics

if __name__ == "__main__":
    auditor = CSVAuditor()
    issues, stats = auditor.generate_report()
    
    print("\n" + "="*70)
    print("Statistics by File:")
    print("="*70)
    for filename, stat in stats.items():
        print(f"{filename}: {stat['total_records']} records")
