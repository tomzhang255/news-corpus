# make dir in Lab/ if not exists to store results for curr dic
FOLDER_NAME=$(pwd | awk -F/ '{print $NF}')
eval mkdir -p "/n/henrich_lab/Lab/${FOLDER_NAME}"

sbatch dic0.sh
sbatch dic1.sh
sbatch dic2.sh
sbatch dic3.sh
sbatch dic4.sh
sbatch dic5.sh
sbatch dic6a.sh
sbatch dic6b.sh
sbatch dic7a.sh
sbatch dic7b.sh
sbatch dic8.sh
sbatch dic9.sh
sbatch dic10.sh
sbatch dic11.sh
