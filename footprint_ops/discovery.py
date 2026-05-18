#!/usr/bin/env python3
"""
Search Engine Discovery Module - Phase 2a

Performs exhaustive searches across major search engines to discover
personal data exposed in search results.

Supports:
- Google (via requests/BeautifulSoup)
- Bing
- DuckDuckGo
- Yandex

Extracts:
- URLs containing personal information
- Search result titles and snippets
- Search ranking positions
- Cached versions
"""

import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote, urlencode
import time
from pathlib import Path
import json

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Represents a search result"""
    url: str
    title: str
    snippet: str
    position: int
    engine: str
    search_term: str
    found_date: str
    cached: bool = False
    risk_level: str = "UNKNOWN"


class SearchEngineDiscovery:
    """Discovers personal data through search engines"""
    
    def __init__(self, rate_limit_delay: float = 2.0, timeout: int = 30):
        """
        Initialize search discovery
        
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
    
    def search_all_engines(self, search_terms: List[str], max_results: int = 50) -> List[SearchResult]:
        """
        Search all available engines with given terms
        
        Args:
            search_terms: List of terms to search
            max_results: Max results per search
        
        Returns:
            List of SearchResult objects
        """
        all_results = []
        
        for term in search_terms:
            logger.info(f"Searching for: {term}")
            
            # Google
            google_results = self.search_google(term, max_results)
            all_results.extend(google_results)
            time.sleep(self.rate_limit_delay)
            
            # Bing
            bing_results = self.search_bing(term, max_results)
            all_results.extend(bing_results)
            time.sleep(self.rate_limit_delay)
            
            # DuckDuckGo
            ddg_results = self.search_duckduckgo(term, max_results)
            all_results.extend(ddg_results)
            time.sleep(self.rate_limit_delay)
            
            # Yandex
            yandex_results = self.search_yandex(term, max_results)
            all_results.extend(yandex_results)
            time.sleep(self.rate_limit_delay)
        
        self.results = all_results
        return all_results
    
    def search_google(self, search_term: str, max_results: int = 50) -> List[SearchResult]:
        """
        Search Google for personal information
        
        Args:
            search_term: Term to search
            max_results: Maximum results to return
        
        Returns:
            List of SearchResult objects
        """
        results = []
        
        try:
            url = f"https://www.google.com/search?q={quote(search_term)}&num=100"
            
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract results
            position = 1
            for result in soup.find_all('div', class_='g'):
                if position > max_results:
                    break
                
                # Extract URL
                link_tag = result.find('a', href=True)
                if not link_tag:
                    continue
                
                url = link_tag['href']
                
                # Extract title
                title_tag = result.find('h3')
                title = title_tag.text if title_tag else ""
                
                # Extract snippet
                snippet_tag = result.find('span', class_='st')
                snippet = snippet_tag.text if snippet_tag else ""
                
                # Assess risk
                risk_level = self._assess_risk_level(title, snippet, url)
                
                if title and url:
                    search_result = SearchResult(
                        url=url,
                        title=title,
                        snippet=snippet,
                        position=position,
                        engine="google",
                        search_term=search_term,
                        found_date=datetime.now().isoformat(),
                        risk_level=risk_level
                    )
                    results.append(search_result)
                    position += 1
            
            logger.info(f"Google: Found {len(results)} results for '{search_term}'")
            
        except Exception as e:
            logger.error(f"Google search failed: {e}")
        
        return results
    
    def search_bing(self, search_term: str, max_results: int = 50) -> List[SearchResult]:
        """
        Search Bing for personal information
        
        Args:
            search_term: Term to search
            max_results: Maximum results to return
        
        Returns:
            List of SearchResult objects
        """
        results = []
        
        try:
            url = f"https://www.bing.com/search?q={quote(search_term)}&count=50"
            
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            position = 1
            for result in soup.find_all('li', class_='b_algo'):
                if position > max_results:
                    break
                
                # Extract URL
                link_tag = result.find('a', href=True)
                if not link_tag:
                    continue
                
                url = link_tag['href']
                
                # Extract title
                title = link_tag.text if link_tag else ""
                
                # Extract snippet
                snippet_tag = result.find('p')
                snippet = snippet_tag.text if snippet_tag else ""
                
                # Assess risk
                risk_level = self._assess_risk_level(title, snippet, url)
                
                if title and url:
                    search_result = SearchResult(
                        url=url,
                        title=title,
                        snippet=snippet,
                        position=position,
                        engine="bing",
                        search_term=search_term,
                        found_date=datetime.now().isoformat(),
                        risk_level=risk_level
                    )
                    results.append(search_result)
                    position += 1
            
            logger.info(f"Bing: Found {len(results)} results for '{search_term}'")
            
        except Exception as e:
            logger.error(f"Bing search failed: {e}")
        
        return results
    
    def search_duckduckgo(self, search_term: str, max_results: int = 50) -> List[SearchResult]:
        """
        Search DuckDuckGo for personal information
        
        Args:
            search_term: Term to search
            max_results: Maximum results to return
        
        Returns:
            List of SearchResult objects
        """
        results = []
        
        try:
            # DuckDuckGo API endpoint
            url = "https://api.duckduckgo.com/"
            params = {
                'q': search_term,
                'format': 'json',
                'no_redirect': 1
            }
            
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract results from AbstractResults
            if 'AbstractURL' in data and data['AbstractURL']:
                position = 1
                result = SearchResult(
                    url=data['AbstractURL'],
                    title=data.get('AbstractTitle', ''),
                    snippet=data.get('AbstractText', ''),
                    position=position,
                    engine="duckduckgo",
                    search_term=search_term,
                    found_date=datetime.now().isoformat(),
                    risk_level=self._assess_risk_level(
                        data.get('AbstractTitle', ''),
                        data.get('AbstractText', ''),
                        data['AbstractURL']
                    )
                )
                results.append(result)
            
            logger.info(f"DuckDuckGo: Found {len(results)} results for '{search_term}'")
            
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
        
        return results
    
    def search_yandex(self, search_term: str, max_results: int = 50) -> List[SearchResult]:
        """
        Search Yandex for personal information
        
        Args:
            search_term: Term to search
            max_results: Maximum results to return
        
        Returns:
            List of SearchResult objects
        """
        results = []
        
        try:
            url = f"https://yandex.com/search/?text={quote(search_term)}"
            
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            position = 1
            for result in soup.find_all('div', class_='serp-item'):
                if position > max_results:
                    break
                
                # Extract URL
                link_tag = result.find('a', class_='Link')
                if not link_tag:
                    continue
                
                url = link_tag.get('href', '')
                
                # Extract title
                title = link_tag.text if link_tag else ""
                
                # Extract snippet
                snippet_tag = result.find('span', class_='text-snippet')
                snippet = snippet_tag.text if snippet_tag else ""
                
                # Assess risk
                risk_level = self._assess_risk_level(title, snippet, url)
                
                if title and url:
                    search_result = SearchResult(
                        url=url,
                        title=title,
                        snippet=snippet,
                        position=position,
                        engine="yandex",
                        search_term=search_term,
                        found_date=datetime.now().isoformat(),
                        risk_level=risk_level
                    )
                    results.append(search_result)
                    position += 1
            
            logger.info(f"Yandex: Found {len(results)} results for '{search_term}'")
            
        except Exception as e:
            logger.error(f"Yandex search failed: {e}")
        
        return results
    
    def _assess_risk_level(self, title: str, snippet: str, url: str) -> str:
        """
        Assess risk level of search result
        
        Returns: CRITICAL, HIGH, MEDIUM, LOW
        """
        text = f"{title} {snippet} {url}".lower()
        
        # Critical indicators
        critical_indicators = ['address', 'phone', 'email', 'ssn', 'credit card', 'home']
        if any(indicator in text for indicator in critical_indicators):
            return "CRITICAL"
        
        # High risk indicators
        high_indicators = ['linkedin', 'facebook', 'personal', 'profile', 'contact']
        if any(indicator in text for indicator in high_indicators):
            return "HIGH"
        
        # Medium risk indicators
        medium_indicators = ['blog', 'social', 'github', 'twitter', 'instagram']
        if any(indicator in text for indicator in medium_indicators):
            return "MEDIUM"
        
        return "LOW"
    
    def export_results(self, output_path: str = "discovery/search_engine_results.json"):
        """Export results to JSON"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            results_data = {
                "timestamp": datetime.now().isoformat(),
                "total_results": len(self.results),
                "results_by_engine": {},
                "results_by_risk": {},
                "detailed_results": [
                    {
                        "url": r.url,
                        "title": r.title,
                        "snippet": r.snippet,
                        "position": r.position,
                        "engine": r.engine,
                        "search_term": r.search_term,
                        "risk_level": r.risk_level,
                        "found_date": r.found_date
                    }
                    for r in self.results
                ]
            }
            
            # Group by engine
            for result in self.results:
                if result.engine not in results_data["results_by_engine"]:
                    results_data["results_by_engine"][result.engine] = []
                results_data["results_by_engine"][result.engine].append(result.url)
            
            # Group by risk
            for result in self.results:
                if result.risk_level not in results_data["results_by_risk"]:
                    results_data["results_by_risk"][result.risk_level] = 0
                results_data["results_by_risk"][result.risk_level] += 1
            
            with open(output_path, 'w') as f:
                json.dump(results_data, f, indent=2, default=str)
            
            logger.info(f"Results exported to {output_path}")
        
        except Exception as e:
            logger.error(f"Failed to export results: {e}")


# Utility function
def discover_search_results(search_terms: List[str]) -> List[SearchResult]:
    """Convenience function to search all engines"""
    discovery = SearchEngineDiscovery()
    return discovery.search_all_engines(search_terms)


if __name__ == "__main__":
    import sys
    
    # Test search
    test_terms = [
        "john smith",
        "john.smith@gmail.com",
        "jsmith",
    ]
    
    discovery = SearchEngineDiscovery()
    results = discovery.search_all_engines(test_terms, max_results=10)
    discovery.export_results()
    
    print(f"✓ Discovered {len(results)} search results")
    print(f"✓ Results exported to discovery/search_engine_results.json")
