# README: Training a Word2vec Model on the News Corpus

## Introduction

`train.py` trains a word2vec model with the post-OCR error corrected corpus. Note that the corpus is now separated into several smaller chunks, so we are training the model sequentially for each chunk and creating checkpoints along the way by saving the most up-to-date model after training on each chunk. To not waste too much storage space, only 2 of the most recent models are present at any given time; we also keep updating a file of the list of corpus files we already processed so that if the batch job fails due to time out, we can simply resubmit the job.

## Execution

- directory notes
    - the post-OCR error corrected corpus is split in several chunks in `/n/henrich_lab/Lab/ocr/` (this is our training data)
    - all outputs of the training process will end of in  `/n/henrich_lab/Lab/word2vec/`
        - `/n/henrich_lab/Lab/word2vec/processed_files.txt` keeps track of which chunks have already been successfully trained
        - `/n/henrich_lab/Lab/word2vec/checkpoints/` store 2 of the most recent models
    - make sure directory `/n/henrich_lab/Lab/word2vec/sbatch_log/` exists before submitting the batch job; this is where the log files of the batch scripts will end up at
- start training
    - submit batch job with `sbatch train.sh`
- on failure
    - E.g., job time out (as the `serial_requeue` partition of the HPC has a 7-day max limit for any job)
    - simply re-submit the job
    - there's no need to modify the `train.py` on failure as the script is smart enough to pick up from the appropriate place based on `processed_files.txt`
    - if the error is other than job-time-out, debug the chunk where the error occurred. Reference sbatch logs.
