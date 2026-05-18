#!/usr/bin/env python3
"""
Database Module - Phase 1b

Handles:
- SQLAlchemy session management
- Database initialization
- Encrypted field operations
- Transaction management
- Query helpers for identity operations
"""

import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from cryptography.fernet import Fernet
import logging
from pathlib import Path
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_url: str = None, encryption_key: str = None):
        """
        Initialize database manager
        
        Args:
            db_url: Database URL (default: sqlite:///footprint_ops.db)
            encryption_key: Fernet encryption key for sensitive fields
        """
        self.db_url = db_url or os.getenv('DATABASE_URL', 'sqlite:///footprint_ops.db')
        self.encryption_key = encryption_key or os.getenv('ENCRYPTION_KEY')
        self.cipher_suite = None
        
        if self.encryption_key:
            try:
                self.cipher_suite = Fernet(self.encryption_key.encode())
            except Exception as e:
                logger.warning(f"Could not initialize encryption: {e}")
        
        self.engine = None
        self.SessionLocal = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize SQLAlchemy engine"""
        try:
            # SQLite specific settings
            if 'sqlite' in self.db_url:
                self.engine = create_engine(
                    self.db_url,
                    connect_args={'check_same_thread': False},
                    poolclass=StaticPool,
                    echo=False
                )
            else:
                # PostgreSQL or other
                self.engine = create_engine(self.db_url, echo=False, pool_pre_ping=True)
            
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info(f"Database engine initialized: {self.db_url}")
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}")
            raise
    
    def create_tables(self):
        """Create all tables from models"""
        try:
            from models import Base
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get a new database session"""
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized")
        return self.SessionLocal()
    
    def encrypt_field(self, value: str) -> str:
        """Encrypt a sensitive field"""
        if not self.cipher_suite or not value:
            return value
        try:
            encrypted = self.cipher_suite.encrypt(value.encode())
            return encrypted.decode()
        except Exception as e:
            logger.warning(f"Encryption failed: {e}. Storing unencrypted.")
            return value
    
    def decrypt_field(self, encrypted_value: str) -> str:
        """Decrypt a sensitive field"""
        if not self.cipher_suite or not encrypted_value:
            return encrypted_value
        try:
            decrypted = self.cipher_suite.decrypt(encrypted_value.encode())
            return decrypted.decode()
        except Exception as e:
            logger.warning(f"Decryption failed: {e}. Returning as-is.")
            return encrypted_value
    
    def save_identity_profile(self, profile_data: dict, identity_id: str = None):
        """
        Save identity profile to database
        
        Args:
            profile_data: Dictionary with identity information
            identity_id: Optional UUID for identity record
        """
        try:
            from models import Identity, Alias, ContactInfo, OnlineAccount, Location
            import uuid
            
            session = self.get_session()
            
            # Generate ID if not provided
            if not identity_id:
                identity_id = str(uuid.uuid4())
            
            # Create/update identity
            identity = Identity(
                id=identity_id,
                legal_name=profile_data.get('sections', {}).get('personal_identifiers', {}).get('legal_name', 'Unknown'),
                primary_email=profile_data.get('sections', {}).get('contact_information', {}).get('primary_email', ''),
                metadata=profile_data
            )
            session.add(identity)
            
            # Store aliases
            aliases = profile_data.get('sections', {}).get('personal_identifiers', {}).get('nicknames', [])
            for alias_text in aliases:
                if alias_text.strip():
                    alias = Alias(
                        id=str(uuid.uuid4()),
                        identity_id=identity_id,
                        alias_text=alias_text.strip(),
                        alias_type='nickname'
                    )
                    session.add(alias)
            
            # Store contact information
            contact_info = profile_data.get('sections', {}).get('contact_information', {})
            
            # Primary email
            if contact_info.get('primary_email'):
                contact = ContactInfo(
                    id=str(uuid.uuid4()),
                    identity_id=identity_id,
                    contact_type='email',
                    contact_value=contact_info['primary_email'],
                    is_active=True
                )
                session.add(contact)
            
            # Secondary emails
            for email in contact_info.get('secondary_emails', []):
                if email.strip():
                    contact = ContactInfo(
                        id=str(uuid.uuid4()),
                        identity_id=identity_id,
                        contact_type='email',
                        contact_value=email.strip(),
                        is_active=True
                    )
                    session.add(contact)
            
            # Phone numbers
            for phone in contact_info.get('phone_numbers', []):
                if phone.strip():
                    contact = ContactInfo(
                        id=str(uuid.uuid4()),
                        identity_id=identity_id,
                        contact_type='phone',
                        contact_value=self.encrypt_field(phone.strip()),
                        is_active=True
                    )
                    session.add(contact)
            
            # Store locations
            location_data = profile_data.get('sections', {}).get('location_history', {})
            
            if location_data.get('current_address'):
                location = Location(
                    id=str(uuid.uuid4()),
                    identity_id=identity_id,
                    location_type='address',
                    location_value=self.encrypt_field(location_data['current_address']),
                    is_public=False
                )
                session.add(location)
            
            # Store online accounts
            accounts = profile_data.get('sections', {}).get('online_presence', {}).get('accounts', {})
            for platform, username in accounts.items():
                if username.strip():
                    account = OnlineAccount(
                        id=str(uuid.uuid4()),
                        identity_id=identity_id,
                        platform=platform,
                        username=username.strip(),
                        is_active=True
                    )
                    session.add(account)
            
            # Commit transaction
            session.commit()
            logger.info(f"Identity profile saved: {identity_id}")
            return identity_id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save identity profile: {e}")
            raise
        finally:
            session.close()
    
    def get_identity(self, identity_id: str):
        """Retrieve identity by ID"""
        try:
            from models import Identity
            session = self.get_session()
            identity = session.query(Identity).filter_by(id=identity_id).first()
            session.close()
            return identity
        except Exception as e:
            logger.error(f"Failed to retrieve identity: {e}")
            return None
    
    def list_identities(self):
        """List all identities"""
        try:
            from models import Identity
            session = self.get_session()
            identities = session.query(Identity).all()
            session.close()
            return identities
        except Exception as e:
            logger.error(f"Failed to list identities: {e}")
            return []
    
    def get_identity_profile(self, identity_id: str) -> dict:
        """Get complete identity profile as dictionary"""
        try:
            from models import Identity, Alias, ContactInfo, OnlineAccount, Location
            session = self.get_session()
            
            identity = session.query(Identity).filter_by(id=identity_id).first()
            if not identity:
                return None
            
            aliases = session.query(Alias).filter_by(identity_id=identity_id).all()
            contacts = session.query(ContactInfo).filter_by(identity_id=identity_id).all()
            locations = session.query(Location).filter_by(identity_id=identity_id).all()
            accounts = session.query(OnlineAccount).filter_by(identity_id=identity_id).all()
            
            session.close()
            
            profile = {
                "identity_id": identity_id,
                "legal_name": identity.legal_name,
                "primary_email": identity.primary_email,
                "created_at": identity.created_at.isoformat() if identity.created_at else None,
                "aliases": [a.alias_text for a in aliases],
                "emails": [c.contact_value for c in contacts if c.contact_type == 'email'],
                "phones": [self.decrypt_field(c.contact_value) for c in contacts if c.contact_type == 'phone'],
                "locations": [self.decrypt_field(l.location_value) for l in locations],
                "online_accounts": [{"platform": a.platform, "username": a.username} for a in accounts]
            }
            
            return profile
        except Exception as e:
            logger.error(f"Failed to get identity profile: {e}")
            return None


# Global database manager instance
_db_manager = None


def get_db_manager() -> DatabaseManager:
    """Get or create the global database manager"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def init_database():
    """Initialize the database (create tables, etc)"""
    db = get_db_manager()
    db.create_tables()
    logger.info("Database initialization complete")


if __name__ == "__main__":
    # Test database initialization
    init_database()
    print("✓ Database initialized successfully")
