<h2>Recruitment Task</h2>

autor: Jakub Podolski

<h4>How to use</h4>
<p>User can create and read logs from files using ProfilLogger and ProfilloggerReader</p>
<p>ProfilLogger and ProfilLoggerReader take Handlers as arguments</p>
<p>ProfilLogger can save to multiple files at once</p>
<p>ProfilLoggerReader can only read logs from a single file at once</p>
<p>Handler are used to point to the file</p>
<p>App supports 4 types of Handlers:</p>
<p><b>ProfilLogger.FileHandler</b>(file_name : Optional[str] = "log.txt") - for .txt files</p>
<p><b>ProfilLogger.CSVHandler</b>(file_name : Optional[str] = "log.csv") - for .csv files</p>
<p><b>ProfilLogger.JsonHandler</b>(file_name : Optional[str] = "log.json") - for .json files</p>
<p><b>ProfilLogger.SQLLiteHandler</b>(file_name : Optional([str] = "log.sqlite") - for .sqlite files</p>
<p>Each Handler has one optional argument file_name</p>
<p>If string passed as argument will be invalid OS file name, the Handler will return error</p>

<p><h4>Example of Handler creation</h4></p>
<p>my_file_handler = ProfilLogger.FileHandler() - will save to and read from "log.txt"</p>
<p>my_json_handler = ProfilLogger.JsonHandler("my_json_logs.json") - will save to and read from "my_json_logs.json"</p>
<p>Remember to end passed file_name with correct file extension</p>

<p><h4>ProfilLogger creation</h4></p>
<p><b>ProfilLogger.ProfilLigger</b>(handler : List[Handlers])</p>
<p>ProfilLogger takes as an argument list of Handlers, with minimum of 1 Handler</p>
<p><h4>Example of ProfilLogger creation</h4></p>
<p>my_csv_handler = ProfilLogger.CSVHandler("my_csv_logs.csv")</p>
<p>my_sqlite_handler = ProfilLogger.SQLLiteHandler("my_sqlite_logs.sqlite")</p>
<p>my_logger = ProfilLogger.ProfilLogger(handlers=[my_csv_handler, my_sqlite_handler]</p>

<p><h4>Creating logs</h4></p>
<p>ProfilLogger.ProfilLogger saves messages only, when log_level attribute is equal or lower compared to log level of method used</p>
<p>Logs are stored in files with following format</p>
<p><b>date</b>- day month year hour:minute:second</p>
<p><b>level</b>- level used to save log entry</p>
<p><b>msg</b>- message passed down by user</p>
<p>Hierarchy of log levels: debug << info << warning << error << critical</p>
<p>By default log_level is set to warning level</p>
<p>In order to change ProfilLogger.ProfilLogger log_level use ProfilLogger.ProfilLogger.set_log_level(level)</p>
<p>To save log use one of the following methods:</p>
<p><b>ProfilLogger.ProfilLogger.debug(message)</b> - Creates log with passed message at debug level and current datetime</p>
<p><b>ProfilLogger.ProfilLogger.info(message)</b> - Creates log with passed message at info level and current datetime</p>
<p><b>ProfilLogger.ProfilLogger.warning(message)</b> - Creates log with passed message at warning level and current datetime</p>
<p><b>ProfilLogger.ProfilLogger.error(message)</b> - Creates log with passed message at error level and current datetime</p>
<p><b>ProfilLogger.ProfilLogger.critical(message)</b> - Creates log with passed message at critical level and current datetime</p>
<p><h4>Example of logging</h4></p>
<p>my_logger.set_log_level("error")</p>
<p>my_logger.warning("my warning message")</p>
<p>my_logger.error("my error message")</p>
<p>Both above lines will execute without errors, but only "my error message" will be saved due to warning being default log level</p>

<p><h4>Reading logs from file</h4></p>
<p>ProfilLoggerReader is class used to read from file</p>
<p>ProfilLoggerReader takes as an argument single Handler</p>
<p>ProfilLoggerReader has 4 methods, used to read logs:</p>
<p><b>ProfilLoggerReader.find_by_text</b>(text : str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) - returns list of logs with given text in it, can be filtered by date</p>
<p><b>ProfilLoggerReader.find_by_regex</b>(regex : str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) - returns list of logs that match given regular expression, can be filtered by date</p>
<p><b>ProfilLoggerReader.groupby_by_level</b>(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) - returns dict where key: value pairs are level: list[LogEntry] with given level, can be filtered by date</p>
<p><b>ProfilLoggerReader.groupby_by_month</b>(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) - returns dict where key: value pairs are month: list[LogEntry] with, can be filtered by date</p>
<p>It is possible to pass str, as any date in iso format</p>


<p><h4>Examples</h4></p>
<p>my_csv_handler = ProfilLogger.CSVHandler("user_creation_logs.csv") # creates Handler pointing to "user_creation_logs.csv" file</p>
<p>my_csv_reader = ProfilLogger.ProfilLoggerReader(handler=my_csv_handler # creates ProfilLoggerReader with given Handler </p>
<p>list_of_logs = my_csv_reader.find_by_text("user not created") # returns list of LogEntry objects with given message</p>
<p>logs_filtered = my.csv_reader.find_by_regex("[c-d] message", start_date="2018-05-21") # returns list of logs past start_date that match regex</p>
<p>logs_grouped = my.csv_reader.group_by_level("start_date="2018-05-21", end_date="2020-06-01") # returns dict where keys are levels, and values are lists of filtered LogEntry objects by date, and given level</p>
<p>logs_grouped = my.csv_reader.group_by_month() # returns dict with all logs, where keys are months logged, and values are lists LogEntry</p>
