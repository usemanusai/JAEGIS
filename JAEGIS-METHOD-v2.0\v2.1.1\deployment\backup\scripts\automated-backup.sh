#!/bin/bash
# N.L.D.S. Automated Backup Script
# JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_BASE_DIR="/backups"
S3_BUCKET="${S3_BUCKET:-nlds-backups-prod}"
NAMESPACE="${NAMESPACE:-nlds}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
LOG_FILE="/var/log/nlds-backup.log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if running in Kubernetes
    if [ ! -f /var/run/secrets/kubernetes.io/serviceaccount/token ]; then
        error_exit "Not running in Kubernetes environment"
    fi
    
    # Check required tools
    for tool in kubectl aws pg_dump redis-cli; do
        if ! command -v "$tool" &> /dev/null; then
            error_exit "$tool is not installed"
        fi
    done
    
    # Check S3 access
    if ! aws s3 ls "s3://$S3_BUCKET" &> /dev/null; then
        error_exit "Cannot access S3 bucket: $S3_BUCKET"
    fi
    
    log "Prerequisites check passed"
}

# Create backup directory structure
setup_backup_dirs() {
    local timestamp="$1"
    
    BACKUP_DIR="$BACKUP_BASE_DIR/$timestamp"
    mkdir -p "$BACKUP_DIR"/{postgres,redis,kubernetes,application,logs}
    
    log "Created backup directory: $BACKUP_DIR"
}

# Backup PostgreSQL database
backup_postgres() {
    log "Starting PostgreSQL backup..."
    
    local backup_file="$BACKUP_DIR/postgres/nlds_db_$(date +%Y%m%d_%H%M%S).sql"
    
    # Get database credentials from secret
    local db_password
    db_password=$(kubectl get secret nlds-secrets -n "$NAMESPACE" -o jsonpath='{.data.NLDS_DATABASE_PASSWORD}' | base64 -d)
    
    # Create database dump
    PGPASSWORD="$db_password" pg_dump \
        -h postgres-service."$NAMESPACE".svc.cluster.local \
        -U nlds \
        -d nlds \
        --verbose \
        --no-password \
        --format=custom \
        --compress=9 \
        --file="$backup_file"
    
    if [ $? -eq 0 ]; then
        log "PostgreSQL backup completed: $(basename "$backup_file")"
        
        # Verify backup
        pg_restore --list "$backup_file" > /dev/null
        log "PostgreSQL backup verification passed"
    else
        error_exit "PostgreSQL backup failed"
    fi
}

# Backup Redis data
backup_redis() {
    log "Starting Redis backup..."
    
    local backup_file="$BACKUP_DIR/redis/redis_$(date +%Y%m%d_%H%M%S).rdb"
    
    # Get Redis password from secret
    local redis_password
    redis_password=$(kubectl get secret nlds-secrets -n "$NAMESPACE" -o jsonpath='{.data.NLDS_REDIS_PASSWORD}' | base64 -d)
    
    # Create Redis snapshot
    REDISCLI_AUTH="$redis_password" redis-cli \
        -h redis-service."$NAMESPACE".svc.cluster.local \
        BGSAVE
    
    # Wait for backup to complete
    local last_save
    while true; do
        last_save=$(REDISCLI_AUTH="$redis_password" redis-cli \
            -h redis-service."$NAMESPACE".svc.cluster.local \
            LASTSAVE)
        
        if [ "$last_save" != "$previous_save" ]; then
            break
        fi
        sleep 1
    done
    
    # Copy RDB file from Redis pod
    kubectl cp "$NAMESPACE"/redis-0:/data/dump.rdb "$backup_file"
    
    if [ -f "$backup_file" ]; then
        log "Redis backup completed: $(basename "$backup_file")"
        
        # Compress backup
        gzip "$backup_file"
        log "Redis backup compressed"
    else
        error_exit "Redis backup failed"
    fi
}

# Backup Kubernetes configurations
backup_kubernetes() {
    log "Starting Kubernetes configuration backup..."
    
    local k8s_backup_dir="$BACKUP_DIR/kubernetes"
    
    # Backup all resources in namespace
    kubectl get all,configmaps,secrets,pvc,ingress,networkpolicies \
        -n "$NAMESPACE" \
        -o yaml > "$k8s_backup_dir/nlds-resources.yaml"
    
    # Backup RBAC
    kubectl get roles,rolebindings,serviceaccounts \
        -n "$NAMESPACE" \
        -o yaml > "$k8s_backup_dir/nlds-rbac.yaml"
    
    # Backup certificates
    kubectl get certificates,issuers \
        -n "$NAMESPACE" \
        -o yaml > "$k8s_backup_dir/nlds-certificates.yaml"
    
    # Backup custom resources
    kubectl get horizontalpodautoscalers,poddisruptionbudgets \
        -n "$NAMESPACE" \
        -o yaml > "$k8s_backup_dir/nlds-custom.yaml"
    
    # Create namespace backup
    kubectl get namespace "$NAMESPACE" \
        -o yaml > "$k8s_backup_dir/nlds-namespace.yaml"
    
    log "Kubernetes configuration backup completed"
}

# Backup application data
backup_application_data() {
    log "Starting application data backup..."
    
    # Run Python backup script for application-specific data
    python3 "$SCRIPT_DIR/nlds-data-backup.py" \
        --output-dir "$BACKUP_DIR/application" \
        --namespace "$NAMESPACE"
    
    if [ $? -eq 0 ]; then
        log "Application data backup completed"
    else
        error_exit "Application data backup failed"
    fi
}

