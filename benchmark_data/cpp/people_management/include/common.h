#ifndef PEOPLE_MANAGEMENT_COMMON_H
#define PEOPLE_MANAGEMENT_COMMON_H

#include <vector>
#include <string>

const std::vector<std::string> columns = {"name", "age", "school", "type"};
const std::vector<std::string> full_columns = {"id", "name", "age", "school", "type"};
const std::vector<std::string> commands = {"add", "search", "delete", "update"};
const std::vector<std::string> targets = {"person", "school"};

const char* const people_sql_name = "sql/people.sql";
const char* const mentorship_sql_name = "sql/mentorship.sql";
const char* const school_sql_name = "sql/school.sql";
const char* const db_name = "database.sqlite3";

const int SUCCESS = 0;
const int DB_OPEN_ERROR = 1;
const int INVALID_OPTION = 2;
const int NOT_ENOUGH_OPTIONS = 3;
const int RECORD_NOT_EXISTS = 4;
const int SQL_EXECUTION_ERROR = 5;
const int FAILURE = 6;

#endif