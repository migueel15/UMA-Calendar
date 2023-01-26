# Installation
1. Clone repo.
2. cd UMA-Calendar
3. Run `pip -r requirements.txt`
4. Create .env file in the same path.
  Add:
    - USER_MAIL="campus mail"
    - USER_PASSWD="campus password"
    - DATABASE_PATH="where to store json file with calendar info"
5. Run `python fetchCalendar.py`

Data will be store in `DATABASE_PATH`
