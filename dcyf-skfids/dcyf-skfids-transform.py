import csv, json, pprint
from sys import argv

def csv2dicts(csv_file_name):
    '''
    Converts a csv of organizations into a list of dicts
    '''
    with open(csv_file_name,'r') as csvfile:
        reader = csv.DictReader(csvfile,dialect='excel')
        all_sfkids_orgs = []
        for row in reader:
            all_sfkids_orgs.append(row)
        return all_sfkids_orgs

def name_matches(sfkids_org, oref_org):
    if oref_org["name"] == sfkids_org["OperatedBy"]:
        return True
    elif oref_org["name"] == sfkids_org["Content_title"]:
        return True
    else:
        return False

def build_org():
    openref_org = {}
    openref_org["name"] = None
    openref_org["locs"] = []
    return openref_org

def org_name(sfkids_org, oref_org):
    '''
    Finds the org name
    '''
    if sfkids_org["OperatedBy"]:
        oref_org["name"] = sfkids_org["OperatedBy"]
    else:
        oref_org["name"] = sfkids_org["Content_title"]

def org_url(sfkids_org, oref_org):
    '''
    Finds the org url
    '''
    oref_org["urls"] = sfkids_org["Website"]

def build_location():
    '''
    Adds the location field to the org
    https://github.com/codeforamerica/ohana-api/wiki/Populating-the-Mongo-database-from-a-JSON-file#location
    '''
    location = {}
    location["accessibility"] = []
    location["address"] = {}
    location["contacts"] = []
    location["coordinates"] = []
    location["description"] = None
    location["emails"] = []
    location["faxes"] = []
    location["hours"] = None
    location["kind"] = None
    location["languages"] = []
    location["mail_address"] = {}
    location["name"] = None
    location["phone"] = []
    location["short_desc"] = None
    location["transportation"] = []
    location["urls"] = []
    return location

def loc_accessibility(sfkids_org, location):
    '''
    Finds the locations accessibility.
    https://github.com/codeforamerica/ohana-api/wiki/Populating-the-Mongo-database-from-a-JSON-file#accessibility
    The SfKids locations either have Yes or N/A
    Not enough info to add it
    '''
    # oref_org['location']["accessibility"].append(sfkids_org["Accessibility"])
    pass

def loc_address(sfkids_org, oref_loc):
    '''
    Finds the locations address.
    https://github.com/codeforamerica/ohana-api/wiki/Populating-the-Mongo-database-from-a-JSON-file#address
    '''
    oref_loc["address"]["street"] = sfkids_org["Address"]
    oref_loc["address"]["city"] = sfkids_org["City"]
    oref_loc["address"]["state"] = sfkids_org["State"]
    oref_loc["address"]["zip"] = sfkids_org["Zip_Code"]

def main(filename):
    all_sfkids_orgs = csv2dicts(filename)
    all_oref_orgs = []
    all_oref_locs = []
    # all_oref_contacts = []

    # Build orgs
    for sfkids_org in all_sfkids_orgs:
        oref_org = build_org()
        org_name(sfkids_org, oref_org)
        org_url(sfkids_org, oref_org)
        all_oref_orgs.append(oref_org)

    # Build locs
    # Add them to correct org
    for sfkids_org in all_sfkids_orgs:
        oref_loc = build_location()
        loc_accessibility(sfkids_org, oref_loc)
        loc_address(sfkids_org, oref_loc)
        # loc_contacts(sfkids_org, oref_loc)

        for oref_org in all_oref_orgs:
            if name_matches(sfkids_org, oref_org):
                oref_org["locs"].append(oref_loc)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(all_oref_orgs)

main(argv[1])