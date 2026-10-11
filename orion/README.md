# Orion

Machine, Easy, Linux. https://app.hackthebox.com/machines/Orion

## Files

- `nmap_initial.txt` — initial `nmap -sCV` scan
- `gobuster_common.txt` — directory/file enumeration of the web app
- `hash.txt` — the bcrypt hash recovered from the app's database (cracked with
  hashcat + rockyou)

## Approach

1. **Recon.** `nmap` found SSH (22) and HTTP (80, nginx). The HTTP service
   redirects to the vhost `orion.htb`.
2. **Web enumeration.** Added `orion.htb` to `/etc/hosts`. The site is a
   telecom company landing page. `gobuster` against `common.txt` found
   `/admin`, which redirects to `/admin/login` — a Craft CMS 5.6.16 login
   page (`X-Powered-By: Craft CMS` in the response headers).
3. **Foothold — CVE-2025-32432.** Craft CMS versions up to 5.6.16 are
   vulnerable to an unauthenticated remote code execution bug in the
   `actions/assets/generate-transform` endpoint, rooted in a Yii framework
   object-injection issue (the request body contains a `__class` key that
   gets deserialized unsafely). CVSS 10.0 critical. Exploited with the
   Metasploit module
   `exploit/linux/http/craftcms_preauth_rce_cve_2025_32432`, giving a shell
   as `www-data`.
4. **Credential exposure.** `/var/www/html/craft/.env` stores the MySQL root
   password in plaintext. Logging into MySQL and reading the `users` table
   gave a bcrypt password hash for the admin account (email `adam@orion.htb`).
5. **Cracking + reuse.** `hashcat -m 3200` against the hash with the rockyou
   wordlist cracked it to `darkangel` in seconds (GPU-accelerated). The same
   password is reused as `adam`'s SSH login — reused credentials give direct
   SSH access and the user flag.
6. **Privilege escalation — CVE-2026-24061.** A `telnetd` (GNU inetutils 2.7)
   was listening on `127.0.0.1:23` only, found via `ss -tln` after gaining a
   shell. This version allows remote authentication bypass: the client-sent
   `USER` telnet environment variable is passed unsanitized into `/bin/login`,
   so setting `USER="-f root"` is interpreted as a `login` flag meaning
   "already authenticated," bypassing the password check entirely:

   ```
   USER="-f root" telnet -a 127.0.0.1
   ```

   This drops straight into a root shell.

## Key CVEs

- [CVE-2025-32432](https://github.com/craftcms/cms/security/advisories/GHSA-f3gw-9ww9-jmc3) —
  Craft CMS pre-auth RCE, CVSS 10.0
- [CVE-2026-24061](https://nvd.nist.gov/vuln/detail/CVE-2026-24061) —
  GNU inetutils telnetd auth bypass via `USER` environment variable
