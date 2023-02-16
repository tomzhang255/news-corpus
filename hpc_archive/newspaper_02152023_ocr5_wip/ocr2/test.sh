#!/bin/bash
#SBATCH -p bigmem                          # Partition (queue)
#SBATCH --job-name=test                    # What to show in squeue
#SBATCH --mail-type=END,FAIL               # When to send mail (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=szhang1@g.harvard.edu  # Where to send mail
#SBATCH --mem=495gb                        # How much memory to request
#SBATCH --nodes=1                          # Minimum number of nodes allocated for this job
#SBATCH --cpus-per-task=64                 # Number of cores requested
#SBATCH --time=01:00:00                    # How long to run (hrs:min:sec)
#SBATCH --output=test%j.txt                 # Where to save the output


echo -n "STARTED JOB AT: "
date
echo ""

module load Anaconda3
python test.py

echo -n "FINISHED JOB AT: "
date
echo ""
