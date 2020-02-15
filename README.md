# MetaDataExtractor
Python repo to extract metadata from a variety of documents (MS Office docs, PDF, images).

**Launch with:**

```
python3 -m pip install requirements.txt

python main.py
````

This will create a json file "metadata.json" stored at the root of the repo. 

You will also find a shinyapp in the visualization folder, convert the json file to csv with the code below and store in /visualization/data/. For some reason python gives a segfault when embedding the code in the repo, so just launch the code below in your favorite IDE to avoid it!

```
import pandas as pd

path = 'data/data/metadata.json'

temp = pd.read_json(path)

df = temp.T

df.to_csv('metadata.csv')
```
