import os

def extract_quoted_text(line):
    # Find the indices of the first and second quotation marks
    first_quote_index = line.find('"')
    second_quote_index = line.find('"', first_quote_index + 1)
    if first_quote_index != -1 and second_quote_index != -1:
        # Extract the text between the first and second quotation marks
        return line[first_quote_index + 1:second_quote_index]
    else:
        return ""  # Return empty string if no quoted text found


def combine_files(folder_path, output_file, nojson=True):
    with open(output_file, 'w', encoding='utf-8') as output:
        # Iterate through all files and subdirectories in the specified folder
        for root, _, files in os.walk(folder_path):
            for file in files:
                # Construct the full path to each file
                file_path = os.path.join(root, file)
                if ".bin" not in file_path and nojson and ".json" not in file_path:
                    try:
                        # Open each file and read its content
                        with open(file_path, 'r', encoding='utf-8') as input_file:
                            #content = input_file.read()
                            content = [line.strip().lstrip('\t') for line in input_file.readlines()]
                            content = [f"{i + 1}: {line}" for i, line in enumerate(content) if 
                                       line and 
                                       "\"" in line and 
                                       line.strip() and 
                                       "INCBIN_U" not in line 
                                       and not line.startswith((".incbin", ".section", ".include", '#include', '@', "//"))
                            ]
                            
                            #content = [ line for line in content]
                            
                            #content = [line for line in content if ]
                            
                            # Write the content to the output file
                            if len(content) > 0:
                                output.write("\n\n\n ========================================" + file_path + "======================================== \n\n\n")
                                content = "\n".join(content)
                                output.write(content)
                                output.write('\n')  # Add a newline between files for readability
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")


# 1. Download the Pokemon Emerald Decompilation Project
# 2. Replace the filepaths below
combine_files(".../pokeemerald-master/data", "output_data.txt")
combine_files(".../pokeemerald-master/src", "output_src.txt")
