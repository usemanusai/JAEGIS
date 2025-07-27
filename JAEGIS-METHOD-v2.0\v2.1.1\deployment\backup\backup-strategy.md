# N.L.D.S. Backup & Disaster Recovery Strategy

## **Overview**

This document outlines the comprehensive backup and disaster recovery strategy for the Natural Language Detection System (N.L.D.S.), ensuring business continuity and data protection in accordance with enterprise requirements.

## **Recovery Objectives**

### **Service Level Objectives (SLOs)**
- **Recovery Time Objective (RTO)**: 15 minutes
- **Recovery Point Objective (RPO)**: 5 minutes
- **Availability Target**: 99.9% uptime
- **Data Integrity**: 100% data consistency

### **Business Impact Classification**
- **Critical**: N.L.D.S. API service, Authentication system
- **High**: Database, Cache, Configuration
- **Medium**: Logs, Metrics, Monitoring data
- **Low**: Temporary files, Build artifacts

## **Backup Strategy**

### **Database Backup**

#### **PostgreSQL Continuous Backup**
```yaml
# PostgreSQL Backup Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-backup-config
  namespace: nlds
data:
  backup-script.sh: |
    #!/bin/bash
    
    # Configuration
    BACKUP_DIR="/backups/postgres"
    RETENTION_DAYS=30
    S3_BUCKET="nlds-backups-prod"
    
    # Create backup directory
    mkdir -p $BACKUP_DIR
    
    # Full backup (daily)
    if [ "$(date +%H)" = "02" ]; then
        echo "Creating full backup..."
        pg_basebackup -h postgres-service -U backup_user -D $BACKUP_DIR/full_$(date +%Y%m%d_%H%M%S) -Ft -z -P
        
        # Upload to S3
        aws s3 sync $BACKUP_DIR/full_$(date +%Y%m%d_%H%M%S) s3://$S3_BUCKET/postgres/full/$(date +%Y%m%d_%H%M%S)/
    fi
    
    # Incremental backup (every 15 minutes)
    echo "Creating WAL archive..."
    pg_receivewal -h postgres-service -U replication_user -D $BACKUP_DIR/wal --synchronous
    
    # Upload WAL files to S3
    aws s3 sync $BACKUP_DIR/wal s3://$S3_BUCKET/postgres/wal/
    
    # Cleanup old backups
    find $BACKUP_DIR -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \;
    
    # Verify backup integrity
    pg_verifybackup $BACKUP_DIR/full_$(date +%Y%m%d_%H%M%S)
```

#### **Automated Backup CronJob**
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: nlds
spec:
  schedule: "*/15 * * * *"  # Every 15 minutes
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: postgres-backup
            image: postgres:14-alpine
            command: ["/bin/bash", "/scripts/backup-script.sh"]
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-backup-secret
                  key: password
            volumeMounts:
            - name: backup-scripts
              mountPath: /scripts
            - name: backup-storage
              mountPath: /backups
          volumes:
          - name: backup-scripts
            configMap:
              name: postgres-backup-config
              defaultMode: 0755
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-storage-pvc
          restartPolicy: OnFailure
```

### **Redis Backup**

#### **Redis Snapshot Backup**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-backup-config
  namespace: nlds
data:
  redis-backup.sh: |
    #!/bin/bash
    
    BACKUP_DIR="/backups/redis"
    S3_BUCKET="nlds-backups-prod"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    
    # Create backup directory
    mkdir -p $BACKUP_DIR
    
    # Create Redis snapshot
    redis-cli -h redis-service BGSAVE
    
    # Wait for backup to complete
    while [ $(redis-cli -h redis-service LASTSAVE) -eq $(redis-cli -h redis-service LASTSAVE) ]; do
        sleep 1
    done
    
    # Copy RDB file
    cp /data/dump.rdb $BACKUP_DIR/redis_backup_$TIMESTAMP.rdb
    
    # Compress backup
    gzip $BACKUP_DIR/redis_backup_$TIMESTAMP.rdb
    
    # Upload to S3
    aws s3 cp $BACKUP_DIR/redis_backup_$TIMESTAMP.rdb.gz s3://$S3_BUCKET/redis/
    
    # Cleanup old backups (keep 7 days)
    find $BACKUP_DIR -name "*.rdb.gz" -mtime +7 -delete
    
    echo "Redis backup completed: redis_backup_$TIMESTAMP.rdb.gz"
```

