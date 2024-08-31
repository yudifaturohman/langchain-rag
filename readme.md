## Getting Started
 Before running this program, please register a GroqCloud account first at the following link [here](https://console.groq.com/login) and if you have created an account, then create a GroqCloud API KEY by clicking the following link [here](https://console.groq.com/keys).

 1. `python -m venv venv`
 2. `source venv/bin/activate`
 3. `pip install -r requirements.txt`
 4. `python ./populate_database.py`
 5. `python ./query_data.py "Product Description Hot Rolled Coil"`

 ## Update document
 1. Place the pdf file inside the `data`
 2. `python ./populate_database.py`