#Uses json builder gem to build json after mapping
require 'json_builder'
require 'csv'
require 'facets/string/titlecase'

#imports csv
class Import_csv
  def initialize(file)
    @file = file
  end

#makes a ruby hash out of the csv data using the headers as keys, keys are converted to symbols and are lowercase
  def make_hash
    data = open(@file)
    csv = CSV.new(data, :headers => true, :header_converters => :symbol)
    csv.to_a.map {|row| row.to_hash }

  end
end
##Classes were made to easily map similar data structures. These could be expanded to clean the data as well. These should also be expanded in order to map more fields that the Ohana api provides. For fields in DC data that Ohana is missing classes and attributes should be built and ohana rails api models should be added.

#Main location class. Top level of nest. Contains nested classes: contacts, address, faxes, phones, services.
class Locations
  attr_reader :name, :contacts, :description, :short_description, :address, :mail_address, :hours, :transportation, :accessibility, :languages, :emails, :faxes, :phones, :urls, :services, :coordinates

  def initialize(options={})
    @name              = options[:name]
    @contacts          = options[:contacts]
    @description       = options[:description]
    @short_description = options[:short_description]
    @address           = options[:address]
    @mail_address      = options[:mail_address]
    @hours             = options[:hours]
    @transportation    = options[:transportation]
    @accessibility     = options[:accessibility]
    @languages         = options[:languages]
    @emails            = options[:emails]
    @faxes             = options[:faxes]
    @phones            = options[:phones]
    @urls              = options[:urls]
    @services          = options[:services]
    @coordinates       = options[:coordinates]
  end
end

class Contacts
  attr_reader :name, :title

  def initialize(options={})
    @name  = options[:name]
    @title = options[:title]
  end
end

class Address
  attr_reader :street, :city, :state, :zip

  def initialize(options={})
    @street = options[:street]
    @city   = options[:city]
    @state  = options[:state]
    @zip    = options[:zip]
  end
end


#not used at the moment
class Mail_address < Address
end

class Phones
  attr_reader :number, :department

  def initialize(options={})
    @number     = options[:number]
    @department = options[:department]
  end
end

class Faxes
  attr_reader :number, :department

  def initialize(options={})
    @number     = options[:number]
    @department = options[:department]
  end
end

class Services
  attr_reader :audience, :eligibility, :fees, :how_to_apply, :service_areas, :keywords, :wait, :funding_sources

  def initialize(options={})
    @audience        = options[:audience]
    @eligibility     = options[:eligibility]
    @fees            = options[:fees]
    @how_to_apply    = options[:how_to_apply]
    @service_areas   = options[:service_areas]
    @keywords        = options[:keywords]
    @wait            = options[:wait]
    @funding_sources = options[:funding_sources]
  end
end

class Organizations
  attr_reader :name

  def initialize(options={})
    @name   = options[:name]
    @locs   = []
  end

  def add_location(location)
    @locs << location
  end
end




