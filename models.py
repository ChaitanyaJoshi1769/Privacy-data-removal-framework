#!/usr/bin/env python3
"""
DATABASE MODELS

Core SQLAlchemy models for:
- Identity graph and correlation
- Exposure inventory
- Removal operations tracking
- Monitoring results
- Audit logs
"""

from datetime import datetime
from enum import Enum
from sqlalchemy import (
    create_engine, Column, String, Integer, Float, Boolean, DateTime,
    Text, ForeignKey, Table, JSON, Index, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# ============================================================================
# ENUMS
# ============================================================================

class ExposureSeverity(str, Enum):
    """Exposure severity classification"""
    CRITICAL = "critical"      # Address, phone, ID exposed
    HIGH = "high"              # Email exposed, account compromised
    MEDIUM = "medium"          # Social media exposure, old content
    LOW = "low"                # Minimal personal data


class ExposureType(str, Enum):
    """Categories of exposure"""
    PEOPLE_SEARCH = "people_search"
    DATA_BROKER = "data_broker"
    SEARCH_ENGINE = "search_engine"
    SOCIAL_MEDIA = "social_media"
    ARCHIVE = "archive"
    BREACH = "breach"
    METADATA = "metadata"
    IMAGE = "image"
    PUBLIC_RECORD = "public_record"
    OTHER = "other"


class RemovalStatus(str, Enum):
    """Status of removal operations"""
    PENDING = "pending"
    SUBMITTED = "submitted"
    IN_PROGRESS = "in_progress"
    VERIFIED_REMOVED = "verified_removed"
    REAPPEARED = "reappeared"
    FAILED = "failed"
    NOT_APPLICABLE = "not_applicable"


class MonitoringFrequency(str, Enum):
    """Monitoring scan frequency"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


# ============================================================================
# IDENTITY & CORRELATION
# ============================================================================

class Identity(Base):
    """Core identity record"""
    __tablename__ = "identities"

    id = Column(String(36), primary_key=True)
    legal_name = Column(String(255), nullable=False, index=True)
    primary_email = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)

    # Relationships
    aliases = relationship("Alias", back_populates="identity", cascade="all, delete-orphan")
    contacts = relationship("ContactInfo", back_populates="identity", cascade="all, delete-orphan")
    locations = relationship("Location", back_populates="identity", cascade="all, delete-orphan")
    accounts = relationship("OnlineAccount", back_populates="identity", cascade="all, delete-orphan")
    exposures = relationship("Exposure", back_populates="identity", cascade="all, delete-orphan")
    correlations = relationship("IdentityCorrelation", back_populates="primary_identity")


class Alias(Base):
    """Alternative names, nicknames, pseudonyms"""
    __tablename__ = "aliases"

    id = Column(String(36), primary_key=True)
    identity_id = Column(String(36), ForeignKey("identities.id"), nullable=False, index=True)
    alias_text = Column(String(255), nullable=False, index=True)
    alias_type = Column(String(50), nullable=False)  # nickname, professional, gamer, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)

    identity = relationship("Identity", back_populates="aliases")

    __table_args__ = (Index("idx_identity_alias", "identity_id", "alias_text"),)


class ContactInfo(Base):
    """Email addresses, phone numbers"""
    __tablename__ = "contact_info"

    id = Column(String(36), primary_key=True)
    identity_id = Column(String(36), ForeignKey("identities.id"), nullable=False, index=True)
    contact_type = Column(String(50), nullable=False)  # email, phone, etc.
    contact_value = Column(String(255), nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    exposure_count = Column(Integer, default=0)
    last_seen = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)

    identity = relationship("Identity", back_populates="contacts")

    __table_args__ = (
        Index("idx_identity_contact", "identity_id", "contact_type"),
        UniqueConstraint("contact_value", name="uq_contact_value")
    )


class Location(Base):
    """Physical locations (addresses, cities, countries)"""
    __tablename__ = "locations"

    id = Column(String(36), primary_key=True)
    identity_id = Column(String(36), ForeignKey("identities.id"), nullable=False, index=True)
    location_type = Column(String(50), nullable=False)  # address, city, country, work, school
    location_value = Column(String(255), nullable=False)
    geocode_lat = Column(Float)
    geocode_lng = Column(Float)
    exposure_count = Column(Integer, default=0)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)

    identity = relationship("Identity", back_populates="locations")


class OnlineAccount(Base):
    """Social media, forums, platform accounts"""
    __tablename__ = "online_accounts"

    id = Column(String(36), primary_key=True)
    identity_id = Column(String(36), ForeignKey("identities.id"), nullable=False, index=True)
    platform = Column(String(100), nullable=False, index=True)  # twitter, linkedin, github, etc.
    username = Column(String(255), nullable=False)
    profile_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_private = Column(Boolean, default=False)
    follower_count = Column(Integer)
    post_count = Column(Integer)
    joined_date = Column(DateTime)
    last_updated = Column(DateTime)
    metadata = Column(JSON)

    identity = relationship("Identity", back_populates="accounts")

    __table_args__ = (
        Index("idx_platform_username", "platform", "username"),
        UniqueConstraint("platform", "username", name="uq_platform_username")
    )


class IdentityCorrelation(Base):
    """Links between identity artifacts (emails, usernames, photos, etc)"""
    __tablename__ = "identity_correlations"

    id = Column(String(36), primary_key=True)
    primary_identity_id = Column(String(36), ForeignKey("identities.id"), nullable=False, index=True)
    secondary_identity_id = Column(String(36), ForeignKey("identities.id"), index=True)
    artifact_type = Column(String(100), nullable=False)  # username, email, photo, metadata, etc.
    artifact_value = Column(String(255))
    confidence_score = Column(Float, default=0.0)  # 0.0-1.0
    correlation_evidence = Column(Text)  # Why we think they're correlated
    created_at = Column(DateTime, default=datetime.utcnow)

    primary_identity = relationship("Identity", back_populates="correlations", foreign_keys=[primary_identity_id])

    __table_args__ = (Index("idx_correlation_confidence", "confidence_score", "artifact_type"),)


# ============================================================================
# EXPOSURE INVENTORY
# ============================================================================

class Exposure(Base):
    """Discovered exposure of personal data"""
    __tablename__ = "exposures"

    id = Column(String(36), primary_key=True)
    identity_id = Column(String(36), ForeignKey("identities.id"), nullable=False, index=True)
    exposure_type = Column(String(50), nullable=False)  # data_broker, search_engine, etc.
    platform = Column(String(100), nullable=False)  # Facebook, Google, Spokeo, etc.
    url = Column(String(500))
    title = Column(String(255))
    description = Column(Text)
    data_exposed = Column(JSON)  # What data was found: {email, phone, address, etc}
    severity = Column(String(50), default="medium")
    discoverable = Column(Boolean, default=True)
    search_rank_position = Column(Integer)  # For search results
    discovery_date = Column(DateTime, default=datetime.utcnow)
    last_verified = Column(DateTime)
    removal_target = Column(Boolean, default=False)  # User marked for removal
    metadata = Column(JSON)

    identity = relationship("Identity", back_populates="exposures")
    removal_operations = relationship("RemovalOperation", back_populates="exposure", cascade="all, delete-orphan")
    monitoring_results = relationship("MonitoringResult", back_populates="exposure", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_identity_exposure_type", "identity_id", "exposure_type"),
        Index("idx_platform_severity", "platform", "severity"),
    )


# ============================================================================
# REMOVAL OPERATIONS
# ============================================================================

class RemovalOperation(Base):
    """Tracking for removal, de-indexing, suppression operations"""
    __tablename__ = "removal_operations"

    id = Column(String(36), primary_key=True)
    exposure_id = Column(String(36), ForeignKey("exposures.id"), nullable=False, index=True)
    operation_type = Column(String(100), nullable=False)  # deletion, deindex, suppression, opt_out
    platform = Column(String(100), nullable=False)
    status = Column(String(50), default="pending")
    status_enum = Column(String(50))  # RemovalStatus enum
    method = Column(String(255))  # How removal was attempted
    request_url = Column(String(500))
    submitted_date = Column(DateTime)
    completed_date = Column(DateTime)
    verification_date = Column(DateTime)
    notes = Column(Text)
    retry_count = Column(Integer, default=0)
    last_retry = Column(DateTime)
    estimated_processing_time = Column(Integer)  # Days
    metadata = Column(JSON)

    exposure = relationship("Exposure", back_populates="removal_operations")

    __table_args__ = (
        Index("idx_removal_status", "status", "platform"),
        Index("idx_removal_date_range", "submitted_date", "completed_date"),
    )


# ============================================================================
# MONITORING & ALERTING
# ============================================================================

class MonitoringJob(Base):
    """Configured monitoring/scanning jobs"""
    __tablename__ = "monitoring_jobs"

    id = Column(String(36), primary_key=True)
    identity_id = Column(String(36), ForeignKey("identities.id"), nullable=False, index=True)
    job_type = Column(String(100), nullable=False)  # discovery, exposure_check, breach_check, etc.
    frequency = Column(String(50), default="daily")
    search_targets = Column(JSON)  # Platforms to monitor
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)


class MonitoringResult(Base):
    """Results from monitoring scans"""
    __tablename__ = "monitoring_results"

    id = Column(String(36), primary_key=True)
    exposure_id = Column(String(36), ForeignKey("exposures.id"), nullable=False, index=True)
    scan_date = Column(DateTime, default=datetime.utcnow)
    scan_type = Column(String(100), nullable=False)  # search_check, data_broker_check, etc.
    still_discoverable = Column(Boolean)
    search_rank_change = Column(Integer)  # Change in ranking
    indexed = Column(Boolean)
    cached_version_exists = Column(Boolean)
    notes = Column(Text)
    metadata = Column(JSON)

    exposure = relationship("Exposure", back_populates="monitoring_results")

    __table_args__ = (Index("idx_monitoring_date", "scan_date"),)


# ============================================================================
# AUDIT & LOGGING
# ============================================================================

class AuditLog(Base):
    """Complete audit trail of all operations"""
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    action = Column(String(100), nullable=False)  # discovered, removed, suppressed, etc.
    target_type = Column(String(100))  # exposure, identity, account, etc.
    target_id = Column(String(36))
    operator = Column(String(100))  # User or automated
    status = Column(String(50))  # success, failed, pending
    details = Column(JSON)
    error_message = Column(Text)
    metadata = Column(JSON)

    __table_args__ = (Index("idx_audit_timestamp_action", "timestamp", "action"),)


class Configuration(Base):
    """Encrypted operational configuration"""
    __tablename__ = "configuration"

    id = Column(String(36), primary_key=True)
    key = Column(String(255), unique=True, nullable=False)
    encrypted_value = Column(Text, nullable=False)
    is_sensitive = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)


# ============================================================================
# INITIALIZATION
# ============================================================================

def init_db(database_url):
    """Initialize database and create tables"""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine


if __name__ == "__main__":
    import os
    db_url = os.getenv("DATABASE_URL", "sqlite:///./footprint_ops.db")
    engine = init_db(db_url)
    print(f"✓ Database initialized: {db_url}")
    print(f"✓ Tables created: {len(Base.metadata.tables)} tables")
