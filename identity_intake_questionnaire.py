#!/usr/bin/env python3
"""
IDENTITY INTAKE QUESTIONNAIRE

This tool collects comprehensive identity data for correlation analysis.
All sensitive data is encrypted locally. This forms the basis for:
- Master identity graph construction
- Correlation analysis across platforms
- Exposure discovery targeting
- Risk prioritization

STRUCTURE:
- Personal identifiers (names, aliases)
- Contact information (email, phone)
- Location history
- Professional/educational history
- Online presence (usernames, profiles, accounts)
- Digital artifacts (domains, repositories, documents)
- Known exposures (breaches, leaks)
"""

# ============================================================================
# SECTION A: PERSONAL IDENTIFIERS
# ============================================================================

PERSONAL_IDENTIFIERS = {
    "instructions": "Provide all names, nicknames, and aliases you've used",
    "questions": [
        {
            "id": "legal_name",
            "question": "What is your legal name?",
            "type": "text",
            "required": True,
            "help": "First, middle, last",
            "example": "John Michael Smith"
        },
        {
            "id": "previous_names",
            "question": "Previous legal names (maiden names, changed names, etc)?",
            "type": "list",
            "required": False,
            "help": "Include marriage names, name changes for any reason",
            "example": ["Jane Doe", "Maria Garcia"]
        },
        {
            "id": "common_nicknames",
            "question": "Common nicknames people call you?",
            "type": "list",
            "required": False,
            "help": "Informal names used in personal/professional contexts",
            "example": ["Mike", "J", "Doc"]
        },
        {
            "id": "professional_aliases",
            "question": "Professional aliases or pen names?",
            "type": "list",
            "required": False,
            "help": "Names used for writing, consulting, branding",
            "example": ["M.J. Smith", "Dr. John Michael"]
        },
        {
            "id": "gamer_handles",
            "question": "Gamer tags or gaming aliases?",
            "type": "list",
            "required": False,
            "help": "Usernames from gaming platforms",
            "example": ["xXSniper420Xx", "ShadowNinja"]
        },
        {
            "id": "family_names",
            "question": "Family member names that appear publicly with you?",
            "type": "list",
            "required": False,
            "help": "Spouse, children, parents, siblings (for correlation)",
            "example": ["Sarah Smith", "Tom Smith Jr"]
        }
    ]
}

# ============================================================================
# SECTION B: CONTACT INFORMATION
# ============================================================================

CONTACT_INFORMATION = {
    "instructions": "All email addresses and phone numbers you've used",
    "questions": [
        {
            "id": "primary_email",
            "question": "Primary email address?",
            "type": "text",
            "required": True,
            "help": "Most commonly used email",
            "validation": "email"
        },
        {
            "id": "secondary_emails",
            "question": "Secondary/historical email addresses?",
            "type": "list",
            "required": False,
            "help": "Old emails, alternative addresses, aliases",
            "example": ["john.smith@company.com", "j.smith1990@gmail.com"]
        },
        {
            "id": "email_variations",
            "question": "Email variations you've used?",
            "type": "list",
            "required": False,
            "help": "john.smith@, j.smith@, js@, johnsmith@",
            "example": ["j.smith@", "john_smith@"]
        },
        {
            "id": "phone_numbers",
            "question": "Phone numbers (primary and historical)?",
            "type": "list",
            "required": False,
            "help": "Include country codes, all past numbers",
            "example": ["+1-555-0123", "+44-20-7123-4567"]
        },
        {
            "id": "username_patterns",
            "question": "Common username patterns you use?",
            "type": "list",
            "required": False,
            "help": "How you typically construct usernames",
            "example": ["jsmith", "j.smith", "john_smith", "smith_john"]
        }
    ]
}

# ============================================================================
# SECTION C: LOCATION HISTORY
# ============================================================================

LOCATION_HISTORY = {
    "instructions": "Current and historical locations",
    "questions": [
        {
            "id": "current_address",
            "question": "Current home address?",
            "type": "text",
            "required": False,
            "help": "Street, city, state, country (consider privacy implications of storing)",
            "note": "Will be stored encrypted. Critical for removal/suppression."
        },
        {
            "id": "previous_addresses",
            "question": "Previous home addresses?",
            "type": "list",
            "required": False,
            "help": "All addresses where you've lived (especially if publicly exposed)",
            "example": ["123 Main St, Springfield, IL", "456 Oak Ave, Chicago, IL"]
        },
        {
            "id": "work_addresses",
            "question": "Work addresses or office locations?",
            "type": "list",
            "required": False,
            "help": "Business addresses associated with you",
        },
        {
            "id": "countries_lived",
            "question": "Countries where you've lived?",
            "type": "list",
            "required": False,
            "example": ["United States", "Canada", "United Kingdom"]
        },
        {
            "id": "cities_lived",
            "question": "Major cities where you've lived?",
            "type": "list",
            "required": False,
            "example": ["New York", "San Francisco", "London"]
        },
        {
            "id": "publicly_exposed_location",
            "question": "Has your location ever been publicly exposed/posted?",
            "type": "bool",
            "required": False,
            "help": "Mark any addresses you know are online"
        }
    ]
}

