# run this file seperately

from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy

TRAINING_DATA = [

            ('Who is Shaka Khan?', {
            
                'entities': [(7, 17, 'PERSON')]
            
            }),
    
            ('I Like Dallas and Moscow.', {
            
                'entities': [(7, 13, 'LOC'), (18, 24, 'LOC')]
                
            })


]

@plac.annotations(

        model = ("Model name. Defaults to blank - 'en' model.", "option", "m", str),
        output_dir = ("Optional output directory", "option", "o", path),
        n_iter = ("Number of training iterations", "option", "n", int))
def main(model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(modal) # load existing spaCy model
        print("Load model '%s'" % model)
    else:
        nlp = spacy.blank('en') # create blank Language class
        print("Created blank 'en' model")
        
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with Spacy

    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
     # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe('ner')

     # add labels 
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])
                
    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes): # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            
            for text, annotations in TRAIN_DATA:
                nlp.update(
                
                        [text], # batch of texts
                        [annotations] # batch of annotations
                        drop = 0.5 # dropout - make it harder to memorise data
                        sgd = optimizer # callable to update weights
                        losses = losses
                )
                
            print(losses)
            
    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
        print('Tokens', [(t.text, t.ent_type, t.ent_job) for t in doc])
        
        
        
if __name__ == '__main__':
    plac.call(main)
    
    # Expected output:
    # Entities [('Shaka Khan', 'PERSON')]
    # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
    # ('Khan', 'PERSON', 1), ('?', '', 2)]
    # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
    # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
    # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)]
             
            
     
       
        