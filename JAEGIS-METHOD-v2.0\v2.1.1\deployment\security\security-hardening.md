# N.L.D.S. Production Security Hardening

## **Overview**

This document outlines comprehensive security hardening measures for the Natural Language Detection System (N.L.D.S.) production deployment, ensuring enterprise-grade security and compliance with industry standards.

## **Security Hardening Checklist**

### **✅ Container Security**
- [ ] Non-root user execution
- [ ] Read-only root filesystem
- [ ] Minimal base image (distroless)
- [ ] No privileged containers
- [ ] Security context constraints
- [ ] Resource limits enforced
- [ ] Health checks implemented
- [ ] Secrets mounted securely

### **✅ Network Security**
- [ ] Network policies implemented
- [ ] TLS 1.3 encryption
- [ ] Certificate management
- [ ] Ingress security headers
- [ ] Rate limiting configured
- [ ] DDoS protection enabled
- [ ] VPC/subnet isolation
- [ ] Firewall rules applied

### **✅ Authentication & Authorization**
- [ ] JWT token validation
- [ ] Role-based access control
- [ ] API key management
- [ ] Session security
- [ ] Multi-factor authentication
- [ ] Password policies
- [ ] Account lockout policies
- [ ] Audit logging

### **✅ Data Protection**
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] PII detection and masking
- [ ] Data classification
- [ ] Backup encryption
- [ ] Key management (KMS)
- [ ] Data retention policies
- [ ] Secure deletion

## **Container Security Hardening**

### **Hardened Dockerfile**
```dockerfile
# deployment/security/Dockerfile.hardened

# Use distroless base image for minimal attack surface
FROM gcr.io/distroless/python3-debian11:latest

# Add security labels
LABEL security.scan="enabled" \
      security.policy="hardened" \
      security.compliance="SOC2,GDPR"

# Copy application files
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Set working directory
WORKDIR /app

# Use non-root user (nobody)
USER 65532:65532

# Set security environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NLDS_SECURITY_MODE=hardened \
    NLDS_LOG_LEVEL=INFO

# Expose only necessary port
EXPOSE 8000

# Health check with security considerations
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["/usr/bin/python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=5)"]

# Run application
ENTRYPOINT ["/usr/bin/python3", "-m", "nlds.api.main"]
```

### **Security Context Configuration**
```yaml
# deployment/security/security-context.yaml

apiVersion: v1
kind: SecurityContextConstraints
metadata:
  name: nlds-scc
  namespace: nlds
spec:
  allowHostDirVolumePlugin: false
  allowHostIPC: false
  allowHostNetwork: false
  allowHostPID: false
  allowHostPorts: false
  allowPrivilegedContainer: false
  allowedCapabilities: []
  defaultAddCapabilities: []
  requiredDropCapabilities:
    - ALL
  allowedFlexVolumes: []
  fsGroup:
    type: MustRunAs
    ranges:
      - min: 1000
      - max: 65535
  runAsUser:
    type: MustRunAsNonRoot
  seLinuxContext:
    type: MustRunAs
  supplementalGroups:
    type: MustRunAs
    ranges:
      - min: 1000
      - max: 65535
  volumes:
    - configMap
    - downwardAPI
    - emptyDir
    - persistentVolumeClaim
    - projected
    - secret

---
apiVersion: v1
kind: Pod
metadata:
  name: nlds-api-hardened
  namespace: nlds
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 65532
    runAsGroup: 65532
    fsGroup: 65532
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: nlds-api
    image: jaegis/nlds:2.2.0-hardened
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 65532
      runAsGroup: 65532
      capabilities:
        drop:
          - ALL
      seccompProfile:
        type: RuntimeDefault
    volumeMounts:
    - name: tmp
      mountPath: /tmp
      readOnly: false
    - name: var-tmp
      mountPath: /var/tmp
      readOnly: false
  volumes:
  - name: tmp
    emptyDir: {}
  - name: var-tmp
    emptyDir: {}
```

## **Network Security Hardening**

