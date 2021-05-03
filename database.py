import mysql.connector

mydb = mysql.connector.connect(
  host="34.126.71.148",
  user="myPEET",
  password="10042541_Pol",
  database="smartbin"
)

mycursor = mydb.cursor()


class DataBase:
    def __init__(self):
        self.users = None
        self.load_users()
        self.load_points()

    def load_points(self):
        self.points = {}
        mycursor.execute("SELECT class_id, class_name, point \
                        FROM Class")
        myresult = mycursor.fetchall()

        for line in myresult:
            class_id, class_name, point = line
            self.points[class_id] = (class_name, point)

    def get_point(self, id):
        return self.points[id][1]

    def load_users(self):
        self.users = {}
        mycursor.execute("SELECT student_id, prefix, first_name \
                        FROM Student")
        myresult = mycursor.fetchall()

        for line in myresult:
            student_id, prefix, first_name = line
            self.users[student_id] = (prefix, first_name)

    def get_user(self, student_id):
        if student_id in self.users:
            return self.users[student_id]
        else:
            return -1

    def validate(self, student_id):
        if self.get_user(student_id) != -1:
            return True
            # return self.users[email][0] == password
        else:
            return False

    def get_sessionID(self):
        mycursor.execute("SELECT MAX(session_id) FROM t_session")
        max_sessionID = mycursor.fetchall()
        
        return max_sessionID[0][0] + 1

    def insert_session(self):
        session_id = self.get_sessionID()
        sql = "INSERT INTO t_session(point_total, create_time, update_time) \
            VALUES(0, NOW(), NOW())"
        mycursor.execute(sql)
        mydb.commit()

        return session_id

    def update_session(self, id, point):
        sql = "UPDATE t_session \
            SET point_total = "+ str(point) +", update_time = NOW() \
            WHERE session_id = "+str(id)+""
        mycursor.execute(sql)
        mydb.commit()

    def insert_trash(self, sid, binID, classID, sessionID, ImageName):
        sql = "INSERT INTO trash(student_id, bin_id, class_id, \
            session_id, img_name, create_time, update_time) \
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())"
        val = (sid, binID, classID, sessionID, ImageName)
        mycursor.execute(sql, val)
        mydb.commit()

    def get_total_point(self, sid):
        mycursor.execute("SELECT totol_point \
                        FROM Student    \
                        WHERE student_id = '"+str(sid)+"'")
        myresult = mycursor.fetchall()

        return myresult[0][0]

    def update_total_point(self, sid, point):
        newpoint = int(self.get_total_point(sid)) + int(point)

        sql = "UPDATE Student \
            SET totol_point = "+str(newpoint)+", update_time = NOW() \
            WHERE student_id = '"+str(sid)+"'"
        mycursor.execute(sql)
        mydb.commit()




db = DataBase()
# db.insert_trash("6040202424", 1, 1, 2, "ImageName.jpg")
print(db.get_total_point('User donate'))

    # def insert_trash(self, id, binID, classID, sessionID, ImageName):
    #     if db.validate_session(id) == False:
    #         db.insert_session(id)

    #     sql = "INSERT INTO trash(student_id, bin_id, class_id, \
    #         session_id, img_name, create_time, update_time) \
    #         VALUES (%s, %s, %s, %s, %s, NOW(), NOW())"
    #     val = (id, binID, classID, sessionID, ImageName)
    #     mycursor.execute(sql, val)
    #     mydb.commit()

    # def validate_session(self, id):
    #     mycursor.execute("SELECT point_total FROM t_session \
    #                     WHERE session_id = " +str(id)+ "")
    #     myresult = mycursor.fetchall()
        
    #     if myresult == []:
    #         return False
    #     else: 
    #         return myresult[0][0]

    # def insert_session(self, id, point):
    #     pointOdd = db.validate_session(id)
    #     if pointOdd == False:
    #         sql = "INSERT INTO t_session(point_total, create_time, update_time) \
    #             VALUES (%s, NOW(), NOW())"
    #         val = (id)
    #         mycursor.execute(sql, val)
    #         mydb.commit()
    #     else:
    #         sql = "UPDATE t_session \
    #             SET point_total = "+ str(pointOdd+point) +", update_time=NOW() \
    #             WHERE session_id = "+str(id)+""
    #         mycursor.execute(sql)
    #         mydb.commit()