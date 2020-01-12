# Sentiment text analysis using lexical resources

- Folder util:
    - loader.py - contains functions for loading resources
    - converter.py - contains functions for converting
    - serbian_stemmer.py - https://github.com/nikolamilosevic86/SerbianStemmer
    - wordnet_helper.py - class for manipulating data from wordnet (english and serbian)
    - classifier_helper.py - file for creating model for svm classifier
    - constants.py - contains string constants for rating documents
- Folder tests:
    - contains tests for functions in project
- main.py - main file
- Pdf document - LaTeX project: https://www.overleaf.com/read/syksdbwjhndc

    
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

## Results:
- Unsupervised:
    - Serbian corpus (2 classes):
        - precision: 53.56%, recall: 82.28%, f measure: 64.88%, accuracy: 55.47%
    - Serbian corpus (3 classes):
        - precision: 62.14%, recall: 95.25% f measure: 75.22%, accuracy: 62.61%
    - English corpus (2 classes):
        - precision: 57.02%, recall: 87.7%, f measure: 69.11%, accuracy: 60.8%
- Supervised:
    - English corpus (2 classes):
        - positive: precision: 77%, recall: 80%, f measure: 79%
        - negative: precision: 78%, recall: 74%, f measure: 76%
## References:
- Manning, Christopher D., and Hinrich Schütze. Foundations of statistical natural language processing.
Vol. 999. Cambridge: MIT press, 1999.
- Bird, S., Klein, E., & Loper, E. Natural language processing with Python: analyzing text with
the natural language toolkit. " O'Reilly Media, Inc.". 2009. (http://www.nltk.org/book/)
- Denecke, Kerstin. Using SentiWordnet for multilingual sentiment analysis. Data Engineering
Workshop, 2008. ICDEW 2008. IEEE 24th International Conference on. IEEE, 2008.
