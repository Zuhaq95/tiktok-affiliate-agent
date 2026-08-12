# TikTok Affiliate Agent - Project Status

Last Updated: 2026-08-12

---

# Overall Progress

Approximately 80% Complete

Core profile extraction architecture is complete and stable.

---

# Completed Sections

## Header ✅

Extracted

- Username
- Display Name
- Rating
- Review Count
- Categories
- Followers
- MCN
- Bio
- Email (if present)
- Website (if present)

Parser

HeaderParser

---

## Sales ✅

Overview Metrics

- GMV
- Items Sold
- GPM
- GMV per Customer

Distribution Charts

- GMV per Sales Channel
- GMV by Product Category

Parser

SalesParser

Helpers

- MetricCardParser
- DistributionParser
- CarouselNavigator

---

## Collaboration ✅

Metrics

- Estimated Post Rate
- Average Commission Rate
- Products
- Brand Collaborations
- Product Price Range

Supports horizontal carousel navigation.

Parser

CollaborationParser

Helpers

- MetricCardParser
- CarouselNavigator

---

## Video ✅

Metrics

- Video GPM
- Videos
- Average Video Views
- Average Engagement Rate
- Average Likes
- Average Comments
- Average Shares

Supports carousel navigation.

Parser

VideoParser

---

## LIVE ✅

Metrics

- LIVE GPM
- LIVE Streams
- Average LIVE Views
- Average LIVE Engagement Rate
- Average LIVE Likes
- Average LIVE Comments
- Average LIVE Shares

Supports carousel navigation.

Parser

LiveParser

---

## Followers ✅ (Partial)

Completed

Gender Distribution

Age Distribution

Pending

Top 5 Locations

Reason

TikTok renders the location chart entirely on a canvas.
There are no DOM elements available for labels or percentages.

Current implementation intentionally skips this section.

Parser

FollowersParser

Helpers

- DistributionParser
- LocationChartParser

---

## Trends ✅

Trend data is extracted directly from TikTok's Creator Profile API.

API

```text
/api/v1/oec/affiliate/creator/marketplace/profile