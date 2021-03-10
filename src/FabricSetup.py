import pysimplegui as sg
import os
import json
import shutil

MCVersion = '1.16.5'
serverName = 'CSET-MC'
path = os.getcwd()

def folder_select():
    MCFolder = ''
    cancel = False
    layout = [[sg.T('Open Minecraft Folder')],[sg.FolderBrowse(target='MCFolder'), sg.In(key='MCFolder')], [sg.Ok(),sg.Button('Cancel'),sg.Button('Get Files')]]
    window = sg.Window(serverName + ' Setup', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):  # if user closes window or clicks cancel
            cancel = True
            break
        if event in (None, 'Get Files'):
            cancel = 'alt'
            break
        MCFolder = values['MCFolder']
        if event in (None, 'Ok'):
            break
    window.close()
    if not os.path.exists(MCFolder + '/launcher_profiles.json') and not cancel:
        popup_result('Incorrect Folder')
        MCFolder, cancel = folder_select()
    return MCFolder, cancel

def popup_result(result):
    layout = [[sg.T(result)], [sg.Ok()]]
    window = sg.Window(serverName + ' Setup', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Ok'):
            break
    window.close()
    
def get_files():
    layout = [[sg.T('Mods Folder')],[sg.FolderBrowse(target='modFolder'), sg.In(key='modFolder')], [sg.Ok()]]
    window = sg.Window(serverName + ' Setup', layout)
    while True:
        event, values = window.read()
        modFolder = values['modFolder']
        if event in (None, 'Ok'):
            break
    window.close()
    if modFolder == '':
        popup_result('No Folder Selected')
        modFolder = get_files()
    return modFolder

def installFabric(installDir):
    fabricJar = ''
    for i in os.listdir(path):
        if 'fabric-installer' in i:
            fabricJar = i
    os.system('java -jar fabric-installer-0.6.1.51.jar client -dir ' + installDir + ' -mcversion ' + MCVersion)

def copy_files(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        shutil.copyfile(s, d)

def get_json(folder):
    with open(folder + '/launcher_profiles.json') as f:
        data = json.load(f)
        f.close()
    return data

def main():
    MCFolder, cancel = folder_select()
    if cancel == 'alt':
        folder = get_files()
        copy_files(path + '/mods/', folder)
        popup_result('Copied Mods to ' + folder)
        return
    if cancel:
        return
    if not 'fabric-loader-' + MCVersion in get_json(MCFolder)['profiles']:
        installFabric(MCFolder)
    if 'gameDir' in get_json(MCFolder)['profiles']['fabric-loader-' + MCVersion]:
        MCFolder = get_json(MCFolder)['profiles']['fabric-loader-' + MCVersion]['gameDir']
    
    copy_files(path + '/mods/', MCFolder + '/mods/')
    
    popup_result('Done!')

main()