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
