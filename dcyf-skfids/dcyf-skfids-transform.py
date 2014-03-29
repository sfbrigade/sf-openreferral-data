import csv, json

def csv2json(csv_file_name,json_file_name):
    jsonfile = open(json_file_name, 'w')
    with open(csv_file_name,'r') as csvfile:
        reader = csv.DictReader(csvfile,dialect='excel')
        fieldnames = reader.fieldnames
        list_of_orgs = []
        for row in reader:
            list_of_orgs.append(row)

    json.dump(list_of_orgs,jsonfile)
    jsonfile.close()

csv2json("Organizations.csv","Organizations.json")

def sfkids2openreferral(json_file_name):

    def organization_name(sfkids_organization, ohana_organization):
        if sfkids_organization["OperatedBy"]:
            ohana_organization["name"] = sfkids_organization["OperatedBy"]
        else:
            ohana_organization["name"] = sfkids_organization["Content_title"]

    def organization_url(sfkids_organization, ohana_organization):
        ohana_organization["urls"] = sfkids_organization["Website"]

    with open(json_file_name) as json_file_obj:
        all_sfkids_organizations = json.load(json_file_obj)
        json_file_obj.close()

    openreferral_json = open("open_referral.json","w")
    all_ohana_organizations = []

    for sfkids_organization in all_sfkids_organizations:
        ohana_organization = {}
        organization_name(sfkids_organization, ohana_organization)
        organization_url(sfkids_organization, ohana_organization)
        print ohana_organization
        all_ohana_organizations.append(ohana_organization)
        
    json.dump(all_ohana_organizations, openreferral_json)
    openreferral_json.close()

sfkids2openreferral('Organizations.json')