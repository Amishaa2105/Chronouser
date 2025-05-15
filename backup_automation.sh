#!/bin/bash

SOURCE_DIR="$1"
DEST_DIR="$2"
FREQUENCY="$3"
COMPRESSION="${4:-none}"
LOG_FILE="./logs/backup.log"

TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
ARCHIVE_NAME="backup_${TIMESTAMP}.tar"
COMPRESSED_ARCHIVE=""

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

perform_backup() {
    log "Starting backup from $SOURCE_DIR to $DEST_DIR with compression: $COMPRESSION"

    # Ensure destination exists
    mkdir -p "$DEST_DIR"
    if [ $? -ne 0 ]; then
        log "Failed to create destination directory: $DEST_DIR"
        exit 1
    fi

    TMP_BACKUP_DIR="${DEST_DIR}/backup_tmp_${TIMESTAMP}"
    mkdir -p "$TMP_BACKUP_DIR"

    # Sync source to temporary directory
    rsync -av --delete "$SOURCE_DIR"/ "$TMP_BACKUP_DIR"/ >> "$LOG_FILE" 2>&1
    if [ $? -ne 0 ]; then
        log "rsync failed! Backup aborted."
        rm -rf "$TMP_BACKUP_DIR"
        exit 1
    fi

    case "$COMPRESSION" in
        none)
            FINAL_BACKUP_PATH="${DEST_DIR}/backup_${TIMESTAMP}"
            mv "$TMP_BACKUP_DIR" "$FINAL_BACKUP_PATH"
            log "Backup saved at $FINAL_BACKUP_PATH without compression."
            ;;
        gzip)
            COMPRESSED_ARCHIVE="${DEST_DIR}/${ARCHIVE_NAME}.gz"
            tar czf "$COMPRESSED_ARCHIVE" -C "$TMP_BACKUP_DIR" .
            if [ $? -eq 0 ]; then
                log "Backup compressed with gzip: $COMPRESSED_ARCHIVE"
                rm -rf "$TMP_BACKUP_DIR"
            else
                log "gzip compression failed!"
                rm -rf "$TMP_BACKUP_DIR"
                exit 1
            fi
            ;;
        bzip2)
            COMPRESSED_ARCHIVE="${DEST_DIR}/${ARCHIVE_NAME}.bz2"
            tar cjf "$COMPRESSED_ARCHIVE" -C "$TMP_BACKUP_DIR" .
            if [ $? -eq 0 ]; then
                log "Backup compressed with bzip2: $COMPRESSED_ARCHIVE"
                rm -rf "$TMP_BACKUP_DIR"
            else
                log "bzip2 compression failed!"
                rm -rf "$TMP_BACKUP_DIR"
                exit 1
            fi
            ;;
        *)
            log "Unknown compression option: $COMPRESSION. Aborting."
            rm -rf "$TMP_BACKUP_DIR"
            exit 1
            ;;
    esac

    log "Backup completed successfully."
}

perform_backup
