import sqlite3

with sqlite3.connect("Volac.db") as db:
    cursor = db.cursor()
    cursor.execute("SELECT * from Staff")
    col = [tuple[0] for tuple in cursor.description]
    print(col)

    positions = [(i,j) for i in range (int(round(len(col)/2,1))) for j in range(4)]
    

    for position, name in zip(positions,col):
        label = QLabel(name)
        grid.addWidget(label,*position)
    
