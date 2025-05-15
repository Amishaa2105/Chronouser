#!/bin/bash
BACKUP_SCRIPT="/mnt/c/Users/siya1/OneDrive/Desktop/ChronoUser_Backup_Automation/backup_automation.sh"
SOURCE_DIR="/mnt/c/Users/siya1/Documents"
DEST_DIR="/mnt/c/Users/siya1/OneDrive/Desktop/ChronoUser_Backup_Automation/Backup files"

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


(crontab -l 2>/dev/null | grep -v "$BACKUP_SCRIPT"; echo "$CRON_TIME /bin/bash \"$BACKUP_SCRIPT\" \"$SOURCE_DIR\" \"$DEST_DIR\" \"$FREQUENCY\"") | crontab -

echo "Cron job installed for $FREQUENCY backups."
