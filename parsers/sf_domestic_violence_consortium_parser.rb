# Parses data found from http://www.sfaws.org/about-us/contact-us.aspx
require 'json'
require 'typhoeus'
require 'nokogiri'

module Parser
  class SFDomesticViolenceConsortiumParser
    URL = "http://www.dvcpartners.org/index.php?option=com_content&view=article&id=46&Itemid=74"
    ADDRESS_REGEX = /\d+ \w*/
    PHONE_REGEX = /ph:/i
    FAX_REGEX = /fax:/i
    DESCRIPTION_REGEX = /.{45}/
    CITY_STATE_ZIP_REGEX = /[^,]+,[a-zA-Z\s]+\s+\d{5}/
      
    def fetch
      Typhoeus.get(URL).body
    end

    def address?(str)
      not ADDRESS_REGEX.match(str).nil?
    end

    def phone?(str)
      not PHONE_REGEX.match(str).nil?
    end

    def fax?(str)
      not FAX_REGEX.match(str).nil?
    end

    def description?(str)
      not DESCRIPTION_REGEX.match(str).nil?
    end

    def city_state_zip?(str)
      not CITY_STATE_ZIP_REGEX.match(str).nil?
    end

    def dom_nodes(html)
      Nokogiri::HTML(html).css("table.contentpaneopen").last.css('tr td')
    end

    def get_all_text_nodes(node)
      nodes = []
      node.children.each do |child|
        if child.children.length > 0
          nodes += get_all_text_nodes(child)
        end
        if child.text?
          nodes << child
        end
      end
      nodes
    end

    def transform(resource)
      data = {}
      organization = {
        "name" => resource.css('strong span:first-child').text.strip,
      }
      resource.css('a').each do |link|
        organization["urls"] = [link["href"]] unless link['href'].to_s.strip.empty?
      end

      street = phone = fax = description = city = state = zip = nil
      text_nodes = get_all_text_nodes(resource)
      text_nodes.map do |text_node|
        text = text_node.text.strip
        normalized_text = text.downcase

        case 
        when address?(normalized_text)
          street = text
        when phone?(normalized_text)
          phone = normalized_text.sub /ph:\s*/, ''
        when fax?(normalized_text)
          fax = normalized_text.sub /fax:\s*/, ''
        when description?(normalized_text)
          description = text
        when city_state_zip?(normalized_text)
          city_state_zip = text.split(',')
          city = city_state_zip.first
          state = city_state_zip.last.split(' ').first
          zip = city_state_zip.last.split(' ').last
        end
      end

      data["organization"] = organization

      location = {
        "address" => {
          "street" => street,
          "city" => city,
          "state" => state,
          "zip" => zip
        },
        "name" => organization["name"],
        "phones" => [
          {"number" => phone }
        ],
        "description" => description,
        "short_desc" => description.length > 200 ? description[0..195] + '...' : description
      }

      location["fax"] = [{"number" => fax}] unless fax.nil?
      data["location"] = location

      data
    end

    def parse
      html = fetch
      json_obj = []

      dom_nodes(html).each { |resource| json_obj << transform(resource) }
      json_obj
    end
  end
end
