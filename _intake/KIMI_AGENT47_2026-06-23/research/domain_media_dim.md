# CSOAI Media, Entertainment, Gaming & Sports Data Sources

> **Research Date**: 2026-06  
> **Purpose**: Free/Open data sources for CSOAI Media/Entertainment/Sports Hive  
> **Sources Searched**: 15+ APIs, Datasets, and Platforms  
> **Total Sources Documented**: 30+

---

## Table of Contents

1. [Streaming & Viewership Data](#1-streaming--viewership-data)
2. [Video & Social Media APIs](#2-video--social-media-apis)
3. [Gaming Industry Data](#3-gaming-industry-data)
4. [Sports Statistics APIs](#4-sports-statistics-apis)
5. [Music & Audio Data](#5-music--audio-data)
6. [Social Media & Community Data](#6-social-media--community-data)
7. [Market Research & Industry Reports](#7-market-research--industry-reports)
8. [Esports Data](#8-esports-data)
9. [Open Datasets & Alternative Sources](#9-open-datasets--alternative-sources)
10. [Quick Comparison Matrix](#10-quick-comparison-matrix)

---

## 1. Streaming & Viewership Data

### 1.1 Twitch Developer API (Helix)

| Attribute | Detail |
|-----------|--------|
| **Name** | Twitch API (Helix) |
| **URL** | https://dev.twitch.tv/docs/api/ |
| **Format** | REST JSON |
| **API Key** | Yes (OAuth 2.0 + Client ID) |
| **Rate Limits** | ~800 points/minute per app token (varies by endpoint) |
| **Free Tier** | Yes - completely free for all non-commercial and most commercial uses |
| **Paid Tier** | Enterprise agreements for very high volume |

**Endpoints Available:**
- `Get Streams` - List all current live streams with viewer counts, game, title
- `Get Games` / `Get Top Games` - Game metadata and ranking by viewership
- `Get Clips` - Most-viewed clips per game/channel
- `Get Videos` - VODs with view counts
- `Get Channel Information` - Channel details, follower counts
- `Get Channel Followers` - Follower counts and follower lists
- `Get Users` - User/channel profile data
- `Get Chatters` - Real-time chat user counts
- `Search Channels` / `Search Categories` - Discovery
- `Get Extension Analytics` / `Get Game Analytics` - Aggregated performance data
- `EventSub` - Real-time webhooks for stream events (go live, follow, etc.)

**CSOAI Use Case:**
- Real-time streaming popularity tracking by game/category
- Viewer count trends, concurrent viewership analysis
- Game launch performance via stream metrics
- Influencer/streamer identification and ranking
- Streaming platform competitive intelligence
- Content creator economy analysis

**Authentication:** Requires Twitch account, app registration at https://dev.twitch.tv/console [^1727^] [^1728^] [^1732^]

---

### 1.2 YouTube Data API v3

| Attribute | Detail |
|-----------|--------|
| **Name** | YouTube Data API v3 |
| **URL** | https://developers.google.com/youtube/v3 |
| **Format** | REST JSON |
| **API Key** | Yes (Google Cloud API key) |
| **Rate Limits** | 10,000 quota units/day per project (free tier) |
| **Free Tier** | Yes - no monetary cost, quota-based |
| **Paid Tier** | Quota extension requests (free, reviewed by Google) |

**Quota Costs per Operation:**
- `videos.list` (stats): 1 unit (~500K video stats/day)
- `channels.list`: 1 unit
- `search.list`: 100 units
- `videos.insert`: ~100 units
- `playlistItems.list`: 1-2 units
- `commentThreads.list`: 1 unit
- `captions.list`: 50 units

**Key Endpoints:**
- Channel statistics (subscribers, views, video count)
- Video metrics (views, likes, comments, duration)
- Search and discovery
- Playlist data
- Comment threads
- Caption/subtitle data

**CSOAI Use Case:**
- Video content performance tracking by channel/topic
- Gaming content trends (let's plays, reviews, esports)
- Influencer ranking and identification
- Music video popularity trends
- Audience engagement analysis
- Content genre performance comparison

**Notes:** No paid commercial tier published by Google. Quota resets at midnight Pacific Time. [^1697^]

---

## 2. Video & Social Media APIs

### 2.1 Social Blade API

| Attribute | Detail |
|-----------|--------|
| **Name** | Social Blade Business API |
| **URL** | https://socialblade.com/developers |
| **Format** | REST JSON |
| **API Key** | Yes (credit-based system) |
| **Rate Limits** | Based on purchased credits |
| **Free Tier** | No free tier; credits start at ~$0.06-$0.50/credit |
| **Paid Tier** | Credit packages: 100 ($50), 500, 1K, 5K, 7.5K credits |

**Supported Platforms:**
- YouTube, Instagram, Facebook, Twitch, TikTok

**Data Available:**
- Follower/subscriber counts (current + historical up to 3 years YouTube, 10 years others)
- View counts and engagement metrics
- Daily/weekly/monthly growth rates
- Social Blade letter grade rankings
- Estimated earnings data
- Top charts and leaderboards by country/category
- Linked social accounts mapping

**CSOAI Use Case:**
- Cross-platform creator ranking and comparison
- Influencer market sizing and tracking
- Platform growth trends (TikTok vs YouTube vs Instagram)
- Creator economy monetization analysis
- Brand partnership intelligence

**Alternatives:** Apify Social Blade Scraper offers free tier access [^1755^] [^1756^] [^1761^]

---

### 2.2 X (Twitter) API

| Attribute | Detail |
|-----------|--------|
| **Name** | X API (formerly Twitter API) |
| **URL** | https://developer.x.com/en/docs/x-api |
| **Format** | REST JSON |
| **API Key** | Yes (OAuth 2.0) |
| **Free Tier** | Free Write-only (1,500 posts/month) |
| **Paid Tier** | Basic $100/mo (10K tweets); Enterprise $42K+/mo |

**Key Capabilities:**
- Tweet lookup and search (paid)
- User profile data
- Real-time streaming (enterprise)
- Posting and engagement (free tier)
- Analytics and metrics

**CSOAI Use Case:**
- Social media trend analysis
- Entertainment buzz tracking
- Live event social engagement
- Brand sentiment monitoring

**Note:** Significantly restricted since 2023 API changes. Academic access available for research. [^1762^]

---

## 3. Gaming Industry Data

### 3.1 Steam Web API (Official - Valve)

| Attribute | Detail |
|-----------|--------|
| **Name** | Steam Web API |
| **URL** | https://partner.steamgames.com/doc/webapi_overview |
| **Format** | JSON, XML, VDF |
| **API Key** | Yes (free, register at steamcommunity.com/dev/apikey) |
| **Rate Limits** | ~100,000 requests/day |
| **Free Tier** | Yes - completely free |
| **Paid Tier** | None |

**Key Endpoints:**
- `ISteamUserStats/GetNumberOfCurrentPlayers` - Live concurrent players per game
- `ISteamUserStats/GetGlobalAchievementPercentagesForApp` - Achievement rates
- `ISteamUserStats/GetPlayerAchievements` - Per-user achievement data
- `ISteamUserStats/GetSchemaForGame` - Game stats and achievements schema
- `ISteamUser/GetPlayerSummaries` - User profile summaries (up to 100 users)
- `ISteamUser/GetFriendList` - Friend networks
- `IPlayerService/GetOwnedGames` - Game libraries, playtime
- `IPlayerService/GetRecentlyPlayedGames` - Recent playtime (2 weeks)
- `ISteamApps/GetAppList` - Full catalog of Steam apps
- Store API (unofficial): pricing, reviews, tags, descriptions

**CSOAI Use Case:**
- Real-time game popularity (concurrent players)
- Game launch performance tracking
- Player engagement and retention metrics
- Achievement completion rate analysis
- Game catalog analysis (genre, pricing trends)
- Platform competitive intelligence

**Historical Note:** Steam does NOT provide historical player counts via API. SteamDB and SteamCharts have been collecting this data since ~2010. [^1694^] [^1695^] [^1696^]

---

### 3.2 SteamDB / SteamCharts (Unofficial Aggregators)

| Attribute | Detail |
|-----------|--------|
| **Name** | SteamCharts.com / SteamDB.info |
| **URL** | https://steamcharts.com / https://steamdb.info |
| **Format** | HTML (scrapable) + API via Parse.bot wrapper |
| **API Key** | No (web scrape) / Yes (for Parse.bot API wrapper) |
| **Rate Limits** | N/A for web; 5 req/min (Parse free tier) |
| **Free Tier** | Website data is free; Parse.bot wrapper has free tier (100 calls/mo) |

**Data Available:**
- Monthly average/peak concurrent players per game
- 24-hour peaks and all-time peaks
- Trending games (by % change)
- Historical player count data (back to ~2010)
- Game metadata (genre, developer, release date)
- Hours played (last 30 days)
- Top games leaderboards

**CSOAI Use Case:**
- Long-term game health tracking
- Genre/platform trend analysis
- Seasonal player behavior patterns
- Game lifecycle analysis
- Competitive landscape monitoring

**Note:** Parse.bot provides a typed REST API wrapper: `api.parse.bot/scraper/3fcf8070-ee16-4adc-be24-2c51d943c5fe/` [^1695^] [^1704^]

---

### 3.3 IGDB (Internet Game Database) API

| Attribute | Detail |
|-----------|--------|
| **Name** | IGDB API |
| **URL** | https://api-docs.igdb.com/ |
| **Format** | REST JSON (POST-based queries) |
| **API Key** | Yes (Twitch Developer OAuth2) |
| **Rate Limits** | 4 requests/second (~10K requests/month effectively) |
| **Free Tier** | Yes - completely free for non-commercial AND commercial use |
| **Paid Tier** | None (fully free) |

**Data Available (500K+ games):**
- Game metadata (title, release date, genres, platforms, themes)
- Developer and publisher information
- Game ratings and aggregated review scores
- Screenshots, artwork, videos
- Platform availability and release dates
- Franchise and series relationships
- Game engines and technologies
- Multiplayer modes and features
- DLC and expansion data
- Player perspectives, themes, keywords

**CSOAI Use Case:**
- Comprehensive game catalog and metadata
- Cross-platform game availability tracking
- Genre trend analysis over time
- Game development ecosystem mapping
- Franchise performance analysis
- Gaming industry timeline analysis

**Authentication:** Requires Twitch account with 2FA, app registration at Twitch Developer Portal [^1698^] [^1699^] [^1701^] [^1702^]

---

### 3.4 RAWG Video Games Database API

| Attribute | Detail |
|-----------|--------|
| **Name** | RAWG Video Games Database API |
| **URL** | https://api.rawg.io/docs/ |
| **Format** | REST JSON |
| **API Key** | Yes (required with every request) |
| **Rate Limits** | 20,000 requests/month (free tier) |
| **Free Tier** | Yes - free for personal use with attribution |
| **Paid Tier** | Contact api@rawg.io for commercial >100K MAU or 500K page views |

**Data Available (350K+ games):**
- Game search with typo handling
- Detailed game information (genre, platform, tags, ratings)
- Metacritic ratings integration
- Store links (cross-platform price tracking)
- Similar games (ML-based visual similarity)
- Steam average playtime data
- RAWG player counts and user ratings
- Screenshots and trailers
- Developer/publisher profiles
- Release calendars

**CSOAI Use Case:**
- Game discovery and recommendation engines
- Cross-store price comparison analysis
- User rating sentiment analysis
- Game similarity and clustering
- Platform exclusivity analysis
- Release schedule intelligence

**Terms:** Free for personal use with RAWG attribution and backlink. Free for commercial startups with <100K MAU. [^1753^] [^1754^] [^1759^] [^1763^] [^1765^]

---

### 3.5 Video Game Insights (Steam Analytics)

| Attribute | Detail |
|-----------|--------|
| **Name** | Video Game Insights (VGI) |
| **URL** | https://app.sensortower.com/vgi/ |
| **Format** | Web UI + downloadable data |
| **API Key** | No (web-based) |
| **Rate Limits** | N/A |
| **Free Tier** | Yes - basic analytics free |
| **Paid Tier** | Sensor Tower subscription for full features |

**Data Available:**
- 100,000+ Steam games with sales estimates
- Top charts (grossing, most played)
- Genre analytics (performance, supply-demand)
- Publisher/developer databases
- Pricing history and trends
- Wishlist data
- Rating analysis
- Revenue estimates

**CSOAI Use Case:**
- Steam market sizing and forecasting
- Genre performance benchmarking
- Indie vs AAA publisher analysis
- Pricing strategy intelligence
- Revenue estimation modeling

---

## 4. Sports Statistics APIs

### 4.1 ESPN Hidden API (Unofficial)

| Attribute | Detail |
|-----------|--------|
| **Name** | ESPN API (undocumented) |
| **URL** | https://site.api.espn.com/apis/site/v2/sports/ |
| **Format** | REST JSON |
| **API Key** | No - completely open, no auth required |
| **Rate Limits** | Not documented; appears generous |
| **Free Tier** | Yes - completely free |
| **Paid Tier** | None |

**Data Available:**
- Live scores for NFL, NBA, MLB, NHL, Soccer, UFC, Cricket, College sports
- Full box scores and play-by-play
- Team and player statistics
- Schedules and results
- Standings and rankings
- Injury reports
- Roster information
- Team news and recaps
- Player profiles and career stats

**Sports Supported:**
- Football (NFL), Basketball (NBA/NCAA), Baseball (MLB)
- Hockey (NHL), Soccer (multiple leagues), UFC/MMA
- Tennis, Golf, Cricket, Rugby, eSports
- Formula 1, NASCAR, Olympics

**CSOAI Use Case:**
- Real-time sports score tracking and alerts
- League-wide performance analytics
- Player statistics trending
- Fan engagement analysis
- Sports betting market intelligence
- Cross-sport popularity comparison

**Example Endpoints:**
- `site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
- `site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard`

**Note:** This is an undocumented internal API. Structure may change without notice. [^1685^] [^1687^] [^1693^]

---

### 4.2 API-SPORTS (API-Football, API-NBA, etc.)

| Attribute | Detail |
|-----------|--------|
| **Name** | API-SPORTS |
| **URL** | https://api-sports.io/ |
| **Format** | REST JSON |
| **API Key** | Yes (free on registration) |
| **Rate Limits** | 100 requests/day (free tier); 30 req/min |
| **Free Tier** | Yes - 100 requests/day, all endpoints |
| **Paid Tier** | Starting at $10/month |

**Available APIs:**
- **API-Football**: 2,000+ competitions, 700+ cups/leagues
- **API-NBA**: NBA games, players, stats, standings
- **API-NHL**: Hockey data
- **API-Baseball**: MLB data
- **API-Formula 1**: F1 races, drivers, constructors
- **API-Rugby**: Rugby union data
- **API-CRICKET**: Cricket matches and stats

**Key Features:**
- Live scores updated every 15 seconds
- Pre-match and live odds
- Line-ups, events, statistics
- Historical data (15+ years)
- Standings, fixtures, results
- Free widgets included

**CSOAI Use Case:**
- Multi-sport live score aggregation
- League-wide statistical analysis
- Sports betting data integration
- Fantasy sports analytics
- Sports market intelligence across leagues

[^1691^] [^1692^] [^1688^]

---

### 4.3 Sportmonks Football API

| Attribute | Detail |
|-----------|--------|
| **Name** | Sportmonks Football API |
| **URL** | https://www.sportmonks.com/ |
| **Format** | REST JSON |
| **API Key** | Yes (free trial available) |
| **Rate Limits** | 3,000 requests/hour (all plans) |
| **Free Tier** | Yes - free trial with limited leagues |
| **Paid Tier** | European Plan, Worldwide Plan (2,200+ leagues), Enterprise |

**Data Available:**
- 2,500+ football leagues globally
- Live scores and match events
- Line-ups, substitutions, goals, cards
- Advanced stats (ball coordinates, xG)
- Historical data archives
- Player profiles and statistics
- Team squads and transfers
- Odds and predictions
- TV stations and fixture lists
- 14-day free trial available

**CSOAI Use Case:**
- Global football analytics dashboard
- League comparison analysis
- Player performance tracking
- Transfer market intelligence
- Match outcome prediction modeling

[^1686^] [^1689^]

---

### 4.4 Football-Data.org

| Attribute | Detail |
|-----------|--------|
| **Name** | football-data.org |
| **URL** | https://www.football-data.org/ |
| **Format** | REST JSON |
| **API Key** | Yes (free token on registration) |
| **Rate Limits** | Not specified (generous for free tier) |
| **Free Tier** | Yes - top competitions free forever |
| **Paid Tier** | Standard (EUR 49/mo, 25 comps), Advanced (EUR 99/mo, 50 comps), Pro (EUR 249/mo, 144 comps) |

**Free Data Includes:**
- Premier League, La Liga, Bundesliga, Serie A, Ligue 1
- Champions League, Europa League
- World Cup, European Championship
- Live scores, fixtures, tables
- Match lineups, goal scorers, assists
- Bookings (yellow/red cards)
- Team squads
- League tables (home/away)

**CSOAI Use Case:**
- European football market analysis
- League performance comparison
- Match outcome analytics
- Fan engagement correlation with results
- Cross-league revenue and attendance analysis

[^1772^] [^1774^] [^1775^]

---

### 4.5 Sportsipy (Python Library - Sports-Reference Scraper)

| Attribute | Detail |
|-----------|--------|
| **Name** | Sportsipy (formerly sports-reference) |
| **URL** | https://sportsipy.readthedocs.io/ |
| **Format** | Python library (returns objects) |
| **API Key** | No |
| **Rate Limits** | Be courteous; add delays between requests |
| **Free Tier** | Completely free, open source |
| **Paid Tier** | None |

**Supported Leagues:**
- NFL (teams, players, box scores, schedules)
- NBA (teams, players, box scores, schedules)
- MLB (teams, players, box scores, schedules)
- NHL (teams, players, box scores, schedules)
- NCAAB / NCAAF (college sports)

**Data Available:**
- Full historical box scores
- Season schedules and results
- Player and team statistics
- Standings and rankings
- Rosters and player info
- Draft data

**CSOAI Use Case:**
- North American sports historical analysis
- Player performance modeling
- Team strength metrics
- Cross-season trend analysis
- Fantasy sports data feeds

**Note:** Being a scraper, functionality depends on Sports-Reference.com HTML structure. [^1692^]

---

### 4.6 MySportsFeeds

| Attribute | Detail |
|-----------|--------|
| **Name** | MySportsFeeds |
| **URL** | https://www.mysportsfeeds.com/ |
| **Format** | JSON, XML, CSV |
| **API Key** | Yes (free trial) |
| **Rate Limits** | Based on plan |
| **Free Tier** | Free non-commercial trial (request required) |
| **Paid Tier** | Paid subscriptions for full access |

**Coverage:**
- NFL, NBA, MLB, NHL (deep North American coverage)
- Real-time scores, player stats, schedules
- Historical box scores
- Highly accurate data (crowdsourced + verified)

**CSOAI Use Case:**
- North American sports analytics
- Real-time score tracking
- Historical sports data analysis
- Fantasy sports applications

[^1692^]

---

## 5. Music & Audio Data

### 5.1 Spotify Web API

| Attribute | Detail |
|-----------|--------|
| **Name** | Spotify Web API |
| **URL** | https://developer.spotify.com/documentation/web-api |
| **Format** | REST JSON |
| **API Key** | Yes (OAuth 2.0) |
| **Rate Limits** | Rolling 30-second window; ~10-20 req/sec in practice; 429 errors with Retry-After header |
| **Free Tier** | Yes - requires Spotify Premium account for Developer Mode (as of 2026) |
| **Paid Tier** | Extended quota mode (requires 250K MAU, registered business) |

**Key Endpoints:**
- `Get Track` / `Get Several Tracks` - Track metadata, popularity, audio features
- `Get Artist` - Artist info, genres, follower count, popularity
- `Get Artist's Top Tracks` - Most popular tracks by artist
- `Get Artist Related Artists` - Similar artists network
- `Get Playlist` / `Get Playlist Items` - Playlist contents and metadata
- `Get Featured Playlists` - Curated playlists (trending)
- `Get New Releases` - Recently released albums
- `Get Audio Features` - Tempo, key, energy, danceability, valence
- `Get Audio Analysis` - Detailed structural analysis of tracks
- `Search` - Full catalog search
- `Get Categories` - Genre/mood categories
- `Get User's Top Artists/Tracks` (with user permission)

**CSOAI Use Case:**
- Music trend analysis by genre, artist, region
- Audio feature analysis (energy, danceability trends)
- Playlist and curation intelligence
- Music popularity forecasting
- Cross-artist similarity networks
- Genre evolution tracking
- Audio feature correlation with popularity

**Note:** As of Feb 2026, Developer Mode requires Premium subscription and is limited to 5 test users. Several endpoints being deprecated. [^1718^] [^1719^] [^1722^] [^1728^]

---

### 5.2 Last.fm API

| Attribute | Detail |
|-----------|--------|
| **Name** | Last.fm Music Discovery API |
| **URL** | https://www.last.fm/api |
| **Format** | REST JSON/XML |
| **API Key** | Yes (free registration) |
| **Rate Limits** | Not formally specified; be respectful |
| **Free Tier** | Yes - completely free |
| **Paid Tier** | None |

**Key Methods:**
- `artist.getInfo` - Artist biography, tags, similar artists, stats
- `artist.getTopTracks` / `artist.getTopAlbums`
- `track.getInfo` - Track metadata, tags, play count
- `album.getInfo` - Album tracks, tags, play count
- `user.getTopArtists` / `user.getTopTracks` - Personal listening data
- `user.getRecentTracks` - Recently played tracks (scrobbles)
- `tag.getTopArtists` / `tag.getTopTracks` - Genre/Tag leaders
- `chart.getTopArtists` / `chart.getTopTracks` - Global charts
- `geo.getTopArtists` / `geo.getTopTracks` - Regional popularity

**CSOAI Use Case:**
- Global music listening trends
- Artist popularity tracking by region
- Genre trend analysis
- User listening behavior patterns
- Music recommendation network analysis
- Long-tail artist discovery
- Regional music preference mapping

[^1685^] [^1693^]

---

## 6. Social Media & Community Data

### 6.1 Reddit API (Official)

| Attribute | Detail |
|-----------|--------|
| **Name** | Reddit Data API |
| **URL** | https://www.reddit.com/dev/api/ |
| **Format** | REST JSON |
| **API Key** | Yes (OAuth 2.0 application registration) |
| **Rate Limits** | 100 QPM (OAuth); 10 QPM (no auth); 60 QPM (PRAW) |
| **Free Tier** | Yes - 100 queries/minute for non-commercial use |
| **Paid Tier** | ~$0.24 per 1,000 API calls for commercial use |

**Key Endpoints:**
- Subreddit listings and metadata (subscribers, activity)
- Post submissions and comments
- User profiles and karma
- Search across subreddits
- Voting data (scores)
- Trending subreddits
- Real-time comment threads

**CSOAI Use Case:**
- Gaming community sentiment analysis (r/gaming, r/pcgaming)
- Entertainment buzz tracking
- Fan community size and engagement analysis
- Topic trend detection
- Brand/product discussion monitoring
- Meme and viral content tracking

**Alternatives:** Pushshift/PullPush (free, historical), PRAW (Python wrapper), Apify Reddit Scraper [^1678^] [^1681^] [^1683^] [^1686^] [^1692^] [^1694^]

---

### 6.2 Pushshift / PullPush (Reddit Archive)

| Attribute | Detail |
|-----------|--------|
| **Name** | PullPush (Pushshift successor) |
| **URL** | https://pullpush.io/ |
| **Format** | REST JSON |
| **API Key** | No (free) |
| **Rate Limits** | Reasonable use policy |
| **Free Tier** | Yes - completely free |
| **Paid Tier** | None |

**Data Available:**
- Full Reddit historical archive (back to Reddit's founding)
- Posts and comments by subreddit
- Search by keyword, author, date range
- Submission metadata (score, upvotes, awards)
- Comment trees and threading

**CSOAI Use Case:**
- Long-term Reddit trend analysis
- Historical community growth tracking
- Viral content archaeology
- Subreddit popularity evolution
- Topic emergence and decline analysis

---

## 7. Market Research & Industry Reports

### 7.1 PwC Global Entertainment & Media Outlook

| Attribute | Detail |
|-----------|--------|
| **Name** | PwC Global E&M Outlook |
| **URL** | https://www.pwc.com/gx/en/issues/business-model-reinvention/outlook/ |
| **Format** | PDF reports + paid dashboard |
| **API Key** | N/A |
| **Rate Limits** | N/A |
| **Free Tier** | Summary reports free; full access $3,900-$7,000 USD |
| **Paid Tier** | Full database subscription with dashboards |

**Free Data Available:**
- Annual summary reports by country/region
- Market size and CAGR forecasts by segment
- Top-level trends analysis
- Infographic summaries

**Coverage (13 segments, 53 countries):**
- Internet advertising, OTT video, Cinema
- Video games & esports, Traditional TV
- Music, radio & podcasts, Newspapers/magazines
- Out-of-home advertising, B2B media

**Key Metrics:**
- Revenue forecasts (2024-2029)
- Year-on-year growth rates
- Digital vs. non-digital revenue splits
- Consumer vs. advertising revenue

**CSOAI Use Case:**
- Entertainment market sizing and forecasting
- Cross-country media market comparison
- Digital transformation trend tracking
- Industry segment growth analysis
- Investment opportunity assessment

**Note:** Free tier provides summary data. Full datasets with Excel downloads require subscription. [^1717^] [^1727^] [^1729^] [^1730^]

---

### 7.2 Newzoo Gaming Market Data

| Attribute | Detail |
|-----------|--------|
| **Name** | Newzoo |
| **URL** | https://newzoo.com/ |
| **Format** | Reports + paid platform |
| **API Key** | No (web-based) |
| **Rate Limits** | N/A |
| **Free Tier** | Free annual Global Games Market Report (44-page preview) |
| **Paid Tier** | Full platform subscription (contact sales) |

**Free Data Available:**
- Global games market revenue ($187.7B in 2024, +2.1% YoY)
- Player and payer forecasts (3.42B players in 2024)
- Segment breakdowns (PC, console, mobile)
- Regional market shares
- Trend analysis summaries
- Top game revenue and engagement charts (monthly)
- 8 abridged trend analyses

**Coverage:**
- 10,000+ PC and console games tracked
- 100+ metrics (MAU, playtime, revenues, play intent)
- 45 markets covered
- 73,000+ consumers surveyed yearly

**CSOAI Use Case:**
- Gaming market sizing and forecasting
- Platform (PC/console/mobile) trend analysis
- Game revenue and engagement benchmarking
- Gamer demographics and psychographics
- Genre performance tracking
- Cross-market gaming penetration analysis

**Note:** Free edition updated quarterly. Full 177-page report + Excel datasets require subscription. [^1724^] [^1725^] [^1737^] [^1738^]

---

### 7.3 Statista Connect API

| Attribute | Detail |
|-----------|--------|
| **Name** | Statista Connect API |
| **URL** | https://www.statista.com/business/connect-api |
| **Format** | REST JSON |
| **API Key** | Yes (requires Statista subscription) |
| **Rate Limits** | Based on plan |
| **Free Tier** | No free API tier; website has some free stats |
| **Paid Tier** | Enterprise API subscription |

**API Types:**
- **Search API** - Search and filter 1M+ datasets
- **Data API** - Raw data points, trends, structured insights

**Coverage:**
- 22,500+ sources
- 600+ industries
- 80,000+ topics
- Media, advertising, gaming, sports data included

**CSOAI Use Case:**
- Industry statistics integration
- Market size data embedding
- Trend visualization data sourcing
- Cross-industry benchmarking

**Note:** First collaboration partner is Canva (230M+ users). API is REST with JSON responses, AWS-backed infrastructure. [^1688^] [^1689^] [^1690^] [^1691^]

---

### 7.4 Nielsen Ad Intel Dataset (Kilts Center)

| Attribute | Detail |
|-----------|--------|
| **Name** | Nielsen Ad Intel |
| **URL** | https://www.chicagobooth.edu/research/kilts/research-data/nielsen-ad-intel |
| **Format** | Structured dataset (requires academic access) |
| **API Key** | N/A (dataset download) |
| **Rate Limits** | N/A |
| **Free Tier** | Free for academic researchers (Kilts Center) |
| **Paid Tier** | Commercial licensing via Nielsen |

**Coverage (since 2010):**
- National TV advertising (Network, Cable, Spanish, Syndicated)
- Local TV advertising (Spot, Clearance)
- Radio advertising
- Magazine and Newspaper advertising
- Digital/Internet advertising (2017+)
- Social media advertising (2022+) - Facebook, Instagram, Twitter, Reddit, TikTok, Pinterest
- Streaming advertising (2022+) - Amazon Prime Video
- FSI coupons, Outdoor/billboards

**CSOAI Use Case:**
- Advertising spend trend analysis
- Cross-media advertising comparison
- Social media ad growth tracking
- Brand competitive advertising intelligence
- TV vs. digital ad shift analysis

[^1731^]

---

## 8. Esports Data

### 8.1 Esports Earnings (esportsearnings.com)

| Attribute | Detail |
|-----------|--------|
| **Name** | Esports Earnings Database |
| **URL** | https://www.esportsearnings.com/ |
| **Format** | HTML (browseable database) |
| **API Key** | No direct API; data is browsable and scrapable |
| **Rate Limits** | N/A (respectful scraping recommended) |
| **Free Tier** | Completely free web access |
| **Paid Tier** | None |

**Data Available:**
- Tournament results and prize pools
- Player earnings rankings (all-time and by game)
- Team earnings rankings
- Country earnings rankings
- Game-specific tournament histories
- Prize pool trends over time
- 60,000+ tournaments tracked
- Top games: Dota 2, CS2, Fortnite, League of Legends, etc.

**CSOAI Use Case:**
- Esports prize pool growth analysis
- Game popularity via tournament activity
- Regional esports market sizing
- Player/team earnings tracking
- Esports investment ROI analysis
- Tournament ecosystem mapping

[^1764^]

---

### 8.2 PandaScore Esports API

| Attribute | Detail |
|-----------|--------|
| **Name** | PandaScore |
| **URL** | https://www.pandascore.co/pricing |
| **Format** | REST JSON + WebSockets |
| **API Key** | Yes (free on signup) |
| **Rate Limits** | 1,000 req/hour (free); 10,000 req/hour (paid) |
| **Free Tier** | Yes - schedules, results, context data, static data |
| **Paid Tier** | Historical EUR 400/mo/game; Live Basic EUR 1,000/mo/game |

**Free Data Includes:**
- Champions, items, static data for all games
- Match schedules (past, present, future)
- Pre-match data (tournaments, teams, players)
- Results and post-match scores

**Paid Data Includes:**
- Post-match detailed statistics
- Historical statistics
- Live WebSocket data
- Play-by-play feeds
- Replay API (query match frames and events)

**Games Covered:**
- League of Legends, Counter-Strike 2, Dota 2
- Valorant, Overwatch 2, Rainbow Six Siege
- Call of Duty, Rocket League, PUBG

**CSOAI Use Case:**
- Esports match results aggregation
- Tournament schedule intelligence
- Team and player performance tracking
- Live esports viewership correlation
- Esports betting market data

[^1778^]

---

### 8.3 Leaguepedia / Esports API (Community)

| Attribute | Detail |
|-----------|--------|
| **Name** | Leaguepedia (via Cargo/CargoExport) |
| **URL** | https://lol.fandom.com/wiki/Help:Leaguepedia_API |
| **Format** | MediaWiki API + CargoExport |
| **API Key** | No |
| **Rate Limits** | MediaWiki rate limits apply |
| **Free Tier** | Completely free |
| **Paid Tier** | None |

**Data Available:**
- League of Legends esports teams and rosters
- Tournament results and brackets
- Player profiles and match history
- Champion pick/ban statistics
- Game-level statistics
- Schedule and results

**CSOAI Use Case:**
- LoL esports historical analysis
- Team performance modeling
- Champion meta trend analysis
- Regional league comparison
- Player career trajectory analysis

---

## 9. Open Datasets & Alternative Sources

### 9.1 GDELT Project (Global Media Monitoring)

| Attribute | Detail |
|-----------|--------|
| **Name** | GDELT Project |
| **URL** | https://www.gdeltproject.org/ |
| **Format** | CSV, BigQuery, API |
| **API Key** | No (100% free and open) |
| **Rate Limits** | No limits |
| **Free Tier** | Entire database is free |
| **Paid Tier** | None |

**Datasets Available:**
- **GDELT Event Database** - 700M+ global news events (1979-present)
- **Global Knowledge Graph (GKG)** - Entities, themes, emotions from news
- **Visual Global Knowledge Graph** - Image analysis from global news
- **Global Entity Graph** - People and organizations in news
- **TV News Advertising Inventory** - Ad data from 100+ US TV stations
- **Web Ngrams** - Global online news ngrams in 152 languages
- **Global Quotation Graph** - Quoted statements across news
- **Special Collections** - 215 years of books, human rights data

**CSOAI Use Case:**
- Global media coverage analysis of entertainment events
- Brand mention tracking across global news
- Entertainment industry sentiment monitoring
- Cultural trend analysis via news coverage
- Cross-country media narrative comparison
- AI-annotated image analysis from news

**Access:** Raw data files, Google BigQuery, GDELT Analysis Service (free cloud tool) [^1771^] [^1776^] [^1777^]

---

### 9.2 Kaggle Gaming & Media Datasets

| Attribute | Detail |
|-----------|--------|
| **Name** | Kaggle Datasets |
| **URL** | https://www.kaggle.com/datasets |
| **Format** | CSV, JSON, SQLite, etc. |
| **API Key** | Yes (Kaggle account) |
| **Rate Limits** | Download-based |
| **Free Tier** | Yes - all datasets free |
| **Paid Tier** | Kaggle Pro for compute |

**Relevant Datasets:**
- Video Game Sales (17K+ games with sales data)
- Steam Store Games (genre, ratings, pricing)
- Twitch Streaming Data (user behavior)
- Spotify Tracks Dataset (audio features, 160K tracks)
- Esports Earnings Dataset
- IMDb Movie Dataset
- Netflix Shows and Movies Dataset
- YouTube Trending Videos Dataset
- League of Legends Match Data
- FIFA 20+ Player Statistics

**CSOAI Use Case:**
- Historical game sales analysis
- Music feature analysis
- Streaming behavior patterns
- Movie/TV content performance
- Player rating systems comparison

---

### 9.3 Google Dataset Search

| Attribute | Detail |
|-----------|--------|
| **Name** | Google Dataset Search |
| **URL** | https://datasetsearch.research.google.com/ |
| **Format** | Various (search engine) |
| **API Key** | No |
| **Rate Limits** | N/A |
| **Free Tier** | Free |
| **Paid Tier** | None |

**CSOAI Use Case:**
- Discovery of gaming, media, sports datasets
- Academic research data finding
- Government open data discovery
- Industry report dataset location

---

### 9.4 World Bank Open Data (Media & Entertainment Indicators)

| Attribute | Detail |
|-----------|--------|
| **Name** | World Bank Open Data |
| **URL** | https://data.worldbank.org/ |
| **Format** | API, CSV, Excel |
| **API Key** | No (free) |
| **Rate Limits** | Reasonable use |
| **Free Tier** | Free |
| **Paid Tier** | None |

**Relevant Indicators:**
- Fixed broadband subscriptions (per 100 people)
- Mobile cellular subscriptions (per 100 people)
- Internet users (% of population)
- GDP per capita (media spend correlation)
- Household consumption expenditure

**CSOAI Use Case:**
- Market penetration analysis
- Digital infrastructure correlation with media consumption
- Cross-country digital readiness comparison
- Economic indicator correlation with entertainment spend

---

### 9.5 StatsBomb Open Data (Football/Soccer)

| Attribute | Detail |
|-----------|--------|
| **Name** | StatsBomb Open Data |
| **URL** | https://github.com/statsbomb/open-data |
| **Format** | JSON (event-level data) |
| **API Key** | No |
| **Rate Limits** | None |
| **Free Tier** | Completely free |
| **Paid Tier** | StatsBomb 360 for full data |

**Data Available:**
- Geolocated event data (passes, shots, pressures, duels)
- Men's and women's competitions
- Multiple seasons
- JSON format, Python/R compatible
- Contextual variables (body orientation, foot used)

**CSOAI Use Case:**
- Advanced football analytics
- Player performance modeling
- Tactical pattern analysis
- Shot quality analysis (xG)
- Pass network analysis

---

### 9.6 Webhose/Webz.io Free News Datasets

| Attribute | Detail |
|-----------|--------|
| **Name** | Webz.io News Datasets |
| **URL** | https://github.com/Webhose/free-news-datasets |
| **Format** | JSON |
| **API Key** | No |
| **Rate Limits** | N/A (download-based) |
| **Free Tier** | Free weekly datasets |
| **Paid Tier** | Webz.io News API Lite (free ongoing) |

**Data Available:**
- ~1,000 news articles per weekly release
- Thematic focus datasets
- Sentiment analysis included
- IPTC categories (sports, entertainment, finance)
- Diverse news sources

**CSOAI Use Case:**
- Media content analysis
- Sports/entertainment news NLP training
- Sentiment analysis model training
- Trend detection in news coverage

[^1744^]

---

## 10. Quick Comparison Matrix

| Source | Category | Free? | Key Needed | Rate Limit | Best For |
|--------|----------|-------|------------|------------|----------|
| **Twitch API** | Streaming | Yes | OAuth | 800/min | Live stream analytics |
| **YouTube Data API** | Video | Yes (quota) | API Key | 10K units/day | Video metrics |
| **Steam Web API** | Gaming | Yes | API Key | 100K/day | Game player counts |
| **IGDB API** | Gaming | Yes | OAuth | 4/sec | Game metadata |
| **RAWG API** | Gaming | Yes | API Key | 20K/mo | Game discovery |
| **ESPN API** | Sports | Yes | None | Undoc. | Live sports scores |
| **API-SPORTS** | Sports | Yes (100/day) | API Key | 100/day | Multi-sport data |
| **Sportmonks** | Sports | Trial | API Key | 3K/hr | Football data |
| **football-data.org** | Sports | Yes | Token | Generous | European football |
| **Spotify Web API** | Music | Yes* | OAuth | ~10-20/sec | Music trends |
| **Last.fm API** | Music | Yes | API Key | Respectful | Listening data |
| **Reddit API** | Social | Yes (100 QPM) | OAuth | 100 QPM | Community trends |
| **Social Blade** | Social | No | Credits | Per credit | Creator analytics |
| **Esports Earnings** | Esports | Yes | None | N/A | Prize pool data |
| **PandaScore** | Esports | Yes (fixtures) | API Key | 1K/hr | Esports stats |
| **GDELT** | Media | Yes | None | None | Global news events |
| **PwC E&M Outlook** | Market | Summary free | N/A | N/A | Market sizing |
| **Newzoo** | Market | Report free | N/A | N/A | Gaming market |
| **Kaggle** | Open Data | Yes | Account | N/A | Historical datasets |
| **Sportsipy** | Sports | Yes | None | Respectful | Historical US sports |

---

## CSOAI Integration Recommendations

### Tier 1: Immediate Integration (Free, No Barriers)
1. **ESPN API** - No auth required, comprehensive sports data
2. **Steam Web API** - Free, rich gaming data, 100K/day limit
3. **Last.fm API** - Free music listening data, global trends
4. **GDELT** - Free global media event data, massive scale
5. **Reddit API** - Free community data (100 QPM)
6. **football-data.org** - Free European football data

### Tier 2: Easy Integration (Free, Registration Required)
1. **Twitch API** - OAuth registration, excellent streaming data
2. **YouTube Data API** - Google Cloud registration, 10K quota
3. **IGDB API** - Twitch OAuth, 500K+ games
4. **RAWG API** - Simple API key, 350K+ games
5. **Spotify Web API** - OAuth (now requires Premium)
6. **API-SPORTS** - Free 100/day tier
7. **PandaScore** - Free fixtures tier

### Tier 3: Market Intelligence (Reports & Summaries)
1. **PwC E&M Outlook** - Free summary reports
2. **Newzoo** - Free annual games market report
3. **Esports Earnings** - Web-browsable database
4. **Kaggle** - Historical datasets for analysis

### Tier 4: Premium (Paid but Valuable)
1. **Social Blade API** - Credit-based creator analytics
2. **Statista Connect** - Enterprise statistics API
3. **Sportmonks** - Paid football tiers
4. **Nielsen** - Academic/commercial licensing

---

## Citation Index

| Ref | Source |
|-----|--------|
| [^1678^] | Reddit Data API Wiki - Rate Limits |
| [^1681^] | Reddit API Pricing 2026 Breakdown |
| [^1683^] | Reddit API Limits and Restrictions |
| [^1685^] | ESPN API Guide / Last.fm API Docs |
| [^1686^] | Sportmonks Free vs Paid Football APIs |
| [^1687^] | How to Access ESPN's Hidden API |
| [^1688^] | ESPN API Alternative (RapidAPI) |
| [^1689^] | API-Football vs Sportmonks Comparison |
| [^1690^] | Free API Live Football Data (RapidAPI) |
| [^1691^] | API-Sports Homepage |
| [^1692^] | 12 Best Free Sports API Options 2025 |
| [^1693^] | Unlocking ESPN's Hidden API (Dev.to) |
| [^1694^] | ISteamUserStats Interface (Steamworks) |
| [^1695^] | SteamCharts API (Parse.bot) |
| [^1696^] | The Ultimate Steam Web API Guide |
| [^1697^] | YouTube API Pricing Complete Guide |
| [^1698^] | IGDB API Pricing Update |
| [^1699^] | IGDB API Documentation |
| [^1701^] | RAWG vs IGDB Reddit Discussion |
| [^1702^] | IGDB API - Akousa Directory |
| [^1704^] | Steam API Historical Player Count (StackOverflow) |
| [^1717^] | PwC E&M Outlook 2025-2029 Report |
| [^1718^] | Spotify Web API Rate Limits (StackOverflow) |
| [^1719^] | Spotify Rate Limit Documentation |
| [^1722^] | Spotify Changes Developer Mode API (TechCrunch) |
| [^1724^] | Newzoo GamesIndustry.biz Archive |
| [^1725^] | Newzoo Homepage |
| [^1727^] | Twitch API Reference |
| [^1728^] | Twitch API Get Started |
| [^1731^] | Nielsen Ad Intel Dataset (Kilts Center) |
| [^1732^] | Twitch API Overview |
| [^1737^] | Newzoo Homepage (revisit) |
| [^1738^] | Newzoo Global Games Market Report 2024 |
| [^1744^] | Webz.io Free News Datasets (GitHub) |
| [^1753^] | RAWG API - Apideposu |
| [^1754^] | RAWG API - APIs.guru |
| [^1755^] | Social Blade Pricing - xpay.sh |
| [^1756^] | Social Blade API Dashboard |
| [^1759^] | RAWG API Documentation |
| [^1761^] | Social Blade Scraper - Apify |
| [^1762^] | Social Media API Pricing Comparison 2026 |
| [^1763^] | RAWG API - Apives |
| [^1764^] | Esports Earnings Homepage |
| [^1765^] | RAWG Launching Public API (Medium) |
| [^1771^] | GDELT Cloud Documentation |
| [^1776^] | GDELT Project Homepage |
| [^1777^] | GDELT Data Querying and Downloading |
| [^1778^] | PandaScore Esports API Pricing |

---

*Document generated for CSOAI Media/Entertainment/Sports Hive integration planning.*
*All URLs and rate limits current as of research date (June 2026).*
