#!/bin/bash
# Adjust these variables to your actual script and directories
BACKUP_SCRIPT="/full/path/to/backup_automation.sh"
SOURCE_DIR="/full/path/to/source"
DEST_DIR="/full/path/to/destination"

FREQUENCY="daily"

case $FREQUENCY in
    daily)
        CRON_TIME="0 2 * * *"  # at 2 AM daily
        ;;
    weekly)
        CRON_TIME="0 2 * * 0"  # at 2 AM every Sunday
        ;;
    monthly)
        CRON_TIME="0 2 1 * *"  # at 2 AM on the 1st of every month
        ;;
    *)
        echo "Invalid frequency"
        exit 1
        ;;
esac

(crontab -l 2>/dev/null | grep -v "$BACKUP_SCRIPT"; echo "$CRON_TIME $BACKUP_SCRIPT $SOURCE_DIR $DEST_DIR $FREQUENCY") | crontab -

echo "Cron job installed for $FREQUENCY backups."