#!/bin/bash

BACKUP_DIR="/"
FILE_NAME=$BACKUP_DIR`date`.sql
pg_dump -U postgres postgres > $FILE_NAME
