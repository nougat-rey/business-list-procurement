# business-list-procurement
Scrapes Yellow Pages for business listings.

- Currently scrapes the business listings for Ottawa.

# Installation

## Environment Setup

Download python 3. Ensure python and pip, its package manager are in your path (the default installer should do this for you).

[Optional] Set up a virtual environment (isolates external packages on a per project basis)
```
>pip install virtualenv
>cd "path_to_project_directory"
>python -m venv env
(on macOS/linux)> source env/bin/activate
(on windows)>.\env\Scripts\activate

... develop ...

>deactivate (returns you to your default env)
```
## Install Dependencies

If you chose to use a virtual env activate it before the next steps. The file 'requirements.txt' contains the project's external dependencies.
```
>cd "path_to_project_directory"
>pip install -r requirements.txt
```
# Current Status

- Extracts approximately 5500 business listings from Yellow Pages' Ottawa listings
- Takes 11 minutes to complete

## Open Issues

- Not consistent, does not extract the exact same number of listings every run
- Does not currently handle multiple pages per listing category in Yellow Pages
- Script will be unable to collect data if too many queries are made (stops working after around 75 queries)
    - A temporary solution has been implemented where the script will reset the chrome driver every 50 page queries (categories)
- Data on Yellow Pages is stored in various orders, not all have been considered currently, so the output excel file has entries that are shifted or out of order
- There exists duplicates on Yellow Pages, script does not consider this and will download all available listings