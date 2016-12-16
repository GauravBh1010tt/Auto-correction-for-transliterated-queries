# Auto-correction-for-transliterated-queries
### This is a query correction system that is designed for transliterated queries.
### Key features of the model:
  - Can be retrained on a new data-set of well spelled queries in mixed languages such as Hindi-English, English-French, Hindi-Bengali, etc.
  - No need of annotated data-set.
  - Portable and easy to use.
  - Currently trained on English corpus only.
  
### Usage:
```python
obj = auto_correct()
obj.run()

enter a query
hw to lrn pythn anddeeplearning eas ily
how to learn python and deep learning easily    11.2134873867
```
### Parameters of the model
There are two parameters of the auto-corrector:
```python
obj = auto_correct(retrain=,data=)
```
For retraining the model, set `retrain` = `True` and pass the queries as the other argument. The queries must be given in the following format:
```python
queries=[]
queries = ['how to handle a 1.5 year old when hitting',
 'how can i avoid getting sick in china',
 'how do male penguins survive without eating for four months',
 'how do i remove candle wax from a polar fleece jacket',
 'how do i find an out of print book']
 obj = auto_correct(retrain=True,data=queries)
```
