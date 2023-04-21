# this script trains a word2vec model with the post-OCR error corrected corpus;
# note that the corpus is now separated into several smaller chunks;
# so we are training the model sequentially for each chunk and creating checkpoints along the way
# by saving the most up-to-date model after training on each chunk;
# to not waste too much storage space, only 2 of the most recent models are present at any given time;
# we also keep updating a file of the list of corpus files we already processed
# so that if the batch job fails due to time out, we can simply resubmit the job


import os
import re
from gc import collect
from datetime import datetime

import pandas as pd
import nltk
from gensim.models import Word2Vec


def log(msg):
    print(f'{datetime.now()} | {msg}\n')


def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    # Remove non-alphanumeric characters
    text = re.sub(r'\W+', ' ', text)
    # Tokenize the text
    words = nltk.word_tokenize(text)
    
    return words


def train_word2vec_model(sentences, model=None):
    # Cold start
    if model is None:
        # Initialize a new Word2Vec model
        model = Word2Vec(vector_size=100,  # google uses 300 but 100 is okay
                         window=4,  # (5-10 is the convention)
                         min_count=1,  # TODO 50 (because corpus is huge)
                         workers=1)  # TODO 64 (for parallel)
        # Build the vocabulary
        model.build_vocab(sentences)

    # If the model exists, update the vocabulary with new sentences
    else:
        model.build_vocab(sentences, update=True)

    # Train the Word2Vec model
    model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs)

    return model


def delete_oldest_model_files(model_dir, keep=2):
    model_files = [f for f in os.listdir(model_dir) if f.endswith('.model')]
    model_files.sort(key=lambda x: os.path.getmtime(os.path.join(model_dir, x)))

    # Delete the oldest model files, keeping only the specified number of most recent files
    for model_file in model_files[:-keep]:
        file_path = os.path.join(model_dir, model_file)
        os.remove(file_path)
        log(f"Deleted old model file: {file_path}")


if __name__ == '__main__':
    # Results directory (public)
    results_directory = '/n/henrich_lab/Lab/word2vec/'

    # Create checkpoints directory if not exists
    checkpoints_directory = f'{results_directory}checkpoints/'
    if not os.path.exists(checkpoints_directory):
        os.makedirs(checkpoints_directory)

    # Identify training data file names
    # corpus_folder_path = 'test_data/'
    corpus_folder_path = '/n/henrich_lab/Lab/ocr/'
    all_files = next(os.walk(corpus_folder_path), (None, None, []))[2]  # [] if no file
    corpus_files = list(filter(lambda f: f.startswith('ocr'), all_files))
    log(f'Listing all corpus files:\n\n{corpus_files}\n\n====================\n')

    # Ignore the processed files (if any)
    try:
        with open(f'{results_directory}processed_files.txt') as f:
            processed_files = f.readlines()
    except FileNotFoundError:
        processed_files = []
    processed_files = [name[:-1] for name in processed_files]  # remove \n at the end
    unprocessed_files = [x for x in corpus_files if x not in processed_files]

    # Iterate over the files
    i = len(processed_files)  # if cold start i = 0, else i > 0
    for f in unprocessed_files:
        log(f"Processing file {i} (max index = {len(corpus_files) - 1}): {f}")
        df = pd.read_csv(f'{corpus_folder_path}{f}')

        # Preprocess the text
        df['text'] = df['text'].apply(preprocess_text)

        # Set the model file name and path for the current corpus file
        curr_mod_file_name = f'mod_{i}.model'
        curr_mod_path = os.path.join(checkpoints_directory, curr_mod_file_name)

        # Set the model file name and path for the previous corpus file
        prev_mod_file_name = f'mod_{i - 1}.model' if i > 0 else None
        prev_mod_path = os.path.join(checkpoints_directory, prev_mod_file_name) if prev_mod_file_name else None

        # Load the saved model from the previous iteration, if it exists
        word2vec_model = None
        if prev_mod_path and os.path.isfile(prev_mod_path):
            log(f"Loading existing model: {prev_mod_path}")
            word2vec_model = Word2Vec.load(prev_mod_path)

        # Train the Word2Vec model
        word2vec_model = train_word2vec_model(df['text'].tolist(), model=word2vec_model)

        # Save the model
        word2vec_model.save(curr_mod_path)
        log(f"Model saved at: {curr_mod_path}\n")

        # Delete the oldest model files, keeping only the 2 most recent files
        delete_oldest_model_files(checkpoints_directory)

        # Record the file we just finished processing
        with open(f'{results_directory}processed_files.txt', 'a') as f_handle:
            f_handle.write(f'{f}\n')

        # Release memory
        del df
        collect()

        i += 1

    log("All files processed.")
