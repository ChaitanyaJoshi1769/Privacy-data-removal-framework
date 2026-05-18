#!/usr/bin/env python3
"""
Data Broker Enumeration Module - Phase 2b

Enumerates and discovers personal information listed on data brokers.

Covered brokers:
- Spokeo - Phone, address, social profiles
- Whitepages - Phone, address, people listings
- Intelius - Public records, background
- MyLife - Profile, contacts, background
- TrueCaller - Phone number lookup
- PeopleFinder - Public records
- US Search - Background info
- Family Tree Now - Genealogy (personal info exposure)
- ZoomInfo - Business/professional profiles

Methods:
- Direct API calls (where available)
- Web scraping with BeautifulSoup
- Pattern matching for detected listings
"""

import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote
import json
from pathlib import Path
import time

logger = logging.getLogger(__name__)


@dataclass
class DataBrokerListing:
    """Represents a listing on a data broker"""
    broker: str
    found: bool
    url: Optional[str] = None
    data_exposed: Dict = None
    profile_details: Dict = None
    risk_level: str = "UNKNOWN"
    last_checked: str = None
    removal_difficulty: str = "UNKNOWN"


class DataBrokerEnumeration:
    """Enumerates personal data on data brokers"""
    
    def __init__(self, rate_limit_delay: float = 2.0, timeout: int = 30):
        """
        Initialize data broker enumeration
        
        Args:
            rate_limit_delay: Delay between requests (seconds)
            timeout: Request timeout (seconds)
        """
        self.rate_limit_delay = rate_limit_delay
        self.timeout = timeout
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Define broker configurations
        self.brokers = {
            'spokeo': {
                'base_url': 'https://www.spokeo.com',
                'search_endpoint': '/search',
                'name': 'Spokeo',
                'risk': 'CRITICAL',
                'difficulty': 'EASY'
            },
            'whitepages': {
                'base_url': 'https://www.whitepages.com',
                'search_endpoint': '/search/people',
                'name': 'Whitepages',
                'risk': 'CRITICAL',
                'difficulty': 'EASY'
            },
            'intelius': {
                'base_url': 'https://www.intelius.com',
                'search_endpoint': '/search',
                'name': 'Intelius',
                'risk': 'HIGH',
                'difficulty': 'MEDIUM'
            },
            'mylife': {
                'base_url': 'https://www.mylife.com',
                'search_endpoint': '/search',
                'name': 'MyLife',
                'risk': 'HIGH',
                'difficulty': 'MEDIUM'
            },
            'truecaller': {
                'base_url': 'https://www.truecaller.com',
                'search_endpoint': '/search',
                'name': 'TrueCaller',
                'risk': 'CRITICAL',
                'difficulty': 'HARD'
            },
            'peoplefinder': {
                'base_url': 'https://www.peoplefinder.com',
                'search_endpoint': '/search',
                'name': 'PeopleFinder',
                'risk': 'HIGH',
                'difficulty': 'EASY'
            },
            'ussearch': {
                'base_url': 'https://www.ussearch.com',
                'search_endpoint': '/search',
                'name': 'US Search',
                'risk': 'MEDIUM',
                'difficulty': 'MEDIUM'
            },
            'familytreenow': {
                'base_url': 'https://www.familytreenow.com',
                'search_endpoint': '/search',
                'name': 'Family Tree Now',
                'risk': 'HIGH',
                'difficulty': 'MEDIUM'
            },
            'zoominfo': {
                'base_url': 'https://www.zoominfo.com',
                'search_endpoint': '/search',
                'name': 'ZoomInfo',
                'risk': 'MEDIUM',
                'difficulty': 'HARD'
            }
        }
    
    def search_all_brokers(self, name: str = None, email: str = None, phone: str = None) -> List[DataBrokerListing]:
        """
        Search all data brokers for personal information
        
        Args:
            name: Full name to search
            email: Email address to search
            phone: Phone number to search
        
        Returns:
            List of DataBrokerListing objects
        """
        all_results = []
        
        for broker_key, broker_config in self.brokers.items():
            logger.info(f"Searching {broker_config['name']}...")
            
            listing = self._search_broker(broker_key, name, email, phone)
            if listing:
                all_results.append(listing)
            
            time.sleep(self.rate_limit_delay)
        
        self.results = all_results
        return all_results
    
    def _search_broker(self, broker_key: str, name: str = None, email: str = None, phone: str = None) -> Optional[DataBrokerListing]:
        """Search a specific broker"""
        broker = self.brokers[broker_key]
        
        try:
            # Route to specific broker handler
            if broker_key == 'spokeo':
                return self._search_spokeo(name, email, phone)
            elif broker_key == 'whitepages':
                return self._search_whitepages(name, email, phone)
            elif broker_key == 'intelius':
                return self._search_intelius(name, email, phone)
            elif broker_key == 'mylife':
                return self._search_mylife(name, email, phone)
            elif broker_key == 'truecaller':
                return self._search_truecaller(phone)
            elif broker_key == 'peoplefinder':
                return self._search_peoplefinder(name, email, phone)
            elif broker_key == 'ussearch':
                return self._search_ussearch(name, email, phone)
            elif broker_key == 'familytreenow':
                return self._search_familytreenow(name)
            elif broker_key == 'zoominfo':
                return self._search_zoominfo(name, email)
        
        except Exception as e:
            logger.error(f"Error searching {broker['name']}: {e}")
        
        return None
    
    def _search_spokeo(self, name: str = None, email: str = None, phone: str = None) -> Optional[DataBrokerListing]:
        """Search Spokeo"""
        broker = self.brokers['spokeo']
        
        try:
            # Build search URL
            if phone:
                search_url = f"{broker['base_url']}/phone-number-lookup/{quote(phone)}"
            elif name:
                search_url = f"{broker['base_url']}/search/people/?q={quote(name)}"
            elif email:
                search_url = f"{broker['base_url']}/search/people/?q={quote(email)}"
            else:
                return None
            
            response = self.session.get(search_url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check if profile found
            if 'No results' not in response.text and 'result-item' in response.text:
                data_exposed = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'listings': 'Found on Spokeo'
                }
                
                listing = DataBrokerListing(
                    broker='Spokeo',
                    found=True,
                    url=search_url,
                    data_exposed=data_exposed,
                    risk_level=broker['risk'],
                    last_checked=datetime.now().isoformat(),
                    removal_difficulty=broker['difficulty']
                )
                
                logger.info(f"✓ Found listing on Spokeo: {search_url}")
                return listing
        
        except Exception as e:
            logger.debug(f"Spokeo search error: {e}")
        
        return None
    
    def _search_whitepages(self, name: str = None, email: str = None, phone: str = None) -> Optional[DataBrokerListing]:
        """Search Whitepages"""
        broker = self.brokers['whitepages']
        
        try:
            if phone:
                search_url = f"{broker['base_url']}/phone/{quote(phone)}"
            elif name:
                search_url = f"{broker['base_url']}/name/{quote(name)}"
            else:
                return None
            
            response = self.session.get(search_url, timeout=self.timeout)
            response.raise_for_status()
            
            if 'No matches' not in response.text:
                data_exposed = {
                    'name': name,
                    'phone': phone,
                    'listings': 'Found on Whitepages'
                }
                
                listing = DataBrokerListing(
                    broker='Whitepages',
                    found=True,
                    url=search_url,
                    data_exposed=data_exposed,
                    risk_level=broker['risk'],
                    last_checked=datetime.now().isoformat(),
                    removal_difficulty=broker['difficulty']
                )
                
                logger.info(f"✓ Found listing on Whitepages: {search_url}")
                return listing
        
        except Exception as e:
            logger.debug(f"Whitepages search error: {e}")
        
        return None
    
    def _search_intelius(self, name: str = None, email: str = None, phone: str = None) -> Optional[DataBrokerListing]:
        """Search Intelius"""
        broker = self.brokers['intelius']
        
        try:
            if name:
                search_url = f"{broker['base_url']}/search/?q={quote(name)}"
            elif phone:
                search_url = f"{broker['base_url']}/search/?q={quote(phone)}"
            else:
                return None
            
            response = self.session.get(search_url, timeout=self.timeout)
            
            if 'found' in response.text.lower() and 'no results' not in response.text.lower():
                listing = DataBrokerListing(
                    broker='Intelius',
                    found=True,
                    url=search_url,
                    data_exposed={'name': name, 'email': email, 'phone': phone},
                    risk_level=broker['risk'],
                    last_checked=datetime.now().isoformat(),
                    removal_difficulty=broker['difficulty']
                )
                
                logger.info(f"✓ Found listing on Intelius: {search_url}")
                return listing
        
        except Exception as e:
            logger.debug(f"Intelius search error: {e}")
        
        return None
    
    def _search_mylife(self, name: str = None, email: str = None, phone: str = None) -> Optional[DataBrokerListing]:
        """Search MyLife"""
        broker = self.brokers['mylife']
        
        try:
            if name:
                search_url = f"{broker['base_url']}/search/people?q={quote(name)}"
            else:
                return None
            
            response = self.session.get(search_url, timeout=self.timeout)
            
            if 'profile' in response.text.lower():
                listing = DataBrokerListing(
                    broker='MyLife',
                    found=True,
                    url=search_url,
                    data_exposed={'name': name},
                    risk_level=broker['risk'],
                    last_checked=datetime.now().isoformat(),
                    removal_difficulty=broker['difficulty']
                )
                
                logger.info(f"✓ Found listing on MyLife: {search_url}")
                return listing
        
        except Exception as e:
            logger.debug(f"MyLife search error: {e}")
        
        return None
    
    def _search_truecaller(self, phone: str = None) -> Optional[DataBrokerListing]:
        """Search TrueCaller (phone only)"""
        broker = self.brokers['truecaller']
        
        if not phone:
            return None
        
        try:
            # TrueCaller API endpoint
            api_url = f"https://api.truecaller.com/api/search"
            params = {'q': phone}
            
            response = self.session.get(api_url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                listing = DataBrokerListing(
                    broker='TrueCaller',
                    found=True,
                    url=f"https://www.truecaller.com/search/{quote(phone)}",
                    data_exposed={'phone': phone},
                    risk_level=broker['risk'],
                    last_checked=datetime.now().isoformat(),
                    removal_difficulty=broker['difficulty']
                )
                
                logger.info(f"✓ Found listing on TrueCaller")
                return listing
        
        except Exception as e:
            logger.debug(f"TrueCaller search error: {e}")
        
        return None
    
    def _search_peoplefinder(self, name: str = None, email: str = None, phone: str = None) -> Optional[DataBrokerListing]:
        """Search PeopleFinder"""
        broker = self.brokers['peoplefinder']
        
        try:
            if name:
                search_url = f"{broker['base_url']}/search/?name={quote(name)}"
            else:
                return None
            
            response = self.session.get(search_url, timeout=self.timeout)
            
            if 'found' in response.text.lower():
                listing = DataBrokerListing(
                    broker='PeopleFinder',
                    found=True,
                    url=search_url,
                    data_exposed={'name': name},
                    risk_level=broker['risk'],
                    last_checked=datetime.now().isoformat(),
                    removal_difficulty=broker['difficulty']
                )
                
                logger.info(f"✓ Found listing on PeopleFinder")
                return listing
        
        except Exception as e:
            logger.debug(f"PeopleFinder search error: {e}")
        
        return None
    
    def _search_ussearch(self, name: str = None, email: str = None, phone: str = None) -> Optional[DataBrokerListing]:
        """Search US Search"""
        broker = self.brokers['ussearch']
        
        try:
            if name:
                search_url = f"{broker['base_url']}/search/?q={quote(name)}"
            else:
                return None
            
            response = self.session.get(search_url, timeout=self.timeout)
            
            listing = DataBrokerListing(
                broker='US Search',
                found='record' in response.text.lower(),
                url=search_url,
                data_exposed={'name': name},
                risk_level=broker['risk'],
                last_checked=datetime.now().isoformat(),
                removal_difficulty=broker['difficulty']
            )
            
            if listing.found:
                logger.info(f"✓ Found listing on US Search")
            return listing
        
        except Exception as e:
            logger.debug(f"US Search error: {e}")
        
        return None
    
    def _search_familytreenow(self, name: str = None) -> Optional[DataBrokerListing]:
        """Search Family Tree Now"""
        broker = self.brokers['familytreenow']
        
        try:
            if not name:
                return None
            
            search_url = f"{broker['base_url']}/search/?q={quote(name)}"
            response = self.session.get(search_url, timeout=self.timeout)
            
            if 'genealogy' in response.text.lower() or 'profile' in response.text.lower():
                listing = DataBrokerListing(
                    broker='Family Tree Now',
                    found=True,
                    url=search_url,
                    data_exposed={'name': name},
                    risk_level=broker['risk'],
                    last_checked=datetime.now().isoformat(),
                    removal_difficulty=broker['difficulty']
                )
                
                logger.info(f"✓ Found listing on Family Tree Now")
                return listing
        
        except Exception as e:
            logger.debug(f"Family Tree Now error: {e}")
        
        return None
    
    def _search_zoominfo(self, name: str = None, email: str = None) -> Optional[DataBrokerListing]:
        """Search ZoomInfo (B2B, but personal info exposure possible)"""
        broker = self.brokers['zoominfo']
        
        try:
            if email:
                search_url = f"{broker['base_url']}/search/?q={quote(email)}"
            elif name:
                search_url = f"{broker['base_url']}/search/?q={quote(name)}"
            else:
                return None
            
            response = self.session.get(search_url, timeout=self.timeout)
            
            listing = DataBrokerListing(
                broker='ZoomInfo',
                found='profile' in response.text.lower(),
                url=search_url,
                data_exposed={'name': name, 'email': email},
                risk_level=broker['risk'],
                last_checked=datetime.now().isoformat(),
                removal_difficulty=broker['difficulty']
            )
            
            if listing.found:
                logger.info(f"✓ Found listing on ZoomInfo")
            return listing
        
        except Exception as e:
            logger.debug(f"ZoomInfo error: {e}")
        
        return None
    
    def export_results(self, output_path: str = "discovery/data_broker_results.json"):
        """Export results to JSON"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            results_data = {
                "timestamp": datetime.now().isoformat(),
                "total_brokers_checked": len(self.brokers),
                "listings_found": len([r for r in self.results if r.found]),
                "critical_findings": len([r for r in self.results if r.found and r.risk_level == 'CRITICAL']),
                "findings": [
                    {
                        "broker": r.broker,
                        "found": r.found,
                        "url": r.url,
                        "data_exposed": r.data_exposed,
                        "risk_level": r.risk_level,
                        "removal_difficulty": r.removal_difficulty,
                        "last_checked": r.last_checked
                    }
                    for r in self.results
                ]
            }
            
            with open(output_path, 'w') as f:
                json.dump(results_data, f, indent=2, default=str)
            
            logger.info(f"Data broker results exported to {output_path}")
        
        except Exception as e:
            logger.error(f"Failed to export results: {e}")


# Utility function
def enumerate_data_brokers(name: str = None, email: str = None, phone: str = None) -> List[DataBrokerListing]:
    """Convenience function to search all data brokers"""
    enumeration = DataBrokerEnumeration()
    return enumeration.search_all_brokers(name, email, phone)


if __name__ == "__main__":
    # Test enumeration
    enumeration = DataBrokerEnumeration()
    results = enumeration.search_all_brokers(
        name="John Smith",
        email="john.smith@example.com",
        phone="+1-555-0123"
    )
    enumeration.export_results()
    
    found = len([r for r in results if r.found])
    print(f"✓ Scanned {len(enumeration.brokers)} data brokers")
    print(f"✓ Found {found} listings")
    print(f"✓ Results exported to discovery/data_broker_results.json")