### **Application Configuration Backup**

#### **Kubernetes Configuration Backup**
```bash
#!/bin/bash
# kubernetes-backup.sh

BACKUP_DIR="/backups/kubernetes"
S3_BUCKET="nlds-backups-prod"
NAMESPACE="nlds"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR/$TIMESTAMP

# Backup all Kubernetes resources
kubectl get all,configmaps,secrets,pvc,ingress -n $NAMESPACE -o yaml > $BACKUP_DIR/$TIMESTAMP/nlds-resources.yaml

# Backup RBAC
kubectl get roles,rolebindings,serviceaccounts -n $NAMESPACE -o yaml > $BACKUP_DIR/$TIMESTAMP/nlds-rbac.yaml

# Backup network policies
kubectl get networkpolicies -n $NAMESPACE -o yaml > $BACKUP_DIR/$TIMESTAMP/nlds-network.yaml

# Backup custom resources
kubectl get certificates,issuers -n $NAMESPACE -o yaml > $BACKUP_DIR/$TIMESTAMP/nlds-certs.yaml

# Create archive
tar -czf $BACKUP_DIR/kubernetes_backup_$TIMESTAMP.tar.gz -C $BACKUP_DIR $TIMESTAMP

# Upload to S3
aws s3 cp $BACKUP_DIR/kubernetes_backup_$TIMESTAMP.tar.gz s3://$S3_BUCKET/kubernetes/

# Cleanup
rm -rf $BACKUP_DIR/$TIMESTAMP
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Kubernetes backup completed: kubernetes_backup_$TIMESTAMP.tar.gz"
```

### **Application Data Backup**

