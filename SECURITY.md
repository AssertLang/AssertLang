# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.x     | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please report it privately.

**Please do NOT create a public GitHub issue for security vulnerabilities.**

### How to Report

1. **Email:** Send details to `security@assertlang.dev` or `hello@assertlang.dev`
2. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
3. **Response time:** We'll respond within 48 hours

### What to Expect

1. **Acknowledgment:** We'll confirm receipt within 48 hours
2. **Investigation:** We'll investigate and assess the severity
3. **Fix:** We'll develop and test a fix
4. **Disclosure:** We'll coordinate disclosure timing with you
5. **Credit:** We'll credit you in the release notes (if desired)

## Security Best Practices

When using AssertLang:

- **API Keys:** Never commit API keys or credentials to .al files
- **Environment Variables:** Use environment variables for sensitive data
- **Tool Security:** Review generated code before deploying to production
- **Network:** Run generated servers behind firewalls in production
- **Rate Limiting:** Use built-in rate limiting features
- **Updates:** Keep AssertLang updated to the latest version

## Known Security Considerations

- Generated servers include rate limiting by default (100 req/min)
- CORS is enabled with origin validation
- Security headers (HSTS, CSP, X-Frame-Options) are included
- Input validation is performed on all verb parameters

## Security Updates

Security fixes will be released as patch versions and announced in:
- GitHub Security Advisories
- CHANGELOG.md
- Discord announcements

## Scope

This policy applies to:
- The AssertLang framework and CLI
- Generated server code
- Official tool adapters
- Documentation examples

**Out of scope:**
- Custom user-created tools
- Third-party integrations
- Deployment infrastructure

## Contact

- **Security issues:** security@assertlang.dev or hello@assertlang.dev
- **General questions:** hello@assertlang.dev
- **GitHub Discussions:** https://github.com/AssertLang/AssertLang/discussions

---

Thank you for helping keep AssertLang and its users safe!
