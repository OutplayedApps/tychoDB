import os 
import psycopg2
dir_path = os.path.dirname(os.path.realpath(__file__))

con = None
#con = connect(user='nishant', host = 'localhost', password='everything')

def performJSONQuery(cur, tableName):
    cur.execute("SELECT row_to_json(%s) FROM %s" % (tableName, tableName))

# Connect to an existing database
conn = psycopg2.connect("dbname=quizdb user=postgres password=postgres")

# Open a cursor to perform database operations
cur = conn.cursor()

#performJSONQuery(cur, "categories")

#performJSONQuery(cur, "subcategories")

tournaments = []

cur.execute("SELECT row_to_json(t), count(tu)  FROM tournaments t left join tossups tu on tu.tournament_id=t.id group by t")
for tournament in cur:
    print tournament
    break
    tournament = tournament[0]
    tournamentFileName = str(tournament["id"]) + ".json"
    tournamentToAdd = {"name": tournament["name"], "difficulty": tournament["difficulty"], "file": tournamentFileName}
    print tournamentToAdd
    tournaments.append(tournamentToAdd)
    break
print tournaments
exit


# Execute a command: this creates a new table
tableName = "tossups"
outputPath = "/output/%s.json" % (tableName,)
#cur.execute("SELECT array_to_json(array_agg(%s)) FROM %s" % (tableName, tableName))
cur.execute("SELECT row_to_json(%s) FROM %s" % (tableName, tableName))
#cur.execute("select * from tossups b where b.text != b.formatted_text")
#cur.execute("select * from bonuses b where b.leadin != b.formatted_leadin")
for record in cur:
    question = {};
    print record
    question = record[0]
    print question
    question = {
        "tournament_id": question["tournament_id"],
        "answer": question["answer"],
        "subcategory_id": question["subcategory_id"],
        "category_id": question["category_id"],
        "round": question["round"],
        "number": question["number"],
        "text": question["formatted_text"] if (tableName == "tossups") else question["formatted_leadin"]
    }
    print question
    break