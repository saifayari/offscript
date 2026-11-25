"""Synthetic educational dataset generators for Phishing & Network Intrusion labs.

NOTE: All data generated here is 100% synthetic and designed strictly for
classroom Machine Learning demonstrations. No real emails, credentials, or
live network traffic are ever collected or scanned.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_phishing_dataset(seed: int = 42) -> pd.DataFrame:
    """Create a deterministic, labeled synthetic dataset of 120 distinct emails.

    Each email is uniquely authored (no near-duplicate template twins across
    train/test splits) and includes realistic borderline messages so held-out
    test evaluation demonstrates real-world classification trade-offs.

    Returns a DataFrame with columns:
        - id, subject, body, text, category, label ('Legitimate' or 'Phishing')
    """
    rng = np.random.default_rng(seed)

    # 60 distinct synthetic legitimate emails
    legit_entries: list[tuple[str, str, str]] = [
        ("Weekly Sprint Review Notes", "Hi team, attached are the sprint notes from today's architecture meeting. Next standup is Tuesday at 10 AM in Room B2.", "Work Update"),
        ("Workshop Room Confirmation", "Hello students, the Intro to AI workshop will take place in Auditorium A this Thursday from 2 PM to 4 PM. Bring your laptops.", "University"),
        ("Planned Server Maintenance Window", "IT Notice: Campus Wi-Fi maintenance runs Sunday 02:00-04:00 AM. No action or password entry is required from your side.", "IT Notice"),
        ("Quarterly Design Feedback Summary", "Thanks everyone for sharing feedback on the dashboard mockups. I uploaded the revised slides to our shared team folder.", "Work Update"),
        ("Project Milestone Reminder", "Hi team, please submit your final presentation slides before Friday at 5 PM so we can review the agenda together.", "Work Update"),
        ("Library Book Return Receipt", "Thank you for returning Introduction to Machine Learning to the university library. Your borrowing balance is zero.", "University"),
        ("Lunch and Learn Session Friday", "Join us Friday at noon in the student lounge for a casual talk on data visualization best practices. Sandwiches provided.", "University"),
        ("Updated Office Holiday Calendar", "Hello all, HR published the updated national holiday calendar on the internal portal. Let me know if you have scheduling questions.", "HR"),
        ("Lab Equipment Checkout Approved", "Your request to reserve two Raspberry Pi kits for the robotics club session has been approved by the lab coordinator.", "University"),
        ("Code Review Follow-Up", "Nice work on the data preprocessing module. I left two minor comments about adding docstrings and unit test coverage.", "Engineering"),
        ("Monthly Newsletter: AI Club Digest", "Welcome to this month's student club digest featuring study group hours, hackathon announcements, and reading recommendations.", "University"),
        ("Course Syllabus Revision v2", "Dear class, I added the reading list for Week 5 covering supervised learning metrics on the official course page.", "University"),
        ("Cloud Sandbox Monthly Receipt #4081", "Your monthly cloud sandbox receipt for 15.00 USD has been processed for your records. No payment update needed.", "Billing"),
        ("Conference Travel Itinerary", "Hi Seif, here is your confirmed train schedule for next week's technology symposium along with the hotel check-in details.", "Travel"),
        ("New Intern Welcome Coffee", "Let's meet tomorrow morning at 9:30 AM on the third floor terrace to welcome our two summer engineering interns.", "HR"),
        ("Backup Storage Summary Report", "Automated summary: All weekly documentation snapshots completed normally with zero disk warnings across department folders.", "IT Notice"),
        ("Research Paper Reading Group", "We will discuss the Transformer attention paper next Wednesday. Please read sections 1 to 3 beforehand if you have time.", "University"),
        ("Team Photo Shoot Schedule", "Marketing will take updated team portraits next Monday between 11 AM and 1 PM in the main atrium. Casual business attire.", "HR"),
        ("Security Best Practices Tip", "Friendly reminder from IT: always double-check sender addresses before opening unexpected attachments or sharing files externally.", "IT Notice"),
        ("Capstone Abstract Deadline Tonight", "Urgent reminder for capstone teams: upload your abstract PDF to the university grading portal before tonight at 11:59 PM.", "University"),
        ("Client Demo Rehearsal Invite", "Hi everyone, let's do a quick 20-minute dry run of our product demo tomorrow at 3 PM using the standard team calendar invite.", "Work Update"),
        ("Cafeteria Menu Updates", "Starting Monday, the campus cafeteria will offer new vegetarian wraps and fresh fruit bowls every weekday afternoon.", "University"),
        ("Printer Toner Replacement Complete", "The third-floor color printer has been restocked with paper and cyan toner. Thanks for your patience this morning.", "IT Notice"),
        ("Grant Application Feedback", "The faculty committee reviewed your research proposal and shared helpful suggestions for strengthening the evaluation section.", "University"),
        ("Python Study Jam This Saturday", "Beginners are welcome at our Saturday coding session. We will cover pandas DataFrames, charts, and basic scikit-learn workflows.", "University"),
        ("Annual Ergonomics Checklist", "HR shared a short guide on adjusting desk height and monitor distance to stay comfortable during long coding sessions.", "HR"),
        ("Data Visualization Dataset Ready", "I cleaned the public weather CSV file for tomorrow's lab exercise and placed it inside the shared classroom repository.", "Engineering"),
        ("Guest Speaker Q&A Summary", "Thank you for attending yesterday's cybersecurity panel. Here are the key takeaways on career paths and ethical hacking clubs.", "University"),
        ("Shared Drive Folder Access Granted", "You now have read access to the Fall Workshop Resources folder as requested by your team lead earlier today.", "IT Notice"),
        ("Parking Permit Renewal Notice", "Campus parking passes for the spring semester can be renewed in person at the student services desk during office hours.", "University"),
        ("Urgent Meeting Room Change", "Urgent update: today's 2 PM design review moved from Room 104 to Room 208 due to projector calibration.", "Work Update"),
        ("Podcast Episode Recommendation", "Thought you might enjoy this interview explaining how decision trees and random forests work in everyday healthcare tools.", "Work Update"),
        ("Volunteer Shift Schedule", "Thanks to everyone helping run the registration desk at Saturday's university tech fair. Shift times are posted on the whiteboard.", "University"),
        ("Quarterly Inventory Audit Done", "Facilities completed the annual laptop inventory check across all classrooms with every device accounted for.", "Operations"),
        ("Welcome to Intro to AI Cohort", "We are excited to host you for our two-hour interactive workshop covering machine learning fundamentals and practical exercises.", "University"),
        ("API Documentation Updated", "Docs update: added clear examples explaining train-test splitting and avoiding data leakage in scikit-learn pipelines.", "Engineering"),
        ("Mentor Office Hours This Week", "I am available Thursday 4 PM to 6 PM to answer questions about your semester projects or career portfolios.", "University"),
        ("Team Retrospective Action Items", "Here are the three process improvements we agreed on during Friday's retrospective meeting.", "Work Update"),
        ("Campus Hackathon Judging Rubric", "Teams will be evaluated on creativity, clarity of explanation, live demo reliability, and real-world usefulness.", "University"),
        ("Password Manager Demo Flyer", "Learn how password managers and multi-factor authentication help protect student accounts during next week's lunchtime demo.", "IT Notice"),
        ("Lab Air Conditioning Repair", "Facilities confirmed technicians will inspect the second-floor study room ventilation tomorrow morning around 8 AM.", "Operations"),
        ("Book Club Next Selection", "Our student reading circle voted for a beginner-friendly biography on early computing pioneers for next month's discussion.", "University"),
        ("Internship Interview Confirmation", "Hello, we look forward to speaking with you on Wednesday at 11 AM regarding the junior data analyst summer internship.", "HR"),
        ("Conference Poster Printing Pickup", "Your research poster print is ready for pickup at the university print shop before 4:30 PM today.", "University"),
        ("Software License Renewal Complete", "Departmental IDE licenses were renewed automatically for the academic year. Restart your editor if prompted.", "IT Notice"),
        ("Peer Review Assignment Ready", "Please review two classmates' data science notebooks before Monday morning using the grading checklist.", "University"),
        ("Office Supply Order Shipped", "Whiteboard markers and sticky notes for the workshop tables arrived at the front reception desk this afternoon.", "Operations"),
        ("Database Query Optimization Note", "Adding an index on the timestamp column cut our analytics dashboard load time from four seconds down to 250 milliseconds.", "Engineering"),
        ("Community Blood Drive Friday", "The campus health center is hosting a voluntary blood drive outside the main library from 9 AM to 3 PM.", "University"),
        ("Updated Study Room Hours", "During final exam week, quiet study halls on floor three will stay open until 11 PM every evening.", "University"),
        ("Design System Color Tokens", "I pushed the final dark navy and cyan palette variables to the UI repository for everyone building workshop slides.", "Engineering"),
        ("Alumni Career Panel Invites", "Three recent graduates working in AI engineering will share resume tips and project advice next Tuesday evening.", "University"),
        ("Travel Expense Reimbursement Paid", "Your train ticket reimbursement from last month's tech meetup has been approved by accounting.", "Billing"),
        ("Git Branching Cheat Sheet", "Here is a quick one-page visual summary of pull requests and merge conflicts for Friday's beginner session.", "Engineering"),
        ("Photography Club Exhibition", "Stop by the student gallery hallway this week to check out portraits and campus architecture shots.", "University"),
        ("Security Awareness Quiz Results", "Congrats to everyone who completed the monthly phishing awareness refresher during onboarding.", "IT Notice"),
        ("Urgent Action: Confirm Dietary Preferences", "Urgent headcount check for tomorrow's workshop lunch: please reply with vegetarian or standard meal preference before 3 PM.", "Operations"),
        ("Password Expiry Policy Reminder", "Reminder from IT: campus passwords rotate every 180 days; change yours anytime from your device settings, never via email links.", "IT Notice"),
        ("Account Verification Note for Speakers", "Hi Seif, could you confirm your bio spelling and workshop title by tomorrow afternoon for the printed event brochure?", "Work Update"),
        ("Grant Winner Announcement", "Congratulations to the robotics student team on earning third place at the regional engineering competition!", "University"),
    ]

    # 60 distinct synthetic phishing-style educational emails (harmless placeholders only)
    phish_entries: list[tuple[str, str, str]] = [
        ("URGENT: Verify Your Account Now", "Your university account will be permanently suspended within 24 hours. Click [verification-portal-link] immediately and enter your password to verify.", "Urgent Verification"),
        ("Immediate Action Required: Account Locked", "Security alert: unusual sign-in detected. Confirm your username, password, and security code right away at [secure-login-form] to restore access.", "Credential Harvest"),
        ("Congratulations! You Won a Brand New Laptop", "Lucky winner! You have been selected to claim a free flagship laptop prize. Pay a small processing fee and enter bank details now.", "Fake Prize"),
        ("Unexpected Password Reset Confirmation", "A password reset was requested for your profile. If you did not authorize this, click [cancel-reset-link] and submit your current password immediately.", "Password Reset Lure"),
        ("Final Warning: Mailbox Storage Full", "Your inbox exceeded 99 percent capacity and incoming messages are blocked. Verify your login credentials at [mail-upgrade-portal] within 2 hours.", "Urgent Verification"),
        ("Claim Your 5000 Dollar Student Grant Prize", "Congratulations! You qualified for an exclusive cash reward. Reply immediately with your national ID, phone number, and bank card to claim.", "Fake Prize"),
        ("Payroll Verification Required Today", "HR requires every employee to re-enter bank routing numbers and portal passwords before 4 PM today or salary deposits will be delayed.", "Credential Harvest"),
        ("Delivery Failed: Customs Fee Needed", "Your package is held at customs. Click [tracking-payment-link] and enter your credit card details within 12 hours to avoid return.", "Fake Invoice"),
        ("Security Alert: Confirm Your Identity", "We noticed unauthorized login activity on your cloud account. Verify your password and MFA backup code now to avoid suspension.", "Credential Harvest"),
        ("URGENT Executive Request: Gift Cards", "Hi, I am stuck in a meeting and need you to purchase 5 digital gift cards urgently. Keep this confidential and email the voucher codes.", "Impersonation"),
        ("Password Expiry Notice: Act Immediately", "Your campus email password expires in 30 minutes. Keep the same password by logging into [quick-renewal-page] right now.", "Password Reset Lure"),
        ("Unclaimed Crypto Bonus Rewards", "Claim your instant 2500 bonus payout before the countdown timer reaches zero. Connect your wallet and enter your recovery phrase now.", "Fake Prize"),
        ("Overdue Invoice #9921 - Action Required", "Attached is an urgent overdue invoice notice. Log in to [billing-confirm-portal] with your corporate password to avoid legal penalty.", "Fake Invoice"),
        ("Mandatory Two-Factor Re-Enrollment", "All staff must re-submit their username, current password, and one-time verification token today at [mfa-update-portal].", "Credential Harvest"),
        ("Scholarship Prize Winner Notification", "You won an international tech scholarship reward! Send your passport photo and bank account number today to unlock your funds.", "Fake Prize"),
        ("Account Deactivation Scheduled Tonight", "Failure to validate your student email credentials before midnight will permanently delete all your files and grades.", "Urgent Verification"),
        ("Suspicious Login From Unknown Device", "Someone signed in from an unrecognized location. Click [verify-device-now] and confirm your password and PIN immediately.", "Password Reset Lure"),
        ("Tax Refund Waiting for Confirmation", "You are eligible for an instant tax refund deposit. Submit your card number, expiration date, and security code to receive funds.", "Fake Invoice"),
        ("Verify Payment Card to Keep Subscription", "Your account billing failed. Update your credit card and account password immediately at [card-verify-link] to prevent termination.", "Fake Invoice"),
        ("Exclusive Survey Reward: Claim 500 Cash", "Complete this 1-minute survey and enter your login credentials to immediately collect your guaranteed 500 cash prize reward.", "Fake Prize"),
        ("IT Helpdesk: Urgent Password Validation", "Hi, IT Helpdesk is auditing logins today. Please reply directly to this message with your current portal password and backup code.", "Credential Harvest"),
        ("Immediate Verification: Shared Document", "You received a confidential salary document. Sign in at [doc-unlock-login] using your email password to view the attachment.", "Credential Harvest"),
        ("Warning: Suspicious Activity Detected", "Critical security notice: confirm your account ownership right now or your profile will be locked permanently within 1 hour.", "Urgent Verification"),
        ("Free Conference VIP Pass Winner", "Congratulations! Claim your free VIP conference voucher immediately by confirming your full credentials and card verification.", "Fake Prize"),
        ("Cloud Drive Quota Exceeded - Act Now", "Your cloud drive is full and files will be erased in 6 hours. Click [storage-verify-now] and enter your password to expand free space.", "Urgent Verification"),
        ("Urgent Bank Transfer Verification", "Your pending transfer requires immediate identity confirmation. Enter your banking username, password, and SMS code right now.", "Credential Harvest"),
        ("Password Reset Required Due to Breach", "Due to a security incident, enter your old password and new password immediately at [emergency-reset-portal] to stay protected.", "Password Reset Lure"),
        ("Unclaimed Parcel Waiting at Depot", "Confirm your shipping address and pay the 3 dollar redelivery charge at [parcel-fee-link] immediately before return.", "Fake Invoice"),
        ("Final Reminder: Verify Student ID Card", "Verify your student portal password within 3 hours at [campus-id-check] or lose access to exam registration.", "Urgent Verification"),
        ("Special Reward Voucher Inside", "You won a loyalty gift voucher! Click [redeem-voucher-now] and log in with your email password to collect your bonus.", "Fake Prize"),
        ("Team Portal Password Sync Needed", "Hi team, please verify your office portal credentials in the updated login sheet before noon to avoid sync errors.", "Credential Harvest"),
        ("Urgent Invoice Confirmation Needed", "Please review the attached payment request and confirm your account login at [invoice-portal-check] right away.", "Fake Invoice"),
        ("Verify MFA Token Within 15 Minutes", "An automated login attempt occurred. Enter your 6-digit MFA code and password immediately at [mfa-protect-check].", "Password Reset Lure"),
        ("Account Suspension Appeal Form", "Your profile has been flagged for removal. Submit your password and recovery email at [appeal-verify-portal] immediately.", "Urgent Verification"),
        ("Congratulations: Smartphone Giveaway", "Your email was randomly selected for a flagship smartphone giveaway! Claim within 1 hour by submitting shipping and card info.", "Fake Prize"),
        ("HR Direct Deposit Update Alert", "We paused your payroll transfer. Re-enter your portal login credentials and account routing details right now.", "Credential Harvest"),
        ("Admin Alert: Re-Authenticate Mailbox", "Your mailbox token expired. Sign in at [webmail-reauth-link] right now to keep receiving important messages.", "Urgent Verification"),
        ("Instant Prize Claim Confirmation", "Reply immediately with your full name, password verification code, and bank card to claim your promotional bonus.", "Fake Prize"),
        ("Security Update: Reset Credentials Now", "Mandatory security patch requires submitting your current password at [security-patch-login] before 5 PM today.", "Password Reset Lure"),
        ("Verify Account Access Before Lockout", "Unusual traffic triggered a lock warning. Confirm your credentials immediately at [unlock-portal-check] to avoid lockout.", "Urgent Verification"),
        ("Cardholder Security Check Required", "Verify your recent online card purchase immediately by entering your PIN and portal password at [bank-check-page].", "Fake Invoice"),
        ("Bonus Student Stipend Approved", "Claim your extra 1200 student stipend prize today! Enter your university login and debit card at [stipend-claim-form].", "Fake Prize"),
        ("Notice: Email Forwarding Suspended", "Your email forwarding stopped due to unverified credentials. Log in at [forward-fix-portal] right away.", "Urgent Verification"),
        ("Password Change Confirmation Needed", "Did you change your recovery email? Verify your password at [recovery-check-link] immediately to protect your data.", "Password Reset Lure"),
        ("Confidential Vendor Bank Change", "Please update our supplier wire transfer account number immediately before paying today's open invoice.", "Fake Invoice"),
        ("Congratulations! Selected for Cashback", "Unlock 350 cashback rewards immediately by entering your card number and online banking login credentials.", "Fake Prize"),
        ("Urgent: Re-Confirm Cloud Permissions", "Your developer permissions expire tonight. Submit your username, password, and API secret at [dev-reauth-portal].", "Credential Harvest"),
        ("Missed Voicemail Notification", "You have 1 new urgent voicemail. Sign in with your corporate email password at [voice-msg-portal] to listen.", "Credential Harvest"),
        ("Warning: Unpaid Toll Balance", "Pay your 4 dollar unpaid highway toll immediately at [toll-pay-portal] with your bank card to avoid late fines.", "Fake Invoice"),
        ("Action Needed: Update Recovery Phone", "Confirm your current password and SMS verification code at [phone-recovery-link] within 2 hours.", "Password Reset Lure"),
        ("Reward Points Expiring Tonight", "Your 15000 reward points expire tonight! Log in at [points-redeem-portal] with your credentials to claim gift cards.", "Fake Prize"),
        ("Account Upgrade Required Immediately", "Upgrade your mailbox security profile by submitting your password and birth date at [security-upgrade-page].", "Urgent Verification"),
        ("Final Notice: Domain Renewal Payment", "Your club website domain expires today. Enter card payment and admin password at [domain-renew-link] immediately.", "Fake Invoice"),
        ("Verify Identity for Remote VPN", "Remote VPN access is restricted until you re-enter your company username and password at [vpn-check-portal].", "Credential Harvest"),
        ("Unexpected Login Attempt Blocked", "Review this blocked attempt immediately by entering your password and 2FA code at [blocked-login-review].", "Password Reset Lure"),
        ("Free Travel Voucher Claim Link", "You won two complimentary flight vouchers! Confirm your passport number and card details immediately at [travel-prize-link].", "Fake Prize"),
        # Intentionally subtle / polite borderline phishing emails to test model limits
        ("Quick Favor Before Friday Meeting", "Hi, could you share the updated shared folder spreadsheet and send me the guest portal password when you get a chance?", "Impersonation"),
        ("Updated Course Portal Notes", "Hello student, please check the updated syllabus attachment and sign in with your campus login on [external-notes-viewer].", "Credential Harvest"),
        ("Meeting Follow-Up Document", "Thanks for today's call! Please open the attached project summary and confirm your Microsoft office login to view comments.", "Impersonation"),
        ("Workshop Certificate Download", "Hello! Your workshop attendance certificate is ready. Kindly confirm your portal username and password at [cert-download-form].", "Credential Harvest"),
    ]

    rows = [
        {"subject": s, "body": b, "category": c, "label": "Legitimate"} for (s, b, c) in legit_entries
    ] + [
        {"subject": s, "body": b, "category": c, "label": "Phishing"} for (s, b, c) in phish_entries
    ]

    df = pd.DataFrame(rows).drop_duplicates(subset=["subject", "body"]).reset_index(drop=True)
    perm = rng.permutation(len(df))
    df = df.iloc[perm].reset_index(drop=True)
    df["id"] = np.arange(1, len(df) + 1)
    df["text"] = "Subject: " + df["subject"] + "\n\n" + df["body"]
    return df[["id", "subject", "body", "text", "category", "label"]]


def generate_network_dataset(n_samples: int = 600, seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic, realistic network activity dataset with natural overlap.

    Features:
        - failed_logins (int): Number of failed authentication attempts
        - connection_count (int): Connections observed in the monitoring window
        - data_sent_mb (float): Outbound traffic volume in megabytes
        - unusual_port (int): 1 if a non-standard port was observed, else 0
        - label (int): 0 = Normal, 1 = Suspicious
    """
    if n_samples < 500:
        raise ValueError("Dataset must contain at least 500 records for educational evaluation.")

    rng = np.random.default_rng(seed)
    n_normal = int(round(n_samples * 0.62))
    n_susp = n_samples - n_normal

    # --- Normal traffic (~62%): includes natural variance (occasional password typos, sync bursts, backups) ---
    norm_failed = rng.poisson(lam=0.85, size=n_normal)
    typo_mask = rng.random(n_normal) < 0.10
    norm_failed[typo_mask] += rng.integers(2, 6, size=typo_mask.sum())

    norm_conn = np.clip(rng.normal(loc=24, scale=13, size=n_normal), 2, 95).round().astype(int)
    update_mask = rng.random(n_normal) < 0.09
    norm_conn[update_mask] = rng.integers(55, 110, size=update_mask.sum())

    norm_data = np.clip(rng.gamma(shape=2.5, scale=16.0, size=n_normal), 1.0, 280.0).round(2)
    backup_mask = rng.random(n_normal) < 0.08
    norm_data[backup_mask] = rng.uniform(115.0, 260.0, size=backup_mask.sum()).round(2)

    norm_port = (rng.random(n_normal) < 0.09).astype(int)

    normal_df = pd.DataFrame({
        "failed_logins": norm_failed,
        "connection_count": norm_conn,
        "data_sent_mb": norm_data,
        "unusual_port": norm_port,
        "label": np.zeros(n_normal, dtype=int),
    })

    # --- Suspicious traffic (~38%): brute-force, port-scan, exfiltration, plus stealthy low-and-slow ---
    p1 = int(n_susp * 0.28)  # Brute-force style
    p2 = int(n_susp * 0.27)  # Scanning / unusual port burst
    p3 = int(n_susp * 0.22)  # Large outbound exfiltration
    p4 = n_susp - (p1 + p2 + p3)  # Stealthy / low-and-slow overlapping normal ranges

    s_failed = np.concatenate([
        rng.integers(6, 24, size=p1),
        rng.integers(1, 7, size=p2),
        rng.integers(0, 5, size=p3),
        rng.integers(2, 6, size=p4),
    ])
    s_conn = np.concatenate([
        rng.integers(18, 65, size=p1),
        rng.integers(75, 240, size=p2),
        rng.integers(25, 95, size=p3),
        rng.integers(32, 68, size=p4),
    ])
    s_data = np.concatenate([
        rng.uniform(10.0, 85.0, size=p1),
        rng.uniform(18.0, 140.0, size=p2),
        rng.uniform(165.0, 620.0, size=p3),
        rng.uniform(48.0, 125.0, size=p4),
    ]).round(2)
    s_port = np.concatenate([
        (rng.random(p1) < 0.35).astype(int),
        (rng.random(p2) < 0.85).astype(int),
        (rng.random(p3) < 0.65).astype(int),
        (rng.random(p4) < 0.30).astype(int),
    ])

    susp_df = pd.DataFrame({
        "failed_logins": s_failed,
        "connection_count": s_conn,
        "data_sent_mb": s_data,
        "unusual_port": s_port,
        "label": np.ones(n_susp, dtype=int),
    })

    df = pd.concat([normal_df, susp_df], ignore_index=True)
    perm = rng.permutation(len(df))
    df = df.iloc[perm].reset_index(drop=True)
    return df


