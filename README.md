# About

This program trains a model to tag whether something is in the beginning (B), inside (I), or outside (O) a noun phrase. For example, the sentence "A large dog is eating", would be tagged "A - B, large - I, dog - I, is - O, eating - O". Many features were used within the maximum entropy modeling, most weight was given to word capitlization, part of speech, and the previous word's tag. 

To see the model in action, run the feature_set.py with the training and test files as arguments, insert training.feature,test.feature into the MAX_ENT directory, cd into MAX_ENT directory and compile train and test files by running the following commands:

```bashb
javac -cp maxent-3.0.0.jar;trove.jar *.java

java -cp .:maxent-3.0.0.jar;trove.jar MEtrain training.chunk model.chunk

java -cp .:maxent-3.0.0.jar;trove.jar MEtag test.chunk model.chunk response.chunk
```


