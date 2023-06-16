from pathlib import Path
import os
#import warnings
#warnings.filterwarnings('ignore')
pathlib = str(Path(__file__).parent.parent.resolve())
workspace = os.path.join(pathlib, "workspace")

import shutil
import time


def run():

    if not os.path.exists(os.path.join(workspace, 'EDA')):
        print(f"Create EDA folder under {workspace}")
        os.mkdir(os.path.join(workspace, 'EDA'))
       
    if not os.path.exists(os.path.join(workspace, 'interactive_notebook.ipynb')):
        shutil.copyfile(
            os.path.join(pathlib, 'assets', 'interactive_notebook.ipynb'), 
            os.path.join(workspace, 'interactive_notebook.ipynb'))
        
    if not os.path.exists(os.path.join(workspace, 'recdp_autofe_overview.jpg')):
        shutil.copyfile(
            os.path.join(pathlib, 'assets', 'recdp_autofe_overview.jpg'), 
            os.path.join(workspace, 'recdp_autofe_overview.jpg'))
    print(f"Copied interactive_notebook to {workspace}")
    
    retry = True
    while retry:
        time.sleep(3)
        try:
            os.makedirs('/root/.ipython/profile_default/startup/', exist_ok=True)
            shutil.copyfile(
                os.path.join(pathlib, 'src', 'startup.py'), 
                os.path.join('/root/.ipython/profile_default/startup/', 'startup.py'))            
            retry = False
        except:
            retry = True
    print(f"Copied startup.py")
        
    
if __name__ == "__main__":
    run()