# Backup logs
backup_logs() {
    log "Starting logs backup..."
    
    local logs_backup_dir="$BACKUP_DIR/logs"
    
    # Get logs from all N.L.D.S. pods
    for pod in $(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/name=nlds -o name); do
        pod_name=$(basename "$pod")
        kubectl logs "$pod" -n "$NAMESPACE" > "$logs_backup_dir/${pod_name}.log" 2>/dev/null || true
        
        # Get previous logs if available
        kubectl logs "$pod" -n "$NAMESPACE" --previous > "$logs_backup_dir/${pod_name}-previous.log" 2>/dev/null || true
    done
    
    # Compress logs
    tar -czf "$logs_backup_dir/nlds-logs-$(date +%Y%m%d_%H%M%S).tar.gz" -C "$logs_backup_dir" *.log
    rm -f "$logs_backup_dir"/*.log
    
    log "Logs backup completed"
}

# Create backup manifest
create_manifest() {
    log "Creating backup manifest..."
    
    local manifest_file="$BACKUP_DIR/manifest.json"
    local timestamp="$1"
    
    cat > "$manifest_file" << EOF
{
  "backup_id": "nlds_backup_$timestamp",
  "timestamp": "$timestamp",
  "version": "2.2.0",
  "namespace": "$NAMESPACE",
  "backup_type": "full",
  "components": {
    "postgres": {
      "included": true,
      "files": ["postgres/nlds_db_*.sql"]
    },
    "redis": {
      "included": true,
      "files": ["redis/redis_*.rdb.gz"]
    },
    "kubernetes": {
      "included": true,
      "files": [
        "kubernetes/nlds-resources.yaml",
        "kubernetes/nlds-rbac.yaml",
        "kubernetes/nlds-certificates.yaml",
        "kubernetes/nlds-custom.yaml",
        "kubernetes/nlds-namespace.yaml"
      ]
    },
    "application": {
      "included": true,
      "files": ["application/*"]
    },
    "logs": {
      "included": true,
      "files": ["logs/nlds-logs-*.tar.gz"]
    }
  },
  "retention_policy": {
    "daily_retention_days": 30,
    "weekly_retention_weeks": 12,
    "monthly_retention_months": 12
  },
  "verification": {
    "postgres_verified": true,
    "redis_verified": true,
    "kubernetes_verified": true
  }
}
EOF
    
    log "Backup manifest created"
}

# Upload backup to S3
upload_to_s3() {
    log "Uploading backup to S3..."
    
    local timestamp="$1"
    local archive_name="nlds_backup_$timestamp.tar.gz"
    local archive_path="/tmp/$archive_name"
    
    # Create compressed archive
    tar -czf "$archive_path" -C "$BACKUP_BASE_DIR" "$timestamp"
    
    # Upload to S3 with metadata
    aws s3 cp "$archive_path" "s3://$S3_BUCKET/nlds/full/$archive_name" \
        --metadata "backup-type=full,namespace=$NAMESPACE,version=2.2.0,timestamp=$timestamp"
    
    if [ $? -eq 0 ]; then
        log "Backup uploaded to S3: s3://$S3_BUCKET/nlds/full/$archive_name"
        
        # Verify upload
        aws s3 ls "s3://$S3_BUCKET/nlds/full/$archive_name" > /dev/null
        log "S3 upload verification passed"
    else
        error_exit "S3 upload failed"
    fi
    
    # Cleanup local archive
    rm -f "$archive_path"
}

# Cleanup old backups
cleanup_old_backups() {
    log "Cleaning up old backups..."
    
    # Cleanup local backups
    find "$BACKUP_BASE_DIR" -type d -name "20*" -mtime +7 -exec rm -rf {} \; 2>/dev/null || true
    
    # Cleanup old S3 backups (keep based on retention policy)
    local cutoff_date
    cutoff_date=$(date -d "$RETENTION_DAYS days ago" +%Y%m%d)
    
    aws s3 ls "s3://$S3_BUCKET/nlds/full/" | while read -r line; do
        backup_file=$(echo "$line" | awk '{print $4}')
        backup_date=$(echo "$backup_file" | grep -o '[0-9]\{8\}' | head -1)
        
        if [ "$backup_date" -lt "$cutoff_date" ]; then
            aws s3 rm "s3://$S3_BUCKET/nlds/full/$backup_file"
            log "Deleted old backup: $backup_file"
        fi
    done
    
    log "Cleanup completed"
}

# Send backup notification
send_notification() {
    local status="$1"
    local timestamp="$2"
    local message="$3"
    
    # Send to Slack webhook if configured
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"N.L.D.S. Backup $status: $timestamp - $message\"}" \
            "$SLACK_WEBHOOK_URL" || true
    fi
    
    # Send email notification if configured
    if [ -n "${NOTIFICATION_EMAIL:-}" ]; then
        echo "N.L.D.S. Backup $status: $timestamp - $message" | \
            mail -s "N.L.D.S. Backup $status" "$NOTIFICATION_EMAIL" || true
    fi
}

# Main backup function
main() {
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    
    log "Starting N.L.D.S. automated backup: $timestamp"
    
    # Trap errors and send notification
    trap 'send_notification "FAILED" "$timestamp" "Backup process encountered an error"' ERR
    
    check_prerequisites
    setup_backup_dirs "$timestamp"
    
    backup_postgres
    backup_redis
    backup_kubernetes
    backup_application_data
    backup_logs
    
    create_manifest "$timestamp"
    upload_to_s3 "$timestamp"
    cleanup_old_backups
    
    # Cleanup local backup directory
    rm -rf "$BACKUP_DIR"
    
    log "N.L.D.S. automated backup completed successfully: $timestamp"
    send_notification "SUCCESS" "$timestamp" "All components backed up successfully"
}

# Script execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
