import os
import random


def pick_random_files_from_each_directory(directory):
    selected_files = []

    # Iterate through each folder
    for root, dirs, files in os.walk(directory):
        if files:
            # Randomly decide how many files to select from this folder (between 1 and min(3, number of files))
            num_files_to_select = random.randint(1, min(3, len(files)))

            # Randomly pick that number of files from the current folder
            random_files = random.sample(files, num_files_to_select)

            # Add the selected files with their full path to the list
            for file in random_files:
                selected_files.append(os.path.join(root, file))

    return selected_files


# Specify the directory you want to iterate through
directory_path = 'dump'

# Get the randomly selected files from each directory
random_files = pick_random_files_from_each_directory(directory_path)

# Output the selected files
print("Randomly selected files from each directory:")
for file in random_files:
    print(file)