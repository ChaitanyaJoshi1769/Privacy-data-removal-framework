#!/usr/bin/env python3
"""
Social Media Scanning Module - Phase 2c

Discovers personal information on social media platforms by:
- Username existence verification
- Profile URL detection
- Public profile information extraction
- Connection/follower analysis
- Post/activity visibility

Covered platforms:
- LinkedIn - Professional profiles
- Twitter/X - Tweets, followers, location
- GitHub - Repos, stars, gists
- Reddit - Posts, comments, user profile
- Stack Overflow - Answers, reputation
- Medium - Articles, followers
- Facebook - Public pages, info
- Instagram - Posts, followers, profile
- YouTube - Channels, subscribers
- Twitch - Streaming profiles
- Discord - Servers, usernames (if public)
- TikTok - Profile, videos
- Telegram - Public channels
- Mastodon - Fediverse profiles
- GitLab - Projects, activity
"""

import logging
import requests
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote
import json
from pathlib import Path
import time

logger = logging.getLogger(__name__)


@dataclass
class SocialMediaProfile:
    """Represents a social media profile"""
    platform: str
    username: str
    found: bool
    profile_url: Optional[str] = None
    is_public: bool = False
    followers_count: Optional[int] = None
    posts_count: Optional[int] = None
    profile_info: Dict = None
    exposure_level: str = "UNKNOWN"
    last_updated: str = None


