import subprocess


def is_mysql_running():
    try:
        # Run a command to check if the MySQL 8.1 service is running
        result = subprocess.run(["sc", "query", "mysql81"], capture_output=True, text=True, check=True)
        return "RUNNING" in result.stdout
    except subprocess.CalledProcessError:
        return False

def start_mysql_service():
    try:
        # Start MySQL 8.1 service using the 'sc start' command
        subprocess.run(["sc", "start", "mysql81"], check=True)
        print("MySQL 8.1 service started.")
    except subprocess.CalledProcessError as e:
        print("Error starting MySQL 8.1 service:", e)

if not is_mysql_running():
    start_mysql_service()
else:
    print("MySQL 8.1 service is already running.")
