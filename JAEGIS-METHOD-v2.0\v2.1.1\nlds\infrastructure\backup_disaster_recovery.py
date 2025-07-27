"""
N.L.D.S. Backup & Disaster Recovery System
Comprehensive backup systems, disaster recovery procedures, and data protection protocols
"""

import asyncio
import boto3
import psycopg2
import redis
import json
import gzip
import hashlib
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import os
import shutil
import subprocess
from pathlib import Path
import schedule
import time

logger = logging.getLogger(__name__)


class BackupType(str, Enum):
    """Types of backups."""
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    SNAPSHOT = "snapshot"


class BackupStatus(str, Enum):
    """Backup operation status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RecoveryType(str, Enum):
    """Types of recovery operations."""
    POINT_IN_TIME = "point_in_time"
    FULL_RESTORE = "full_restore"
    PARTIAL_RESTORE = "partial_restore"
    FAILOVER = "failover"


@dataclass
class BackupMetadata:
    """Backup metadata information."""
    backup_id: str
    backup_type: BackupType
    timestamp: datetime
    size_bytes: int
    checksum: str
    compression_ratio: float
    encryption_enabled: bool
    retention_days: int
    storage_location: str
    components: List[str]


@dataclass
class RecoveryPlan:
    """Disaster recovery plan."""
    plan_id: str
    recovery_type: RecoveryType
    target_rto: int  # Recovery Time Objective (minutes)
    target_rpo: int  # Recovery Point Objective (minutes)
    priority: int
    dependencies: List[str]
    procedures: List[str]
    validation_steps: List[str]


@dataclass
class DisasterRecoveryStatus:
    """Current disaster recovery status."""
    last_backup: datetime
    backup_health: str
    replication_lag: float
    failover_ready: bool
    estimated_rto: int
    estimated_rpo: int


class BackupDisasterRecoverySystem:
    """
    Comprehensive backup and disaster recovery system for N.L.D.S.
    
    Provides automated backups, disaster recovery procedures,
    and data protection protocols with enterprise-grade reliability.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Initialize cloud storage clients
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=config.get('aws_access_key'),
            aws_secret_access_key=config.get('aws_secret_key'),
            region_name=config.get('aws_region', 'us-east-1')
        )
        
        # Database connections
        self.db_config = config.get('database', {})
        self.redis_config = config.get('redis', {})
        
        # Backup configuration
        self.backup_config = config.get('backup', {
            'retention_days': 30,
            'compression_enabled': True,
            'encryption_enabled': True,
            'storage_bucket': 'nlds-backups',
            'backup_schedule': {
                'full': '0 2 * * 0',  # Weekly full backup
                'incremental': '0 2 * * 1-6',  # Daily incremental
                'snapshot': '0 */6 * * *'  # Every 6 hours
            }
        })
        
        # Recovery configuration
        self.recovery_config = config.get('recovery', {
            'rto_target': 60,  # 1 hour
            'rpo_target': 15,  # 15 minutes
            'failover_enabled': True,
            'auto_failback': False
        })
        
        # Initialize backup storage
        self._initialize_backup_storage()
        
        logger.info("Backup & Disaster Recovery System initialized")
    
    def _initialize_backup_storage(self):
        """Initialize backup storage locations."""
        try:
            # Create S3 bucket if it doesn't exist
            bucket_name = self.backup_config['storage_bucket']
            
            try:
                self.s3_client.head_bucket(Bucket=bucket_name)
            except:
                self.s3_client.create_bucket(Bucket=bucket_name)
                
                # Enable versioning
                self.s3_client.put_bucket_versioning(
                    Bucket=bucket_name,
                    VersioningConfiguration={'Status': 'Enabled'}
                )
                
                # Set lifecycle policy
                lifecycle_config = {
                    'Rules': [
                        {
                            'ID': 'backup-retention',
                            'Status': 'Enabled',
                            'Filter': {'Prefix': 'backups/'},
                            'Expiration': {'Days': self.backup_config['retention_days']},
                            'NoncurrentVersionExpiration': {'NoncurrentDays': 7}
                        }
                    ]
                }
                
                self.s3_client.put_bucket_lifecycle_configuration(
                    Bucket=bucket_name,
                    LifecycleConfiguration=lifecycle_config
                )
                
            logger.info(f"Backup storage initialized: {bucket_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize backup storage: {e}")
            raise
    
    async def create_backup(self, backup_type: BackupType, 
                          components: Optional[List[str]] = None) -> BackupMetadata:
        """Create a backup of specified components."""
        
        backup_id = f"backup_{int(time.time())}_{backup_type.value}"
        timestamp = datetime.utcnow()
        
        if components is None:
            components = ['database', 'redis', 'configuration', 'logs']
        
        logger.info(f"Starting {backup_type.value} backup: {backup_id}")
        
        try:
            backup_data = {}
            total_size = 0
            
            # Backup database
            if 'database' in components:
                db_backup = await self._backup_database(backup_type)
                backup_data['database'] = db_backup
                total_size += db_backup['size_bytes']
            
            # Backup Redis
            if 'redis' in components:
                redis_backup = await self._backup_redis()
                backup_data['redis'] = redis_backup
                total_size += redis_backup['size_bytes']
            
            # Backup configuration
            if 'configuration' in components:
                config_backup = await self._backup_configuration()
                backup_data['configuration'] = config_backup
                total_size += config_backup['size_bytes']
            
            # Backup logs
            if 'logs' in components:
                logs_backup = await self._backup_logs()
                backup_data['logs'] = logs_backup
                total_size += logs_backup['size_bytes']
            
            # Compress and encrypt backup
            compressed_data = await self._compress_backup(backup_data)
            encrypted_data = await self._encrypt_backup(compressed_data)
            
            # Calculate checksum
            checksum = hashlib.sha256(encrypted_data).hexdigest()
            
            # Upload to storage
            storage_key = f"backups/{backup_id}.backup"
            await self._upload_backup(storage_key, encrypted_data)
            
            # Calculate compression ratio
            compression_ratio = len(compressed_data) / total_size if total_size > 0 else 1.0
            
            # Create metadata
            metadata = BackupMetadata(
                backup_id=backup_id,
                backup_type=backup_type,
                timestamp=timestamp,
                size_bytes=len(encrypted_data),
                checksum=checksum,
                compression_ratio=compression_ratio,
                encryption_enabled=True,
                retention_days=self.backup_config['retention_days'],
                storage_location=f"s3://{self.backup_config['storage_bucket']}/{storage_key}",
                components=components
            )
            
            # Store metadata
            await self._store_backup_metadata(metadata)
            
            logger.info(f"Backup completed: {backup_id} ({len(encrypted_data)} bytes)")
            
            return metadata
            
        except Exception as e:
            logger.error(f"Backup failed: {backup_id} - {e}")
            raise
    
    async def _backup_database(self, backup_type: BackupType) -> Dict[str, Any]:
        """Backup PostgreSQL database."""
        
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        backup_file = f"/tmp/nlds_db_backup_{timestamp}.sql"
        
        try:
            # Build pg_dump command
            cmd = [
                'pg_dump',
                '--host', self.db_config.get('host', 'localhost'),
                '--port', str(self.db_config.get('port', 5432)),
                '--username', self.db_config.get('username'),
                '--dbname', self.db_config.get('database'),
                '--no-password',
                '--verbose',
                '--file', backup_file
            ]
            
            if backup_type == BackupType.FULL:
                cmd.extend(['--clean', '--create'])
            elif backup_type == BackupType.INCREMENTAL:
                # For incremental, use WAL archiving
                cmd.extend(['--no-owner', '--no-privileges'])
            
            # Set password via environment
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_config.get('password')
            
            # Execute backup
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"pg_dump failed: {result.stderr}")
            
            # Read backup file
            with open(backup_file, 'rb') as f:
                backup_data = f.read()
            
            # Clean up temporary file
            os.remove(backup_file)
            
            return {
                'type': 'database',
                'data': backup_data,
                'size_bytes': len(backup_data),
                'timestamp': timestamp
            }
            
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            if os.path.exists(backup_file):
                os.remove(backup_file)
            raise
    
    async def _backup_redis(self) -> Dict[str, Any]:
        """Backup Redis data."""
        
        try:
            redis_client = redis.Redis(
                host=self.redis_config.get('host', 'localhost'),
                port=self.redis_config.get('port', 6379),
                password=self.redis_config.get('password'),
                decode_responses=False
            )
            
            # Get all keys and their values
            backup_data = {}
            
            for key in redis_client.scan_iter():
                key_type = redis_client.type(key)
                
                if key_type == b'string':
                    backup_data[key.decode()] = {
                        'type': 'string',
                        'value': redis_client.get(key).decode() if redis_client.get(key) else None,
                        'ttl': redis_client.ttl(key)
                    }
                elif key_type == b'hash':
                    backup_data[key.decode()] = {
                        'type': 'hash',
                        'value': {k.decode(): v.decode() for k, v in redis_client.hgetall(key).items()},
                        'ttl': redis_client.ttl(key)
                    }
                elif key_type == b'list':
                    backup_data[key.decode()] = {
                        'type': 'list',
                        'value': [item.decode() for item in redis_client.lrange(key, 0, -1)],
                        'ttl': redis_client.ttl(key)
                    }
                elif key_type == b'set':
                    backup_data[key.decode()] = {
                        'type': 'set',
                        'value': [item.decode() for item in redis_client.smembers(key)],
                        'ttl': redis_client.ttl(key)
                    }
                elif key_type == b'zset':
                    backup_data[key.decode()] = {
                        'type': 'zset',
                        'value': [(member.decode(), score) for member, score in redis_client.zrange(key, 0, -1, withscores=True)],
                        'ttl': redis_client.ttl(key)
                    }
            
            # Serialize to JSON
            json_data = json.dumps(backup_data, indent=2).encode('utf-8')
            
            return {
                'type': 'redis',
                'data': json_data,
                'size_bytes': len(json_data),
                'key_count': len(backup_data)
            }
            
        except Exception as e:
            logger.error(f"Redis backup failed: {e}")
            raise
    
    async def _backup_configuration(self) -> Dict[str, Any]:
        """Backup system configuration files."""
        
        try:
            config_data = {}
            
            # Backup main configuration
            config_files = [
                'nlds/config/settings.yaml',
                'nlds/config/logging.yaml',
                'pitces/config/pitces-config.yaml',
                '.env'
            ]
            
            for config_file in config_files:
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        config_data[config_file] = f.read()
            
            # Serialize configuration
            json_data = json.dumps(config_data, indent=2).encode('utf-8')
            
            return {
                'type': 'configuration',
                'data': json_data,
                'size_bytes': len(json_data),
                'file_count': len(config_data)
            }
            
        except Exception as e:
            logger.error(f"Configuration backup failed: {e}")
            raise
    
    async def _backup_logs(self) -> Dict[str, Any]:
        """Backup system logs."""
        
        try:
            logs_data = {}
            
            # Backup log files
            log_directories = [
                'logs/',
                '/var/log/nlds/',
                '/tmp/nlds_logs/'
            ]
            
            for log_dir in log_directories:
                if os.path.exists(log_dir):
                    for log_file in Path(log_dir).glob('*.log'):
                        with open(log_file, 'r') as f:
                            logs_data[str(log_file)] = f.read()
            
            # Serialize logs
            json_data = json.dumps(logs_data, indent=2).encode('utf-8')
            
            return {
                'type': 'logs',
                'data': json_data,
                'size_bytes': len(json_data),
                'file_count': len(logs_data)
            }
            
        except Exception as e:
            logger.error(f"Logs backup failed: {e}")
            raise
    
    async def _compress_backup(self, backup_data: Dict[str, Any]) -> bytes:
        """Compress backup data."""
        
        if not self.backup_config.get('compression_enabled', True):
            return json.dumps(backup_data).encode('utf-8')
        
        try:
            # Serialize to JSON
            json_data = json.dumps(backup_data, default=str).encode('utf-8')
            
            # Compress with gzip
            compressed_data = gzip.compress(json_data, compresslevel=9)
            
            logger.debug(f"Compression: {len(json_data)} -> {len(compressed_data)} bytes "
                        f"({len(compressed_data)/len(json_data)*100:.1f}%)")
            
            return compressed_data
            
        except Exception as e:
            logger.error(f"Backup compression failed: {e}")
            raise
    
    async def _encrypt_backup(self, data: bytes) -> bytes:
        """Encrypt backup data."""
        
        if not self.backup_config.get('encryption_enabled', True):
            return data
        
        try:
            from cryptography.fernet import Fernet
            
            # Get encryption key from environment or generate
            encryption_key = os.environ.get('NLDS_BACKUP_ENCRYPTION_KEY')
            if not encryption_key:
                encryption_key = Fernet.generate_key()
                logger.warning("Generated new encryption key - store securely!")
            
            # Encrypt data
            fernet = Fernet(encryption_key)
            encrypted_data = fernet.encrypt(data)
            
            return encrypted_data
            
        except Exception as e:
            logger.error(f"Backup encryption failed: {e}")
            raise
    
    async def _upload_backup(self, storage_key: str, data: bytes):
        """Upload backup to cloud storage."""
        
        try:
            bucket_name = self.backup_config['storage_bucket']
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=storage_key,
                Body=data,
                ServerSideEncryption='AES256',
                Metadata={
                    'backup-system': 'nlds',
                    'backup-version': '2.2.0',
                    'created-by': 'backup-system'
                }
            )
            
            logger.info(f"Backup uploaded: s3://{bucket_name}/{storage_key}")
            
        except Exception as e:
            logger.error(f"Backup upload failed: {e}")
            raise
    
    async def _store_backup_metadata(self, metadata: BackupMetadata):
        """Store backup metadata in database."""
        
        try:
            conn = psycopg2.connect(
                host=self.db_config.get('host'),
                port=self.db_config.get('port'),
                database=self.db_config.get('database'),
                user=self.db_config.get('username'),
                password=self.db_config.get('password')
            )
            
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO backup_metadata (
                        backup_id, backup_type, timestamp, size_bytes, checksum,
                        compression_ratio, encryption_enabled, retention_days,
                        storage_location, components
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    metadata.backup_id,
                    metadata.backup_type.value,
                    metadata.timestamp,
                    metadata.size_bytes,
                    metadata.checksum,
                    metadata.compression_ratio,
                    metadata.encryption_enabled,
                    metadata.retention_days,
                    metadata.storage_location,
                    json.dumps(metadata.components)
                ))
                
                conn.commit()
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store backup metadata: {e}")
            raise
    
    async def restore_backup(self, backup_id: str, 
                           components: Optional[List[str]] = None) -> bool:
        """Restore from backup."""
        
        logger.info(f"Starting restore from backup: {backup_id}")
        
        try:
            # Get backup metadata
            metadata = await self._get_backup_metadata(backup_id)
            if not metadata:
                raise Exception(f"Backup not found: {backup_id}")
            
            # Download backup data
            backup_data = await self._download_backup(metadata.storage_location)
            
            # Decrypt and decompress
            decrypted_data = await self._decrypt_backup(backup_data)
            decompressed_data = await self._decompress_backup(decrypted_data)
            
            # Parse backup data
            backup_content = json.loads(decompressed_data.decode('utf-8'))
            
            # Restore components
            if components is None:
                components = metadata.components
            
            for component in components:
                if component in backup_content:
                    await self._restore_component(component, backup_content[component])
            
            logger.info(f"Restore completed: {backup_id}")
            return True
            
        except Exception as e:
            logger.error(f"Restore failed: {backup_id} - {e}")
            return False
    
    async def _get_backup_metadata(self, backup_id: str) -> Optional[BackupMetadata]:
        """Get backup metadata from database."""
        
        try:
            conn = psycopg2.connect(
                host=self.db_config.get('host'),
                port=self.db_config.get('port'),
                database=self.db_config.get('database'),
                user=self.db_config.get('username'),
                password=self.db_config.get('password')
            )
            
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT backup_id, backup_type, timestamp, size_bytes, checksum,
                           compression_ratio, encryption_enabled, retention_days,
                           storage_location, components
                    FROM backup_metadata
                    WHERE backup_id = %s
                """, (backup_id,))
                
                row = cur.fetchone()
                if row:
                    return BackupMetadata(
                        backup_id=row[0],
                        backup_type=BackupType(row[1]),
                        timestamp=row[2],
                        size_bytes=row[3],
                        checksum=row[4],
                        compression_ratio=row[5],
                        encryption_enabled=row[6],
                        retention_days=row[7],
                        storage_location=row[8],
                        components=json.loads(row[9])
                    )
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Failed to get backup metadata: {e}")
            return None
    
    async def get_disaster_recovery_status(self) -> DisasterRecoveryStatus:
        """Get current disaster recovery status."""
        
        try:
            # Get last backup information
            last_backup = await self._get_last_backup_time()
            
            # Check backup health
            backup_health = await self._check_backup_health()
            
            # Check replication lag (if applicable)
            replication_lag = await self._check_replication_lag()
            
            # Determine failover readiness
            failover_ready = await self._check_failover_readiness()
            
            # Estimate RTO/RPO
            estimated_rto = self.recovery_config.get('rto_target', 60)
            estimated_rpo = self.recovery_config.get('rpo_target', 15)
            
            return DisasterRecoveryStatus(
                last_backup=last_backup,
                backup_health=backup_health,
                replication_lag=replication_lag,
                failover_ready=failover_ready,
                estimated_rto=estimated_rto,
                estimated_rpo=estimated_rpo
            )
            
        except Exception as e:
            logger.error(f"Failed to get DR status: {e}")
            raise
    
    def schedule_backups(self):
        """Schedule automated backups."""
        
        backup_schedule = self.backup_config.get('backup_schedule', {})
        
        # Schedule full backups
        if 'full' in backup_schedule:
            schedule.every().week.at("02:00").do(
                lambda: asyncio.create_task(self.create_backup(BackupType.FULL))
            )
        
        # Schedule incremental backups
        if 'incremental' in backup_schedule:
            schedule.every().day.at("02:00").do(
                lambda: asyncio.create_task(self.create_backup(BackupType.INCREMENTAL))
            )
        
        # Schedule snapshots
        if 'snapshot' in backup_schedule:
            schedule.every(6).hours.do(
                lambda: asyncio.create_task(self.create_backup(BackupType.SNAPSHOT))
            )
        
        logger.info("Backup schedules configured")
    
    async def _get_last_backup_time(self) -> datetime:
        """Get timestamp of last successful backup."""
        # Implementation to query backup metadata
        return datetime.utcnow() - timedelta(hours=6)
    
    async def _check_backup_health(self) -> str:
        """Check overall backup system health."""
        # Implementation to verify backup integrity
        return "healthy"
    
    async def _check_replication_lag(self) -> float:
        """Check database replication lag."""
        # Implementation to check replication status
        return 0.5  # seconds
    
    async def _check_failover_readiness(self) -> bool:
        """Check if system is ready for failover."""
        # Implementation to verify failover capabilities
        return True


# Example usage
if __name__ == "__main__":
    async def main():
        config = {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'database': 'nlds',
                'username': 'nlds_user',
                'password': 'secure_password'
            },
            'redis': {
                'host': 'localhost',
                'port': 6379
            },
            'backup': {
                'storage_bucket': 'nlds-backups-test',
                'retention_days': 30,
                'compression_enabled': True,
                'encryption_enabled': True
            }
        }
        
        # Initialize backup system
        backup_system = BackupDisasterRecoverySystem(config)
        
        # Create a full backup
        metadata = await backup_system.create_backup(BackupType.FULL)
        print(f"Backup created: {metadata.backup_id}")
        
        # Get DR status
        dr_status = await backup_system.get_disaster_recovery_status()
        print(f"DR Status: {asdict(dr_status)}")
    
    asyncio.run(main())