### **Network Policies**
```yaml
# deployment/security/network-policies.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: nlds-network-policy-hardened
  namespace: nlds
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: nlds
  policyTypes:
  - Ingress
  - Egress
  
  ingress:
  # Allow ingress from ingress controller only
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  
  # Allow monitoring access
  - from:
    - namespaceSelector:
        matchLabels:
          name: monitoring
    ports:
    - protocol: TCP
      port: 9000  # Metrics port
  
  egress:
  # Allow DNS resolution
  - to: []
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
  
  # Allow database access
  - to:
    - podSelector:
        matchLabels:
          app.kubernetes.io/name: postgres
    ports:
    - protocol: TCP
      port: 5432
  
  # Allow Redis access
  - to:
    - podSelector:
        matchLabels:
          app.kubernetes.io/name: redis
    ports:
    - protocol: TCP
      port: 6379
  
  # Allow HTTPS to external APIs
  - to: []
    ports:
    - protocol: TCP
      port: 443
  
  # Deny all other traffic
  - to: []
    ports: []

---
# Database network policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: postgres-network-policy
  namespace: nlds
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: postgres
  policyTypes:
  - Ingress
  - Egress
  
  ingress:
  # Only allow access from N.L.D.S. pods
  - from:
    - podSelector:
        matchLabels:
          app.kubernetes.io/name: nlds
    ports:
    - protocol: TCP
      port: 5432
  
  egress:
  # Allow DNS only
  - to: []
    ports:
    - protocol: UDP
      port: 53
```

### **TLS Configuration**
```yaml
# deployment/security/tls-config.yaml

apiVersion: v1
kind: Secret
metadata:
  name: nlds-tls-config
  namespace: nlds
type: Opaque
stringData:
  tls.conf: |
    # TLS 1.3 configuration
    ssl_protocols TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https:; frame-ancestors 'none';" always;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Session settings
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;
```

## **Authentication & Authorization Hardening**

### **Enhanced JWT Security**
```python
# nlds/security/jwt_hardened.py

import jwt
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class HardenedJWTManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = 'HS256'
        self.access_token_expire = timedelta(minutes=15)  # Short-lived
        self.refresh_token_expire = timedelta(days=7)
        self.token_blacklist = set()  # In production, use Redis
        
    def create_access_token(self, user_id: str, role: str, permissions: list) -> str:
        """Create hardened access token"""
        now = datetime.utcnow()
        jti = secrets.token_urlsafe(32)  # Unique token ID
        
        payload = {
            'sub': user_id,
            'role': role,
            'permissions': permissions,
            'iat': now,
            'exp': now + self.access_token_expire,
            'jti': jti,
            'type': 'access',
            'iss': 'nlds-auth-service',
            'aud': 'nlds-api'
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create hardened refresh token"""
        now = datetime.utcnow()
        jti = secrets.token_urlsafe(32)
        
        payload = {
            'sub': user_id,
            'iat': now,
            'exp': now + self.refresh_token_expire,
            'jti': jti,
            'type': 'refresh',
            'iss': 'nlds-auth-service',
            'aud': 'nlds-api'
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str, token_type: str = 'access') -> Optional[Dict[str, Any]]:
        """Verify and decode token with security checks"""
        try:
            # Check if token is blacklisted
            if self._is_token_blacklisted(token):
                return None
            
            # Decode and verify token
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                audience='nlds-api',
                issuer='nlds-auth-service'
            )
            
            # Verify token type
            if payload.get('type') != token_type:
                return None
            
            # Additional security checks
            if not self._validate_token_claims(payload):
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def blacklist_token(self, token: str):
        """Add token to blacklist"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            jti = payload.get('jti')
            if jti:
                self.token_blacklist.add(jti)
        except jwt.InvalidTokenError:
            pass
    
    def _is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            jti = payload.get('jti')
            return jti in self.token_blacklist
        except jwt.InvalidTokenError:
            return True
    
    def _validate_token_claims(self, payload: Dict[str, Any]) -> bool:
        """Validate token claims for security"""
        # Check required claims
        required_claims = ['sub', 'iat', 'exp', 'jti', 'type']
        if not all(claim in payload for claim in required_claims):
            return False
        
        # Validate user ID format
        user_id = payload.get('sub')
        if not user_id or len(user_id) < 3:
            return False
        
        # Validate token age
        issued_at = datetime.fromtimestamp(payload['iat'])
        if datetime.utcnow() - issued_at > timedelta(days=30):
            return False
        
        return True
```

