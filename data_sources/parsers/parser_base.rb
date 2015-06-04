#
# Bootstrap for easy parser script running.
# To run: ruby parser_base.rb FILE [FILE] [FILE]...
# Parsers should implement the following API:
# - Parser.fetch_data
# - Parser.parse     ==> returns a ruby object
# - Parser.data_path ==> string, where the json file should be written to
#
require 'pp'
require 'json'

module Parser
  JSON_PATH = "../json_output/"
  def self.run
    files = ARGV[1] ? ARGV[1..-1] : Dir.glob('./*_parser.rb')
    files.each do |parser|
      puts "loading #{parser}"
      require_relative parser
    end

    parsers = Parser.constants.select {|klass| klass.to_s.end_with? 'Parser' }
    parsers.each do |klass_name|
      puts klass_name
      klass = Parser.const_get(klass_name).new
      klass.fetch
      data = klass.parse

      valid_data = data.select {|d| valid? d }
      pp valid_data
      warn "Some data was invalid, please check the output" unless valid_data.length == data.length
      write_json(data, klass_name)
    end
  end

  # required json fields, as defined at http://github.com
  def self.valid?(data)
    return false unless organization_valid? data["organization"]
    return false unless location_valid? data["location"]

    true
  end

  def self.organization_valid?(org_data)
    # needs to be cast into boolean
    !!(org_data and org_data.include? "name" and not org_data["name"].strip.empty?)
  end

  def self.location_valid?(loc_data)
    !!(
      loc_data and 
      loc_data.include? "address" and
      self.address_valid?(loc_data["address"]) and
      loc_data.include? "description" and
      loc_data.include? "name"
    )
  end

  def self.address_valid?(addr_data)
    !!(
      addr_data and
      addr_data.include? "street" and
      addr_data.include? "city" and
      addr_data.include? "state" and
      addr_data.include? "zip"
    )
  end

  def self.write_json(data, class_name)
    return unless data.length > 0
    # FileUtils.mkdir(JSON_PATH) unless File.exist? JSON_PATH
    puts "writing file"
    path = File.join(JSON_PATH, "#{class_name}.json")
    puts "... writing to #{path}"
    File.open(path, 'w') {|f| f << data.to_json }
  end
end

Parser.run