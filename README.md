# Sentiment text analysis using lexical resources

- Folder util:
    - parser.py - contains functions for parsing film reviews from corpuses
    - loader.py - contains functions for loading resources
    - converter.py - contains functions for converting
    - serbian_stemmer.py - https://github.com/nikolamilosevic86/SerbianStemmer
    - wordnet_helper.py - class for manipulating data from wordnet (english and serbian)
    - constants.py - contains string constants for rating documents
- Folder entity:
    - word.py - class for representing word
    - sentence.py - class for representing sentence
    - text.py - class for representing text
- Folder tests:
    - contains tests for functions in project
- main.py - main file
- Pdf document - LaTeX project: https://www.overleaf.com/read/syksdbwjhndc

    
## Input data:
- Download all input data and locate them in folder src/input_data:
    - Serbian corpus - film reviews: https://github.com/vukbatanovic/SerbMR, 
    - English corpus - film reviews: http://www.cs.cornell.edu/people/pabo/movie-review-data/review_polarity.tar.gz
    
## Libraries:
- re
- pathlib
- csv
- os
- chardet
- nltk
- transliterate
- pandas
- xml


## References:

- Manning, Christopher D., and Hinrich Schütze. Foundations of statistical natural language processing.
Vol. 999. Cambridge: MIT press, 1999.
- Bird, S., Klein, E., & Loper, E. Natural language processing with Python: analyzing text with
the natural language toolkit. " O'Reilly Media, Inc.". 2009. (http://www.nltk.org/book/)
- Denecke, Kerstin. Using SentiWordnet for multilingual sentiment analysis. Data Engineering
Workshop, 2008. ICDEW 2008. IEEE 24th International Conference on. IEEE, 2008.
