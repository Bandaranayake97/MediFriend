import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="13906@Mysql",
    database="medifriends"
)




def get_dbfirstaid(disease):
    try:
        print(disease)
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT First_aid FROM firstaid WHERE Desease_Name= %s "
        values = (disease,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        print("successfully")
        return result
    except mysql.connector.Error as err:
        print("Error retrieving movie info: {}".format(err))
        return None
    except Exception as e:
        print("An error Occurred: {}".format(e))
        return None

def get_dbdoctor(doctor):
    try:
        print("in to ")
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT doctor.Doctor_Name , doctor.Contact_Number, doctor.Date FROM doctor where Meditation_Category= %s ")
        values = (doctor,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        print(result)
        return result
    except mysql.connector.Error as err:
        print("Error retrieving movie info: {}".format(err))
        return None
    except Exception as e:
        print("An error Occurred: {}".format(e))
        return None




#
def add_apointment(disease):
    try:
        print(disease)
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT doctor.Doctor_Name, doctor.Contact_Number, doctor.Date FROM doctor INNER JOIN firstaid ON doctor.Doctor_ID = firstaid.Doctor_ID where firstaid.Desease_Name= %s "
        values = (disease,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        print(result)
        if result:
            cursor = cnx.cursor()
            query = "INSERT INTO apoint (DiseaseName, DoctorName, Date) VALUES (%s, %s, %s);"
            values = (disease, result['Doctor_Name'], result['Date'])
            cursor.execute(query, values)
            cursor = cnx.cursor()
            query = "SELECT ApointmentID FROM apoint WHERE DiseaseName = %s ORDER BY ApointmentID DESC LIMIT 1;"
            values = (disease,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            print(result)
            print(result[0])
            apointment_id = result[0]
            print(apointment_id)
            cnx.commit()
            cursor.close()
            print("Appointment inserted successfully")
            return apointment_id
        else:
            print("Doctor not found for the given disease.")
            return -1

    except mysql.connector.Error as err:
        print("Error inserting appointment: {}".format(err))
        cnx.rollback()
        return -1

    except Exception as e:
        print("An error occurred: {}".format(e))
        cnx.rollback()
        return -1


def add_apoint(doctor):
    try:
        print("doctor add function")
        print(doctor)
        doctor=doctor[0]
        print(doctor)
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT Doctor_Name, Date FROM doctor WHERE Meditation_Category = %s"
        values = (doctor,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        print(result)
        cursor = cnx.cursor()
        print(result['Doctor_Name'])
        query = "INSERT INTO apoint (DiseaseName, DoctorName, Date) VALUES (%s, %s, %s);"
        values = (doctor, result['Doctor_Name'], result['Date'])
        cursor.execute(query, values)
        cnx.commit()
        cursor.close()
        return result
    except mysql.connector.Error as err:
        print("Error inserting appointment: {}".format(err))
        cnx.rollback()
        return -1

    except Exception as e:
        print("An error occurred: {}".format(e))
        cnx.rollback()
        return -1
