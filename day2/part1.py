def is_safe_report(report):
    levels = list(map(int, report.split()))
    
    increasing = all(levels[i] < levels[i + 1] and 1 <= levels[i + 1] - levels[i] <= 3 for i in range(len(levels) - 1))
    decreasing = all(levels[i] > levels[i + 1] and 1 <= levels[i] - levels[i + 1] <= 3 for i in range(len(levels) - 1))
    
    return increasing or decreasing

def count_safe_reports(file_path):
    with open(file_path, 'r') as file:
        reports = file.readlines()
    
    safe_count = sum(is_safe_report(report.strip()) for report in reports)
    
    return safe_count

file_path = 'input'
print(count_safe_reports(file_path))