# ============================================================================
# SECTION D: EDUCATION & EMPLOYMENT
# ============================================================================

EDUCATION_EMPLOYMENT = {
    "instructions": "Schools, universities, employers",
    "questions": [
        {
            "id": "universities",
            "question": "Universities attended?",
            "type": "list",
            "required": False,
            "help": "Name, graduation year if publicly available",
            "example": ["University of California (2020)", "MIT (2015)"]
        },
        {
            "id": "schools",
            "question": "Secondary schools?",
            "type": "list",
            "required": False,
            "help": "High school, preparatory schools",
            "example": ["Lincoln High School", "St. Joseph Academy"]
        },
        {
            "id": "employers",
            "question": "Current and previous employers?",
            "type": "list",
            "required": False,
            "help": "Company names, job titles if publicly listed",
            "example": ["Tech Corp (2018-2022, Senior Engineer)", "StartupX (2022-present)"]
        },
        {
            "id": "llc_businesses",
            "question": "LLCs, sole proprietorships, or businesses you operate?",
            "type": "list",
            "required": False,
            "help": "Business names, registration dates",
            "example": ["Smith Consulting LLC", "TechCorp Solutions"]
        },
        {
            "id": "professional_memberships",
            "question": "Professional memberships or associations?",
            "type": "list",
            "required": False,
            "help": "IEEE, bar association, medical licensing, etc.",
            "example": ["IEEE Member #12345", "California Bar Association"]
        }
    ]
}

# ============================================================================
# SECTION E: ONLINE PRESENCE & ACCOUNTS
# ============================================================================

ONLINE_PRESENCE = {
    "instructions": "All social media, forums, and online accounts",
    "questions": [
        {
            "id": "linkedin_profiles",
            "question": "LinkedIn profiles (current and past)?",
            "type": "list",
            "required": False,
            "help": "Include URLs or profile IDs",
            "example": ["linkedin.com/in/jsmith"]
        },
        {
            "id": "twitter_accounts",
            "question": "Twitter/X accounts?",
            "type": "list",
            "required": False,
            "help": "Handles including ones you don't actively use",
            "example": ["@jsmith", "@smith_john"]
        },
        {
            "id": "github_accounts",
            "question": "GitHub accounts?",
            "type": "list",
            "required": False,
            "help": "All usernames, including inactive",
            "example": ["github.com/jsmith", "github.com/john-michael-smith"]
        },
        {
            "id": "stackoverflow",
            "question": "Stack Overflow accounts?",
            "type": "list",
            "required": False,
            "help": "Profile URLs or usernames",
        },
        {
            "id": "reddit_accounts",
            "question": "Reddit accounts?",
            "type": "list",
            "required": False,
            "help": "All usernames (including throwaway accounts if memorable)",
            "example": ["/u/jsmith", "/u/throwaway_12345"]
        },
        {
            "id": "discord_handles",
            "question": "Discord handles or server memberships?",
            "type": "list",
            "required": False,
            "help": "Username and any associated server IDs",
        },
        {
            "id": "telegram_accounts",
            "question": "Telegram usernames or contacts?",
            "type": "list",
            "required": False,
            "help": "Public usernames or profile links",
        },
        {
            "id": "instagram_accounts",
            "question": "Instagram accounts?",
            "type": "list",
            "required": False,
            "help": "All usernames, public and private",
            "example": ["@jsmith_photography"]
        },
        {
            "id": "facebook_profiles",
            "question": "Facebook profiles?",
            "type": "list",
            "required": False,
            "help": "Personal profiles, pages, business accounts",
        },
        {
            "id": "tiktok_accounts",
            "question": "TikTok accounts?",
            "type": "list",
            "required": False,
            "help": "Usernames on creator platform",
        },
        {
            "id": "youtube_channels",
            "question": "YouTube channels?",
            "type": "list",
            "required": False,
            "help": "All channel URLs",
            "example": ["youtube.com/@jsmith"]
        },
        {
            "id": "twitch_channels",
            "question": "Twitch channels?",
            "type": "list",
            "required": False,
            "help": "Streamer profiles",
        },
        {
            "id": "medium_profiles",
            "question": "Medium blog profiles?",
            "type": "list",
            "required": False,
            "help": "Medium.com/@username",
        },
        {
            "id": "substack_newsletters",
            "question": "Substack newsletters or profiles?",
            "type": "list",
            "required": False,
            "help": "Newsletter names, publication URLs",
        },
        {
            "id": "other_forums",
            "question": "Other forums or community accounts?",
            "type": "list",
            "required": False,
            "help": "Hacker News, Product Hunt, niche communities, etc.",
            "example": ["Hacker News: jsmith", "Product Hunt: @smithjohn"]
        },
        {
            "id": "dating_apps",
            "question": "Dating app profiles (Tinder, Bumble, Hinge, etc)?",
            "type": "list",
            "required": False,
            "help": "May contain photos/personal info",
        },
        {
            "id": "crypto_wallets",
            "question": "Public cryptocurrency wallets or addresses?",
            "type": "list",
            "required": False,
            "help": "Bitcoin, Ethereum, etc. addresses",
            "example": ["1A1z7agoat2agoatA1gao2agoa"]
        },
        {
            "id": "professional_platforms",
            "question": "Other professional platforms (AngelList, ProductHunt, etc)?",
            "type": "list",
            "required": False,
        }
    ]
}

