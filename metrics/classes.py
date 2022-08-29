from robot.api import ResultVisitor

class SuiteResults(ResultVisitor):

    def __init__(self, suite_list):
        self.suite_list = suite_list
    
    def start_suite(self, suite):
        if suite.tests:
            try:
                stats = suite.statistics.all
            except:
                stats = suite.statistics
            
            try:
                skipped = stats.skipped
            except:
                skipped = 0

            suite_json = {
                "Name" : suite.longname,
                "Id" : suite.id,
                "Status" : suite.status,
                "Documentation" : suite.doc,
                "Total" : stats.total,
                "Pass" : stats.passed,
                "Fail" : stats.failed,
                "Skip" : skipped,
                "Time" : suite.elapsedtime,
            }
            self.suite_list.append(suite_json)

class TestResults(ResultVisitor):

    def __init__(self, test_list):
        self.test_list = test_list
    
    def visit_task(self, test):
        test_json = {
            "Suite Name" : test.parent,
            "Task Name" : test,
            "Task Id" : test.id,
            "Status" : test.status,
            "Documentation" : test.doc,
            "Time" : test.elapsedtime,
            "Message" : test.message,
            "Tags" : test.tags 
        }
        self.test_list.append(test_json)


class KeywordResults(ResultVisitor):

    def __init__(self, kw_list, ignore_library, ignore_type):
        self.kw_list = kw_list
        self.ignore_library = ignore_library
        self.ignore_type = ignore_type
        
    def start_keyword(self, kw):
        if (kw.libname not in self.ignore_library) and (kw.type not in self.ignore_type):
            kw_json = {
                "Name" : kw.name,
                "Status" : kw.status,
                "Time" : kw.elapsedtime
            }
            self.kw_list.append(kw_json)