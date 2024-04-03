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


def find_path(file_path):
    i = file_path.rfind("\\")
    return file_path[:i]


def make_txt(file_path):
    i = file_path.rfind(".")
    return file_path[:i] + ".txt"

def combine_files(folder_path, output_folder, nojson=True):
    # Iterate through all files and subdirectories in the specified folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            #print(root, file)
            # Construct the full path to each file
            file_path = os.path.join(root, file)
            if  (".aif" not in file_path and
                ".mid" not in file_path and
                ".pcm" not in file_path and 
                ".gba" not in file_path and 
                ".png" not in file_path and 
                ".bin" not in file_path and 
                ".json" not in file_path and nojson):
                    
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
                            try:
                                myfile_path = file_path[len(folder_path)+1:]
                                output_path = make_txt(os.path.join(output_folder, myfile_path))
                                if not os.path.exists(find_path(output_path)):
                                    os.makedirs(find_path(output_path))

                                with open(output_path, 'w', encoding='utf-8') as output:
                                    content = "\n".join(content)
                                    output.write(content)
                            except Exception as e:
                                print(f"Error writing file {file_path}: {e}")
                                
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")


# I am pretty sure we only need the data/ and src/ folders, but you can extract also just extract everything 
# 1. Download the Pokemon Emerald Decompilation Project
# 2. Replace the filepaths below                  
combine_files("..\\pokeemerald-master", "..\\text-base")