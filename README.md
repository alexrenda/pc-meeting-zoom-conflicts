# Handing Conflicts in a PC Meeting in Zoom

This guide will discuss handling conflicts during a Zoom-based PC meeting. This is the procedure used during the MLSys 2023 TPC meeting. It is inspired by the set of scripts [here](https://github.com/emeryberger/PC-Resources/tree/master/PC-meeting-scripts).

The core process is that the meeting proceeds in the main room, and conflicted reviewers are brought into and taken out of a Conflict breakout room.

## Pre-meeting setup

1. Create a scheduled Zoom meeting in the web UI. While configuring this meeting, click to show options at the bottom of the page, click Breakout Room pre-assign, click "+ Create Rooms", and create a breakout room. The name and content of the room do not matter, all that matters is that there is some breakout room pre-assignment configured. If the breakout room pre-assign option is not available, make sure it is enabled in your personal user settings in Zoom. Note that the person who will be actively managing conflicts in Zoom should be the host of the meeting.
2. Collect **Zoom account email addresses** of participants. For MLSys we did not do this ahead of time (and instead collected email addresses at the start of the meeting), which was a mistake. Instead, here are several options (which we did not test):
    * Require registration for the meeting. Combined with authentication as described [here](https://support.zoom.us/hc/en-us/articles/211579443-Scheduling-and-customizing-a-meeting-with-registration), this should force attendees to provide zoom email addresses
    * Send out forms asking participants to give you zoom email addresses. Note that many people do not know what their zoom email address is.
3. Collect conflicts for each paper. If you use the code in this repo, there are stub CSVs provided.

## At the start of the meeting

Test the process below, assigning everyone in the meeting to a conflict breakout room. Everyone who is not automatically assigned (i.e., who is left in the main room) has an issue with their setup and must either log into Zoom, or otherwise get their email address recorded.

## During the meeting

One person (the Zoom meeting host) must manage conflicts. Depending on how fast you go through papers, this may be a full-time job; this should likely be someone who is not planning to participate in discussion.

For each paper, perform the following steps:
1. Generate a CSV with conflict room assignments. If using the code in this repo, this is performed in the Jupyter notebook (which will essentially serve as a dashboard for the conflict manager)
2. Go to https://zoom.us/meeting/MEETING_ID/edit. Note that in the meeting list, the Edit button may be greyed out, but going directly to this URL bypasses that.
3. Click to show options at the bottom of the page, click to edit breakout rooms, click "Import from CSV", and upload the CSV generated in Step 1. Click "Save" for the breakout rooms, then click "Save" for the meeting.
4. Exit and re-enter the main room of the meeting. Ideally you should do this by joining and leaving a breakout room. You must do this in order for the CSV applied in Step 3 to take effect.
5. Close breakout rooms.
6. In the breakout room menu, click Recreate -> Recover to pre-assigned rooms.
7. [Optional] click the gear on the bottom left of the breakout room menu, and select "Allow participants to choose room". This is unset each time, and must be manually re-set each time. You should also make sure that the other options are correctly configured (specifically, automatically moving all assigned participants into the breakout room)
8. Click Open All Rooms
9. Manually assign any stragglers (those whose email you don't have, or who are calling in or otherwise not logged in to Zoom) to the conflict room.
10. Monitor for people joining/rejoining the meeting, and ensure that they are assigned the correct room.

Note that the conflict manager can run steps 1-4 while discussing the previous paper; this does not destroy breakout rooms currently in progress.


## Limitations, other notes
- This entire system is fragile, and clearly not an intentional Zoom feature. It may break at any time.
- Zoom limits breakout room assignments to 200 people. If your meeting exceeds this, you may not be able to run automatic assignments.
- Attendees without zoom email addresses (e.g., those calling in) cannot be automatically assigned, and must be handled manually.
- Zoom messages become a poor way of communicating, since they are lost upon switching to/from a breakout room.


# Code in this repo

This repo also provides code and stubs for generating CSV files:
- `Meeting.ipynb` serves as a dashboard for managing the meeting, in which you can associate reviewers with email addresses, and generate CSVs to upload to zoom.
- `meeting.py`, providing the backend for `Meeting.ipynb`
- `conflicts.csv`, which is a CSV with each row representing a conflict for a given paper
- `reviewers.csv`, which is a CSV with each row representing a mapping from a reviewer name to a reviewer email. The meeting software essentially treats this as a database, continually reading from and appending to it. A given reviewer can have multiple entries in this database, representing for example distinct CMT and Zoom email addresses, or multiple Zoom email addresses. In the case of exceeding the 200 person breakout room assignment, later email addresses for a given reviewer are considered fresher.
- `ignore.csv`, which is a csv with reviewer names that should not be automatically assigned to breakout rooms (i.e., those running the PC meeting).
