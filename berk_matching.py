import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import time

def main():
    return setupGspread()

def setupGspread():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    request_sheet = client.open("Berkeley_Grocery_Database").worksheet("Request_Query")  # Open the spreadsheet
    request_data = request_sheet.get_all_records()  # Get a list of all records


    volunteer_sheet = client.open("Berkeley_Grocery_Database").worksheet("Volunteer_Query")
    volunteer_data = volunteer_sheet.get_all_records()
    
    matches_sheet = client.open("Berkeley_Grocery_Database").worksheet("Matches")

    return formatData(request_data, volunteer_data), matches_sheet

def formatData(request_data, volunteer_data):
    #Formats data into dictionary in the form {ID : {every dictionary} , ID: {every dictionary}, etc.}
    request_dictionary = {}
    for info in request_data:
        request_dictionary[info['ID']] = {key: val for key, val in info.items()}

    #Changes format from {Whole Foods: 1} to {Store : Whole Foods} for stores, cities, days, and times.
    volunteer_dictionary = {}
    for info in volunteer_data:
        volunteer_dictionary[info['ID']] = {key: info[key] for key in ('Email', 'Name', 'Phone', 'Contact')}
        volunteer_dictionary[info['ID']]['Store'] = {key for key in ('Central Berkeley Trader Joe’s', 'North Berkeley Safeway', 'North Berkeley Trader Joe’s', 'South Berkeley Berkeley Bowl', 'South Berkeley/Oakland Safeway', 'Southwest Berkeley Berkeley Bowl', 'Other') if info[key] == 1}
        volunteer_dictionary[info['ID']]['Day'] = {key for key in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') if info[key] == 1}
        volunteer_dictionary[info['ID']]['Time'] = {key for key in ('Delivery1', 'Delivery2', 'Delivery3', 'Delivery4', 'Delivery5', 'Delivery6') if info[key] == 1}

    return create_joint_dictionary(request_dictionary, volunteer_dictionary)
    

def create_joint_dictionary(request_dictionary, volunteer_dictionary):
    """
    Creates a joint dictionary based on the constraints in request and volunteer.
    request_dictionary: a dictionary representing all constraints of seniors
    volunteer_dictionary: a dictionary representing all constraints of volunteers
    returns: a dictionary with key as volunteer ID and value as a set of all seniors they could possibly be matched with
    """
    joint_dict = {}
    for key1 in request_dictionary:
        #set every single volunteer to set() first, before assigning real pairings if conditions are met
        joint_dict[key1] = set()
        for key in volunteer_dictionary:
            #make sure the store, city, day constraints are met
            if (request_dictionary[key1]['Store'] in volunteer_dictionary[key]['Store']) and (request_dictionary[key1]['Day'] in volunteer_dictionary[key]['Day']):
                #massive logic statement to decide whether the times match
                if (0.25 <= request_dictionary[key1]['Time'] <= (8/24) and 'Delivery1' in volunteer_dictionary[key]['Time']) or ((8/24) <= request_dictionary[key1]['Time'] <= (12/24) and 'Delivery2' in volunteer_dictionary[key]['Time']) or ((12/24) <= request_dictionary[key1]['Time'] <= (15/24) and 'Delivery3' in volunteer_dictionary[key]['Time']) or ((15/24) <= request_dictionary[key1]['Time'] <= (18/24) and 'Delivery4' in volunteer_dictionary[key]['Time']) or ((18/24) <= request_dictionary[key1]['Time'] <= (21/24) and 'Delivery5' in volunteer_dictionary[key]['Time']) or ((21/24) <= request_dictionary[key1]['Time'] <= (23/24) and 'Delivery6' in volunteer_dictionary[key]['Time']):
                    #if both are met, then these people match!!! whoo
                    joint_dict[key1].add(key)

    return joint_dict, request_dictionary, volunteer_dictionary

def create_subgraph(joint_dictionary):
    subgraph = {key: val for key, val in joint_dictionary.items() if val != set()}
    return subgraph

def request_capacity(subgraph):
    capacity = {key: 4 for key in subgraph}
    return capacity

def volunteer_ab(subgraph):
    ability = {}
    for key in subgraph.values():
        for elem in key:
            if not elem in ability:
                ability[elem] = 1
    return ability

def boolify_matching_problem(request_preferences, senior_limit, volunteer_ability):
    """
    Convert a request-volunteer matching problem into a Boolean formula.

    request_preferences: a dictionary mapping a name (string) to a set of 
                        volunteer names (strings) that work for that request
    senior_limit: a dictionary mapping each senior name to a positive
                        integer for how many volunteers they can be matched with

    Returns: a CNF formula encoding the matching problem
    """

    def requests_preferences(request_preferences, senior_limit):
        """
        Return a CNF just for requests being matched in at least one of their preferences.
        """
        
        CNF = []

        #append a list of tuples to a larger list containing requests with their preferences
        for key in request_preferences:
            CNF.append([('{0}_{1}'.format(key, pref), True) for pref in request_preferences[key]])
        return CNF

    def request_to_volunteer(request_preferences, volunteer_ability):
        """
        Return a CNF to make sure every volunteer has been matched to exactly one senior, and no more.
        """
        
        CNF = []
        requests = [request for request in request_preferences]
        
        #append a list of tuples to a larger list containing all possible pairs of requests to each volunteer
        for i in range(0, len(requests)):
            for j in range(i+1, len(requests)):
                for key in volunteer_ability:
                    CNF.append([('{0}_{1}'.format(requests[el], key), False) for el in (i, j)])
        return CNF


    
    #once each condition's lists are created, concatenate them in order to form the overall CNF
    CNF = requests_preferences(request_preferences, senior_limit) + request_to_volunteer(request_preferences, volunteer_ability) 
    
    return CNF


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.
    """

    #check for whether the formula is valid or not and return None if unsatisfiable 
    if len(formula) == 0:
        return {}
    elif [] in formula:
        return None
  
    def create_new_formula(formula, elem):
        """
        Create a new formula constructed from formula parameter given elem parameter is satisfied.

        formula: list that encodes the original statement
        elem: a tuple that should be satisfied to return the new formula

        Returns: a list which contains a modified formula
        """

        new_formula = [k for k in formula if elem not in k and (elem[0], not elem[1]) not in k]
        for k in formula:
            if (elem[0], not elem[1]) in k:
                new_formula.append([el for el in k if el != (elem[0], not elem[1])])
        return new_formula

    #loop through unit clauses since they must be true
    for clause in formula:
        if len(clause) == 1:
            #elem = the only element in the clause
            elem = clause[0]
            #create a new formula f1 that eliminates statements based on elem being satisfied
            f1 = create_new_formula(formula, elem)
            #check whether satisfying this clause results in a valid result. if valid, update dictionary. otherwise, return None
            check_unit = satisfying_assignment(f1)
            if check_unit is not None:
                check_unit[elem[0]] = elem[1]
                return check_unit
            else:
                return None
    
    #once unit clauses are looped through, check through other clauses
    for clause in formula:
        if len(clause) > 1:
            for elem in clause:
                #create a new formula f2 that eliminates statements based on elem being satisfied
                f2 = create_new_formula(formula, elem)
                #check whether satisfying elem results in a valid result. if valid, update dictionary. otherwise, formula f3.
                check_existing = satisfying_assignment(f2)
                if check_existing is not None:
                    check_existing[elem[0]] = elem[1]
                    return check_existing
                elif check_existing is None:
                    #create a new formula f3 that eliminates statements based on elem not being satisfied
                    f3 = create_new_formula(formula, (elem[0], not elem[1]))
                    #check whether not satisfying element results in a valid result. if valid, update dictionary. otherwise, return None.
                    check_other = satisfying_assignment(f3)
                    if check_other is not None:
                        if not elem[0] in check_other:
                            check_other[elem[0]] = not elem[1]
                            return check_other
                    else:
                        return None
        #in the process, new unit clauses may be created. check again and update accordingly
        elif len(clause) == 1:
            return satisfying_assignment(formula)

def get_matches(satisfying_assignment, joint_dict):
    matches_dict =  {key.split('_')[0]: {'match': key.split('_')[1], 'options': []} for key, val in satisfying_assignment.items() if val == True}
    for match in matches_dict:
        for option in joint_dict[match]:
            if option != matches_dict[match]['match']:
                if len(matches_dict[match]['options']) < 2:
                    matches_dict[match]['options'].append(option)
    for match in matches_dict:
        if matches_dict[match]['options'] == []:
            del matches_dict[match]['options']
    print(matches_dict)
    return matches_dict

def update_worksheet_with_matches():
    results = main()
    joint_dict = results[0][0]
    matches_worksheet = results[1]
    request_preferences = create_subgraph(joint_dict)
    senior_limit = request_capacity(request_preferences)
    volunteer_ability = volunteer_ab(request_preferences)
    
    matches_with_id = get_matches(satisfying_assignment(boolify_matching_problem(request_preferences, senior_limit, volunteer_ability)), joint_dict)
    request_data = results[0][1]
    volunteer_data = results[0][2]
    
    request_headers = ['Name', 'Email', 'Phone', 'Contact', 'Store', 'Day', 'Time', 'Address', 'Payment']
    i = 2
    for request in matches_with_id.keys():
        for j in range(len(request_headers)):
            matches_worksheet.update_cell(i, j+1, request_data[request][request_headers[j]])
            time.sleep(1)
        matches_worksheet.update_cell(i, 10, volunteer_data[matches_with_id[request]['match']]['Name'])
        time.sleep(1)
        matches_worksheet.update_cell(i, 11, volunteer_data[matches_with_id[request]['match']]['Email'])
        time.sleep(1)
        matches_worksheet.update_cell(i, 12, volunteer_data[matches_with_id[request]['match']]['Phone'])
        time.sleep(1)
        if 'options' in matches_with_id[request]:
            for k in range(len(matches_with_id[request]['options'])):
                matches_worksheet.update_cell(i, 13+3*k, volunteer_data[matches_with_id[request]['options'][k]]['Name'])
                time.sleep(1)
                matches_worksheet.update_cell(i, 14+3*k, volunteer_data[matches_with_id[request]['options'][k]]['Email'])
                time.sleep(1)
                matches_worksheet.update_cell(i, 15+3*k, volunteer_data[matches_with_id[request]['options'][k]]['Phone'])
        i+=1

if __name__ == '__main__':
    update_worksheet_with_matches()