#### **N.L.D.S. Application State Backup**
```python
#!/usr/bin/env python3
# nlds-data-backup.py

import os
import json
import boto3
import psycopg2
import redis
from datetime import datetime
from pathlib import Path

class NLDSDataBackup:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir = Path(f"/backups/nlds/{self.timestamp}")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # AWS S3 client
        self.s3 = boto3.client('s3')
        self.bucket = 'nlds-backups-prod'
        
        # Database connection
        self.db_conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'postgres-service'),
            database=os.getenv('POSTGRES_DB', 'nlds'),
            user=os.getenv('POSTGRES_USER', 'nlds'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        
        # Redis connection
        self.redis_conn = redis.Redis(
            host=os.getenv('REDIS_HOST', 'redis-service'),
            port=int(os.getenv('REDIS_PORT', '6379')),
            password=os.getenv('REDIS_PASSWORD'),
            decode_responses=True
        )
    
    def backup_user_sessions(self):
        """Backup active user sessions"""
        print("Backing up user sessions...")
        
        cursor = self.db_conn.cursor()
        cursor.execute("""
            SELECT session_id, user_id, created_at, expires_at, session_data
            FROM user_sessions 
            WHERE expires_at > NOW()
        """)
        
        sessions = cursor.fetchall()
        
        backup_data = {
            'timestamp': self.timestamp,
            'session_count': len(sessions),
            'sessions': [
                {
                    'session_id': row[0],
                    'user_id': row[1],
                    'created_at': row[2].isoformat(),
                    'expires_at': row[3].isoformat(),
                    'session_data': row[4]
                }
                for row in sessions
            ]
        }
        
        with open(self.backup_dir / 'user_sessions.json', 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        cursor.close()
        print(f"Backed up {len(sessions)} active sessions")
    
    def backup_processing_cache(self):
        """Backup Redis processing cache"""
        print("Backing up processing cache...")
        
        # Get all cache keys
        cache_keys = self.redis_conn.keys('nlds:cache:*')
        
        cache_data = {
            'timestamp': self.timestamp,
            'cache_entries': {}
        }
        
        for key in cache_keys:
            try:
                value = self.redis_conn.get(key)
                ttl = self.redis_conn.ttl(key)
                cache_data['cache_entries'][key] = {
                    'value': value,
                    'ttl': ttl
                }
            except Exception as e:
                print(f"Error backing up cache key {key}: {e}")
        
        with open(self.backup_dir / 'processing_cache.json', 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        print(f"Backed up {len(cache_keys)} cache entries")
    
    def backup_api_keys(self):
        """Backup API key configurations"""
        print("Backing up API key configurations...")
        
        cursor = self.db_conn.cursor()
        cursor.execute("""
            SELECT key_id, key_name, key_type, permissions, created_at, last_used
            FROM api_keys 
            WHERE active = true
        """)
        
        api_keys = cursor.fetchall()
        
        backup_data = {
            'timestamp': self.timestamp,
            'api_key_count': len(api_keys),
            'api_keys': [
                {
                    'key_id': row[0],
                    'key_name': row[1],
                    'key_type': row[2],
                    'permissions': row[3],
                    'created_at': row[4].isoformat(),
                    'last_used': row[5].isoformat() if row[5] else None
                }
                for row in api_keys
            ]
        }
        
        with open(self.backup_dir / 'api_keys.json', 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        cursor.close()
        print(f"Backed up {len(api_keys)} API key configurations")
    
    def backup_system_metrics(self):
        """Backup recent system metrics"""
        print("Backing up system metrics...")
        
        cursor = self.db_conn.cursor()
        cursor.execute("""
            SELECT metric_name, metric_value, timestamp, labels
            FROM system_metrics 
            WHERE timestamp > NOW() - INTERVAL '24 hours'
            ORDER BY timestamp DESC
        """)
        
        metrics = cursor.fetchall()
        
        backup_data = {
            'timestamp': self.timestamp,
            'metric_count': len(metrics),
            'time_range': '24 hours',
            'metrics': [
                {
                    'metric_name': row[0],
                    'metric_value': row[1],
                    'timestamp': row[2].isoformat(),
                    'labels': row[3]
                }
                for row in metrics
            ]
        }
        
        with open(self.backup_dir / 'system_metrics.json', 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        cursor.close()
        print(f"Backed up {len(metrics)} system metrics")
    
    def create_backup_manifest(self):
        """Create backup manifest with metadata"""
        manifest = {
            'backup_id': f"nlds_backup_{self.timestamp}",
            'timestamp': self.timestamp,
            'version': '2.2.0',
            'backup_type': 'application_data',
            'files': [
                'user_sessions.json',
                'processing_cache.json',
                'api_keys.json',
                'system_metrics.json'
            ],
            'retention_policy': {
                'daily_retention': 30,
                'weekly_retention': 12,
                'monthly_retention': 12
            }
        }
        
        with open(self.backup_dir / 'manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)
    
    def upload_to_s3(self):
        """Upload backup to S3"""
        print("Uploading backup to S3...")
        
        # Create tar archive
        import tarfile
        archive_path = f"/backups/nlds_data_backup_{self.timestamp}.tar.gz"
        
        with tarfile.open(archive_path, 'w:gz') as tar:
            tar.add(self.backup_dir, arcname=f"nlds_backup_{self.timestamp}")
        
        # Upload to S3
        s3_key = f"nlds/application_data/nlds_data_backup_{self.timestamp}.tar.gz"
        self.s3.upload_file(archive_path, self.bucket, s3_key)
        
        print(f"Backup uploaded to s3://{self.bucket}/{s3_key}")
        
        # Cleanup local files
        os.remove(archive_path)
        import shutil
        shutil.rmtree(self.backup_dir)
    
    def run_backup(self):
        """Execute complete backup process"""
        try:
            print(f"Starting N.L.D.S. data backup: {self.timestamp}")
            
            self.backup_user_sessions()
            self.backup_processing_cache()
            self.backup_api_keys()
            self.backup_system_metrics()
            self.create_backup_manifest()
            self.upload_to_s3()
            
            print("N.L.D.S. data backup completed successfully")
            
        except Exception as e:
            print(f"Backup failed: {e}")
            raise
        finally:
            self.db_conn.close()

if __name__ == "__main__":
    backup = NLDSDataBackup()
    backup.run_backup()
```

## **Disaster Recovery Procedures**

### **Recovery Scenarios**

#### **Scenario 1: Single Pod Failure**
**RTO**: 2 minutes | **RPO**: 0 minutes

```bash
# Automatic recovery via Kubernetes
# 1. Kubernetes detects pod failure
# 2. Automatically restarts pod
# 3. Load balancer routes traffic to healthy pods
# 4. No manual intervention required

# Verification steps:
kubectl get pods -n nlds
kubectl describe pod <failed-pod-name> -n nlds
kubectl logs <new-pod-name> -n nlds
```

#### **Scenario 2: Database Failure**
**RTO**: 10 minutes | **RPO**: 5 minutes