# ============================================================================
# SECTION F: DIGITAL ARTIFACTS & CONTENT
# ============================================================================

DIGITAL_ARTIFACTS = {
    "instructions": "Domains, blogs, repositories, documents you own or created",
    "questions": [
        {
            "id": "personal_domains",
            "question": "Personal domains you own or have owned?",
            "type": "list",
            "required": False,
            "help": "Including expired/parked domains",
            "example": ["jsmith.com", "john-smith-consulting.net"]
        },
        {
            "id": "websites",
            "question": "Personal websites or blogs?",
            "type": "list",
            "required": False,
            "help": "Current and archived sites",
            "example": ["jsmith.com", "blog.jsmith.com"]
        },
        {
            "id": "old_websites",
            "question": "Old/deprecated websites or portfolios?",
            "type": "list",
            "required": False,
            "help": "Even if offline, may be in Internet Archive",
        },
        {
            "id": "git_repositories",
            "question": "Public Git repositories (GitHub, GitLab, etc)?",
            "type": "list",
            "required": False,
            "help": "All public repos with your identity",
            "example": ["github.com/jsmith/myproject"]
        },
        {
            "id": "documentation_written",
            "question": "Technical documentation or articles written?",
            "type": "list",
            "required": False,
            "help": "Published articles, tech docs, guides",
        },
        {
            "id": "publicly_uploaded_pdfs",
            "question": "PDFs with your name/info publicly available?",
            "type": "list",
            "required": False,
            "help": "CVs, resumes, whitepapers, research papers",
        },
        {
            "id": "resume_locations",
            "question": "Where your resume/CV might be publicly available?",
            "type": "list",
            "required": False,
            "help": "Indeed, LinkedIn, university sites, etc.",
        },
        {
            "id": "image_uploads",
            "question": "Profile pictures or photos you've uploaded to accounts?",
            "type": "text",
            "required": False,
            "help": "Approximate number and platforms",
            "example": "5-10 photos across LinkedIn, Twitter, GitHub"
        },
        {
            "id": "podcast_appearances",
            "question": "Podcast episodes featuring you?",
            "type": "list",
            "required": False,
            "help": "Podcast name, episode title/date",
        },
        {
            "id": "conference_talks",
            "question": "Conference talks or presentations?",
            "type": "list",
            "required": False,
            "help": "Conference, date, talk title, video links",
        },
        {
            "id": "news_mentions",
            "question": "News articles or press mentions?",
            "type": "list",
            "required": False,
            "help": "Publication, date, URL if known",
        },
        {
            "id": "scientific_publications",
            "question": "Scientific publications or academic papers?",
            "type": "list",
            "required": False,
            "help": "ArXiv, Google Scholar, institutional repositories",
        }
    ]
}

# ============================================================================
# SECTION G: SECURITY & EXPOSURE HISTORY
# ============================================================================

