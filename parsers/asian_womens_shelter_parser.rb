# Parses data found from http://www.sfaws.org/about-us/contact-us.aspx
require 'json'

module Parser
  def self.run
    puts AsianWomensShelter.parse()
  end

  # I couldn't find much data being listed here,
  # so this will just spit out the resource data for the Asian Womens Shelter
  class AsianWomensShelter
    # DATA = <<-ADDRESS
    #     Asian Women's Shelter
    #     3543 18th Street # 19
    #     San Francisco, CA 94110

    #     Business Line: (415) 751-7110
    #     Fax: (415) 751-0806
    #     info@sfaws.org
    # ADDRESS 

    def self.parse
      {
        organization: {
          name: "Asian Women's Shelter",
          urls: ["http://www.sfaws.org"]
        },
        location: {
          address: {
            street: "3543 18th Street # 19",
            city: "San Francisco",
            state: "CA",
            zip: 94110
          },
          name: "Asian Women's Shelter",
          emails: ["info@sfaws.org"],
          phones: [
            {number: "(415) 751-7110"}
          ],
          faxes: [
            {number: "(415) 751-0806"}
          ]
        },
        description: "Services include our nationally recognized shelter program, language advocacy program, crisis line, case management, and programs in support of underserved communities such as queer Asian survivors and trafficked survivors. Women's Program",
        short_description: "Shelter program, language advocacy program, crisis line, case management"
      }.to_json
    end
  end
end

Parser.run()