#This class is the work horse class to build the json
class Build_json
  attr_reader :data
  def initialize(data)
    @data = data #array of hashes
  end

  #fills in a organization name based on which fields are not null. If no name, then name will be 'No Name'
  def find_agency(row)
    official = row[:officiallname]
    publicName = row[:publicname]
    parent = row[:parentagency]
    if official
      official.titlecase
    elsif publicName
      publicName.titlecase
    elsif parent
      parent.titlecase
    else
      'No Name'
    end
  end

  #by passing in the row of data, and the types of fields you need to build a class from, this method will build classes on the fly from that data into an array. Then nils are removed so empty data isn't mapped.
  def map_fields(row, array_of_fields)
    result = array_of_fields.map do |field|
      if row[field[0]]
        #the class you pass in is used here and class objects are built
        yield(row, field)
      end
    end
    #removes nil values
    result.compact
  end

  #takes a data row and the field you want to map and default's 'NA' if the field is not in the row or it is nil
  def missing_value_replace(row,field)
    row[field] ? row[field] : "NA"
  end

  #giant function that needs to be broken apart. Builds the objects from the row of data. Uses json_builder to buld the json from the mappings
  def map_row(row)
    addresses =
      Address.new(street: row[:physicaladdress1].to_s + ' ' + row[:physicaladdress2].to_s,
                  city:   row[:physicalcity],
                  state:  row[:physicalstateprovince],
                  zip:    row[:physicalpostalcode])

    faxes = [
      Faxes.new(number: row[:phonefax])
    ]

    services = [
      Services.new(audience:        row[:resourceinfo],
                   eligibility:     row[:eligibility],
                   fees:            row[:feestructuresource],
                   how_to_apply:    row[:applicationprocess].to_s + ' ' + row[:documentsrequired].to_s,
                   service_areas:   [row[:coveragearea]].compact,
                   keywords:        [row[:tax]].compact,
                   funding_sources: [row[:sourceoffunds]].compact)
    ]
    locations = [
      Locations.new(
                    name:               find_agency(row),
                    #uses map_fields to build contact objects if the fields contain data
                    contacts:           map_fields(row,[[:mailingattentionname, :none],
                                                        [:seniorworkername, :seniorworkertitle],
                                                        [:maincontactname, :maincontacttitle]]) do |row, field|
                                                          Contacts.new(name: row[field[0]], title: missing_value_replace(row, field[1]))
                                                        end ,
                     description:       row[:agencydescription],
                     short_description: missing_value_replace(row,:physicallocationdescription),
                     address:           addresses,
                     mail_address:      Address.new(street: row[:mailingaddress1].to_s + ' ' + row[:mailingaddress2].to_s,
                                                    city: row[:mailingcity],
                                                    state: row[:mailingstateprovince],
                                                    zip: row[:mailingpostalcode]),
                     hours:             row[:hours],
                     transportation:    row[:publicaccesstransportation].to_s + ' ' + row[:busservicetransportation].to_s,
                     languages:         [row[:languagesoffered]].compact,
                     emails:            [row[:emailaddressmain],
                                        row[:seniorworkeremailaddress],
                                        row[:maincontactemailaddress]].compact,
                     faxes:             faxes,
                     phones:            map_fields(row,[[:phone1number, :phone1name],
                                                       [:phone2number, :phone2name],
                                                       [:phone3number, :phone3name],
                                                       [:phone4number, :phone4name],
                                                       [:phone5number, :phone5description],
                                                       [:phonetty, 'tty'],
                                                       [:phonetollfree, 'toll-free'],
                                                       [:phonenumberhotline, 'phone hotline'],
                                                       [:phonenumberbusinessline, 'phone business line'],
                                                       [:phonenumberoutofarea, 'phone out of area'],
                                                       [:phonenumberafterhours, 'phone after hours'],
                                                       [:seniorworkerphonenumber,'senior worker'],
                                                       [:maincontactphonenumber,'main contact']]) do |row, field|
                                                         Phones.new(number: row[field[0]], department: row[field[1]])
                                                       end,
                     urls:             [row[:websiteaddress]].compact,
                     services:         services,
                     coordinates:      [row[:longitude],row[:latitude]]
                   )
    ]

    return locations

=begin
    #builds the json using the mappings from above
    JSONBuilder::Compiler.generate do
      name row[:resourceagencynum]
      locs locations do |loc|
        name loc.name
        #this style builds an json array of objects
        contacts loc.contacts do |contact|
          name contact.name
          title contact.title
        end
        description loc.description
        short_desc loc.short_description
        #this style builds a json object
        address do
          street loc.address.street
          city loc.address.city
          state loc.address.state
          zip loc.address.zip
        end
        #if there isn't a mail address, don't map it
        if loc.mail_address.street
          mail_address do
            street loc.mail_address.street
            city loc.mail_address.city
            state loc.mail_address.state
            zip loc.mail_address.zip
          end
        end
        hours loc.hours
        transportation loc.transportation
        languages loc.languages
        emails loc.emails
        faxes loc.faxes do |fax|
          number fax.number
        end
        phones loc.phones do |phone|
          number phone.number
          department phone.department
        end
        urls loc.urls
        servs loc.services do |service|
          audience service.audience
          eligibility service.eligibility
          fees service.fees
          how_to_apply service.how_to_apply
          service_areas service.service_areas
          keywords service.keywords
          #no wait in DC data
          wait ''
          funding_sources service.funding_sources
        end
      end
    end