PREDEFINED_SAMPLE_EMAILS: dict[str, str] = {
    "Legitimate: Team Workshop Update": (
        "Subject: Room Confirmation for Thursday AI Workshop\n\n"
        "Hello everyone, the Intro to AI session starts at 2:00 PM in Auditorium B. "
        "Please bring your laptop so you can experiment with the interactive exercises. "
        "Let me know if you have any questions beforehand."
    ),
    "Phishing: Urgent Account Verification": (
        "Subject: URGENT: Your Account Will Be Suspended\n\n"
        "Security notice: we detected unusual sign-in activity on your student profile. "
        "Click [verify-account-link] immediately and enter your username and password "
        "within 24 hours to avoid permanent lockout."
    ),
    "Phishing: Fake Prize Notification": (
        "Subject: Congratulations! Claim Your Free Laptop Prize\n\n"
        "You have been selected as today's lucky campus giveaway winner! "
        "Submit your bank card details and portal password immediately to claim your reward."
    ),
    "Phishing: Unexpected Password Reset": (
        "Subject: Unexpected Password Reset Request\n\n"
        "Someone requested a password reset on your account. If this was not you, "
        "log in immediately at [emergency-reset-portal] and confirm your current password and MFA code."
    ),
    "Borderline: Urgent Legitimate IT Deadline": (
        "Subject: Urgent Reminder: Submit Final Project Slides Today\n\n"
        "Urgent reminder for all teams: please upload your presentation slides to the "
        "official course folder before 5 PM today. No login links or passwords needed."
    ),
}


PREDEFINED_NETWORK_SCENARIOS: dict[str, dict[str, int | float | str]] = {
    "SCENARIO 1 – NORMAL ACTIVITY": {
        "failed_logins": 1,
        "connection_count": 18,
        "data_sent_mb": 22.5,
        "unusual_port": 0,
        "description": "Routine office workstation session: 1 typo login, moderate connections, normal data transfer on standard ports.",
    },
    "SCENARIO 2 – SUSPICIOUS ACTIVITY": {
        "failed_logins": 14,
        "connection_count": 155,
        "data_sent_mb": 340.0,
        "unusual_port": 1,
        "description": "Repeated failed logins, high connection burst, large outbound transfer, and an unusual port observed.",
    },
    "SCENARIO 3 – MIXED ACTIVITY": {
        "failed_logins": 2,
        "connection_count": 46,
        "data_sent_mb": 82.0,
        "unusual_port": 0,
        "description": "Gray-area session: slightly elevated logins, connections, and outbound volume, yet standard ports and no extreme spike.",
    },
}
