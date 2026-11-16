# Third-party notices

Apart from the Contributor Covenant text named below, this repository copies no third-party text into its skills or docs. Skill text is original.

## Contributor Covenant

- Source: https://www.contributor-covenant.org/version/3/0/
- License: Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0), as stated in the retained Code of Conduct.
- Use: `CODE_OF_CONDUCT.md` is adapted from Contributor Covenant version 3.0. The attribution is in that file.

## Cybersecurity research

The security audit, pentest and repair skills use original prose and standard-library fixtures. Their methods were compared with the following English and Chinese sources on 2026-11-16. Instructions, technical examples and licenses were inspected, not just repository summaries. No third-party scripts, payloads, scanners or containers were executed or copied into this repository.

Links on branches can change. SHA-256 values identify the retrieved primary text, not an entire repository or a successful behavioral test.

| Source | Inspected file and license | Method retained or boundary rejected | Retrieved text SHA-256 |
|---|---|---|---|
| Cloudflare | [Inspected file](https://raw.githubusercontent.com/cloudflare/security-audit-skill/main/skills/security-audit/SKILL.md); [MIT](https://raw.githubusercontent.com/cloudflare/security-audit-skill/main/LICENSE) | Separate source evidence, uncertainty and coverage; keep source audits distinct from runtime tests. | `5e3e96a1e438d8f35fef0a1e38f02d4f00e2bdf910401b7dfe00e6779c6dac85` |
| Trail of Bits patch validation | [Inspected file](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/post-patch-validation/skills/post-patch-validation/SKILL.md); [CC BY-SA 4.0](https://raw.githubusercontent.com/trailofbits/skills/main/LICENSE) | Compare baseline and patch with independent controls; reject harness errors as vulnerability reproduction. | `33b604f4d7d62eab393d710edb98b18505fcbe079c07c9428daa018f29439b54` |
| OpenAI | [Inspected file](https://raw.githubusercontent.com/openai/codex-security/main/plugins/codex-security/skills/fix-finding/SKILL.md); [Apache-2.0](https://raw.githubusercontent.com/openai/codex-security/main/LICENSE) | Trace the shared cause and every caller; preserve legitimate behavior instead of adopting vendor workbench stages. | `5182ad87bd342a7785bb6ef1800abfe59af5d98662522f6fa43c53f4d7c5cf3e` |
| Kedibin-Win | [Inspected file](https://raw.githubusercontent.com/Kedibin-Win/pentest-skill/main/SKILL.md); [MIT](https://raw.githubusercontent.com/Kedibin-Win/pentest-skill/main/LICENSE) | Use an explicit scope and minimal proof; reject false positives and host-specific workflow assumptions. | `e0753a0ec97c2dccc269429bd389c39eab76cf430938a4ca2c9105a87e094890` |
| zhaoxuya520 | [Inspected file](https://raw.githubusercontent.com/zhaoxuya520/reverse-skill/main/skills/pentest-tools/SKILL.md); [MIT](https://raw.githubusercontent.com/zhaoxuya520/reverse-skill/main/LICENSE) | Verify candidate findings against the scope contract; do not adopt automatic tool bootstrap or tool catalogs as evidence. | `5bab5fe16593998862c763959ae6643e1bf81ed8d75bfa924f42c2aabd1170c9` |
| Tencent | [Inspected file](https://raw.githubusercontent.com/Tencent/AI-Infra-Guard/main/skill-scan/skill_scan/prompt/agents/vuln_review.md); [Apache-2.0](https://raw.githubusercontent.com/Tencent/AI-Infra-Guard/main/LICENSE) | Reconstruct findings from source and seek counterevidence; do not adopt the scanner or its infrastructure. | `0e9ea0509b431edc9ca33a6c701f7b87a90097e21c0c06fbab31b133e57a285f` |
| OWASP authorization | [Inspected file](https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x17-V8-Authorization.md); [CC BY-SA 4.0](https://raw.githubusercontent.com/OWASP/ASVS/master/LICENSE.md) | Enforce actor-bound authority in the trusted layer; do not claim full ASVS compliance. | `60c188b1703cab2086841d8f1b4adc0ededf66ed38c676a11bb92347646b5330` |
| OWASP encoding | [Inspected file](https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md); [CC BY-SA 4.0](https://raw.githubusercontent.com/OWASP/ASVS/master/LICENSE.md) | Use parameter binding and context-specific interpretation; copied payload catalogs are not a verification method. | `8c0e36a42c3cbf711e2579eb68e1fea8090f52301cac7c400d7c392207b24ee7` |
| Vulhub | [Inspected file](https://raw.githubusercontent.com/vulhub/vulhub/master/vite/CVE-2026-39363/README.zh-cn.md); [MIT](https://raw.githubusercontent.com/vulhub/vulhub/master/LICENSE) | Check alternate protocol paths; the HTTP guard did not cover the WebSocket path. No exploit or container was executed. | `4f5d1c75ec2abd35ef0d5a41c226738fe316c8ba01e225b7716d524920ee467a` |

Additional inspected material includes Trail of Bits' [property-based testing skill](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/property-based-testing/skills/property-based-testing/SKILL.md), under the same CC BY-SA 4.0 license. Its retrieved-text SHA-256 is `9448cacb65c6237a7c22dc59602667177ecae405524079ae9ff92240590b995a`. Independent properties informed the attack, variant and legitimate-control checks; its runner infrastructure was not adopted.

The Chinese repositories' root READMEs were also inspected. Vulhub's [compose fixture](https://raw.githubusercontent.com/vulhub/vulhub/master/vite/CVE-2026-39363/docker-compose.yml) and [environment index](https://raw.githubusercontent.com/vulhub/vulhub/master/environments.toml) were checked against its example. The linked [Vite advisory](https://github.com/vitejs/vite/security/advisories/GHSA-p9ff-h696-f583) independently identifies the missing WebSocket enforcement path and its exposure conditions. A published container port is not evidence of isolation.

Current-risk context came from [CISA's KEV catalog](https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.json), [Mandiant's MNDT-2026-0042 disclosure](https://raw.githubusercontent.com/mandiant/Vulnerability-Disclosures/master/2026/MNDT-2026-0042.md) and [Barracuda's primary advisory](https://trust.barracuda.com/security/pre-authentication-authorization-bypass-command-injection). The inspected catalog was version `2026.11.13`, containing 1,781 vulnerability entries, not attack counts. Barracuda's November 9 update reported limited observed exploitation and required a reachable administrative interface. These sources motivate checking alternate enforcement paths, not claims about a global increase in attacks.

These citations are research attribution, not a ranking or certification. Repository independence and fork ancestry were not established; translations, mirrors and repeated advisories are not independent corroboration. Unavailable pages were excluded. Research does not grant target authorization, and green local fixtures do not establish comprehensive cybersecurity coverage.
