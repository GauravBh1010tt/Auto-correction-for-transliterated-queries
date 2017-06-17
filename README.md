# Auto-correction-for-transliterated-queries
### PLease refer to my blog [Transliterated Queries 2 – Deep Learning](https://deeplearn.school.blog/2017/01/05/__trashed/) for the implementation details.

The project is inspired by my following papers:
* [Language Identification and Disambiguation in Indian Mixed-Script.](http://link.springer.com/chapter/10.1007%2F978-3-319-28034-9_14)
* [Construction of a Semi-Automated model for FAQ Retrieval via Short Message Service.](http://dl.acm.org/citation.cfm?id=2838717)

Refer to my blog for implementation of above papers:  [Simple Markov Model for correcting Transliterated Queries](https://deeplearn.school.blog/2016/12/17/auto-correction-for-transliterated-queries/#more-63)
  
### Dependencies:
Install the following packages for using the project:

    pip install nltk
    pip install keras
    pip install tensorflow
    pip install h5py
  
### Usage:
```python
import auto_correct as auto
model = auto.auto_correct()
model.run()

enter a query
hw to lrn pythn anddeeplearning eas ily
how to learn python and deep learning easily    11.2134873867
```
### Parameters of the model
```python
auto_correct(data=,re_train=,vocab_size=,step=,batch_size=,nb_epoch=,embed_dims=)
        
```
For retraining the model, set `re_train` = `True` and pass the queries as the other argument. The queries must be given in the following format:
```python
queries=[]
queries = ['how to handle a 1.5 year old when hitting',
 'how can i avoid getting sick in china',
 'how do male penguins survive without eating for four months',
 'how do i remove candle wax from a polar fleece jacket',
 'how do i find an out of print book']

model = auto.auto_correct(re_train=True,data=queries)
```
The other parameters to the model are 
  -  `vocab_size` - The size of vocabulary used i.e. the number of unique words
  -  `step` - The size of sliding window
  -  `batch_size` - Number of training samples to be passed on one iteration
  -  `nb_epoch` - Total number of iteration
  -  `embed_dims` - Embedding dimension size
