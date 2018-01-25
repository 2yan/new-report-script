import os
from tkinter import filedialog
import json
import shutil
import glob
from pprint import pprint

def __init_config():
    print('No Config Found: Where are your reports stored?')
    
    report_folder = filedialog.askdirectory(title = 'Where are your reports stored?')

    config = {
            'report_folder':report_folder,
            }
    
    with open('config.txt', 'w') as outfile:
        json.dump(config, outfile)
    print('Setting Report Location as {}'.format(report_folder))
    
    return config

def load_config():
    try:
        with open('config.txt') as infile:
            config = json.load(infile)
    except FileNotFoundError:
        config = __init_config()
    
    if not os.path.isdir('copy files'):
        os.mkdir('copy files')
        filenames = filedialog.askopenfilenames()
        for filename in filenames: 
            shutil.copy(filename, 'copy files')
            
    return config


def report_for(config):
    report_folder = config['report_folder']

    people = next(os.walk(report_folder))[1]

    options = dict(zip(range(len(people)), people))
    pprint(options)
    selection = input('''Which Person will this report go to ?\n If this is for a new person,
                      just type their name.\n\n <NUMBER OR NEW NAME HERE>:''')
    try:
        selection = int(selection)
    except ValueError:
        os.mkdir(report_folder +'/' + selection)
        return report_folder + '/' + selection
    
    try:
        person = options[selection]
    except KeyError:
        print('Sorry That number does not exist in the options, try again:')
        return False
    return report_folder + '/' + person 

def get_report_name(person):
    report_name = input('What is the New reports name? \n\n <NAME HERE>:' )
    try:
        os.mkdir(person + '/' + report_name)
    except FileExistsError:
        pass
    return person + '/' + report_name

config = load_config()
name = report_for(config)
while name == False:
    name = report_for(config) 

report_name = get_report_name(name)

for file in glob.glob('copy files/*.*'):
    shutil.copy(file, report_name)

input('Done! > Press Enter to Continue')