class SocialMediaScanning:
    """Scans for personal presence on social media"""
    
    def __init__(self, rate_limit_delay: float = 1.0, timeout: int = 15):
        """
        Initialize social media scanner
        
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
        
        # Define platform configurations
        self.platforms = {
            'linkedin': {
                'base_url': 'https://www.linkedin.com/in',
                'exposure': 'HIGH',
                'data_exposed': ['name', 'email', 'phone', 'location', 'work history']
            },
            'twitter': {
                'base_url': 'https://twitter.com',
                'exposure': 'HIGH',
                'data_exposed': ['username', 'tweets', 'followers', 'location', 'bio']
            },
            'github': {
                'base_url': 'https://github.com',
                'exposure': 'HIGH',
                'data_exposed': ['repositories', 'commits', 'email', 'location', 'bio']
            },
            'reddit': {
                'base_url': 'https://www.reddit.com/user',
                'exposure': 'MEDIUM',
                'data_exposed': ['posts', 'comments', 'karma', 'subreddits']
            },
            'stackoverflow': {
                'base_url': 'https://stackoverflow.com/users',
                'exposure': 'MEDIUM',
                'data_exposed': ['answers', 'questions', 'tags', 'reputation']
            },
            'medium': {
                'base_url': 'https://medium.com/@',
                'exposure': 'MEDIUM',
                'data_exposed': ['articles', 'followers', 'bio']
            },
            'facebook': {
                'base_url': 'https://www.facebook.com',
                'exposure': 'HIGH',
                'data_exposed': ['profile', 'photos', 'friends', 'posts', 'location']
            },
            'instagram': {
                'base_url': 'https://www.instagram.com',
                'exposure': 'HIGH',
                'data_exposed': ['photos', 'followers', 'location tags', 'bio']
            },
            'youtube': {
                'base_url': 'https://www.youtube.com/@',
                'exposure': 'MEDIUM',
                'data_exposed': ['videos', 'channel info', 'subscribers', 'playlists']
            },
            'twitch': {
                'base_url': 'https://www.twitch.tv',
                'exposure': 'MEDIUM',
                'data_exposed': ['streams', 'followers', 'channel info']
            },
            'discord': {
                'base_url': 'https://discord.com/users',
                'exposure': 'LOW',
                'data_exposed': ['servers (if public)', 'username']
            },
            'tiktok': {
                'base_url': 'https://www.tiktok.com/@',
                'exposure': 'HIGH',
                'data_exposed': ['videos', 'followers', 'likes', 'location hints']
            },
            'telegram': {
                'base_url': 'https://t.me',
                'exposure': 'LOW',
                'data_exposed': ['public channels', 'username']
            },
            'mastodon': {
                'base_url': 'https://mastodon.social/@',
                'exposure': 'LOW',
                'data_exposed': ['posts', 'followers', 'bio']
            },
            'gitlab': {
                'base_url': 'https://gitlab.com',
                'exposure': 'HIGH',
                'data_exposed': ['projects', 'commits', 'bio', 'email (if visible)']
            }
        }
    
    def scan_all_platforms(self, usernames: List[str]) -> List[SocialMediaProfile]:
        """
        Scan all platforms for given usernames
        
        Args:
            usernames: List of usernames to search
        
        Returns:
            List of SocialMediaProfile objects
        """
        all_profiles = []
        
        for username in usernames:
            logger.info(f"Scanning platforms for: {username}")
            
            for platform_key, platform_config in self.platforms.items():
                profile = self._scan_platform(platform_key, username)
                if profile:
                    all_profiles.append(profile)
                
                time.sleep(self.rate_limit_delay)
        
        self.results = all_profiles
        return all_profiles
    
    def _scan_platform(self, platform_key: str, username: str) -> Optional[SocialMediaProfile]:
        """Scan a specific platform for username"""
        
        try:
            if platform_key == 'linkedin':
                return self._scan_linkedin(username)
            elif platform_key == 'twitter':
                return self._scan_twitter(username)
            elif platform_key == 'github':
                return self._scan_github(username)
            elif platform_key == 'reddit':
                return self._scan_reddit(username)
            elif platform_key == 'stackoverflow':
                return self._scan_stackoverflow(username)
            elif platform_key == 'medium':
                return self._scan_medium(username)
            elif platform_key == 'facebook':
                return self._scan_facebook(username)
            elif platform_key == 'instagram':
                return self._scan_instagram(username)
            elif platform_key == 'youtube':
                return self._scan_youtube(username)
            elif platform_key == 'twitch':
                return self._scan_twitch(username)
            elif platform_key == 'discord':
                return self._scan_discord(username)
            elif platform_key == 'tiktok':
                return self._scan_tiktok(username)
            elif platform_key == 'telegram':
                return self._scan_telegram(username)
            elif platform_key == 'mastodon':
                return self._scan_mastodon(username)
            elif platform_key == 'gitlab':
                return self._scan_gitlab(username)
        
        except Exception as e:
            logger.debug(f"Error scanning {platform_key} for {username}: {e}")
        
        return None
    
    def _scan_linkedin(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan LinkedIn"""
        try:
            url = f"https://www.linkedin.com/in/{quote(username.lower())}"
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            
            if response.status_code == 200:
                profile = SocialMediaProfile(
                    platform='LinkedIn',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='HIGH',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Professional information visible'}
                )
                logger.info(f"✓ Found LinkedIn: {url}")
                return profile
        except Exception as e:
            logger.debug(f"LinkedIn scan error: {e}")
        
        return None
    
    def _scan_twitter(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan Twitter/X"""
        try:
            url = f"https://twitter.com/{quote(username)}"
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            
            if response.status_code == 200:
                profile = SocialMediaProfile(
                    platform='Twitter',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='HIGH',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Posts, followers, location visible'}
                )
                logger.info(f"✓ Found Twitter: {url}")
                return profile
        except Exception as e:
            logger.debug(f"Twitter scan error: {e}")
        
        return None
    
    def _scan_github(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan GitHub"""
        try:
            url = f"https://github.com/{quote(username)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200 and '404' not in response.text:
                profile = SocialMediaProfile(
                    platform='GitHub',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='HIGH',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Public repos, commits, email (if visible)'}
                )
                logger.info(f"✓ Found GitHub: {url}")
                return profile
        except Exception as e:
            logger.debug(f"GitHub scan error: {e}")
        
        return None
    
    def _scan_reddit(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan Reddit"""
        try:
            url = f"https://www.reddit.com/user/{quote(username)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if 'u_' not in response.url and response.status_code == 200:
                profile = SocialMediaProfile(
                    platform='Reddit',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='MEDIUM',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Posts, comments, profile info'}
                )
                logger.info(f"✓ Found Reddit: {url}")
                return profile
        except Exception as e:
            logger.debug(f"Reddit scan error: {e}")
        
        return None
    
    def _scan_stackoverflow(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan Stack Overflow"""
        try:
            # Stack Overflow uses numeric IDs, so username search is limited
            url = f"https://stackoverflow.com/search?q={quote(username)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if 'no results found' not in response.text.lower():
                profile = SocialMediaProfile(
                    platform='Stack Overflow',
                    username=username,
                    found=True,
                    profile_url=url,
                    exposure_level='MEDIUM',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Answers, questions, reputation'}
                )
                logger.info(f"✓ Found Stack Overflow mentions for: {username}")
                return profile
        except Exception as e:
            logger.debug(f"Stack Overflow scan error: {e}")
        
        return None
    
    def _scan_medium(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan Medium"""
        try:
            url = f"https://medium.com/@{quote(username)}"
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            
            if response.status_code == 200:
                profile = SocialMediaProfile(
                    platform='Medium',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='MEDIUM',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Articles, bio, followers'}
                )
                logger.info(f"✓ Found Medium: {url}")
                return profile
        except Exception as e:
            logger.debug(f"Medium scan error: {e}")
        
        return None
    
    def _scan_facebook(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan Facebook"""
        try:
            url = f"https://www.facebook.com/{quote(username)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if 'Page Not Found' not in response.text:
                profile = SocialMediaProfile(
                    platform='Facebook',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='HIGH',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Profile, photos, posts (if public)'}
                )
                logger.info(f"✓ Found Facebook: {url}")
                return profile
        except Exception as e:
            logger.debug(f"Facebook scan error: {e}")
        
        return None
    
    def _scan_instagram(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan Instagram"""
        try:
            url = f"https://www.instagram.com/{quote(username)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if 'not found' not in response.text.lower() and response.status_code == 200:
                profile = SocialMediaProfile(
                    platform='Instagram',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='HIGH',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Photos, followers, location tags'}
                )
                logger.info(f"✓ Found Instagram: {url}")
                return profile
        except Exception as e:
            logger.debug(f"Instagram scan error: {e}")
        
        return None
    
    def _scan_youtube(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan YouTube"""
        try:
            url = f"https://www.youtube.com/@{quote(username)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200 and 'not found' not in response.text.lower():
                profile = SocialMediaProfile(
                    platform='YouTube',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='MEDIUM',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Videos, subscribers, channel info'}
                )
                logger.info(f"✓ Found YouTube: {url}")
                return profile
        except Exception as e:
            logger.debug(f"YouTube scan error: {e}")
        
        return None
    
    def _scan_twitch(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan Twitch"""
        try:
            url = f"https://www.twitch.tv/{quote(username)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                profile = SocialMediaProfile(
                    platform='Twitch',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='MEDIUM',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Stream info, followers, schedule'}
                )
                logger.info(f"✓ Found Twitch: {url}")
                return profile
        except Exception as e:
            logger.debug(f"Twitch scan error: {e}")
        
        return None
    
    def _scan_discord(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan Discord (limited, mostly servers)"""
        try:
            # Discord doesn't have traditional user URLs for non-bots
            # This is a placeholder for custom Discord searches
            return None
        except Exception as e:
            logger.debug(f"Discord scan error: {e}")
        
        return None
    
    def _scan_tiktok(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan TikTok"""
        try:
            url = f"https://www.tiktok.com/@{quote(username)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200 and 'not found' not in response.text.lower():
                profile = SocialMediaProfile(
                    platform='TikTok',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='HIGH',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Videos, followers, likes, location hints'}
                )
                logger.info(f"✓ Found TikTok: {url}")
                return profile
        except Exception as e:
            logger.debug(f"TikTok scan error: {e}")
        
        return None
    
    def _scan_telegram(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan Telegram (public channels only)"""
        try:
            url = f"https://t.me/{quote(username)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200 and 'channel not found' not in response.text.lower():
                profile = SocialMediaProfile(
                    platform='Telegram',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='LOW',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Public channel info'}
                )
                logger.info(f"✓ Found Telegram: {url}")
                return profile
        except Exception as e:
            logger.debug(f"Telegram scan error: {e}")
        
        return None
    
    def _scan_mastodon(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan Mastodon"""
        try:
            url = f"https://mastodon.social/@{quote(username)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200 and '404' not in response.text:
                profile = SocialMediaProfile(
                    platform='Mastodon',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='LOW',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Posts, followers, bio'}
                )
                logger.info(f"✓ Found Mastodon: {url}")
                return profile
        except Exception as e:
            logger.debug(f"Mastodon scan error: {e}")
        
        return None
    
    def _scan_gitlab(self, username: str) -> Optional[SocialMediaProfile]:
        """Scan GitLab"""
        try:
            url = f"https://gitlab.com/{quote(username)}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200 and '404' not in response.text:
                profile = SocialMediaProfile(
                    platform='GitLab',
                    username=username,
                    found=True,
                    profile_url=url,
                    is_public=True,
                    exposure_level='HIGH',
                    last_updated=datetime.now().isoformat(),
                    profile_info={'exposure': 'Projects, commits, bio, email'}
                )
                logger.info(f"✓ Found GitLab: {url}")
                return profile
        except Exception as e:
            logger.debug(f"GitLab scan error: {e}")
        
        return None
    
    def export_results(self, output_path: str = "discovery/social_media_results.json"):
        """Export results to JSON"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            results_data = {
                "timestamp": datetime.now().isoformat(),
                "total_platforms_scanned": len(self.platforms),
                "profiles_found": len([r for r in self.results if r.found]),
                "high_exposure_accounts": len([r for r in self.results if r.exposure_level == 'HIGH']),
                "profiles": [
                    {
                        "platform": p.platform,
                        "username": p.username,
                        "found": p.found,
                        "profile_url": p.profile_url,
                        "is_public": p.is_public,
                        "exposure_level": p.exposure_level,
                        "last_updated": p.last_updated,
                        "profile_info": p.profile_info
                    }
                    for p in self.results
                ]
            }
            
            with open(output_path, 'w') as f:
                json.dump(results_data, f, indent=2, default=str)
            
            logger.info(f"Social media results exported to {output_path}")
        
        except Exception as e:
            logger.error(f"Failed to export results: {e}")


# Utility function
def scan_social_media(usernames: List[str]) -> List[SocialMediaProfile]:
    """Convenience function to scan all platforms"""
    scanner = SocialMediaScanning()
    return scanner.scan_all_platforms(usernames)


if __name__ == "__main__":
    # Test scanning
    scanner = SocialMediaScanning()
    
    usernames = ["chaitanyajoshi1769", "c_joshi", "chaitanya"]
    results = scanner.scan_all_platforms(usernames)
    scanner.export_results()
    
    found = len([r for r in results if r.found])
    print(f"✓ Scanned {len(scanner.platforms)} platforms")
    print(f"✓ Found {found} profiles")
    print(f"✓ Results exported to discovery/social_media_results.json")