SECURITY_EXPOSURE = {
    "instructions": "Known data breaches, leaked credentials, security incidents",
    "questions": [
        {
            "id": "known_breaches",
            "question": "Data breaches you're aware of (from Have I Been Pwned)?",
            "type": "list",
            "required": False,
            "help": "Site name, approximate date, type of data",
            "example": ["LinkedIn breach 2012", "Yahoo breach 2013"]
        },
        {
            "id": "exposed_passwords",
            "question": "Passwords you've used that may be exposed?",
            "type": "bool",
            "required": False,
            "help": "Track in password manager, not here",
        },
        {
            "id": "leaked_personal_data",
            "question": "Personal information leaked (address, phone, etc)?",
            "type": "bool",
            "required": False,
            "help": "Mark any known leaks",
        },
        {
            "id": "paste_sites_exposure",
            "question": "Ever had data posted to Pastebin, Paste.ee, etc?",
            "type": "bool",
            "required": False,
        },
        {
            "id": "doxing_incidents",
            "question": "Ever been doxed or had info maliciously posted?",
            "type": "bool",
            "required": False,
            "help": "Important for removal priority"
        },
        {
            "id": "revenge_porn_exposure",
            "question": "Any intimate images non-consensually shared online?",
            "type": "bool",
            "required": False,
            "help": "Contact platform support + legal (NCMEC, FBI IC3)"
        },
        {
            "id": "dark_web_exposure",
            "question": "Ever checked if your data appears on dark web?",
            "type": "bool",
            "required": False,
        },
        {
            "id": "credit_monitoring",
            "question": "Evidence of identity theft or credit fraud?",
            "type": "bool",
            "required": False,
            "help": "File credit freeze if true"
        }
    ]
}

# ============================================================================
# SECTION H: PRIORITIES & SPECIAL CONSIDERATIONS
# ============================================================================

PRIORITIES = {
    "instructions": "What's most important to remove/suppress?",
    "questions": [
        {
            "id": "removal_priorities",
            "question": "What's your top removal priority?",
            "type": "list",
            "required": False,
            "help": "Rank by urgency",
            "example": ["Home address", "Phone number", "Photo from incident"]
        },
        {
            "id": "safety_concerns",
            "question": "Any safety concerns (stalking, harassment, abuse)?",
            "type": "text",
            "required": False,
            "help": "Impacts removal strategy and urgency"
        },
        {
            "id": "professional_implications",
            "question": "Professional implications of exposure?",
            "type": "text",
            "required": False,
            "help": "Job, reputation, client relationships affected?"
        },
        {
            "id": "financial_implications",
            "question": "Financial implications of exposure?",
            "type": "text",
            "required": False,
            "help": "Identity theft risk, business impact?"
        },
        {
            "id": "specific_incidents",
            "question": "Any specific incidents you want to remediate?",
            "type": "text",
            "required": False,
            "help": "Describe what happened and impact",
        },
        {
            "id": "removal_targets",
            "question": "Specific websites/platforms to target for removal?",
            "type": "list",
            "required": False,
            "help": "Where you most want to be removed from",
        },
        {
            "id": "acceptable_footprint",
            "question": "What minimal online presence is acceptable?",
            "type": "text",
            "required": False,
            "help": "LinkedIn only? GitHub only? Complete erasure?",
            "example": "Keep GitHub for professional credibility, remove everything else"
        },
        {
            "id": "timeline_urgency",
            "question": "Timeline urgency?",
            "type": "choice",
            "choices": ["ASAP (emergency)", "1 week", "1 month", "Ongoing priority"],
            "required": False,
        }
    ]
}

# ============================================================================
# INTERACTIVE INTAKE SCRIPT
# ============================================================================

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    IDENTITY INTAKE QUESTIONNAIRE                           ║
║                                                                            ║
║  This questionnaire establishes your digital identity profile.             ║
║  All data is encrypted and stored locally.                                 ║
║                                                                            ║
║  Estimated time: 30-60 minutes                                             ║
║  You can save progress and return later                                    ║
╚════════════════════════════════════════════════════════════════════════════╝

INSTRUCTIONS:
- Answer as completely as possible
- Include historical information (old emails, previous usernames, etc)
- Be specific where helpful (include URLs, dates, profiles)
- Skip questions that don't apply
- Mark anything currently exposed as publicly discoverable

SECTIONS:
A. Personal Identifiers
B. Contact Information
C. Location History
D. Education & Employment
E. Online Presence & Accounts
F. Digital Artifacts & Content
G. Security & Exposure History
H. Priorities & Special Considerations
    """)

    print("\n[Interactive mode would execute here with proper CLI framework]")
    print("Run: python footprint_ops/cli.py intake --interactive")