=end
  end
end

def construct_hash(loc)
  locs = {
    "name" => "",
    "description" => "",
    "short_desc" => "",
    "address_attributes" => {},
    "hours" => "",
    #no mapping
    "accessibility" => [],
    "contacts_attributes" => [],
    "coordinates" => [],
    "emails" => [],
    "faxes_attributes" => [],
    #no mapping
    "kind" => "",
    "languages" => [],
    "phones_attributes" => [],
    "transportation" => "",
    "urls" => [],
    "services_attributes" => []
  }
  #strings
  locs["name"] = loc.name.to_s.titlecase
  locs["description"] = loc.description
  locs["short_desc"] = loc.short_description
  locs["transportation"] = loc.transportation
  locs["hours"] = loc.hours
  if loc.coordinates
    locs["coordinates"] = loc.coordinates
  end
  locs["emails"] = loc.emails
  locs["languages"] = loc.languages
  if loc.faxes
    loc.faxes.each do |fax|
      locs["faxes_attributes"] << {"number"=>fax.number}
    end
  end
  locs["address_attributes"] = {
    "street"=>loc.address.street,
    "city"=>loc.address.city,
    "state"=>loc.address.state,
    "zip"=>loc.address.zip.to_s[0..4]
  }
  if loc.mail_address.street
    locs["mail_address_attributes"] = {
      "street"=>loc.mail_address.street,
      "city"=>loc.mail_address.city,
      "state"=>loc.mail_address.state,
      "zip"=>loc.mail_address.zip.to_s[0..4]
    }
  end
  if loc.phones
    loc.phones.each do |phone|
      locs["phones_attributes"] << {"number"=>phone.number, "department"=>phone.department}
    end
  end
  locs["urls"] = loc.urls
  if loc.contacts
    loc.contacts.each do |contact|
      locs["contacts_attributes"] << {"name"=>contact.name,"title"=>contact.title}
    end
  end
  if loc.services
    loc.services.each do |service|
      locs["services_attributes"] << {
        "audience" => service.audience,
        "eligibility" => service.eligibility,
        "fees" => service.fees,
        "how_to_apply" => service.how_to_apply,
        "service_areas" => service.service_areas,
        "keywords" => service.keywords,
        "funding_sources" => service.funding_sources
      }
    end
  end
  return locs
end

#read and load csv
import = Import_csv.new('sf_only.csv')
csv = import.make_hash

#build csv file with json per row
json = Build_json.new(csv)

orgs = {}

json.data.each do |row|
  if row[:parentagencynum] == "0"
    orgs[row[:resourceagencynum]] = {"name" =>json.find_agency(row), "locations" => [], "urls" => [row[:websiteaddress]].compact }
    json.map_row(row).each do |location|
        orgs[row[:resourceagencynum]]["locations"] << construct_hash(location)
    end
  else
    if orgs[row[:parentagencynum]]
      json.map_row(row).each do |location|
        orgs[row[:parentagencynum]]["locations"] << construct_hash(location)
      end
    end
  end
end

#read row by row and output json to file

##
File.open('sf.json', 'wb') do |f|
  #f.puts "["
  orgs.each do |key, value|
    puts "writing " + value["name"]
    #calls map row on each row and adds it to the file
    f.puts value.to_json
  end
  #f.puts "]"
end
