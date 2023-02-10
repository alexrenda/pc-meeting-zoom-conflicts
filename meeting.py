#!/usr/bin/env python

import collections
import pandas as pd

conflicts = pd.read_csv('conflicts.csv')
conflicts = conflicts.groupby('# Paper ID')['Reviewer Email'].apply(','.join).reset_index()
conflicts.columns = ['id', 'emails']

def read_reviewer_name_to_emails():
    reviewers = collections.OrderedDict()
    with open('reviewers.csv') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, email = line.split(',')
            if name not in reviewers:
                reviewers[name] = []
            reviewers[name].append(email)

    return reviewers

def to_ignore():
    with open('ignore.csv') as f:
        return set(map(str.strip, f.read().splitlines()))

def read_reviewer_email_to_name():
    reviewers = {}
    with open('reviewers.csv') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, email = line.split(',')
            reviewers[email] = name

    return reviewers

def append_reviewer_email(name, email):
    name_to_emails = read_reviewer_name_to_emails()
    if name not in name_to_emails:
        print('!!!!!! {} is not in the reviewer list !!!!!!!'.format(name))

    emails_to_name = read_reviewer_email_to_name()
    if email in emails_to_name:
        print('Ignoring {},{}'.format(name,email))
        return

    with open('reviewers.csv', 'a') as f:
        print('{},{}'.format(name.strip(), email.strip()), file=f)

def get_unmatched_emails(emails):
    if isinstance(emails, str):
        emails = set(emails.split(','))
    elif isinstance(emails, set) or isinstance(emails, list) or isinstance(emails, tuple):
        emails = set(emails)
    else:
        raise ValueError('Invalid type of emails: {}'.format(type(emails)))

    reviewers = read_reviewer_email_to_name()
    return emails - set(reviewers.keys())

def assign_everyone_to_breakout_room():
    ignored = to_ignore()
    with open('reviewers.csv') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    names = [line.split(',')[0] for line in lines]
    names = [name for name in names if name not in ignored]
    n_unique_reviewer_names = len(set(names))
    n_extra_space = 200 - n_unique_reviewer_names
    written_names = set()
    lines_written = 0

    with open('zoom_rooms.csv', 'w') as f:
        print('Pre-assign Room Name,Email Address', file=f)

        for line in lines[::-1]:
            name, email = line.split(',')
            if name in ignored:
                continue
            if name in written_names and n_extra_space <= 0:
                continue
            if name in written_names:
                n_extra_space -= 1
            written_names.add(name)
            print('Discussion Room,{}'.format(email), file=f)
            lines_written += 1

    print('Wrote {} lines to zoom_rooms.csv'.format(lines_written))

def write_conflict_assignment_of_paper(paper_id):
    ignored = to_ignore()
    with open('reviewers.csv') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    reviewer_name_to_emails = read_reviewer_name_to_emails()
    reviewer_email_to_name = read_reviewer_email_to_name()

    lines_written = 0

    with open('zoom_rooms.csv', 'w') as f:
        print('Pre-assign Room Name,Email Address', file=f)

        conflicted_reviewer_emails = set(conflicts[conflicts['id'] == paper_id]['emails'].values[0].split(','))
        conflicted_reviewer_names = set()

        for email in conflicted_reviewer_emails:
            conflicted_reviewer_names.add(reviewer_email_to_name[email])

        for name in conflicted_reviewer_names:
            conflicted_reviewer_emails.update(reviewer_name_to_emails[name])
            print('CONFLICTED: {} ({})'.format(name, reviewer_name_to_emails[name]))

        conflicted_reviewer_names = conflicted_reviewer_names - ignored

        n_extra_space = 200 - len(set(conflicted_reviewer_names))
        written_names = set()

        # now write the conflicted reviewers to the Conflict Room
        for line in lines[::-1]:
            name, email = line.split(',')
            if name not in conflicted_reviewer_names:
                continue

            if name in written_names and n_extra_space <= 0:
                continue

            if name in written_names:
                n_extra_space -= 1

            written_names.add(name)
            print('Conflict Room,{}'.format(email), file=f)
            lines_written += 1

    print('Wrote {} lines to zoom_rooms.csv'.format(lines_written))

def get_emails_from_breakout_room_assignment(file_name):
    return set(pd.read_csv(file_name)['Email Address'].values)