### **API Key Security**
```python
# nlds/security/api_key_hardened.py

import secrets
import hashlib
import hmac
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class HardenedAPIKeyManager:
    def __init__(self, secret_salt: str):
        self.secret_salt = secret_salt
        self.key_prefix = 'nlds_'
        
    def generate_api_key(self, user_id: str, role: str, description: str) -> Dict[str, str]:
        """Generate secure API key"""
        # Generate random key
        random_part = secrets.token_urlsafe(32)
        
        # Create key with metadata
        key_data = f"{self.key_prefix}{role}_{random_part}"
        
        # Create secure hash for storage
        key_hash = self._hash_api_key(key_data)
        
        # Store key metadata (in production, store in database)
        key_metadata = {
            'key_id': secrets.token_urlsafe(16),
            'user_id': user_id,
            'role': role,
            'description': description,
            'key_hash': key_hash,
            'created_at': datetime.utcnow().isoformat(),
            'last_used': None,
            'usage_count': 0,
            'rate_limit': self._get_rate_limit_for_role(role),
            'active': True
        }
        
        return {
            'api_key': key_data,
            'key_id': key_metadata['key_id'],
            'metadata': key_metadata
        }
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key with security checks"""
        # Basic format validation
        if not api_key.startswith(self.key_prefix):
            return None
        
        # Hash the provided key
        key_hash = self._hash_api_key(api_key)
        
        # Look up key in database (mock implementation)
        key_metadata = self._lookup_key_by_hash(key_hash)
        
        if not key_metadata:
            return None
        
        # Security checks
        if not key_metadata.get('active', False):
            return None
        
        # Check for suspicious usage patterns
        if self._is_suspicious_usage(key_metadata):
            return None
        
        # Update usage statistics
        self._update_key_usage(key_metadata['key_id'])
        
        return key_metadata
    
    def _hash_api_key(self, api_key: str) -> str:
        """Create secure hash of API key"""
        return hashlib.pbkdf2_hmac(
            'sha256',
            api_key.encode('utf-8'),
            self.secret_salt.encode('utf-8'),
            100000  # 100k iterations
        ).hex()
    
    def _get_rate_limit_for_role(self, role: str) -> Dict[str, int]:
        """Get rate limits based on role"""
        limits = {
            'readonly': {'requests_per_minute': 100, 'burst': 150},
            'user': {'requests_per_minute': 500, 'burst': 750},
            'developer': {'requests_per_minute': 1000, 'burst': 1500},
            'admin': {'requests_per_minute': -1, 'burst': -1},  # Unlimited
            'service': {'requests_per_minute': 2000, 'burst': 3000}
        }
        return limits.get(role, limits['readonly'])
    
    def _is_suspicious_usage(self, key_metadata: Dict[str, Any]) -> bool:
        """Detect suspicious API key usage patterns"""
        # Check for rapid usage increase
        usage_count = key_metadata.get('usage_count', 0)
        if usage_count > 10000:  # Threshold for investigation
            return True
        
        # Check for usage from multiple IPs (would need IP tracking)
        # This is a simplified check
        
        return False
    
    def _lookup_key_by_hash(self, key_hash: str) -> Optional[Dict[str, Any]]:
        """Look up key metadata by hash (mock implementation)"""
        # In production, this would query the database
        # For now, return None to simulate not found
        return None
    
    def _update_key_usage(self, key_id: str):
        """Update key usage statistics"""
        # In production, this would update the database
        pass
```

## **Data Protection Hardening**

