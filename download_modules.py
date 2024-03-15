import nltk
import os

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')

def install_module(module):
    os.system("pip install "+module)


if __name__ == "__main__":
    module_list = ["Distance", "autocorrect", "requests", "beautifulsoup4", "nltk", "numpy", "scikit-learn", "python-Levenshtein"]
    
    for module in module_list:
        install_module(module)