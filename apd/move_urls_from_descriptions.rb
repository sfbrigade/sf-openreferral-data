#!/usr/bin/ruby -w

require 'json'

file_name = ARGV.first.to_s
json = JSON.parse(File.open(file_name).read)

json.each do |program|
	program_location = program['locations'].first
	websites = program_location['description'].match(/(www\.[-\w]+\.[a-z]*)\s*(www\.[-\w]+\.[a-z]*)?/).to_s
	program_location['urls'] = [websites] if program_location['urls'].first.empty?
	program_location['description'].sub! websites, ''
	program_location['services_attributes'].first['description'].sub! websites, ''
end

# save results in a different file in case of errors. cp to preferred file after verification.
File.open("result-#{file_name}", 'w') do |f|
	f.puts JSON.generate(json)
end