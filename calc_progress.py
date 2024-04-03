import os
import re

progress = {}

pattern = r"\d+:[ ]+\""

folder_path = f".{os.sep}text{os.sep}"

#extract file progress
for root, _, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        myfile_path = file_path[len(folder_path):]
        
        if "ipynb" not in myfile_path:
            with open(file_path, 'r', encoding='utf-8') as input_file:
                content = [line for line in input_file.readlines()]
                # Matches digits followed by a colon and a double quote

                if "      |=======================================|" in content[0]:
                    content = content[1:]
                
                if myfile_path[:4] == "data": 
                    count = sum(1 for line in content if re.match(pattern, line))

                elif myfile_path[:3] == "src":
                    count = 0

                progress[myfile_path] = (len(content), count)
            
            
updated_progress = {f".{os.sep}" + key.replace('_', os.sep): value for key, value in progress.items()}
branch_sums = updated_progress.copy()

# add file progress backwards up the folders
for path, value in updated_progress.items():
    # Split the path into its components (folders)
    folders = path.split(os.sep)
    # Initialize the current branch path
    branch_path = ''
        
    for i, folder in enumerate(folders[:-1]):  # Exclude the file name at the end
        # Update the current branch path
        if i == 0:
            branch_path += folder
        else:
            branch_path += os.sep + folder
            
        #branch_path = '\\'.join([branch_path, folder]) #[1:]
        # Add the value to the sum for the current branch
        if branch_path not in branch_sums:
            branch_sums[branch_path] = (0, 0)

        #branch_file_counts[branch_path] = branch_file_counts.get(branch_path, 0) + 1
        branch_sums[branch_path] = (branch_sums[branch_path][0] + value[0], branch_sums[branch_path][1] + value[1])


# take care of special case
for path, value in updated_progress.items():
    # Split the path into its components (folders)
    folders = path.split(os.sep)
    # Initialize the current branch path
    branch_path = ''
        
    for i, folder in enumerate(folders): 
        # Update the current branch path
        if i == 0:
            branch_path += folder
        else:
            branch_path += os.sep + folder
            

    if branch_path[:-4] in branch_sums:
        branch_sums[branch_path[:-4]] = (branch_sums[branch_path[:-4]][0] + value[0], branch_sums[branch_path[:-4]][1] + value[1])
        


branch_sums = dict(sorted(branch_sums.items()))


progresslist = list(progress.keys())
progressreplace = [p.replace("_", os.sep) for p in progresslist]

def generate_collapsible_md(file_paths):
    structure = {}

    # Build the folder structure
    for path, val in file_paths.items():
        if path == "." or ".ipynb" in path:
            continue
        
        components = path[2:].split(os.sep)
        #print(path, components)
        current_level = structure
        
        for i, component in enumerate(components[:-1]):
            if component not in current_level:
                current_level[component] = {}
             
            current_level = current_level[component]
        
        
        if "." in components[-1]:
            if components[-1][:-4] in current_level:
                current_level[components[-1][:-4]][components[-1]] = val

            else:
                current_level[components[-1]] = val
        
        else:
            current_level[components[-1]] = {}

        #print(structure)
            
    # Generate markdown
    markdown = ""
    def generate_md(structure, path=".", depth=2):
        nonlocal markdown
        for folder, contents in structure.items():
            #print(branch_sums[path])
            
            mydir = path + os.sep + folder
            
            if mydir in branch_sums:
                val = branch_sums[mydir]
                
            else:
                val = contents
                
            
            searchdir = mydir
            splitdir = searchdir.split(os.sep)
            if len(splitdir) > 1 and splitdir[-1][:-4] == splitdir[-2]:
                searchdir = os.sep.join([i for i in splitdir if i != splitdir[-2]])
                #print(searchdir)
            
            found = True
            if searchdir not in progress:
                found = False
                for i, s in enumerate(progressreplace): 
                    if searchdir[2:] in s and (searchdir[2:]==s or progresslist[i][len(searchdir)-2]==os.sep):
                        found = True
                        
                        # ???? why replace?
                        pathy = progresslist[i][:len(searchdir)-2].replace("\\", "/")
                        break
                
                if not found:
                    pass
                    #print("not found!!", mydir)
                    
            #mydir2 = mydir.replace("\\", "/")[2:]
            if found:
                pathy = f"<a href='text/{pathy}' class='internal-link'>{folder}</a>"
            else:
                pathy = folder

            if isinstance(contents, dict):        
                markdown += "\t" * (depth-2) + f"<div class='h_{depth}'> <h{depth} data-heading='{folder}'>{folder} {val}</h{depth}>\n"
                
                if found:
                    pass
                    #markdown += pathy
                    
                generate_md(contents, mydir, depth + 1)
                markdown += "\t" * (depth-2) + "</div>\n"
                
            else:
                markdown += "\t" * (depth-2) + f"<div class='h_{depth}'>{pathy} {val}</div>\n" #"\t" * (depth + 1) + "No files" + "</details>\n"
    
    #print(structure)
    generate_md(structure)
    return markdown


file_header = "As of now, only the progress from files under data/ is being correctly calculated. \n\n ```(total number of lines, number of translated lines)```\n\n"

if __name__ == "__main__":
    try:
        file = open("progress.md", "w")
        file.write(file_header)
        file.write(generate_collapsible_md(branch_sums))
        file.close()
        
    except Exception as e:
        print(e)
    
    os.system("PAUSE")