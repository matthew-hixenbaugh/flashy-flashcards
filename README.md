## flashy-flashcards
simple flashcard app for german vocab


./data/german_words.csv is the vocab input with columns: German,English,Score

if the Score column does not exist, it will be created


# importing your own language .csv
    
-change DATA_PATH to the location of your new .csv

-change LANGUAGE to the name of your first column, ex. Something,English,Score => LANGUAGE = "Something"
    


output file "to_learn.csv" contains all words in which your score is lower than your median score
