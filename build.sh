#!/bin/bash
set -e
pip install -r requirements.txt
python -c "
from sentence_transformers import SentenceTransformer
print('Downloading model...')
SentenceTransformer('all-MiniLM-L6-v2')
print('Model downloaded and cached.')
"
```

In Render dashboard → your service → **Settings** → **Build Command**, set it to:
```
chmod +x build.sh && ./build.sh
```

And **Start Command**:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT