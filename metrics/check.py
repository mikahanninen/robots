from robot.api import ExecutionResult
from robotframework_metrics.suite_results import SuiteResults
from robotframework_metrics.test_results import TestResults
from robotframework_metrics.keyword_results import KeywordResults

def main():
    result = ExecutionResult("output.xml")
    suite_list = []
    test_list = []
    kw_list = []
    ignore_library = []
    ignore_type = []
    result.visit(SuiteResults(suite_list))
    result.visit(TestResults(test_list))
    result.visit(KeywordResults(kw_list, ignore_library, ignore_type))
    bytime = sorted(kw_list, key=lambda d: d['Time'], reverse=True) 
    for kw in bytime:
        if kw['Status'] == 'NOT RUN':
            continue        
        print(kw)

    print("Done.")


if __name__  == "__main__":
    main()