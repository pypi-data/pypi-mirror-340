
"""
Contains system specifc information. At the Moment, this is all hard-coded.
In the future, this will be part of the installation of AIzymes.

set_system() contains general variables.
submit_head() constructs the submission header to submit jobs.

"""

import sys
import os
import getpass

def set_system(self):
    
    if self.SYSTEM == 'GRID':       
        
        self.rosetta_ext          = "linuxgccrelease"
        self.bash_args            = ""
        self.ROSETTA_PATH         = "/home/bunzelh/rosetta_src_2021.16.61629_bundle/main/source/"
        self.FIELD_TOOLS          = f'{self.FOLDER_HOME}/../../../src/FieldTools.py'
        self.FOLDER_ProteinMPNN   = f'{os.path.expanduser("~")}/ProteinMPNN'
        self.FOLDER_ProteinMPNN_h = f'{os.path.expanduser("~")}/ProteinMPNN/helper_scripts'
            
    elif self.SYSTEM == 'GRID_parallel':       
        
        self.rosetta_ext          = "linuxgccrelease"
        self.bash_args            = ""
        self.ROSETTA_PATH         = "/home/bunzelh/rosetta_src_2021.16.61629_bundle/main/source/"
        self.FIELD_TOOLS          = f'{self.FOLDER_HOME}/../../../src/FieldTools.py'
        self.FOLDER_ProteinMPNN   = f'{os.path.expanduser("~")}/ProteinMPNN'
        self.FOLDER_ProteinMPNN_h = f'{os.path.expanduser("~")}/ProteinMPNN/helper_scripts'
        
    elif self.SYSTEM == 'SCC':       
        
        self.rosetta_ext          = "linuxgccrelease"
        self.bash_args            = ""
        self.ROSETTA_PATH         = "/scratch-scc/projects/scc_mmtm_bunzel/rosetta.source.release-371/main/source/"
        self.FIELD_TOOLS          = f'{self.FOLDER_HOME}/../../../src/FieldTools.py'
        self.FOLDER_ProteinMPNN   = f'{os.path.expanduser("~")}/ProteinMPNN'
        self.FOLDER_ProteinMPNN_h = f'{os.path.expanduser("~")}/ProteinMPNN/helper_scripts'  
        
    elif self.SYSTEM == 'RAVEN':       
        
        self.rosetta_ext          = "linuxgccrelease"
        self.bash_args            = ""
        self.ROSETTA_PATH         = f"/u/bunzela/bin/rosetta.source.release-371/main/source/"
        self.FIELD_TOOLS          = f'/u/{getpass.getuser()}/bin/AIzymes_dev/src/FieldTools.py'
        self.FOLDER_ProteinMPNN   = f'/u/{getpass.getuser()}/bin/ProteinMPNN'
        self.FOLDER_ProteinMPNN_h = f'/u/{getpass.getuser()}/bin/ProteinMPNN/helper_scripts'
        self.FOLDER_LigandMPNN    = f'/u/{getpass.getuser()}/bin/LigandMPNN'
                
    elif self.SYSTEM == 'BLUEPEBBLE':     
        
        self.rosetta_ext          = "linuxgccrelease"
        self.bash_args            = ""
        self.ROSETTA_PATH         = "/user/work/qz22231/rosetta.source.release-371/main/source"
        self.FIELD_TOOLS          = "/user/work/qz22231/AIzymes/AIzymes_git/AIzymes/src/FieldTools.py" #'../../../src/FieldTools.py'
        self.FOLDER_ProteinMPNN   = "/user/work/qz22231/ProteinMPNN"
        self.FOLDER_ProteinMPNN_h = "/user/work/qz22231/ProteinMPNN/helper_scripts"
        self.BLUEPEBBLE_ACCOUNT   = "ptch000721"
                
    elif self.SYSTEM == 'ABBIE_LOCAL':    
        
        self.rosetta_ext          = "linuxgccrelease"
        self.bash_args            = "OMP_NUM_THREADS=1 "
        self.ROSETTA_PATH         = "ERROR! NOT YET CONFIGURED"
        self.FIELD_TOOLS          = f'{self.FOLDER_HOME}/../../../src/FieldTools.py'
        self.SUBMIT_HEAD          = ""
        self.FOLDER_ProteinMPNN   = f'{os.path.expanduser("~")}/ProteinMPNN'
        self.FOLDER_ProteinMPNN_h = f'{os.path.expanduser("~")}/ProteinMPNN/helper_scripts'
        
    else:

        print(f"{self.SYSTEM} not defined in set_system(self), located in setup_system.py.")
        sys.exit()
        
def submit_head(self, index, job, ram):

    # Note: All RUN_INTERACTIVE jobs are also RUN_PARALLEL jobs!
    if self.RUN_PARALLEL == True:
        
        return ""
            
    elif self.SYSTEM == 'GRID': 

        return f"""#!/bin/bash
#$ -V
#$ -cwd
#$ -N {self.SUBMIT_PREFIX}_{job}_{index}
#$ -hard -l mf={ram}G
#$ -o {self.FOLDER_HOME}/{index}/scripts/{job}_{index}.out
#$ -e {self.FOLDER_HOME}/{index}/scripts/{job}_{index}.err
"""         
          
    elif self.SYSTEM == 'BLUEPEBBLE':     
        
        return f"""#!/bin/bash
#SBATCH --account={self.BLUEPEBBLE_ACCOUNT}
#SBATCH --partition=short
#SBATCH --mem=40GB
#SBATCH --ntasks-per-node=1
#SBATCH --time=2:00:00    
#SBATCH --nodes=1          
#SBATCH --job-name={self.SUBMIT_PREFIX}_{job}_{index}
#SBATCH --output={self.FOLDER_HOME}/{index}/scripts/AI_{job}_{index}.out
#SBATCH --error={self.FOLDER_HOME}/{index}/scripts/AI_{job}_{index}.err
"""    
        
    else:

        print(f"{self.SYSTEM} not yet setup for submission of jobs! Please adjust submit_head(), which is part of setup_system.py!")
        sys.exit()