```bash
#!/bin/bash
# database-recovery.sh

echo "Starting database recovery procedure..."

# 1. Assess damage
kubectl get pods -n nlds -l app.kubernetes.io/name=postgres

# 2. Stop application pods to prevent data corruption
kubectl scale deployment nlds-api --replicas=0 -n nlds

# 3. Restore from latest backup
LATEST_BACKUP=$(aws s3 ls s3://nlds-backups-prod/postgres/full/ | sort | tail -n 1 | awk '{print $4}')
aws s3 sync s3://nlds-backups-prod/postgres/full/$LATEST_BACKUP /tmp/postgres-restore/

# 4. Restore database
kubectl exec -it postgres-0 -n nlds -- pg_restore -d nlds /tmp/postgres-restore/

# 5. Apply WAL files for point-in-time recovery
kubectl exec -it postgres-0 -n nlds -- pg_receivewal --synchronous

# 6. Verify database integrity
kubectl exec -it postgres-0 -n nlds -- psql -d nlds -c "SELECT COUNT(*) FROM user_sessions;"

# 7. Restart application
kubectl scale deployment nlds-api --replicas=3 -n nlds

# 8. Verify application health
kubectl get pods -n nlds
curl -f https://api.jaegis.ai/health

echo "Database recovery completed"
```

#### **Scenario 3: Complete Cluster Failure**
**RTO**: 15 minutes | **RPO**: 5 minutes

```bash
#!/bin/bash
# cluster-recovery.sh

echo "Starting complete cluster recovery..."

# 1. Provision new Kubernetes cluster
# (Assuming infrastructure as code deployment)
terraform apply -var="cluster_name=nlds-recovery"

# 2. Restore Kubernetes configurations
kubectl apply -f /backups/kubernetes/latest/nlds-resources.yaml
kubectl apply -f /backups/kubernetes/latest/nlds-rbac.yaml
kubectl apply -f /backups/kubernetes/latest/nlds-network.yaml

# 3. Restore secrets (from secure backup)
kubectl create secret generic nlds-secrets \
  --from-literal=NLDS_JWT_SECRET=$JWT_SECRET \
  --from-literal=NLDS_DATABASE_PASSWORD=$DB_PASSWORD \
  --from-literal=NLDS_REDIS_PASSWORD=$REDIS_PASSWORD \
  -n nlds

# 4. Restore persistent volumes
kubectl apply -f /backups/kubernetes/latest/nlds-pv.yaml

# 5. Restore database
./database-recovery.sh

# 6. Restore Redis cache
kubectl exec -it redis-0 -n nlds -- redis-cli FLUSHALL
kubectl cp /backups/redis/latest/dump.rdb redis-0:/data/dump.rdb -n nlds
kubectl delete pod redis-0 -n nlds  # Restart to load backup

# 7. Deploy applications
kubectl apply -f deployment/kubernetes/nlds-deployment.yaml

# 8. Verify complete system
./health-check.sh

echo "Cluster recovery completed"
```

### **Recovery Testing**

#### **Monthly Disaster Recovery Drill**
```bash
#!/bin/bash
# dr-drill.sh

echo "Starting monthly DR drill..."

# 1. Create test environment
kubectl create namespace nlds-dr-test

# 2. Deploy from backups
./cluster-recovery.sh --namespace=nlds-dr-test --test-mode

# 3. Run automated tests
python -m pytest tests/dr/ --namespace=nlds-dr-test

# 4. Performance validation
./load-test.sh --target=nlds-dr-test.jaegis.ai

# 5. Generate DR report
./generate-dr-report.sh

# 6. Cleanup test environment
kubectl delete namespace nlds-dr-test

echo "DR drill completed"
```

## **Backup Monitoring & Alerting**

### **Backup Health Monitoring**
```yaml
# Backup monitoring alerts
- alert: BackupFailed
  expr: |
    increase(backup_job_failures_total[1h]) > 0
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Backup job failed"
    description: "Backup job {{ $labels.job }} has failed"

- alert: BackupDelayed
  expr: |
    time() - backup_last_success_timestamp > 3600
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "Backup is delayed"
    description: "No successful backup in the last hour"
```

---

**Document Version**: 1.0  
**Last Updated**: July 26, 2025  
**Next Review**: August 26, 2025  
**Owner**: N.L.D.S. Operations Team
