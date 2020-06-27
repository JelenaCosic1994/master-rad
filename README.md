# Sentiment text analysis using lexical resources

- Folder util:
    - loader.py - contains functions for loading resources
    - converter.py - contains functions for converting
    - wordnet_helper.py - class for manipulating data from wordnet (english and serbian)
    - classifier_helper.py - file for creating model for svm classifier
    - constants.py - contains string constants for rating documents
- Folder tests:
    - contains tests for functions in project
- Folder results:
    - contains results  
- main.py - main file
- Pdf document - LaTeX project: https://www.overleaf.com/read/tncvwrbzmdbc

    
## Input data:
- Download all input data and locate them in folder src/input_data:
    - Serbian corpus (3 classes) - film reviews: https://github.com/vukbatanovic/SerbMR (SerbMR-3C - csv format),
        - positive (841), negative (841) and neutral (841) reviews
    - Serbian corpus (2 classes) - film reviews: https://github.com/vukbatanovic/SerbMR (SerbMR-2C - csv format),
        - positive (841) and negative (841) reviews
    - English corpus - film reviews: http://www.cs.cornell.edu/people/pabo/movie-review-data/review_polarity.tar.gz
        - positive (1000) and negative (1000) reviews
    
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
- string
- sklearn
- numpy
- unittest

## Results:
- Unsupervised:
    - English corpus (2 classes):
        - precision: 58.11%, recall: 85.20%, f measure: 69.09%, accuracy: 61.90%
    - Serbian corpus (2 classes):
        - precision: 53.98%, recall: 82.97%, f measure: 65.42%, accuracy: 56.12%
    - Serbian corpus (3 classes):
        - precision: 39.03%, recall: 36.31% f measure: 32,46%, accuracy: 57.54%

- Supervised:
    - English corpus (2 classes):
        - precision: 76.50%, recall: 75.50%, f measure: 75.50%, accuracy: 76.00%
    - Serbian corpus (2 classes):
        - precision: 67%, recall: 67%, f measure: 67%, accuracy: 67%
    - Serbian corpus (3 classes):
        - precision: 49%, recall: 49%, f measure: 49%, accuracy: 48.60%
        
## References:
- Manning, Christopher D., and Hinrich Schütze. Foundations of statistical natural language processing.
Vol. 999. Cambridge: MIT press, 1999.
- Bird, S., Klein, E., & Loper, E. Natural language processing with Python: analyzing text with
the natural language toolkit. " O'Reilly Media, Inc.". 2009. (http://www.nltk.org/book/)
- Denecke, Kerstin. Using SentiWordnet for multilingual sentiment analysis. Data Engineering
Workshop, 2008. ICDEW 2008. IEEE 24th International Conference on. IEEE, 2008.
