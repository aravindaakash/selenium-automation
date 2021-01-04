require 'fileutils'
home_path = Dir.home
source_location = "#{home_path}/Desktop"
destination_location = "#{home_path}/Documents"
destination_folder = "#{destination_location}/Desktop_files"

source_files = Dir.glob("#{source_location}/*")

Dir.mkdir(destination_folder) unless Dir.exist?(destination_folder)
errors_messages = []

source_files.each do |file|
    destination_type_folder = destination_folder
    unless File.directory?(file)
        file_type = file.split('.').last
        destination_type_folder = "#{destination_folder}/#{file_type}"
        Dir.mkdir(destination_type_folder) unless Dir.exist?(destination_type_folder)
    end
    begin
        FileUtils.mv(file, destination_type_folder)    
    rescue
        errors_messages << file
    end
end


puts "Successfully Cleared #{source_files.count-errors_messages.count} files"
puts "Failed to Cleared file(s) due to \n #{errors_messages.join("\n")}" if errors_messages.any?