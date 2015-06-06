#!/usr/bin/ruby -w

require 'json'

file_name = ARGV.first.to_s
json = JSON.parse(File.open(file_name).read)

json.each do |program|
	program['notes'] = ''
end

# save results in a different file in case of errors. cp to preferred file after verification.
File.open("result-#{file_name}", 'w') do |f|
	f.puts JSON.generate(json)
end