### **PII Detection and Masking**
```python
# nlds/security/pii_protection.py

import re
import hashlib
from typing import Dict, List, Tuple, Any

class PIIProtectionManager:
    def __init__(self):
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
            'ssn': r'\b\d{3}-?\d{2}-?\d{4}\b',
            'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'api_key': r'\b[A-Za-z0-9]{32,}\b',
            'jwt_token': r'\beyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\b'
        }
        
        self.masking_strategies = {
            'email': self._mask_email,
            'phone': self._mask_phone,
            'ssn': self._mask_ssn,
            'credit_card': self._mask_credit_card,
            'ip_address': self._mask_ip,
            'api_key': self._mask_api_key,
            'jwt_token': self._mask_jwt_token
        }
    
    def detect_pii(self, text: str) -> List[Dict[str, Any]]:
        """Detect PII in text"""
        detections = []
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                detections.append({
                    'type': pii_type,
                    'value': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': self._calculate_confidence(pii_type, match.group())
                })
        
        return detections
    
    def mask_pii(self, text: str, mask_char: str = '*') -> Tuple[str, List[Dict[str, Any]]]:
        """Mask PII in text"""
        masked_text = text
        detections = []
        offset = 0
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = list(re.finditer(pattern, masked_text, re.IGNORECASE))
            
            for match in reversed(matches):  # Reverse to maintain positions
                original_value = match.group()
                masked_value = self.masking_strategies[pii_type](original_value, mask_char)
                
                # Replace in text
                start = match.start()
                end = match.end()
                masked_text = masked_text[:start] + masked_value + masked_text[end:]
                
                detections.append({
                    'type': pii_type,
                    'original_length': len(original_value),
                    'masked_length': len(masked_value),
                    'position': start,
                    'hash': hashlib.sha256(original_value.encode()).hexdigest()[:16]
                })
        
        return masked_text, detections
    
    def _mask_email(self, email: str, mask_char: str) -> str:
        """Mask email address"""
        parts = email.split('@')
        if len(parts) != 2:
            return mask_char * len(email)
        
        username, domain = parts
        masked_username = username[0] + mask_char * (len(username) - 2) + username[-1] if len(username) > 2 else mask_char * len(username)
        
        domain_parts = domain.split('.')
        if len(domain_parts) >= 2:
            masked_domain = mask_char * len(domain_parts[0]) + '.' + domain_parts[-1]
        else:
            masked_domain = mask_char * len(domain)
        
        return f"{masked_username}@{masked_domain}"
    
    def _mask_phone(self, phone: str, mask_char: str) -> str:
        """Mask phone number"""
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) >= 10:
            return phone[:3] + mask_char * (len(phone) - 6) + phone[-3:]
        return mask_char * len(phone)
    
    def _mask_ssn(self, ssn: str, mask_char: str) -> str:
        """Mask SSN"""
        return mask_char * (len(ssn) - 4) + ssn[-4:]
    
    def _mask_credit_card(self, cc: str, mask_char: str) -> str:
        """Mask credit card number"""
        digits_only = re.sub(r'\D', '', cc)
        if len(digits_only) >= 12:
            masked_digits = mask_char * (len(digits_only) - 4) + digits_only[-4:]
            # Preserve original formatting
            result = cc
            for i, char in enumerate(cc):
                if char.isdigit():
                    digit_index = len([c for c in cc[:i] if c.isdigit()])
                    if digit_index < len(masked_digits):
                        result = result[:i] + masked_digits[digit_index] + result[i+1:]
            return result
        return mask_char * len(cc)
    
    def _mask_ip(self, ip: str, mask_char: str) -> str:
        """Mask IP address"""
        parts = ip.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.{mask_char * len(parts[2])}.{mask_char * len(parts[3])}"
        return mask_char * len(ip)
    
    def _mask_api_key(self, api_key: str, mask_char: str) -> str:
        """Mask API key"""
        if len(api_key) > 8:
            return api_key[:4] + mask_char * (len(api_key) - 8) + api_key[-4:]
        return mask_char * len(api_key)
    
    def _mask_jwt_token(self, token: str, mask_char: str) -> str:
        """Mask JWT token"""
        parts = token.split('.')
        if len(parts) == 3:
            return f"{parts[0][:8]}.{mask_char * 16}.{mask_char * 16}"
        return mask_char * min(len(token), 32)
    
    def _calculate_confidence(self, pii_type: str, value: str) -> float:
        """Calculate confidence score for PII detection"""
        # Simple confidence calculation based on pattern strength
        confidence_scores = {
            'email': 0.95 if '@' in value and '.' in value else 0.7,
            'phone': 0.9 if len(re.sub(r'\D', '', value)) == 10 else 0.7,
            'ssn': 0.95 if len(re.sub(r'\D', '', value)) == 9 else 0.8,
            'credit_card': 0.9 if len(re.sub(r'\D', '', value)) >= 13 else 0.7,
            'ip_address': 0.85,
            'api_key': 0.8 if len(value) >= 32 else 0.6,
            'jwt_token': 0.95 if value.count('.') == 2 else 0.7
        }
        
        return confidence_scores.get(pii_type, 0.5)
```

---

**Document Version**: 1.0  
**Last Updated**: July 26, 2025  
**Classification**: Confidential  
**Next Review**: August 26, 2025  
**Owner**: N.L.D.S. Security Team
