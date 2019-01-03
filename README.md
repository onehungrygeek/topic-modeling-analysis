# Topic Modeling Analysis: User Manual
[![Python Version](https://img.shields.io/badge/Python-v3.6.6-blue.svg)](https://www.python.org/downloads/release/python-366/) &nbsp; ![](https://img.shields.io/badge/Algorithms-LSI%2C%20HDP%2C%20LDA%2C%20LDAMallet-red.svg) &nbsp; [![Operating System Tested](https://img.shields.io/badge/Tested%20on-Ubuntu%2018.10-yellow.svg)](https://www.ubuntu.com/#download)
### Setup:
1. Requirements:

    a. Python:
    * Download and install **Python 3.6.6** by visiting [this download link](https://www.python.org/downloads/release/python-366/)
    * Set environment variable for above installed Python. Check how to do the same for [Windows here](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path) or [Linux here](https://stackoverflow.com/questions/3671837/setup-python-variable-environment-on-ubuntu)

    b. Important Python Libraries:
    
    Install below mentioned libraries. Click on the library names to open the installation manual for each.
      * [Gensim (v3.6.0)](https://radimrehurek.com/gensim/install.html)
      * [Matplotlib (v3.0.1)](https://matplotlib.org/users/installing.html)
      * [Spacy (v2.0.16)](https://spacy.io/usage/)
      * [NLTK (v3.30)](https://www.nltk.org/install.html)
      * [pyLDAvis (v2.1.2)](https://pypi.org/project/pyLDAvis/)
      * [Plotly (v3.4.2)](https://plot.ly/python/getting-started/)

    Generally, you can install above mentioned libraries by typing this in the terminal/command prompt:
    ```sh
    pip install <library_name>
    ```
    For example,
    ```sh
    pip install matplotlib
    ```
    You can also install all requirements by downloading [this requirements.txt file](https://raw.githubusercontent.com/onehungrygeek/topic-modeling-analysis/master/requirements.txt). Then open a terminal/command prompt in same folder as the downloaded requirements.txt file and type
    ```sh
    pip install -r requirements.txt
    ```

2. Clone the Github repository:

    The topic modeling analysis Github repository is located [at this link](https://github.com/onehungrygeek/topic-modeling-analysis). You can either download the repository zip and uncompress it or type the command below in the terminal/command prompt:
    ```sh
    git clone https://github.com/onehungrygeek/topic-modeling-analysis.git
    ```

3. Input dataset requirements:

    Format: `.txt`
    
    The input dataset for this program requires to be in a specific format. The dataset must contain the responses/paragraphs in one single line as one document i.e. one document on each line. One document can be just a few words, a single line or a few lines that form a paragraph. Such one document needs to be on one line.

4. Download mallet and set mallet path:

    Download the mallet model from [this link](http://mallet.cs.umass.edu/download.php) and unzip it to some directory. You then need to update mallet path and environment variable so that LdaMallet model in gensim works properly.

    **Note: These two path setting commands are already present in below mentioned 2 python files. Just update the directory to match your directory**

    Mallet path for **Windows 10**
    Suppose you extracted the mallet zip to `C:/mallet/` directory then provide respective paths as shown below in `compute_models.py` and `compute_all_coherence_scores.py` files.
    ```python
    os.environ.update({'MALLET_HOME': r'c:/mallet/'})
    mallet_path = 'c:\\mallet\\bin\\mallet'
    ```
    Mallet path for **Ubuntu 18.10**
    Suppose you extracted the mallet zip to `/home/username/mallet` directory then provide respective paths as shown below in `compute_models.py` and `compute_all_coherence_scores.py` files.
    ```python
    os.environ.update({'MALLET_HOME': r'/home/username/mallet/'})
    mallet_path = '/home/username/mallet/bin/mallet'
    ```
5. Create account on Plotly:

    Sign up for Plotly using [this link](https://plot.ly/Auth/login/) and grab an API key using [this link.](https://plot.ly/settings/api) This is required to generate graphs and view them on your system's default internet browser. The free tier account on Plotly allows creation of 100 graphs per day and storage of 25 unique graphs on Plotly's online file storage. This username and API key needs to be updated in the `config.py` file. Generally, the plots are located at the web address like this `https://plot.ly/~YOUR_USER_NAME_HERE`

***

### Folder Structure:

![](https://user-images.githubusercontent.com/19870554/50667131-ed6e3300-0f85-11e9-832b-6b09a3ed4025.png)

***
### Parameters to tweak:
Below are a few of the important parameters that you can tweak as per your needs. But, you can find a complete list of available parameters for all gensim models here: [LSI Model Parameters](https://radimrehurek.com/gensim/models/lsimodel.html), [HDP Model Parameters](https://radimrehurek.com/gensim/models/hdpmodel.html), [LDA Model Parameters](https://radimrehurek.com/gensim/models/ldamodel.html), [LDAMallet Model Parameters](https://radimrehurek.com/gensim/models/wrappers/ldamallet.html)

Open the `config.py` file in your favorite editor and feel free to tweak the parameters. A detailed description for each one of them is mentioned down below.

![](https://user-images.githubusercontent.com/19870554/50666876-a7649f80-0f84-11e9-922b-a69213eda4fe.png)

1. `num_topics`:
   * *Note*: Only LSI, LDA and LDA Mallet
   * *Default Value*: `5`
   * *Description*: The number of requested latent topics to be extracted from the training corpus. This variable will set how many topics you need the algorithms to generate. (Note: HDP does not require num_topics because it computes all possible number of topics in given input. If you want to change individual `num_topics`, you can do that in `compute_models.py` file under respective gensim model arguments.)
2. `num_words`:
   * *Note*: Only LSI, LDA and LDA Mallet
   * *Default*: `10`
   * *Description*:  The number of words to be included per topics (ordered by significance/probability). By default, all topics contain 10 keywords. Change it as shown in example below.
3. `max_topics`:
   * *Default*: `50`
   * *Description*: The program generates a graph of coherence scores for different models with increasing num of topics. This variable is set so as to generate models till the given `max_topics`. The above default value of 50 computes coherence scores for models starting with 5 topics and then goes up to 50 with steps of 5. Like 5 topics, 10 topics, 15 topics, ... 50 topics.
   Note: You cannot run this analysis for HDP model because it does not accept num_topics parameter.
4. `measure`:
   * *Default*: `c_v`
   * *Possible Values*: c_v, c_uci, c_npmi, u_mass
   * *Description*: Coherence measure to be used. Best method - `c_v`. Fastest method - `u_mass`, `c_uci` also known as `c_pmi`. For `u_mass` corpus should be provided, if texts is provided, it will be converted to corpus using the dictionary. For `c_v`, `c_uci` and `c_npmi` texts should be provided (corpus isn’t needed).
5. `random_state`:
   * *Note*: Only HDP and LDA
   * *Default*: `100`
   * *Description*: Either a randomState object or a seed to generate one. Useful for reproducibility of same outputs.
6. `update_every`:
   * *Note*: Only LDA
   * *Default*: `1`
   * *Description*: Number of documents to be iterated through for each update. Set to 0 for batch learning, > 1 for online iterative learning.
7. `chunksize`:
   * *Note*: Only LSI, HDP and LDA
   * *Default*: `100`
   * *Description*: Number of documents to be used in each training chunk.
8. `passes`:
   * *Note*: Only LDA
   * *Default*: `100`
   * *Description*: Number of passes through the corpus during training.
9. `alpha`:
   * *Note*: Only LDA
   * *Default*: `auto`
   * *Description*: Can be set to an 1D array of length equal to the number of expected topics that expresses our a-priori belief for the each topics’ probability. Alternatively default prior selecting strategies can be employed by supplying a string:
     * `asymmetric`: Uses a fixed normalized asymmetric prior of 1.0 / topicno.
     * `auto`: Learns an asymmetric prior from the corpus.
10. `per_word_topics`:
    * *Note*: Only LDA
    * *Default*: `True`
    * *Description*: If True, the model also computes a list of topics, sorted in descending order of most likely topics for each word, along with their phi values multiplied by the feature length (i.e. word count).
11. `username`:
    * *Note*: Please sign up for a new account on Plotly instead of using the default from [this link](https://plot.ly/Auth/login/). The default account has already reached the allowed free graphs quota on Plotly.
    * *Default*: `akshay94`
    * *Description*: The username for the graphs generated using Plotly online library.
12. `api_key`:
    * *Note*: Please generate a new API key for the newly created account on Plotly using [this link](https://plot.ly/settings/api).
    * *Default*: `ieUGzhNg4U33RPn74RXi`
    * *Description*: API key for tracking graph generation and usage for above username.

***
### Usage:
Open the terminal/command prompt in the directory where the Github repository is cloned or unzipped. Type:
```sh
python main.py
```
If you have multiple versions of Python installed, the command will most probably be like:
```sh
python3 main.py
```
Wait for the terminal/command prompt to import all the necessary modules for the processing. It will then ask you for the input dataset. Type the dataset name with the `.txt` extension and press enter:
```sh
Enter text file name for analysis: YOUR_DATASET_NAME_HERE.txt
```
**All output files are appended with the timestamp when the program started so that no files are overwritten and always stay unique**
Check your terminal/command prompt for the live output of each algorithm (LSI, LDA, HDP and LDAMallet). This output will also be saved after successful completion of the program. Also, another output files and graphs are saved in the `Output_Files` directory.
