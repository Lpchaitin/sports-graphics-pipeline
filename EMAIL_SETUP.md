# 📧 Email Notifications Setup Guide

Automatically send generated graphics via Gmail when picks are processed.

## 🎯 What This Does

After graphics are generated, an email is automatically sent with:
- ✅ All generated PNG files as attachments
- ✅ Summary of how many graphics were created
- ✅ Date and pick information
- ✅ Professional HTML email design

---

## 🔐 Step 1: Create Gmail App Password

**⚠️ Important:** Gmail requires an "App Password" (not your regular password) for automated email sending.

### Enable 2-Factor Authentication (if not already enabled)

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** (left sidebar)
3. Under "How you sign in to Google," click **2-Step Verification**
4. Follow the prompts to enable 2FA (if not already enabled)

### Create App Password

1. Go to: https://myaccount.google.com/apppasswords
   - Or: Google Account → Security → 2-Step Verification → App passwords
2. Sign in if prompted
3. Under "Select app," choose **Mail**
4. Under "Select device," choose **Other (Custom name)**
5. Enter name: `MLB Graphics Pipeline`
6. Click **Generate**
7. **COPY THE 16-CHARACTER PASSWORD** (looks like: `abcd efgh ijkl mnop`)
   - You won't see it again!
   - Remove spaces when using it

---

## 🔑 Step 2: Add Secrets to GitHub

Go to: https://github.com/Lpchaitin/sports-graphics-pipeline/settings/secrets/actions

Click **"New repository secret"** for each of these:

### Secret 1: GMAIL_USERNAME
- **Name:** `GMAIL_USERNAME`
- **Value:** Your full Gmail address (e.g., `yourname@gmail.com`)

### Secret 2: GMAIL_APP_PASSWORD
- **Name:** `GMAIL_APP_PASSWORD`
- **Value:** The 16-character app password from Step 1 (no spaces)
  - Example: `abcdefghijklmnop`

### Secret 3: EMAIL_RECIPIENT
- **Name:** `EMAIL_RECIPIENT`
- **Value:** Email address to receive graphics
  - Can be the same as GMAIL_USERNAME or different
  - Examples: `yourname@gmail.com` or `team@company.com`

---

## ✅ Step 3: Enable the Workflow

The workflow is already created: `.github/workflows/email-graphics.yml`

Commit and push it:

```bash
cd /workspaces/sports-graphics-pipeline
git add .github/workflows/email-graphics.yml
git commit -m "Add email notifications for generated graphics"
git push
```

---

## 🧪 Step 4: Test It

### Option A: Trigger Graphics Generation

1. Run the "Send Picks to Graphics Pipeline" workflow from MLB-Model repo
2. Wait for graphics to generate
3. Email should send automatically!

### Option B: Re-run Previous Workflow

1. Go to: https://github.com/Lpchaitin/sports-graphics-pipeline/actions
2. Click on a successful "Generate MLB Graphics" run
3. Click **"Re-run all jobs"**
4. Email workflow should trigger after completion

---

## 📧 What the Email Looks Like

**Subject:** `MLB Graphics Ready - 20260419 (6 games)`

**Includes:**
- Professional HTML layout with your branding
- Summary: Date, number of graphics, pick details
- All PNG files attached (ready to download)
- Link back to the workflow run

**Attachments:**
- `20260419_kc_at_nyy.png`
- `20260419_tb_at_pit.png`
- `20260419_cin_at_min.png`
- etc. (all generated graphics)

---

## 🎨 Customization Options

### Change Recipient Email

Update the `EMAIL_RECIPIENT` secret to send to a different address.

### Send to Multiple Recipients

Edit `.github/workflows/email-graphics.yml`, line with `to:`:

```yaml
to: email1@example.com,email2@example.com,email3@example.com
```

### Change Email Design

Edit the HTML in email-graphics.yml under "Create email body" step.

### Add CC/BCC

Add to the email step:

```yaml
cc: someone@example.com
bcc: analytics@example.com
```

---

## 🔍 Troubleshooting

### "Authentication failed" error

**Cause:** Wrong app password or username

**Fix:**
1. Verify `GMAIL_USERNAME` is your full Gmail address
2. Regenerate app password at https://myaccount.google.com/apppasswords
3. Update `GMAIL_APP_PASSWORD` secret (no spaces in the password)

### "2-Step Verification required"

**Cause:** 2FA not enabled on Gmail

**Fix:** 
1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Then create app password

### Email not sending

**Cause:** Workflow didn't trigger or graphics workflow failed

**Fix:**
1. Check that graphics workflow completed successfully
2. Check Actions tab for email workflow run
3. View logs for specific error messages

### Attachments too large

**Cause:** Gmail has 25MB limit

**Fix:** Graphics should be ~1MB total (well under limit), but if needed:
- Generate fewer graphics
- Or upload to cloud storage and link instead

---

## 🔒 Security Notes

✅ **App passwords are secure:**
- They're specific to one app/device
- Can be revoked anytime without changing your main password
- Don't give access to your full Google account

✅ **GitHub Secrets are encrypted:**
- Only visible to workflow runs
- Never exposed in logs
- Can be updated/deleted anytime

⚠️ **Best practices:**
- Use a dedicated Gmail account for automation (optional)
- Revoke app password if no longer needed
- Review GitHub Secret access permissions periodically

---

## 📊 Full Automated Flow

```
1. Model generates predictions → Commit to MLB-Model
                ↓
2. MLB-Model workflow → Sends CSV to graphics-pipeline
                ↓
3. Graphics-pipeline workflow → Generates graphics
                ↓
4. Email workflow (NEW!) → Sends graphics to your email
                ↓
5. You receive email with all graphics attached! 📧🎨
```

---

## 🎉 You're All Set!

Once you complete the 3 steps:
1. ✅ Gmail App Password created
2. ✅ GitHub Secrets added
3. ✅ Workflow committed

Every time graphics are generated, they'll automatically be emailed to you!

---

## 💡 Alternative: Send to Slack/Discord Instead

If you prefer Slack or Discord notifications instead of email, let me know and I can set that up instead!
