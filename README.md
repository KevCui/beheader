# headershrink

> Find out the minimum required headers of a cURL request

## Why I need it?

Not all the HTTP request headers impact the HTTP response: some are mandatory, some are redundant. If you want to get rid of unnecessary headers, this script will do the job and make cURL request look nice & clean.

## Usage

```
usage: headershrink.py curl [URL] [-X REQUEST] [-H HEADER] [-d DATA]

optional arguments:
  -h, --help            show this help message and exit
  -X REQUEST, --request REQUEST
                        Request method
  -H HEADER, --header HEADER
                        Request headers
  -d DATA, --data DATA, --data-raw DATA
                        Request data
```

### Example

- GET request:

```bash
$ ./headershrink.py curl 'https://duckduckgo.com/js/spice/dictionary/hyphenation/test' \
  -H 'authority: duckduckgo.com' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'user-agent: AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://duckduckgo.com/' \
  -H 'accept-language: en-US,en;q=0.9' \
  --compressed

[INFO] Checking combination 0
[INFO] >> Header(s): {}
[INFO] Header is not needed ¯\_(ツ)_/¯
curl -X GET "https://duckduckgo.com/js/spice/dictionary/hyphenation/test" --compressed
```

- POST request

```bash
$ ./headershrink.py curl 'https://ssc.33across.com/api/v1/hb' \
  -H 'authority: ssc.33across.com' \
  -H 'user-agent: AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' \
  -H 'content-type: text/plain' \
  -H 'accept: */*' \
  -H 'origin: https://www.w3schools.com' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.w3schools.com/tags/ref_httpmethods.asp' \
  -H 'accept-language: en-US,en;q=0.9' \
  --data-binary '{"imp":[{"banner":{"format":[{"w":728,"h":90},{"w":970,"h":90}],"ext":{"ttx":{"viewability":{"amount":100}}}},"ext":{"ttx":{"prod":"siab"}}}],"site":{"id":"beuMI6FAar6QjTaKlId8sQ","page":"https://www.w3schools.com/tags/ref_httpmethods.asp"},"id":"72a047f5071ac","user":{"ext":{"consent":"CO7ZHtzO7ZHtzDlAkAENA7CsAP_AAH_AACiQG2Nf_X_fb3_j-_599_t0eY1f9_7_v20zjheds-8Nyd_X_L8X_2M7vB36pr4KuR4ku3bBAQdtHOncTQmR6IlVqTLsbk2Mr7NKJ7PEmlsbe2dYGH9_n9XT_ZKZ79_v___7________77______3_v7wNsAJMNS-AiyEsYCSaNKoUQIQriQ6AEAFFCMLRNYQErgp2VwEfoIGACA1ARgRAgxBRiyCAAAAAJKIgBADwQCIAiAQAAgBUgIQAEaAILACQMAgAFANCwAiiCECQgyOCo5RAgIkWignkjAEoudjCCEEAAA"}},"regs":{"ext":{"gdpr":1,"us_privacy":"1---"}},"ext":{"ttx":{"prebidStartedAt":1602882648477,"caller":[{"name":"prebidjs","version":"3.27.1"}]}},"source":{"ext":{"schain":{"ver":"1.0","complete":1,"nodes":[{"asi":"snigelweb.com","sid":"7088","domain":"w3schools.com","hp":1}]}}}}' \
  --compressed

[INFO] Checking combination 0
[INFO] >> Header(s): {}
[INFO] Checking combination 1
[INFO] >> Header(s): {'authority': 'ssc.33across.com'}
[INFO] >> Header(s): {'user-agent': 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
[INFO] >> Header(s): {'content-type': 'text/plain'}
[INFO] Found min. combination: content-type
curl -X POST "https://ssc.33across.com/api/v1/hb" -H 'content-type: text/plain' --data '{"imp":[{"banner":{"format":[{"w":728,"h":90},{"w":970,"h":90}],"ext":{"ttx":{"viewability":{"amount":100}}}},"ext":{"ttx":{"prod":"siab"}}}],"site":{"id":"beuMI6FAar6QjTaKlId8sQ","page":"https://www.w3schools.com/tags/ref_httpmethods.asp"},"id":"72a047f5071ac","user":{"ext":{"consent":"CO7ZHtzO7ZHtzDlAkAENA7CsAP_AAH_AACiQG2Nf_X_fb3_j-_599_t0eY1f9_7_v20zjheds-8Nyd_X_L8X_2M7vB36pr4KuR4ku3bBAQdtHOncTQmR6IlVqTLsbk2Mr7NKJ7PEmlsbe2dYGH9_n9XT_ZKZ79_v___7________77______3_v7wNsAJMNS-AiyEsYCSaNKoUQIQriQ6AEAFFCMLRNYQErgp2VwEfoIGACA1ARgRAgxBRiyCAAAAAJKIgBADwQCIAiAQAAgBUgIQAEaAILACQMAgAFANCwAiiCECQgyOCo5RAgIkWignkjAEoudjCCEEAAA"}},"regs":{"ext":{"gdpr":1,"us_privacy":"1---"}},"ext":{"ttx":{"prebidStartedAt":1602882648477,"caller":[{"name":"prebidjs","version":"3.27.1"}]}},"source":{"ext":{"schain":{"ver":"1.0","complete":1,"nodes":[{"asi":"snigelweb.com","sid":"7088","domain":"w3schools.com","hp":1}]}}}}' --compressed
```

The result of cURL command line is saved in `<unixtime>.curl`.

---

<a href="https://www.buymeacoffee.com/kevcui" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-orange.png" alt="Buy Me A Coffee" height="60px" width="217px"></a>