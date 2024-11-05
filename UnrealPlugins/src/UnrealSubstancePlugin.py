import tkinter.filedialog
from unreal import ToolMenuContext, ToolMenus, ToolMenuEntryScript, uclass, ufunction
import sys
import os
import importlib
import tkinter

srcDir = os.path.dirname(os.path.abspath(__file__))
if srcDir not in sys.path:
    sys.path.append(srcDir)

import UnrealUtilities
importlib.reload(UnrealUtilities)

@uclass()
class LoadFromDirEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context):
        window = tkinter.Tk()
        window.withdraw()
        fileDir = tkinter.filedialog.askdirectory()
        window.destroy()
        UnrealUtilities.UnrealUtility().LoadFromDir(fileDir)


@uclass()
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context: ToolMenuContext) -> None:
        UnrealUtilities.UnrealUtility().FindOrCreateBaseMaterial()

class UnrealSubstancePlugin:
    def __init__(self):
        self.subMenuName="SubstancePlugin"
        self.subMenuLabel="Substance Plugin"
        self.InitUI()
    
    def InitUI(self):
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")
        self.subMenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "SubstancePlugin", "Substance Plugin",)
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript())
        self.AddEntryScript("LoadFromDir", "Load From Directory", LoadFromDirEntryScript())
        ToolMenus.get().refresh_all_widgets()

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):
        script.init_entry(self.subMenu.menu_name, self.subMenu.menu_name, "", name, label)
        script.register_menu_entry()

UnrealSubstancePlugin()