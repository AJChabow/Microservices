import os, csv

def get_unit_tests_for_riego_ivia():
    with open(os.path.join(os.getcwd(),"calculations/test-resources/unit_tests_for_riego_ivia.csv"), "r") as file:
        list_of_tests = []
        reader = csv.reader(file)
        for line in reader:
            list_of_tests.append(line)
    return list_of_tests

def test_does_calculation_match_ivia():
    print(get_unit_tests_for_riego_ivia())
        
test_does_calculation_match_ivia()