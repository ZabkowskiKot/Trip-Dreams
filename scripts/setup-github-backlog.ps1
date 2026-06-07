# One-time script: create milestones and backlog issues for Trip Dreams.
# Run: .\scripts\setup-github-backlog.ps1
# Requires: gh CLI logged in (gh auth login)

$repo = "ZabkowskiKot/Trip-Dreams"
$ErrorActionPreference = "Stop"

function New-Milestone {
    param([string]$Title, [string]$Description)
    $existing = gh api "repos/$repo/milestones" --jq ".[] | select(.title==`"$Title`") | .number" 2>$null
    if ($existing) {
        Write-Host "Milestone exists: $Title (#$existing)"
        return [int]$existing
    }
    $body = @{ title = $Title; description = $Description; state = "open" } | ConvertTo-Json
    $num = gh api -X POST "repos/$repo/milestones" --input - <<< $body --jq ".number"
    Write-Host "Created milestone: $Title (#$num)"
    return [int]$num
}

function New-Issue {
    param(
        [string]$Title,
        [string]$Body,
        [string[]]$Labels,
        [int]$Milestone = 0,
        [switch]$Close
    )
    $args = @("issue", "create", "--repo", $repo, "--title", $Title, "--body", $Body)
    foreach ($l in $Labels) { $args += @("--label", $l) }
    if ($Milestone -gt 0) { $args += @("--milestone", $Title) }
    # gh issue create --milestone uses title not number
    $url = & gh @args 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Failed: $Title — $url" }
    Write-Host "Created: $Title"
    if ($Close) {
        $num = ($url -replace '.*issues/(\d+).*', '$1')
        gh issue close $num --repo $repo | Out-Null
        Write-Host "  Closed #$num (done)"
    }
}

Write-Host "`n=== Trip Dreams backlog setup ===`n"

# Milestones (iterations)
$m1 = New-Milestone "Done — Foundation" "OAuth, Firestore, profiles, groups API, group-scoped dreams"
$m2 = New-Milestone "Next — Groups & invites" "Invite friends and collaborate in groups"
$m3 = New-Milestone "Dream Planner polish" "Edit/delete dreams, UX improvements for Stage 1"
$m4 = New-Milestone "Calendar sync (Stage 2)" "Google Calendar availability"
$m5 = New-Milestone "Trip Organizer (Stage 3)" "Itinerary and expense splitting"
$m6 = New-Milestone "Trip Summary (Stage 4)" "Recap, photos, sharing"

# Helper: create with milestone by title
function Add-BacklogIssue {
    param([string]$Title, [string]$Body, [string[]]$Labels, [string]$MilestoneTitle, [switch]$Close)
    $args = @("issue", "create", "--repo", $repo, "--title", $Title, "--body", $Body, "--milestone", $MilestoneTitle)
    foreach ($l in $Labels) { $args += @("--label", $l) }
    $out = & gh @args
    Write-Host "Created: $Title"
    if ($Close) {
        $num = ($out -replace '.*issues/(\d+).*', '$1')
        gh issue close $num --repo $repo | Out-Null
        Write-Host "  Closed #$num"
    }
}

Write-Host "`n--- Foundation (closed) ---"
Add-BacklogIssue "Google OAuth login and session" @"
## Done
- [x] Google sign-in flow
- [x] Session persistence
- [x] Guest vs logged-in UI
"@ @("epic:platform") "Done — Foundation" -Close

Add-BacklogIssue "Firestore persistence" @"
## Done
- [x] Firestore client with named database
- [x] users, groups, dreams collections
- [x] In-memory fallback for local dev
"@ @("epic:platform") "Done — Foundation" -Close

Add-BacklogIssue "User profiles (read-only, auto locale)" @"
## Done
- [x] Profile from Google account
- [x] Auto currency/timezone from locale + browser
- [x] Simplified timezones (CET, GMT, WET, UTC)
- [x] Logged-out profile shows login CTA
"@ @("epic:platform") "Done — Foundation" -Close

Add-BacklogIssue "Groups API and group-scoped dreams" @"
## Done
- [x] Create and list groups
- [x] Dreams belong to a group
- [x] Stage 1 dream planner UI
"@ @("epic:groups", "epic:dream-planner") "Done — Foundation" -Close

Write-Host "`n--- Next iteration ---"
Add-BacklogIssue "Group invite codes and join links" @"
## Goal
Let a group owner invite friends via a shareable link or short code.

## Acceptance criteria
- [ ] Generate unique invite code per group
- [ ] API: join group by code (authenticated user)
- [ ] New member appears in group members list
- [ ] Invalid/expired code shows clear error
"@ @("epic:groups", "priority:high", "enhancement") "Next — Groups & invites"

Add-BacklogIssue "Join group UI (replace placeholder)" @"
## Goal
Replace the ""coming in a later step"" alert with a real join flow.

## Acceptance criteria
- [ ] Join by code input on Groups page
- [ ] Success redirects to the joined group
- [ ] Works on mobile layout
"@ @("epic:groups", "priority:high", "enhancement") "Next — Groups & invites"

Add-BacklogIssue "Display group members on group detail" @"
## Goal
Show who is in the group on the group detail page.

## Acceptance criteria
- [ ] List member names and emails (or avatars later)
- [ ] Updates after someone joins via invite
"@ @("epic:groups", "priority:medium", "enhancement") "Next — Groups & invites"

Add-BacklogIssue "Leave a group" @"
## Goal
Allow a member to leave a group they joined.

## Acceptance criteria
- [ ] Leave button on group detail or groups list
- [ ] User removed from members; group removed from their list
- [ ] Owner cannot leave if sole member (or transfer ownership — TBD)
"@ @("epic:groups", "priority:low", "enhancement") "Next — Groups & invites"

Write-Host "`n--- Dream Planner polish ---"
Add-BacklogIssue "Edit a dream destination" @"
## Acceptance criteria
- [ ] Edit button on each dream card
- [ ] PATCH API for dream fields (location, priority, budget)
- [ ] Changes persist in Firestore
"@ @("epic:dream-planner", "priority:high", "enhancement") "Dream Planner polish"

Add-BacklogIssue "Delete a dream destination" @"
## Acceptance criteria
- [ ] Delete with confirmation
- [ ] DELETE API endpoint
- [ ] List refreshes after delete
"@ @("epic:dream-planner", "priority:high", "enhancement") "Dream Planner polish"

Write-Host "`n--- Future epics ---"
Add-BacklogIssue "Connect Google Calendar" @"
## Goal
Stage 2 — let users connect Calendar for availability.

## Acceptance criteria
- [ ] OAuth scope for Calendar (read-only)
- [ ] Connect button on profile or Stage 2
- [ ] Store connection status on user profile
"@ @("epic:calendar", "priority:medium", "enhancement") "Calendar sync (Stage 2)"

Add-BacklogIssue "Show group availability from calendars" @"
## Acceptance criteria
- [ ] Fetch free/busy for group members
- [ ] Display in Stage 2 UI
- [ ] Handle members without calendar connected
"@ @("epic:calendar", "priority:medium", "enhancement") "Calendar sync (Stage 2)"

Add-BacklogIssue "Suggest meeting times for the trip" @"
## Acceptance criteria
- [ ] Algorithm finds overlapping free weekends
- [ ] Show top 3 suggestions in UI
"@ @("epic:calendar", "priority:low", "enhancement") "Calendar sync (Stage 2)"

Add-BacklogIssue "Itinerary builder (Stage 3)" @"
## Acceptance criteria
- [ ] Add/edit/delete itinerary items (date, location, activity)
- [ ] Timeline view on group detail Stage 3
"@ @("epic:organizer", "enhancement") "Trip Organizer (Stage 3)"

Add-BacklogIssue "Expense tracking and cost split" @"
## Acceptance criteria
- [ ] Add expenses with amount and who paid
- [ ] Calculate per-person balance
- [ ] ""Who owes who"" summary
"@ @("epic:organizer", "enhancement") "Trip Organizer (Stage 3)"

Add-BacklogIssue "Trip summary and photo gallery (Stage 4)" @"
## Acceptance criteria
- [ ] Trip overview after ""completion""
- [ ] Photo upload or links
- [ ] Share/export summary
"@ @("epic:summary", "enhancement") "Trip Summary (Stage 4)"

Add-BacklogIssue "Mobile responsive QA pass" @"
## Goal
Verify BUG_FIXES test checklist on real devices.

## Acceptance criteria
- [ ] Desktop sidebar and navigation
- [ ] Mobile hamburger and touch targets
- [ ] Dark mode persistence
"@ @("epic:platform", "priority:medium") "Dream Planner polish"

Add-BacklogIssue "Update README for current API" @"
## Acceptance criteria
- [ ] Document POST /api/profile/sync (not PATCH /api/profile)
- [ ] Profile auto-locale behavior
"@ @("epic:platform", "documentation") "Dream Planner polish"

Write-Host "`n=== Done! Open: https://github.com/ZabkowskiKot/Trip-Dreams/issues ===`n"
