# Sentiment text analysis using lexical resources

- Folder parser:
    - parser.py - contains functions for parsing film reviews from corpuses
    - loader.py - contains functions for loading resources for parsing
- Folder stemmer:
    - stemmer.py - https://github.com/nikolamilosevic86/SerbianStemmer
- Folder tests:
    - contains tests for functions in project
- Pdf document - LaTeX project: https://www.overleaf.com/read/syksdbwjhndc

    
## Input data:
- Download all input data and locate them in folder src/input_data:
    - Corpus - film reviews: https://github.com/vukbatanovic/SerbMR, 
    - Stop words: https://drive.google.com/file/d/1tDSfweQkpWcatid1ykOQCJzRH26nZfnb/view?usp=sharing

## Libraries:
- re
- pathlib
- csv
- os
- chardet
- nltk
- transliterate


## References:

- Manning, Christopher D., and Hinrich Schütze. Foundations of statistical natural language processing.
Vol. 999. Cambridge: MIT press, 1999.
- Bird, S., Klein, E., & Loper, E. Natural language processing with Python: analyzing text with
the natural language toolkit. " O'Reilly Media, Inc.". 2009. (http://www.nltk.org/book/)
- Denecke, Kerstin. Using SentiWordnet for multilingual sentiment analysis. Data Engineering
Workshop, 2008. ICDEW 2008. IEEE 24th International Conference on. IEEE, 2008.
