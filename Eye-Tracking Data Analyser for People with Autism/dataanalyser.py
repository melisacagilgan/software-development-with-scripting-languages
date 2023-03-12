import matplotlib.pyplot as plt
import copy
import sys


def menu():
    option = 0
    choices = {1: 'Total number of people',
               2: 'Total time viewed', 3: 'Total number of fixations'}
    while(option != 3):
        option = int(input("1. Compare the total number of people, the total time viewed, and the total number of fixations for people with and without autism for a particular element on an image\n"
                           "2. Compare the total number of people, the total time viewed, and the total number of fixations for people with and without autism on an image\n"
                           "3. Exit\n"
                           "Please enter your option: "))
        if option < 1 or option > 3:
            print("Invalid option! Please try again.")
        else:
            file_dict = read_files(sys.argv[1], sys.argv[2])

            if option == 1:
                letter = input(
                    "Please enter an element to be compared: ").upper()
                while(letter not in file_dict.keys()):
                    print("Invalid option! Please try again.")
                    letter = input(
                        "Please enter element to be compared: ").upper()

                choice = int(input("1. Compare total number of people\n"
                                   "2. Compare total time viewed\n"
                                   "3. Compare Total number of fixations\n"
                                   "Please enter your option: "))
                while(choice not in choices.keys()):
                    print("Invalid option! Please try again.")
                    choice = int(input("1. Compare total number of people\n"
                                       "2. Compare total time viewed\n"
                                       "3. Compare Total number of fixations\n"
                                       "Please enter your option: "))

                plot_graph_with_element(file_dict, letter, choices[choice])

            elif option == 2:
                choice = int(input("1. Compare total number of people\n"
                                   "2. Compare total time viewed\n"
                                   "3. Compare Total number of fixations\n"
                                   "Please enter your option: "))
                while(choice not in choices.keys()):
                    print("Invalid option! Please try again.")
                    choice = int(input("1. Compare total number of people\n"
                                       "2. Compare total time viewed\n"
                                       "3. Compare Total number of fixations\n"
                                       "Please enter your option: "))

                plot_whole_data(file_dict, choices[choice])

    print("Goodbye!")


# Create a dictionary to store the top-left and bottom-right coordinates of each fixation
def create_segments(img_x, img_y, rows, columns):
    x_step = img_x / columns
    y_step = img_y / rows
    segmentations = {}
    for i in range(rows*columns):
        segmentations[chr(65+i)] = [int(i % columns * x_step), int(
            i // columns * y_step), int((i % columns + 1) * x_step), int((i // columns + 1) * y_step)]
    return segmentations


# Create a dictionary of asd and control files
def create_dict(x, y):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
               'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
    asd_dict = {'Total number of people': 0,
                'Total time viewed': 0, 'Total number of fixations': 0}
    ctrl_dict = {'Total number of people': 0,
                 'Total time viewed': 0, 'Total number of fixations': 0}
    file_dict = {}
    for i in range(x*y):
        file_dict[letters[i]] = {'ASD': copy.deepcopy(
            asd_dict), 'CONTROL': copy.deepcopy(ctrl_dict)}
    return list(file_dict.keys()), file_dict


# Update the dictionary with the data from the file
def update_dict(asd_line, user_fixations, segmentations, file_dict, letters, type):
    Idx = int(asd_line[0])
    x_coord = int(asd_line[1])
    y_coord = int(asd_line[2])
    duration = int(asd_line[3])

    if Idx == 0:
        user_fixations.clear()

    for (i, coords) in enumerate(segmentations.values()):
        if x_coord >= coords[0] and x_coord < coords[2] and y_coord >= coords[1] and y_coord < coords[3]:
            file_dict[(letters[i])][type]['Total number of fixations'] += 1
            file_dict[(letters[i])][type]['Total time viewed'] += duration

            if letters[i] not in user_fixations:
                user_fixations.append(letters[i])
                file_dict[(letters[i])
                          ][type]['Total number of people'] += 1
    return file_dict


# Read the files and store the data in a dictionary
def read_files(asd_filename, ctrl_filename):
    # Get the image dimensions
    img = sys.argv[3].split('x')
    img_x = int(img[0])
    img_y = int(img[1])

    asd_user_fixations = []
    ctrl_user_fixations = []

    # Get the grid dimensions
    grids = sys.argv[4].split('x')
    grid_x = int(grids[0])
    grid_y = int(grids[1])
    try:
        with open(asd_filename, 'r') as asd_file, open(ctrl_filename, 'r') as ctrl_file:
            for (asd_i, asd_line), ctrl_line in zip(enumerate(asd_file), ctrl_file):
                asd_line = asd_line.split(',')
                ctrl_line = ctrl_line.split(',')
                if asd_i == 0:
                    letters, file_dict = create_dict(grid_x, grid_y)
                    segmentations = create_segments(
                        img_x, img_y, grid_x, grid_y)
                else:
                    file_dict = update_dict(asd_line, asd_user_fixations,
                                            segmentations, file_dict, letters, 'ASD')
                    file_dict = update_dict(
                        ctrl_line, ctrl_user_fixations, segmentations, file_dict, letters, 'CONTROL')
    except FileNotFoundError:
        print("File not found!")
        sys.exit(1)

    return file_dict


# Plot a graph of the specified fixation's data for a specific statistics type
def plot_graph_with_element(file_dict, letter, choice):

    groups = ["People with Autism", "People Without Autism"]

    values = [file_dict[letter]['ASD'][choice],
              file_dict[letter]['CONTROL'][choice]]
    plt.bar(groups, values)
    plt.xlabel('Groups')
    plt.ylabel(choice)
    plt.title(
        'Comparison Between People with & without Autism for Element ' + letter)
    plt.show()


# Plot a graph of all fixation's data for a specific statistics type
def plot_whole_data(file_dict, choice):
    asd = 0
    ctrl = 0
    for letter in file_dict.keys():
        asd += file_dict[letter]['ASD'][choice]

    for letter in file_dict.keys():
        ctrl += file_dict[letter]['CONTROL'][choice]

    groups = ["People with Autism", "People Without Autism"]
    values = [asd, ctrl]
    plt.bar(groups, values)
    plt.xlabel('Groups')
    plt.ylabel(choice)
    plt.title('Comparison Between People with & without Autism for all elements')
    plt.show()


# Main function
def main():
    menu()


if __name__ == "__main__":
    main()
