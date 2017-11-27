
# Connecting
```
psql -U postgres
# password: postgres
\list
\connect quizdb # to this database.
\dt # list tables
```
# Dump importing
```
cd "C:\Users\arama\git\tychoDB\quizbowl"
psql -U postgres quizdb < import/data.sql

SET client_encoding = 'UTF8';
copy (SELECT array_to_json(array_agg(categories)) FROM categories) to './output/categories.json';
copy (SELECT array_to_json(array_agg(tossups)) FROM tossups) to '/output/tossups.json';
```

```
DB name: quizdb
             List of relations
 Schema |     Name      | Type  |  Owner
--------+---------------+-------+----------
 public | bonus_parts   | table | postgres
 public | bonuses       | table | postgres
 public | categories    | table | postgres
 public | subcategories | table | postgres
 public | tossups       | table | postgres
 public | tournaments   | table | postgres
(6 rows)

bonuses: formatted_text, id, formatted_answer
bonus_parts: formatted_text, bonus_id, formatted_answer
```

Difficulties:
1 - MS
2 - Easy HS
3 - Regular HS
4 - Hard HS
5 - National HS
6 - Easy College
7 - Regular College
8 - Hard College
9 - Open