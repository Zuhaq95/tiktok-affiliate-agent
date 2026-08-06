# TikTok Affiliate Agent

---

# Project Goal

Build a fully automated TikTok Shop Affiliate Creator Discovery Agent.

Workflow

Search Creators
    ↓
AI Rank
    ↓
Open Creator
    ↓
Extract Profile
    ↓
Store Structured Data
    ↓
AI Recommendation Engine

---

# Current Architecture

## Profile Extraction

ProfileExtractor

    HeaderParser

    PageSectionCollector

        ↓

    SalesParser

    CollaborationParser

    VideoParser

    LiveParser

    FollowersParser

    TrendParser

Each parser owns exactly one page section.

---

# Folder Structure

profiles/

    creator_profile.py

    page_sections.py

    page_section_collector.py

    helpers/

        metric_card_parser.py

        carousel_navigator.py

        distribution_parser.py

        chart_parser.py

        parser_utils.py

    models/

        header_info.py
        sales_info.py
        collaboration_info.py
        video_info.py
        followers_info.py
        trend_info.py

    header_parser.py

    sales_parser.py

    collaboration_parser.py

    video_parser.py

    live_parser.py

    followers_parser.py

    trend_parser.py

---

# Core Helpers

## MetricCardParser

Responsibility

- Parse visible metric cards
- Never move carousel

Used by

- Sales
- Collaboration
- Video
- LIVE

---

## CarouselNavigator

Responsibility

- Detect right arrow
- Navigate carousel
- Stop when no more pages exist

Never parses data.

---

## DistributionParser

Responsibility

Parse donut chart legends.

Examples

- GMV per Sales Channel
- Product Categories
- Gender
- Age

---

## PageSectionCollector

Discovers all major white-card sections once.

Returns

PageSections

which contains

- Header
- Navigation
- Sales
- Sales Charts
- Collaboration
- Video
- LIVE
- Followers
- Trends
- Example Videos
- Product Videos

No parser searches the page anymore.

---

# Current Progress

## Completed

✅ Profile opener

✅ Header parser

✅ Sales parser

✅ Collaboration parser

✅ MetricCardParser

✅ CarouselNavigator

✅ DistributionParser

✅ PageSectionCollector

---

## In Progress

None

---

## Remaining

⬜ VideoParser

⬜ LiveParser

⬜ FollowersParser

⬜ TrendParser

⬜ ExampleVideosParser

⬜ SimilarCreatorsParser

---

# Design Principles

Every class has one responsibility.

Examples

ProfileExtractor

Coordinates extraction only.

SalesParser

Parses Sales only.

MetricCardParser

Parses metric cards only.

CarouselNavigator

Moves carousel only.

PageSectionCollector

Discovers page structure only.

---

# Important Discoveries

Creator Details page consists of 11 major white sections.

1 Header

2 Navigation

3 Sales

4 Sales Charts

5 Collaboration

6 Video

7 LIVE

8 Followers

9 Trends

10 Example Videos

11 Product Videos

PageSectionCollector maps these into PageSections.

---

# Known Issues

None.

---

# Next Task

Implement VideoParser using

MetricCardParser

+

CarouselNavigator

+

PageSectionCollector

Architecture already supports it.
