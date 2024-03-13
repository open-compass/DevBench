import sqlite3
import subprocess
import os

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def execute_query(connection, query):
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def connect_to_db(db_name):
    connection = sqlite3.connect(db_name)
    return connection

def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    ret_code = process.returncode
    return ret_code, out, err

def test_add_school():
    command = "./UMM add school -name Maths"
    ret_code, stdout, stderr = execute_command(command)
    assert ret_code == 0
    db_connection = connect_to_db("database.sqlite3")
    query = "SELECT * FROM school WHERE name='Maths';"
    result = execute_query(db_connection, query)
    found = False
    for record in result:
        if record["name"] == "Maths":
            found = True
    assert found

def test_add_person():
    command = "./UMM add person -name 'Joe' -age 23 -school 1 -type 1"
    ret_code, stdout, stderr = execute_command(command)
    assert ret_code == 0
    db_connection = connect_to_db("database.sqlite3")
    query = "SELECT * FROM people WHERE name='Joe';"
    result = execute_query(db_connection, query)
    found = False
    for record in result:
        if record["name"] == "Joe":
            found = True
    assert found

    command = "./UMM add person -name 'Bob' -age 56 -school 1 -type 2"
    ret_code, stdout, stderr = execute_command(command)
    assert ret_code == 0
    query = "SELECT * FROM people WHERE name='Bob';"
    result = execute_query(db_connection, query)
    found = False
    for record in result:
        if record["name"] == "Bob":
            found = True
    assert found

def test_search_person():
    command = "./UMM search person -name 'Bob'"
    ret_code, stdout, stderr = execute_command(command)
    assert ret_code == 0
    assert "Bob" in stdout.decode("utf-8")

def test_search_school():
    command = "./UMM search school -name 'Maths'"
    ret_code, stdout, stderr = execute_command(command)
    assert ret_code == 0
    assert "Maths" in stdout.decode("utf-8")

def test_update_person():
    db_connection = connect_to_db("database.sqlite3")
    command = "./UMM update person -name 'Jack' -age 22 -id 1"
    ret_code, stdout, stderr = execute_command(command)
    assert ret_code == 0
    query = "SELECT * FROM people WHERE name='Joe';"
    result = execute_query(db_connection, query)
    assert len(result) == 0
    query = "SELECT * FROM people WHERE name='Jack';"
    result = execute_query(db_connection, query)
    assert len(result) == 1

def test_update_school():
    command = "./UMM update school -id 1 -name 'Arts'"
    ret_code, stdout, stderr = execute_command(command)
    db_connection = connect_to_db("database.sqlite3")
    assert ret_code == 0
    query = "SELECT * FROM school WHERE id=1;"
    result = execute_query(db_connection, query)
    assert len(result) == 1
    assert result[0]["name"] == "Arts"

def test_mentor():
    command = "./UMM mentor assign -student 1 -mentor 2"
    ret_code, stdout, stderr = execute_command(command)
    assert ret_code == 0
    db_connection = connect_to_db("database.sqlite3")
    query = "SELECT * FROM mentorship WHERE mentor=2 and student=1;"
    result = execute_query(db_connection, query)
    assert len(result) == 1
    command = "./UMM mentor lookup -student 1"
    ret_code, stdout, stderr = execute_command(command)
    assert "Bob" in stdout.decode("utf-8")


def main():
    # clean up
    try:
        os.remove("database.sqlite3")
    except OSError:
        pass

    test_add_school()
    test_add_person()
    test_search_person()
    test_search_school()
    test_update_person()
    test_update_school()
    test_mentor()
    print("test passed")

if __name__ == "__main__":
    main()