# TikTok Affiliate Agent

Last Updated: 2026-08-07

---

# Project Goal

Build a fully automated TikTok Shop Affiliate Creator Discovery Agent.

Workflow

Search Creators
    ↓
AI Rank Creators
    ↓
Open Creator Profile
    ↓
Extract Complete Profile
    ↓
Store Structured Data
    ↓
AI Recommendation Engine

The project is designed to be modular, reusable, scalable and easy to maintain.

---

# Current Architecture

```
ProfileExtractor
        │
        ▼
PageSectionCollector
        │
        ▼
PageSections
        │
        ├── HeaderParser
        ├── SalesParser
        ├── CollaborationParser
        ├── VideoParser
        ├── LiveParser
        ├── FollowersParser
        ├── TrendParser
        ├── ExampleVideosParser
        └── SimilarCreatorsParser
```

PageSectionCollector discovers the page structure once.

Each parser receives only the section it owns.

No parser searches the entire page anymore.

---

# Folder Structure

```
profiles/

│
├── creator_profile.py
│
├── page_sections.py
├── page_section_collector.py
│
├── helpers/
│   ├── metric_card_parser.py
│   ├── carousel_navigator.py
│   ├── distribution_parser.py
│   ├── chart_parser.py
│   ├── video_card_parser.py
│   └── parser_utils.py
│
├── models/
│   ├── header_info.py
│   ├── sales_info.py
│   ├── collaboration_info.py
│   ├── video_info.py
│   ├── followers_info.py
│   └── trend_info.py
│
├── header_parser.py
├── sales_parser.py
├── collaboration_parser.py
├── video_parser.py
├── live_parser.py
├── followers_parser.py
├── trend_parser.py
├── example_videos_parser.py
└── similar_creators_parser.py
```

---

# Page Structure

The Creator Details page currently contains 11 major white sections.

| Index | Section |
|------:|---------|
| 1 | Header |
| 2 | Navigation Tabs |
| 3 | Sales |
| 4 | Sales Charts |
| 5 | Collaboration |
| 6 | Video |
| 7 | LIVE |
| 8 | Followers |
| 9 | Trends |
|10 | Example Videos |
|11 | Product Videos |

PageSectionCollector validates these sections before parsing.

---

# Helper Classes

## MetricCardParser

Responsibility

Parse only the visible metric cards.

Never clicks buttons.

Never moves the carousel.

Used by

- Sales
- Collaboration
- Video
- LIVE

---

## CarouselNavigator

Responsibility

Navigate horizontal metric carousels safely.

Only clicks the carousel navigation button.

Never clicks

- Back button
- Invite button
- Header buttons
- Sidebar buttons

Used by

- Sales
- Collaboration
- Video
- LIVE

---

## DistributionParser

Responsibility

Parse donut chart legends.

Uses TikTok semantic classes

- pcm-pc-container
- pcm-pc-legend-label
- pcm-pc-legend-value

Supported charts

- GMV per Sales Channel
- GMV by Product Category
- Gender
- Age

---

## ParserUtils

Provides reusable conversion helpers.

Current methods

- money_to_float()
- percent_to_float()
- count_to_int()
- extract_number()

---

## VideoCardParser

Reserved for Example Videos parsing.

Not implemented yet.

---

# Completed Modules

## HeaderParser

Status

✅ Complete

Extracts

- Username
- Display Name
- Rating
- Review Count
- Categories
- Followers
- MCN
- Bio
- Email
- Website

---

## SalesParser

Status

✅ Complete

Extracts

Overview Metrics

- GMV
- Items Sold
- GPM
- GMV per Customer

Distribution Charts

- GMV per Sales Channel
- GMV by Product Category

Uses

- MetricCardParser
- CarouselNavigator
- DistributionParser

---

## CollaborationParser

Status

✅ Complete

Extracts

- Estimated Post Rate
- Average Commission Rate
- Products
- Brand Collaborations
- Product Price Range

Uses

- MetricCardParser
- CarouselNavigator

---

## VideoParser

Status

✅ Complete

Extracts

- Video GPM
- Videos
- Average Video Views
- Average Engagement Rate
- Average Likes
- Average Comments
- Average Shares

Uses

- MetricCardParser
- CarouselNavigator

---

# Remaining Modules

Analytics

⬜ LiveParser

⬜ FollowersParser

⬜ TrendParser

Content

⬜ ExampleVideosParser

Discovery

⬜ SimilarCreatorsParser

---

# Design Principles

Each class has exactly one responsibility.

Examples

ProfileExtractor

Coordinates extraction only.

SalesParser

Parses Sales only.

VideoParser

Parses Video only.

MetricCardParser

Parses metric cards only.

CarouselNavigator

Navigates carousel only.

DistributionParser

Parses donut chart legends only.

PageSectionCollector

Discovers page layout only.

---

# Major Refactoring Completed

Completed

✅ Introduced PageSectionCollector

✅ Introduced PageSections

✅ Removed page-wide searching from parsers

✅ Scoped every parser to its own section

✅ Replaced unsafe button searching with CarouselNavigator

✅ DistributionParser rewritten using semantic TikTok CSS classes

✅ Sales Charts separated from Sales Metrics

Architecture is now considered stable.

No further architectural changes are planned unless TikTok changes the page layout.

---

# Current Progress

Infrastructure

✅ Complete

Profile

✅ Header

✅ Sales

✅ Collaboration

✅ Video

Analytics

⬜ LIVE

⬜ Followers

⬜ Trends

Content

⬜ Example Videos

Discovery

⬜ Similar Creators

Overall Progress

████████████░░░░░░░░░░

Approximately 50% complete.

---

# Next Task

Implement LiveParser.

Expected implementation

```
ProfileExtractor
        │
        ▼
sections.live
        │
        ▼
LiveParser
        │
        ├── MetricCardParser
        └── CarouselNavigator
        │
        ▼
LiveInfo
```

LiveParser should follow the same architecture as VideoParser.

No new helper classes are expected.

---

# Notes

This document is the single source of truth for the project.

Whenever a major milestone is completed, regenerate this file instead of patching individual sections.

Future conversations should begin by loading this document before continuing development.