# NOTE: for some reason the single line "I get it now!" in data/text/birch_speech.inc is not replaced??


import os
import re

progress = {}

j = 0

script_dir = os.path.dirname(__file__)

folder_path_a = os.path.join("..", "pokeemerald-master-translated") + os.sep # output folder
folder_path_b = os.path.join(".", "text") + os.sep                           # input folder

#print(folder_path_a, folder_path_b)

def extract_quoted_text(line):
    # Find the indices of the first and second quotation marks
    number = line.find(":")
    first_quote_index = line.find('"')
    second_quote_index = line.find('"', first_quote_index + 1)
    if first_quote_index != -1 and second_quote_index != -1 and number != -1:
        # Extract the text between the first and second quotation marks
        return (int(line[:number]), line[first_quote_index + 1:second_quote_index])
    else:
        return (-1, "")  # Return empty string if no quoted text found

    
def replace_quoted_text(line, text):
    first_quote_index = line.find('"')
    second_quote_index = line.find('"', first_quote_index + 1)

    return line[:first_quote_index+1] + text + line[second_quote_index:]


print("Starting Insertion!")

try :
    for root, _, files in os.walk(folder_path_b):
        for file in files:
            file_path = os.path.join(root, file)
            myfile_path = file_path[len(folder_path_b):]

            # figure out file ending
            file_path_base = os.path.join(folder_path_a, myfile_path) 

            end_index = file_path_base.rfind(".")
            file_index = file_path_base.rfind(os.sep)

            mylist = os.listdir(file_path_base[:file_index])
            r = re.compile(file_path_base[file_index+1:end_index+1] + "*")
            myfile = list(filter(r.match, mylist))[0]

            if myfile.rfind(".") == -1 and "maps" in myfile_path:
                myfile = os.path.join(myfile, "scripts.inc")

            file_path_base = os.path.join(file_path_base[:file_index], myfile)

            empty = " "
            print(f"================= {(myfile_path + ' '):=<70}")

            if "ipynb" not in myfile_path:
                with open(file_path_base, 'r', encoding='utf-8') as input_file:
                    content = [line for line in input_file.readlines()]

                with open(file_path, 'r', encoding='utf-8') as input_file:
                    new_content = [extract_quoted_text(line) for line in input_file.readlines()]
                    new_content = [c for c in new_content if c[0] != -1]

                    j+=1
                    for i, t in new_content:
                        n = i-1
                        if j < 0:
                            print(i, "a: " + content[n].replace("\n", ""), "b: " + t.replace("\n", ""))
                            print(replace_quoted_text(content[n], t))
                        content[n] = replace_quoted_text(content[n], t)


                    #print("\n\n")

                    #if i < 30:
                    #    print(f"================= {myfile_path} =================")
                    #    print("\n".join([f"{c[0]}: {c[1]}" for c in content]),"\n\n")


                with open(file_path_base, 'w', encoding='utf-8') as output_file:
                    #if "Littleroot" in myfile_path:
                    #    print("".join(content))
                    output_file.write("".join(content))
    
except Exception as e:
    print(e)
    
print("Insertion Done!")