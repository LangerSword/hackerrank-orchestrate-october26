# Flip dump v2 — 57 entries

## case_124 — support_retained

- status: INCOMPLETE; requested_at: 2026-08-05T10:00:00+00:00; audit_at: 2026-08-17T10:00:00+00:00
- subject: user_122; emails=['holm.linnea@gmail.com']; phones=['46702188482']; hashes=['ca9b38f9286e8ce2cf57034327846ddd0263e0d5a19498b64d726fa46681dda9']
- tied by: [('user_122', 'user_id', 'exact')]
- deciding fact observed_at: 2026-08-17T10:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260819.json
- finding: REPORT_EXPOSED_PII support_platform support_9126 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```json
{
 "resource_id": "support_9126",
 "ticket_id": "CS-8126",
 "subject_reference": "user_122",
 "channel": "email",
 "message_text": "Please send the delivery update to holm.linnea@gmail.com. The affected order includes: Cotton bedsheet set."
}
```

why: the engine reads `PRESENT` on support_9126; disabling this rule removes the only finding.

## case_160 — support_retained

- status: INCOMPLETE; requested_at: 2026-07-05T07:00:00+00:00; audit_at: 2026-08-02T07:00:00+00:00
- subject: user_158; emails=['navarro.sofia82@gmail.com', 'navarro.sofia@gmail.com']; phones=['34659731854']; hashes=['6377857190a2ae7153918237cc9e21c9e385f70c1111df038a460cd06f9dd27c', 'd07d11273079b2c23f1126fce576af3b3c284fd4a82f867062117e1823454caa']
- tied by: [('user_158', 'user_id', 'exact')]
- deciding fact observed_at: 2026-08-02T07:00:00+00:00; file: evidence/databases/customer_data_read_replica_20260802.sql
- finding: REPORT_EXPOSED_PII support_platform support_4148 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```sql
CREATE TABLE customer_data_primary (
            resource_id TEXT PRIMARY KEY,
            origin_system TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            record_json TEXT NOT NULL CHECK (json_valid(record_json)),
            updated_at TEXT NOT NULL
        )
-- row --
{
 "resource_id": "support_4148",
 "origin_system": "support_platform",
 "collection_name": "support_conversations",
 "record_json": "{\"resource_id\":\"support_4148\",\"ticket_id\":\"CS-8148\",\"subject_reference\":\"user_158\",\"channel\":\"email\",\"message_text\":\"Please send the delivery update to navarro.sofia82@gmail.com. The affected order includes: Travel backpack.\"}",
 "updated_at": "2026-08-02T07:00:00Z"
}
```

why: the engine reads `PRESENT` on support_4148; disabling this rule removes the only finding.

## case_232 — support_retained

- status: INCOMPLETE; requested_at: 2026-06-08T07:00:00+00:00; audit_at: 2026-06-28T07:00:00+00:00
- subject: user_230; emails=['gyasi.efua@gmail.com']; phones=['233246430035', '233249837846']; hashes=['46ebec8a58e51d5dcfa8229221a6af5e9052e10a9e076165367c7d4d1d281788']
- tied by: [('user_230', 'user_id', 'exact')]
- deciding fact observed_at: 2026-06-28T07:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260630.json
- finding: REPORT_EXPOSED_PII support_platform support_9862 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```json
{
 "resource_id": "support_9862",
 "ticket_id": "CS-8862",
 "subject_reference": "user_230",
 "channel": "email",
 "message_text": "Please send the delivery update to gyasi.efua@gmail.com. The affected order includes: Cotton bedsheet set."
}
```

why: the engine reads `PRESENT` on support_9862; disabling this rule removes the only finding.

## case_280 — support_retained

- status: INCOMPLETE; requested_at: 2026-05-06T09:00:00+00:00; audit_at: 2026-06-03T09:00:00+00:00
- subject: user_278; emails=['nielsen.ingrid@gmail.com']; phones=['46702931240']; hashes=['fc0c3c89882906ef7b01f4eca6d7161442dd633fbc0d9f7a84243c0dd1efbe82']
- tied by: [('user_278', 'user_id', 'exact')]
- deciding fact observed_at: 2026-06-03T09:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260605.json
- finding: REPORT_EXPOSED_PII support_platform support_7073 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```json
{
 "resource_id": "support_7073",
 "ticket_id": "CS-6073",
 "subject_reference": "user_278",
 "channel": "email",
 "message_text": "Please send the delivery update to nielsen.ingrid@gmail.com. The affected order includes: Running shoes."
}
```

why: the engine reads `PRESENT` on support_7073; disabling this rule removes the only finding.

## case_282 — support_retained

- status: INCOMPLETE; requested_at: 2026-05-24T09:00:00+00:00; audit_at: 2026-06-03T09:00:00+00:00
- subject: user_280; emails=['ohamdan2049@gmail.com']; phones=['971524547774', '971529730092']; hashes=['a568fad099489a0a75fb70a216fe45fa1b25eb8a114b349cf818db6397229906']
- tied by: [('user_280', 'user_id', 'exact')]
- deciding fact observed_at: 2026-06-03T09:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260605.json
- finding: REPORT_EXPOSED_PII support_platform support_8370 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```json
{
 "resource_id": "support_8370",
 "ticket_id": "CS-7370",
 "subject_reference": "user_280",
 "channel": "email",
 "message_text": "Please send the delivery update to ohamdan2049@gmail.com. The affected order includes: Ceramic coffee set."
}
```

why: the engine reads `PRESENT` on support_8370; disabling this rule removes the only finding.

## case_342 — support_retained

- status: INCOMPLETE; requested_at: 2026-04-24T10:00:00+00:00; audit_at: 2026-05-04T10:00:00+00:00
- subject: user_340; emails=['cnavarro7189@gmail.com']; phones=['34617660989', '34755377597']; hashes=['85a211bec208d769b481ab64c7a0fc3a15dea56ac8699bffd3dadbc642e627c9']
- tied by: [('cnavarro7189@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-05-04T10:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260511.json
- finding: REPORT_EXPOSED_PII support_platform support_3399 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```json
{
 "recorded_at": "2026-05-04T10:00:00Z",
 "system": "support_platform",
 "resource_id": "support_3399",
 "record_type": "SUPPORT_MESSAGE",
 "result": "IDENTIFIABLE",
 "lookup_value": "cnavarro7189@gmail.com"
}
```

why: the engine reads `PRESENT` on support_3399; disabling this rule removes the only finding.

## case_460 — support_retained

- status: INCOMPLETE; requested_at: 2026-02-05T12:00:00+00:00; audit_at: 2026-03-05T12:00:00+00:00
- subject: user_458; emails=['parker.grace@gmail.com']; phones=['447700900458']; hashes=['2a281960e606f04db81aa827a2400f2c9eb6ed91248d7031b586a02928272b7c']
- tied by: [('user_458', 'user_id', 'exact')]
- deciding fact observed_at: 2026-03-05T12:00:00+00:00; file: evidence/databases/customer_data_reporting_replica_20260305.sql
- finding: REPORT_EXPOSED_PII support_platform support_4146 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```sql
CREATE TABLE customer_data_primary (
            resource_id TEXT PRIMARY KEY,
            origin_system TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            record_json TEXT NOT NULL CHECK (json_valid(record_json)),
            updated_at TEXT NOT NULL
        )
-- row --
{
 "resource_id": "support_4146",
 "origin_system": "support_platform",
 "collection_name": "support_conversations",
 "record_json": "{\"resource_id\":\"support_4146\",\"ticket_id\":\"CS-8146\",\"subject_reference\":\"user_458\",\"channel\":\"email\",\"message_text\":\"Please send the delivery update to parker.grace@gmail.com. The affected order includes: Ceramic coffee set.\"}",
 "updated_at": "2026-03-05T12:00:00Z"
}
```

why: the engine reads `PRESENT` on support_4146; disabling this rule removes the only finding.

## case_484 — support_retained

- status: INCOMPLETE; requested_at: 2026-02-06T09:00:00+00:00; audit_at: 2026-02-18T09:00:00+00:00
- subject: user_482; emails=['rao.neel@gmail.com']; phones=['919377993032']; hashes=['e04a28ea51afdeda586b65bc2ec7bd17f775a002e0d817a7f90d96aa7a96bf1c']
- tied by: [('rao.neel@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-02-18T09:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260223.json
- finding: REPORT_EXPOSED_PII support_platform support_7973 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```json
{
 "recorded_at": "2026-02-18T09:00:00Z",
 "system": "support_platform",
 "resource_id": "support_7973",
 "record_type": "SUPPORT_MESSAGE",
 "result": "IDENTIFIABLE",
 "lookup_value": "rao.neel@gmail.com"
}
```

why: the engine reads `PRESENT` on support_7973; disabling this rule removes the only finding.

## case_508 — support_retained

- status: INCOMPLETE; requested_at: 2026-01-23T07:00:00+00:00; audit_at: 2026-02-08T07:00:00+00:00
- subject: user_506; emails=['kang.junseo@gmail.com']; phones=['821011117523']; hashes=['e8e87b410e165e673548cb8a164da97e2752941764ebd0411ee71b0f0d4ada62']
- tied by: [('user_506', 'user_id', 'exact')]
- deciding fact observed_at: 2026-02-08T07:00:00+00:00; file: evidence/databases/customer_data_reporting_replica_20260208.sql
- finding: REPORT_EXPOSED_PII support_platform support_2691 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```sql
CREATE TABLE customer_data_primary (
            resource_id TEXT PRIMARY KEY,
            origin_system TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            record_json TEXT NOT NULL CHECK (json_valid(record_json)),
            updated_at TEXT NOT NULL
        )
-- row --
{
 "resource_id": "support_2691",
 "origin_system": "support_platform",
 "collection_name": "support_conversations",
 "record_json": "{\"resource_id\":\"support_2691\",\"ticket_id\":\"CS-6691\",\"subject_reference\":\"user_506\",\"channel\":\"email\",\"message_text\":\"Please send the delivery update to kang.junseo@gmail.com. The affected order includes: Mechanical keyboard.\"}",
 "updated_at": "2026-02-08T07:00:00Z"
}
```

why: the engine reads `PRESENT` on support_2691; disabling this rule removes the only finding.

## case_520 — support_retained

- status: INCOMPLETE; requested_at: 2026-01-06T06:00:00+00:00; audit_at: 2026-02-03T06:00:00+00:00
- subject: user_518; emails=['suzuki.daichi90@gmail.com', 'suzuki.daichi@gmail.com']; phones=['819027733305']; hashes=['437adbd76c9c1cc0bcec823a9e44e48c817f64c43488cf740a069ed98fc1eb48', 'ed01c805bb0eebb48ea9a195a3816c768e5aa94a8e650ffe4469b34bee746d60']
- tied by: [('suzuki.daichi90@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-02-03T05:58:08+00:00; file: evidence/logs/operations_stream_me_central_20260203.log
- finding: REPORT_EXPOSED_PII support_platform support_9251 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```
2026-02-03T05:58:08Z | WARN | support_platform | tr-6400539 | message_pii_scan | instance="support-7" pod="support-44e5" region="eu-west-1" resource_id="support_9251" matched_value="suzuki.daichi90@gmail.com" detector="direct_identifier"
```

why: the engine reads `PRESENT` on support_9251; disabling this rule removes the only finding.

## case_522 — support_retained

- status: INCOMPLETE; requested_at: 2026-01-24T06:00:00+00:00; audit_at: 2026-02-03T06:00:00+00:00
- subject: user_520; emails=['csantos2609@gmail.com']; phones=['5521938423428', '5541996242948']; hashes=['266ca9201e0d49cd2e70e42bcb472f2342c4adbb446304c0fba4fc707e4a4ecd']
- tied by: [('csantos2609@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-02-03T05:57:48+00:00; file: evidence/logs/operations_stream_me_central_20260203.log
- finding: REPORT_EXPOSED_PII support_platform support_8538 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```
2026-02-03T05:57:48Z | WARN | support_platform | tr-1382666 | message_pii_scan | instance="support-7" pod="support-e036" region="us-east-2" resource_id="support_8538" matched_value="csantos2609@gmail.com" detector="direct_identifier"
```

why: the engine reads `PRESENT` on support_8538; disabling this rule removes the only finding.

## case_53 — support_retained

- status: INCOMPLETE; requested_at: 2026-05-22T04:00:00+00:00; audit_at: 2026-05-25T09:00:00+00:00
- subject: user_22; emails=['kagyeman8947@fastmail.com']; phones=['233247524312']; hashes=['2223309bb52ac82b56ee55504acf27956503f83a61a81703bd9f24a5f5a292c6']
- tied by: [('kagyeman8947@fastmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-05-24T07:00:00+00:00; file: evidence/images/support_ticket_console_20260524.png
- finding: REPORT_EXPOSED_PII support_platform support_1034 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

digest entry:
```json
[
 {
  "system": "support_platform",
  "record_type": "SUPPORT_MESSAGE",
  "resource_id": "support_1034",
  "state": "IDENTIFIABLE",
  "identifiers": [
   "kagyeman8947@fastmail.com"
  ],
  "user_ref": "user_22",
  "observed_at": "2026-05-24T07:00:00Z"
 }
]
```
OCR text (first 4000 chars):
```
FILE_ID: evidence_28
PATH: evidence/images/support_ticket_console_20260524.png
ORIGIN: support_platform
CAPTURED_AT: 2026-05-24T07:00:00Z
---
Northstar Shop Helpline Console © Search tickets, customers, orders.. Production Help (HC
Inbo> . ” ~
Q) b CS-5034 - Where is my delivery? iAo A | Bpot
[ My tickets support_1034 - Kofi Agyeman - Normal priority
[[] Assigned to me
[J Mentions Customer Email Assigned Tags
Kofi Agyeman kagyeman8947@fastmail.com Maya Chen Delivery - Tracking - Order update
[J Knowledge base Conversation Updated moments ago - 4 records Order ORD-20265034
(] Report ime sender lessage
[ Reports T Send. Messag Product Running shoes,
2] 0913 Northstar Bot We received your message and are checking the order details. Carrler Swintship
Activity

```

why: the engine reads `PRESENT` on support_1034; disabling this rule removes the only finding.

## case_66 — support_retained

- status: INCOMPLETE; requested_at: 2026-09-02T09:00:00+00:00; audit_at: 2026-09-16T09:00:00+00:00
- subject: user_64; emails=['hcho154598@gmail.com', 'hcho1545@gmail.com']; phones=['821073249252']; hashes=['4dd108cb17bcad910ff2b0a6c96e72635a978fd616de5c1cdf039ace8b8bdf68', '534c275f5c4ba84f1347e7a6fce50e184fbf54a0f5f98fa3d61001803b543a33']
- tied by: [('hcho154598@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-09-16T08:51:30+00:00; file: evidence/logs/structured_service_events_eu_west_20260918.log
- finding: REPORT_EXPOSED_PII support_platform support_4249 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```
2026-09-16T08:51:30Z {"severity":"WARN","logger":"support_platform","service":"support_platform","instance":"support-4","pod":"support-6cd2","region":"us-east-2","trace_id":"tr-5428224","resource_id":"support_4249","event":"message_pii_scan","matched_value":"hcho154598@gmail.com","detector":"direct_identifier"}
```

why: the engine reads `PRESENT` on support_4249; disabling this rule removes the only finding.

## case_76 — support_retained

- status: INCOMPLETE; requested_at: 2026-08-18T08:00:00+00:00; audit_at: 2026-09-11T08:00:00+00:00
- subject: user_74; emails=['osei.ama@gmail.com']; phones=['233249010733']; hashes=['c68d117e3474e6a2e8818d6cc1ad40db9ac0f6b8020e224a5fe4829e1343612b']
- tied by: [('user_74', 'user_id', 'exact')]
- deciding fact observed_at: 2026-09-11T08:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260913.json
- finding: REPORT_EXPOSED_PII support_platform support_9746 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```json
{
 "resource_id": "support_9746",
 "ticket_id": "CS-8746",
 "subject_reference": "user_74",
 "channel": "email",
 "message_text": "Please send the delivery update to osei.ama@gmail.com. The affected order includes: Ceramic coffee set."
}
```

why: the engine reads `PRESENT` on support_9746; disabling this rule removes the only finding.

## case_88 — support_retained

- status: INCOMPLETE; requested_at: 2026-08-21T07:00:00+00:00; audit_at: 2026-09-06T07:00:00+00:00
- subject: user_86; emails=['oladipo.ikenna98@gmail.com', 'oladipo.ikenna@gmail.com']; phones=['2348038829733']; hashes=['30de6a7d8a938fb60879958dfcb9010864629953230c6b7a6eb9a1ceb8161fd3', 'fa0b727dafea31a06ef3cab04b8160bdba38071adf9b10fcf4b7f4dcd9b44ce1']
- tied by: [('oladipo.ikenna98@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-09-06T07:00:00+00:00; file: evidence/logs/search_index_diagnostic_20260906.log
- finding: REPORT_EXPOSED_PII support_platform support_2967 state=PRESENT
- rule under test: policy: SUPPORT_MESSAGE is REDACT, not RETAIN

```
2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=35 system="support_platform" resource_id="support_2967" record_type="SUPPORT_MESSAGE" result="IDENTIFIABLE" subject_reference="oladipo.ikenna98@gmail.com"
```

why: the engine reads `PRESENT` on support_2967; disabling this rule removes the only finding.

## case_161 — analytics_retained

- status: INCOMPLETE; requested_at: 2026-07-04T07:00:00+00:00; audit_at: 2026-08-02T07:00:00+00:00
- subject: user_159; emails=['noah-sullivan83@gmail.com', 'noah-sullivan@gmail.com']; phones=['16465550159']; hashes=['1763309b894355fa93694fc0cbfdba4cf4c72f373f9ca7471ec9f6e354138475', '9f380df55818348191a8a8e8b2da5baeedd4ca140e987939972eee4154cab492']
- tied by: [('9f380df55818348191a8a8e8b2da5baeedd4ca140e987939972eee4154cab492', 'hash', 'exact'), ('p:16465550159', 'phone', 'exact'), ('user_159', 'user_id', 'exact'), ('noah-sullivan@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-08-02T07:00:00+00:00; file: evidence/databases/customer_data_read_replica_20260802.sql
- finding: REPORT_EXPOSED_PII analytics_platform analytics_2008 state=PRESENT
- rule under test: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN

```sql
CREATE TABLE customer_data_primary (
            resource_id TEXT PRIMARY KEY,
            origin_system TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            record_json TEXT NOT NULL CHECK (json_valid(record_json)),
            updated_at TEXT NOT NULL
        )
-- row --
{
 "resource_id": "analytics_2008",
 "origin_system": "analytics_platform",
 "collection_name": "customer_analytics_reports",
 "record_json": "{\"resource_id\":\"analytics_2008\",\"user_id\":\"user_159\",\"email\":\"noah-sullivan@gmail.com\",\"phone\":\"+1 (646) 555-0159\",\"email_hash\":\"9f380df55818348191a8a8e8b2da5baeedd4ca140e987939972eee4154cab492\",\"reporting_window\":\"last_90_days\",\"metrics\":{\"sessions_30d\":12,\"products_viewed_30d\":28,\"orders_completed_90d\":3,\"revenue_90d_usd\":237.57},\"recent_activity\":[{\"event\":\"product_viewed\",\"product\":\"Noise-cancelling headphones\"},{\"event\":\"added_to_cart\",\"product\":\"Noise-cancelling headphones\"},{\"event\":\"purchase_completed\",\"product\":\"Noise-cancelling headphones\",\"quantity\":1}]}",
 "updated_at": "2026-08-02T07:00:00Z"
}
```

why: the engine reads `PRESENT` on analytics_2008; disabling this rule removes the only finding.

## case_245 — analytics_retained

- status: INCOMPLETE; requested_at: 2026-06-05T12:00:00+00:00; audit_at: 2026-06-18T12:00:00+00:00
- subject: user_243; emails=['nana-appiah@gmail.com']; phones=['233244460431']; hashes=['907194c8e56b7c083d7eec62f2ea2b0d1ee0ce99b14acaaf4d547511b4f1515d']
- tied by: [('nana-appiah@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-06-18T11:44:03+00:00; file: evidence/databases/customer_data_inventory_20260618.sql
- finding: REPORT_EXPOSED_PII analytics_platform analytics_4010 state=PRESENT
- rule under test: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN

```sql
CREATE TABLE customer_analytics_profiles (resource_id TEXT PRIMARY KEY, customer_reference TEXT, email TEXT, phone TEXT, email_hash TEXT, audience_cohort TEXT NOT NULL, updated_at TEXT NOT NULL)
-- row --
{
 "resource_id": "analytics_4010",
 "customer_reference": null,
 "email": "nana-appiah@gmail.com",
 "phone": null,
 "email_hash": null,
 "audience_cohort": "mobile_browser",
 "updated_at": "2026-06-18T11:36:09Z"
}
```

why: the engine reads `PRESENT` on analytics_4010; disabling this rule removes the only finding.

## case_293 — analytics_retained

- status: INCOMPLETE; requested_at: 2026-05-03T07:00:00+00:00; audit_at: 2026-05-24T07:00:00+00:00
- subject: user_291; emails=['erik-johansson@gmail.com']; phones=['46702232145']; hashes=['6a1d845c584bbd3ae96fcef0729f77f0723b850d867a226fc62c03eee0f8a26a']
- tied by: [('erik-johansson@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-05-24T06:39:55+00:00; file: evidence/databases/customer_data_inventory_20260524.sql
- finding: REPORT_EXPOSED_PII analytics_platform analytics_5854 state=PRESENT
- rule under test: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN

```sql
CREATE TABLE customer_analytics_profiles (resource_id TEXT PRIMARY KEY, customer_reference TEXT, email TEXT, phone TEXT, email_hash TEXT, audience_cohort TEXT NOT NULL, updated_at TEXT NOT NULL)
-- row --
{
 "resource_id": "analytics_5854",
 "customer_reference": null,
 "email": "erik-johansson@gmail.com",
 "phone": null,
 "email_hash": null,
 "audience_cohort": "returning_customer",
 "updated_at": "2026-05-24T04:03:44Z"
}
```

why: the engine reads `PRESENT` on analytics_5854; disabling this rule removes the only finding.

## case_377 — analytics_retained

- status: INCOMPLETE; requested_at: 2026-03-20T06:00:00+00:00; audit_at: 2026-04-14T06:00:00+00:00
- subject: user_375; emails=['rina-sato@gmail.com']; phones=['819040061113', '819065425325']; hashes=['10b096b817b742db5fe102d212f403b668460d13b6830ec15a40e9cac662989a']
- tied by: [('rina-sato@gmail.com', 'email', 'exact'), ('user_375', 'user_id', 'exact'), ('10b096b817b742db5fe102d212f403b668460d13b6830ec15a40e9cac662989a', 'hash', 'exact'), ('p:819065425325', 'phone', 'exact')]
- deciding fact observed_at: 2026-04-14T06:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260416.json
- finding: REPORT_EXPOSED_PII analytics_platform analytics_3651 state=PRESENT
- rule under test: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN

```json
{
 "resource_id": "analytics_3651",
 "user_id": "user_375",
 "email": "rina-sato@gmail.com",
 "phone": "+81 90 6542 5325",
 "email_hash": "10b096b817b742db5fe102d212f403b668460d13b6830ec15a40e9cac662989a",
 "reporting_window": "last_90_days",
 "metrics": {
  "sessions_30d": 17,
  "products_viewed_30d": 28,
  "orders_completed_90d": 1,
  "revenue_90d_usd": 37.38
 },
 "recent_activity": [
  {
   "event": "product_viewed",
   "product": "Mechanical keyboard"
  },
  {
   "event": "purchase_completed",
   "product": "Mechanical keyboard",
   "quantity": 2
  }
 ]
}
```

why: the engine reads `PRESENT` on analytics_3651; disabling this rule removes the only finding.

## case_401 — analytics_retained

- status: INCOMPLETE; requested_at: 2026-03-06T11:00:00+00:00; audit_at: 2026-04-04T11:00:00+00:00
- subject: user_399; emails=['kwame-asante@gmail.com']; phones=['233243830646']; hashes=['a7e46c52df6c4eebaff410d77dd66813153bac69be158211fb7e1a830f9a59b7']
- tied by: [('kwame-asante@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-04-04T10:04:19+00:00; file: evidence/databases/customer_data_inventory_20260404.sql
- finding: REPORT_EXPOSED_PII analytics_platform analytics_6872 state=PRESENT
- rule under test: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN

```sql
CREATE TABLE customer_analytics_profiles (resource_id TEXT PRIMARY KEY, customer_reference TEXT, email TEXT, phone TEXT, email_hash TEXT, audience_cohort TEXT NOT NULL, updated_at TEXT NOT NULL)
-- row --
{
 "resource_id": "analytics_6872",
 "customer_reference": null,
 "email": "kwame-asante@gmail.com",
 "phone": null,
 "email_hash": null,
 "audience_cohort": "mobile_browser",
 "updated_at": "2026-04-04T09:55:56Z"
}
```

why: the engine reads `PRESENT` on analytics_6872; disabling this rule removes the only finding.

## case_437 — analytics_retained

- status: INCOMPLETE; requested_at: 2026-02-18T07:00:00+00:00; audit_at: 2026-03-15T07:00:00+00:00
- subject: user_435; emails=['zofia-novak@gmail.com']; phones=['48530927757', '48765328958']; hashes=['05388aad688ef79b8b1ca9c7c156d1cbda09eea0d55455a2790557257d14a585']
- tied by: [('zofia-novak@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-03-15T07:00:00+00:00; file: evidence/logs/notification_delivery_20260315.log
- finding: REPORT_EXPOSED_PII analytics_platform analytics_6172 state=PRESENT
- rule under test: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN

```
2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=12 system="analytics_platform" resource_id="analytics_6172" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="zofia-novak@gmail.com"
```

why: the engine reads `PRESENT` on analytics_6172; disabling this rule removes the only finding.

## case_50 — analytics_retained

- status: INCOMPLETE; requested_at: 2026-07-11T07:00:00+00:00; audit_at: 2026-07-14T12:00:00+00:00
- subject: user_20; emails=['darwish.omar@icloud.com']; phones=['971524526308', '971528588894']; hashes=['09f05b9fb59a2493e9349bbfeac4ab5288a534689c8ecbe44bcc106f5ede50a7']
- tied by: [('darwish.omar@icloud.com', 'email', 'exact')]
- deciding fact observed_at: 2026-07-13T10:00:00+00:00; file: evidence/images/analytics_profile_view_20260713.png
- finding: REPORT_EXPOSED_PII analytics_platform analytics_7438 state=PRESENT
- rule under test: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN

digest entry:
```json
[
 {
  "system": "analytics_platform",
  "record_type": "ANALYTICS_PROFILE",
  "resource_id": "analytics_7438",
  "state": "IDENTIFIABLE",
  "identifiers": [
   "darwish.omar@icloud.com"
  ],
  "user_ref": "user_20",
  "observed_at": "2026-07-13T10:00:00Z"
 }
]
```
OCR text (first 4000 chars):
```
FILE_ID: evidence_19
PATH: evidence/images/analytics_profile_view_20260713.png
ORIGIN: analytics_platform
CAPTURED_AT: 2026-07-13T10:00:00Z
---
Northstar Shop Pulse Analytics p Search users, products, orders or events... Production Help (PA
o 5
U Omar Darwish Last0 days Fiter | Expont
i) o user_20 - analytics_7438 - darwish.omar@icloud.com
‘7‘ Event timeline Sessions (12) Orders (2) Products viewed (19)
12 19 2 USD 167.42 67%/33% Organic search
[ Journeys Event timeline Uptted moments ago -5 records  Profile attributes
(] Audiences Time Event Product  detail Value Device Market A
0 repors 3 e P— Coramic coffe et Usp aazn s R
2 14:20 Checkout started 2items USD 84.21 Mobile Interast Coffee & dining
Loy 1 suzoza wz20Te
5 e roduct downd Coramic coffe et - ol
Frtann 21 A 2028 o 7
) rae e tocat Coramic coffe et usp e200 wobie
Activity
e roduct downd PR ueo 1860 oeson ey
4 oo
4 som
4 2am

```

why: the engine reads `PRESENT` on analytics_7438; disabling this rule removes the only finding.

## case_128 — flow_never_active

- status: INCOMPLETE; requested_at: 2026-08-01T10:00:00+00:00; audit_at: 2026-08-17T10:00:00+00:00
- subject: user_126; emails=['adwoa.frimpong@outlook.com']; phones=['233244474725']; hashes=['8d1682a4a7aecdae22601d8605461458f9140c66d2a8e581ca5d64331daf5a33']
- tied by: [('adwoa.frimpong@outlook.com', 'email', 'exact')]
- deciding fact observed_at: 2026-08-17T10:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260819.json
- finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_5550 state=ACTIVE
- rule under test: state: enabled=true means an active data flow

```json
{
 "resource_id": "data_flow_5550",
 "connector_name": "customer-events-to-warehouse-7",
 "destination": "customer_analytics_warehouse",
 "subject_selector": "adwoa.frimpong@outlook.com",
 "enabled": true,
 "mode": "continuous_sync"
}
```

why: the engine reads `ACTIVE` on data_flow_5550; disabling this rule removes the only finding.

## case_224 — flow_never_active

- status: INCOMPLETE; requested_at: 2026-06-16T07:00:00+00:00; audit_at: 2026-06-28T07:00:00+00:00
- subject: user_222; emails=['neel.singh@outlook.com']; phones=['919865010962']; hashes=['d7d75b201f9e0609ee1ea10dc645219c4a4ea933e3b2417c9fcedea3eb14db1d']
- tied by: [('neel.singh@outlook.com', 'email', 'exact')]
- deciding fact observed_at: 2026-06-28T07:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260630.json
- finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_1140 state=ACTIVE
- rule under test: state: enabled=true means an active data flow

```json
{
 "resource_id": "data_flow_1140",
 "connector_name": "customer-events-to-warehouse-5",
 "destination": "customer_analytics_warehouse",
 "subject_selector": "neel.singh@outlook.com",
 "enabled": true,
 "mode": "continuous_sync"
}
```

why: the engine reads `ACTIVE` on data_flow_1140; disabling this rule removes the only finding.

## case_248 — flow_never_active

- status: INCOMPLETE; requested_at: 2026-06-02T12:00:00+00:00; audit_at: 2026-06-18T12:00:00+00:00
- subject: user_246; emails=['junseo.cho@outlook.com']; phones=['821040902216']; hashes=['1762d8628f7afb8055fc7db560ce9112df2b6404064ef09a8515d259a17b59d5']
- tied by: [('junseo.cho@outlook.com', 'email', 'exact')]
- deciding fact observed_at: 2026-06-18T11:44:03+00:00; file: evidence/databases/customer_data_inventory_20260618.sql
- finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_677 state=ACTIVE
- rule under test: state: enabled=true means an active data flow

```sql
CREATE TABLE connector_subscriptions (resource_id TEXT PRIMARY KEY, customer_reference TEXT, customer_email TEXT, connector_name TEXT NOT NULL, enabled INTEGER NOT NULL CHECK (enabled IN (0,1)), last_delivery_status TEXT NOT NULL, updated_at TEXT NOT NULL)
-- row --
{
 "resource_id": "data_flow_677",
 "customer_reference": null,
 "customer_email": "junseo.cho@outlook.com",
 "connector_name": "analytics_identity_bridge",
 "enabled": 1,
 "last_delivery_status": "delivered",
 "updated_at": "2026-06-18T09:38:20Z"
}
```

why: the engine reads `ACTIVE` on data_flow_677; disabling this rule removes the only finding.

## case_284 — flow_never_active

- status: INCOMPLETE; requested_at: 2026-05-17T08:00:00+00:00; audit_at: 2026-05-29T08:00:00+00:00
- subject: user_282; emails=['kofi.appiah96@outlook.com', 'kofi.appiah@outlook.com']; phones=['233247346692']; hashes=['b5d4717ca30cca101b072414b76ab16055a338dadc63f5eed1abb91029d1bb35', 'db9864e1fdb5cef9f33c25aa018ae9e017c0447dde217c5ee321377ce62dadf8']
- tied by: [('kofi.appiah96@outlook.com', 'email', 'exact')]
- deciding fact observed_at: 2026-05-29T06:46:09+00:00; file: evidence/logs/resource_lookup_trace_20260529_074313.log
- finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_6953 state=ACTIVE
- rule under test: state: enabled=true means an active data flow

```
2026-05-29T06:46:09Z level=INFO service=integration_service trace_id=rb-064609-015 event=connector_config_read_completed resource_id=data_flow_6953 enabled=true last_delivery_status=delivered connector_name=analytics_identity_bridge customer_email=kofi.appiah96@outlook.com customer_reference=null
```

why: the engine reads `ACTIVE` on data_flow_6953; disabling this rule removes the only finding.

## case_350 — flow_never_active

- status: INCOMPLETE; requested_at: 2026-04-11T09:00:00+00:00; audit_at: 2026-04-29T09:00:00+00:00
- subject: user_348; emails=['zanele.tshabalala@gmail.com']; phones=['27722915260']; hashes=['ff438045157577fabcb25bcd921fdf3da273e5b96f09851ed074d717506cca15']
- tied by: [('zanele.tshabalala@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-04-29T05:58:22+00:00; file: evidence/records/service_resource_export_20260429_083222.json
- finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_9775 state=ACTIVE
- rule under test: state: enabled=true means an active data flow

```json
{
 "connector_name": "search_profile_indexer",
 "customer_email": "zanele.tshabalala@gmail.com",
 "customer_reference": null,
 "enabled": true,
 "last_delivery_status": "delivered",
 "observed_at": "2026-04-29T05:58:22Z",
 "resource_id": "data_flow_9775"
}
```

why: the engine reads `ACTIVE` on data_flow_9775; disabling this rule removes the only finding.

## case_38 — flow_never_active

- status: INCOMPLETE; requested_at: 2026-09-05T12:00:00+00:00; audit_at: 2026-10-01T12:00:00+00:00
- subject: user_36; emails=['sipho.mokoena@gmail.com']; phones=['27728882338']; hashes=['2dd0cf113bc5d0ebd0bbde0a990570461d6287fa987f5d24b8df4abb5fa373c7']
- tied by: [('SIPHO.MOKOENA@GMAIL.COM', 'email', 'exact')]
- deciding fact observed_at: 2026-10-01T12:00:00+00:00; file: evidence/records/customer_account_handover_20261001.txt
- finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_7495 state=ACTIVE
- rule under test: state: enabled=true means an active data flow

```
- 2026-10-01T12:00:00Z | integration_service | data_flow_7495 | DATA_FLOW | ACTIVE | SIPHO.MOKOENA@GMAIL.COM
```

why: the engine reads `ACTIVE` on data_flow_7495; disabling this rule removes the only finding.

## case_39 — flow_never_active

- status: INCOMPLETE; requested_at: 2026-08-05T05:00:00+00:00; audit_at: 2026-08-08T10:00:00+00:00
- subject: user_14; emails=['jain.aditi@gmail.com']; phones=['919394758446']; hashes=['ea61073600454d4cb320cd63802b6e63ceb0a1398a7b4dd10049a71729471d00']
- tied by: [('user_14', 'user_id', 'exact')]
- deciding fact observed_at: 2026-08-07T08:00:00+00:00; file: evidence/images/connector_management_console_20260807.png
- finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_1121 state=ACTIVE
- rule under test: state: enabled=true means an active data flow

digest entry:
```json
[
 {
  "system": "integration_service",
  "record_type": "DATA_FLOW",
  "resource_id": "data_flow_1121",
  "state": "ACTIVE",
  "identifiers": [
   "user_14"
  ],
  "user_ref": "user_14",
  "observed_at": "2026-08-07T08:00:00Z"
 },
 {
  "system": "integration_service",
  "record_type": "DATA_FLOW",
  "resource_id": "data_flow_9846",
  "state": "ACTIVE",
  "identifiers": [
   "lucia-torres@gmail.com"
  ],
  "user_ref": "user_15",
  "observed_at": "2026-08-07T08:00:00Z"
 }
]
```
OCR text (first 4000 chars):
```
FILE_ID: evidence_14
PATH: evidence/images/connector_management_console_20260807.png
ORIGIN: integration_admin
CAPTURED_AT: 2026-08-07T08:00:00Z
---
Northstar Shop BridgeOps o Search connectors... Production Help (B
Northstar Shop / BridgeOps / Connections
Ce i .
[ Connections e T oo | [ oon
[ PRODUCTION - u-viest - 07 Aug 2026 08:00 UTC
_ Topology  Throughput  Recent delveries
O Monitoring
O Events Healthy Events | hour Delivery p95 Backiog Destination health
12 413 18s 18 Healthy
[ settings Topology Updated moments ago 4 records data_flow_1121
2| data_flow_9846 customer_analytics_warehouse lucia-torres@gmail.com Continuous 842 07:59:36 Destination customer_analytics_warehouse
Activity

```

why: the engine reads `ACTIVE` on data_flow_1121; disabling this rule removes the only finding.

## case_56 — flow_never_active

- status: INCOMPLETE; requested_at: 2026-08-28T10:00:00+00:00; audit_at: 2026-09-21T10:00:00+00:00
- subject: user_54; emails=['elena.romero88@outlook.com', 'elena.romero@outlook.com']; phones=['34794608812']; hashes=['1e90d6d1006bed607b5e1c2ec515ed496292cb6ec3cf1caf45fc37bddfbc1894', '3a48dce7e5d314f3be962473b0a6e2291ede20ff22a7e1b9a4b7e8a00eadaac3']
- tied by: [('elena.romero88@outlook.com', 'email', 'exact')]
- deciding fact observed_at: 2026-09-21T10:00:00+00:00; file: evidence/databases/customer_data_read_replica_20260921.sql
- finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_373 state=ACTIVE
- rule under test: state: enabled=true means an active data flow

```sql
CREATE TABLE customer_data_primary (
            resource_id TEXT PRIMARY KEY,
            origin_system TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            record_json TEXT NOT NULL CHECK (json_valid(record_json)),
            updated_at TEXT NOT NULL
        )
-- row --
{
 "resource_id": "data_flow_373",
 "origin_system": "integration_service",
 "collection_name": "connector_configurations",
 "record_json": "{\"resource_id\":\"data_flow_373\",\"connector_name\":\"customer-events-to-warehouse-6\",\"destination\":\"customer_analytics_warehouse\",\"subject_selector\":\"elena.romero88@outlook.com\",\"enabled\":true,\"mode\":\"continuous_sync\"}",
 "updated_at": "2026-09-21T10:00:00Z"
}
```

why: the engine reads `ACTIVE` on data_flow_373; disabling this rule removes the only finding.

## case_74 — flow_never_active

- status: INCOMPLETE; requested_at: 2026-08-20T08:00:00+00:00; audit_at: 2026-09-11T08:00:00+00:00
- subject: user_72; emails=['salma.mansour@gmail.com']; phones=['971505799364']; hashes=['f8de08ac2adb79e272590a64382e246528d6547f1a9ce4299c6f0024d5f02f80']
- tied by: [('salma.mansour@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-09-11T08:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260913.json
- finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_4595 state=ACTIVE
- rule under test: state: enabled=true means an active data flow

```json
{
 "resource_id": "data_flow_4595",
 "connector_name": "customer-events-to-warehouse-4",
 "destination": "customer_analytics_warehouse",
 "subject_selector": "salma.mansour@gmail.com",
 "enabled": true,
 "mode": "continuous_sync"
}
```

why: the engine reads `ACTIVE` on data_flow_4595; disabling this rule removes the only finding.

## case_92 — flow_never_active

- status: INCOMPLETE; requested_at: 2026-08-17T07:00:00+00:00; audit_at: 2026-09-06T07:00:00+00:00
- subject: user_90; emails=['doyun.lim@outlook.com']; phones=['821010073954', '821059631958']; hashes=['db6b5ab5a95162a05bcf8b15ce995a76f76ab1aee40d9ccf1dc26ec142a39240']
- tied by: [('doyun.lim@outlook.com', 'email', 'exact')]
- deciding fact observed_at: 2026-09-06T07:00:00+00:00; file: evidence/logs/search_index_diagnostic_20260906.log
- finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_7535 state=ACTIVE
- rule under test: state: enabled=true means an active data flow

```
2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=18 system="integration_service" resource_id="data_flow_7535" record_type="DATA_FLOW" result="ACTIVE" subject_reference="doyun.lim@outlook.com"
```

why: the engine reads `ACTIVE` on data_flow_7535; disabling this rule removes the only finding.

## case_98 — flow_never_active

- status: INCOMPLETE; requested_at: 2026-08-06T06:00:00+00:00; audit_at: 2026-09-01T06:00:00+00:00
- subject: user_96; emails=['maja.eriksen86@gmail.com', 'maja.eriksen@gmail.com']; phones=['46705640930']; hashes=['1d4f8cdcb5b9be2e4f7328c895e3ae296356f1ecc71224d3adec7001c69d373a', 'cc009487604f6f57b71e79b264f5b95432d2dfcf9b0ea02f95116e97a0eb2cc2']
- tied by: [('maja.eriksen86@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-09-01T03:43:18+00:00; file: evidence/records/service_resource_export_20260901_053316.json
- finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_3165 state=ACTIVE
- rule under test: state: enabled=true means an active data flow

```json
{
 "connector_name": "analytics_identity_bridge",
 "customer_email": "maja.eriksen86@gmail.com",
 "customer_reference": null,
 "enabled": true,
 "last_delivery_status": "delivered",
 "observed_at": "2026-09-01T03:43:18Z",
 "resource_id": "data_flow_3165"
}
```

why: the engine reads `ACTIVE` on data_flow_3165; disabling this rule removes the only finding.

## case_123 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-08-06T10:00:00+00:00; audit_at: 2026-08-17T10:00:00+00:00
- subject: user_121; emails=['m.mercier28@gmail.com']; phones=['33636374161']; hashes=['f86e324feaff7a751e9cf6813fd1bcf8b483d698eadded1b1e8d5b6c39a10132']
- tied by: [('m.mercier28@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-08-17T10:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260819.json
- finding: REPORT_RESTORE_RISK backup_service backup_8742 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```json
{
 "resource_id": "backup_8742",
 "archive_path": "s3://customer-backups/weekly/segment-06.tar.zst",
 "subject_reference": "m.mercier28@gmail.com",
 "restore_allowed": true,
 "encryption": "AES-256"
}
```

why: the engine reads `ACTIVE` on backup_8742; disabling this rule removes the only finding.

## case_147 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-07-23T08:00:00+00:00; audit_at: 2026-08-07T08:00:00+00:00
- subject: user_145; emails=['l.fernandez84@gmail.com']; phones=['34691583526', '34776829829']; hashes=['0c02dab8cd949dc8c60f0f502ccfbbf7af8f0c41a6f74bc3acadcc51447bc4e7']
- tied by: [('l.fernandez84@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-08-07T07:35:24+00:00; file: evidence/records/service_resource_export_20260807_074104.json
- finding: REPORT_RESTORE_RISK backup_service backup_4244 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```json
{
 "archive_key": "archive/customer-data/backup_4244.tar.zst",
 "customer_email": "l.fernandez84@gmail.com",
 "customer_reference": null,
 "observed_at": "2026-08-07T07:35:24Z",
 "resource_id": "backup_4244",
 "restore_allowed": true
}
```

why: the engine reads `ACTIVE` on backup_4244; disabling this rule removes the only finding.

## case_159 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-07-06T07:00:00+00:00; audit_at: 2026-08-02T07:00:00+00:00
- subject: user_157; emails=['a.basu1281@gmail.com', 'a.basu12@gmail.com']; phones=['919486359898']; hashes=['d0ae25a96189696f76034675ef540308002b68d1cbd2ca9402609392a9275ec8', 'e5d9db2558b93eaf5fc1731b4d7b1e21bc76e6c82e90633fd8675db1ccd1bc28']
- tied by: [('a.basu1281@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-08-02T07:00:00+00:00; file: evidence/databases/customer_data_read_replica_20260802.sql
- finding: REPORT_RESTORE_RISK backup_service backup_1214 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```sql
CREATE TABLE customer_data_primary (
            resource_id TEXT PRIMARY KEY,
            origin_system TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            record_json TEXT NOT NULL CHECK (json_valid(record_json)),
            updated_at TEXT NOT NULL
        )
-- row --
{
 "resource_id": "backup_1214",
 "origin_system": "backup_service",
 "collection_name": "backup_catalog",
 "record_json": "{\"resource_id\":\"backup_1214\",\"archive_path\":\"s3://customer-backups/weekly/segment-30.tar.zst\",\"subject_reference\":\"a.basu1281@gmail.com\",\"restore_allowed\":true,\"encryption\":\"AES-256\"}",
 "updated_at": "2026-08-02T07:00:00Z"
}
```

why: the engine reads `ACTIVE` on backup_1214; disabling this rule removes the only finding.

## case_171 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-07-09T06:00:00+00:00; audit_at: 2026-07-28T06:00:00+00:00
- subject: user_169; emails=['l.nascimento40@gmail.com']; phones=['5511990673405']; hashes=['93749c4ec1b500268f5fb2dc1e9ce7b1a6fadb8fd70150baab05bd4120ebb009']
- tied by: [('l.nascimento40@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-07-28T05:56:08+00:00; file: evidence/logs/application_trace_ap_northeast_20260730.log
- finding: REPORT_RESTORE_RISK backup_service backup_5520 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```
2026-07-28T05:56:08Z [ERROR] [backup_service] [tr-7064208] restore_candidate_evaluated: instance="backup-2" pod="backup-2a70" region="ap-south-1" resource_id="backup_5520" eligible="true" deletion_block="false"
```

why: the engine reads `ACTIVE` on backup_5520; disabling this rule removes the only finding.

## case_207 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-06-23T09:00:00+00:00; audit_at: 2026-07-08T09:00:00+00:00
- subject: user_205; emails=['k.mthembu24@gmail.com']; phones=['27722104279', '27726145136']; hashes=['b992186fb60aa0a0d51f7cb2c68c3622bac6a3ad62438b168c5564e133d882e9']
- tied by: [('k.mthembu24@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-07-08T09:00:00+00:00; file: evidence/databases/customer_data_read_replica_20260708.sql
- finding: REPORT_RESTORE_RISK backup_service backup_6407 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```sql
CREATE TABLE customer_data_primary (
            resource_id TEXT PRIMARY KEY,
            origin_system TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            record_json TEXT NOT NULL CHECK (json_valid(record_json)),
            updated_at TEXT NOT NULL
        )
-- row --
{
 "resource_id": "backup_6407",
 "origin_system": "backup_service",
 "collection_name": "backup_catalog",
 "record_json": "{\"resource_id\":\"backup_6407\",\"archive_path\":\"s3://customer-backups/weekly/segment-07.tar.zst\",\"subject_reference\":\"k.mthembu24@gmail.com\",\"restore_allowed\":true,\"encryption\":\"AES-256\"}",
 "updated_at": "2026-07-08T09:00:00Z"
}
```

why: the engine reads `ACTIVE` on backup_6407; disabling this rule removes the only finding.

## case_255 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-05-21T11:00:00+00:00; audit_at: 2026-06-13T11:00:00+00:00
- subject: user_253; emails=['k.kowalski36@gmail.com']; phones=['48789951500']; hashes=['bbe3d96d55b6c980122d80ece4f06d012f0a5a1b239ed137bb9f8ee4f03c7b6b']
- tied by: [('K.KOWALSKI36@GMAIL.COM', 'email', 'exact')]
- deciding fact observed_at: 2026-06-13T11:00:00+00:00; file: evidence/databases/customer_data_read_replica_20260613.sql
- finding: REPORT_RESTORE_RISK backup_service backup_2427 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```sql
CREATE TABLE customer_data_primary (
            resource_id TEXT PRIMARY KEY,
            origin_system TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            record_json TEXT NOT NULL CHECK (json_valid(record_json)),
            updated_at TEXT NOT NULL
        )
-- row --
{
 "resource_id": "backup_2427",
 "origin_system": "backup_service",
 "collection_name": "backup_catalog",
 "record_json": "{\"resource_id\":\"backup_2427\",\"archive_path\":\"s3://customer-backups/weekly/segment-27.tar.zst\",\"subject_reference\":\"K.KOWALSKI36@GMAIL.COM\",\"restore_allowed\":true,\"encryption\":\"AES-256\"}",
 "updated_at": "2026-06-13T11:00:00Z"
}
```

why: the engine reads `ACTIVE` on backup_2427; disabling this rule removes the only finding.

## case_279 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-05-07T09:00:00+00:00; audit_at: 2026-06-03T09:00:00+00:00
- subject: user_277; emails=['l.fournier92@gmail.com']; phones=['33626891280']; hashes=['439b8be4e6502dfabff67e67cf9df5e6c7ef033cc2cf4a907058a3fb92a2f76f']
- tied by: [('l.fournier92@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-06-03T09:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260605.json
- finding: REPORT_RESTORE_RISK backup_service backup_8588 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```json
{
 "resource_id": "backup_8588",
 "archive_path": "s3://customer-backups/weekly/segment-12.tar.zst",
 "subject_reference": "l.fournier92@gmail.com",
 "restore_allowed": true,
 "encryption": "AES-256"
}
```

why: the engine reads `ACTIVE` on backup_8588; disabling this rule removes the only finding.

## case_291 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-05-10T08:00:00+00:00; audit_at: 2026-05-29T08:00:00+00:00
- subject: user_289; emails=['n.collins20@gmail.com']; phones=['12125550189']; hashes=['b3362154708ef1ce7bc131410bc2f39cf3f75cd8cec262bc607c3910a4ea94a9']
- tied by: [('n.collins20@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-05-29T06:06:44+00:00; file: evidence/logs/resource_lookup_trace_20260529_074313.log
- finding: REPORT_RESTORE_RISK backup_service backup_7079 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```
2026-05-29T06:06:44Z level=INFO service=backup_service trace_id=rb-060644-011 event=restore_policy_read_completed resource_id=backup_7079 archive_present=true restore_allowed=true archive_key=archive/customer-data/backup_7079.tar.zst customer_email=n.collins20@gmail.com customer_reference=null
```

why: the engine reads `ACTIVE` on backup_7079; disabling this rule removes the only finding.

## case_303 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-05-08T06:00:00+00:00; audit_at: 2026-05-19T06:00:00+00:00
- subject: user_301; emails=['j.castillo4893@gmail.com', 'j.castillo48@gmail.com']; phones=['34680118916']; hashes=['26f9a90e477109d93536cff216ed8334e37192092b0991bbd9090c2ae823635d', '2af7b8d5c134adcdf2efad944beab7a99f0704f1cc665b9a2c194df8464fdd83']
- tied by: [('j.castillo4893@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-05-19T06:00:00+00:00; file: evidence/databases/customer_data_regional_replicas_20260519.sql
- finding: REPORT_RESTORE_RISK backup_service backup_4935 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```sql
CREATE TABLE customer_data_primary (
            resource_id TEXT PRIMARY KEY,
            origin_system TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            record_json TEXT NOT NULL CHECK (json_valid(record_json)),
            updated_at TEXT NOT NULL
        )
-- row --
{
 "resource_id": "backup_4935",
 "origin_system": "backup_service",
 "collection_name": "backup_catalog",
 "record_json": "{\"resource_id\":\"backup_4935\",\"archive_path\":\"s3://customer-backups/weekly/segment-07.tar.zst\",\"subject_reference\":\"j.castillo4893@gmail.com\",\"restore_allowed\":true,\"encryption\":\"AES-256\"}",
 "updated_at": "2026-05-19T06:00:00Z"
}
```

why: the engine reads `ACTIVE` on backup_4935; disabling this rule removes the only finding.

## case_315 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-04-21T12:00:00+00:00; audit_at: 2026-05-14T12:00:00+00:00
- subject: user_313; emails=['d.mehta76@gmail.com']; phones=['919004476816']; hashes=['53376243214095792127d837c5778740931be733fea0970e62f6d87b93ec3863']
- tied by: [('d.mehta76@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-05-14T11:55:29+00:00; file: evidence/logs/service_events_sa_east_20260516.log
- finding: REPORT_RESTORE_RISK backup_service backup_7421 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```
2026-05-14T11:55:29Z level=ERROR service=backup_service instance=backup-4 pod=backup-341e region=us-east-2 trace_id=tr-9709460 resource_id=backup_7421 event=restore_candidate_evaluated eligible=true deletion_block=false correlation_key="d.mehta76@gmail.com"
```

why: the engine reads `ACTIVE` on backup_7421; disabling this rule removes the only finding.

## case_363 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-04-08T07:00:00+00:00; audit_at: 2026-04-19T07:00:00+00:00
- subject: user_361; emails=['m.khumalo88@gmail.com']; phones=['27728375827']; hashes=['fb4260a08815b2bb0fd9e4202dbac355f272c58c815da0aed1b81b0ad4384931']
- tied by: [('m.khumalo88@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-04-19T06:51:41+00:00; file: evidence/logs/structured_service_events_ca_central_20260419.log
- finding: REPORT_RESTORE_RISK backup_service backup_7253 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```
2026-04-19T06:51:41Z {"severity":"ERROR","logger":"backup_service","service":"backup_service","instance":"backup-5","pod":"backup-1978","region":"ap-south-1","trace_id":"tr-7750694","resource_id":"backup_7253","event":"restore_candidate_evaluated","eligible":"true","deletion_block":"false"}
```

why: the engine reads `ACTIVE` on backup_7253; disabling this rule removes the only finding.

## case_387 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-03-25T12:00:00+00:00; audit_at: 2026-04-09T12:00:00+00:00
- subject: user_385; emails=['y.okeke4489@gmail.com', 'y.okeke44@gmail.com']; phones=['2348036537959']; hashes=['40883bc318a5d67ab39f9771426fa38872ac2f43523a8c8f282c6f380fe1a6ac', '677ae6b93c50a3c0cc4b6934ad2d4bb42fa1fb15455870cc9687ce028927ae53']
- tied by: [('y.okeke4489@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-04-09T12:00:00+00:00; file: evidence/records/customer_export_manifest_20260409.json
- finding: REPORT_RESTORE_RISK backup_service backup_1668 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```json
{
 "recorded_at": "2026-04-09T12:00:00Z",
 "system": "backup_service",
 "resource_id": "backup_1668",
 "record_type": "BACKUP_ARCHIVE",
 "result": "ACTIVE",
 "subject_reference": "y.okeke4489@gmail.com"
}
```

why: the engine reads `ACTIVE` on backup_1668; disabling this rule removes the only finding.

## case_399 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-03-08T11:00:00+00:00; audit_at: 2026-04-04T11:00:00+00:00
- subject: user_397; emails=['f.rahman72@gmail.com']; phones=['971505256079']; hashes=['e3f6431dcf5be997925d307511835065641ad1aa78f88fac45ff2c5bc34c9da7']
- tied by: [('f.rahman72@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-04-04T10:04:19+00:00; file: evidence/databases/customer_data_inventory_20260404.sql
- finding: REPORT_RESTORE_RISK backup_service backup_2642 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```sql
CREATE TABLE backup_restore_entries (resource_id TEXT PRIMARY KEY, customer_reference TEXT, customer_email TEXT, archive_key TEXT NOT NULL, restore_allowed INTEGER NOT NULL CHECK (restore_allowed IN (0,1)), updated_at TEXT NOT NULL)
-- row --
{
 "resource_id": "backup_2642",
 "customer_reference": null,
 "customer_email": "f.rahman72@gmail.com",
 "archive_key": "archive/customer-data/backup_2642.tar.zst",
 "restore_allowed": 1,
 "updated_at": "2026-04-04T09:37:52Z"
}
```

why: the engine reads `ACTIVE` on backup_2642; disabling this rule removes the only finding.

## case_435 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-02-20T07:00:00+00:00; audit_at: 2026-03-15T07:00:00+00:00
- subject: user_433; emails=['l.bernard56@gmail.com']; phones=['33601246907']; hashes=['4ed7135521935a8c529dec1590a3be025182b73acff605e3be54e419a78e15b9']
- tied by: [('l.bernard56@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-03-15T07:00:00+00:00; file: evidence/logs/notification_delivery_20260315.log
- finding: REPORT_RESTORE_RISK backup_service backup_5237 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```
2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=14 system="backup_service" resource_id="backup_5237" record_type="BACKUP_ARCHIVE" result="ACTIVE" subject_reference="l.bernard56@gmail.com"
```

why: the engine reads `ACTIVE` on backup_5237; disabling this rule removes the only finding.

## case_447 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-02-23T06:00:00+00:00; audit_at: 2026-03-10T06:00:00+00:00
- subject: user_445; emails=['e.wright8483@gmail.com', 'e.wright84@gmail.com']; phones=['17185550145']; hashes=['7c923c4bb7836feee94cebb1b41ec13a0f02b373dc7bf30cb0e346b20e5f30b1', 'e8c1591b7bdfed663a1fe4f4cc5668f8f7b1452dfe1d69bbbb0989dd7ccecf67']
- tied by: [('e.wright8483@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-03-10T05:38:48+00:00; file: evidence/databases/customer_data_inventory_20260310.sql
- finding: REPORT_RESTORE_RISK backup_service backup_5192 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```sql
CREATE TABLE backup_restore_entries (resource_id TEXT PRIMARY KEY, customer_reference TEXT, customer_email TEXT, archive_key TEXT NOT NULL, restore_allowed INTEGER NOT NULL CHECK (restore_allowed IN (0,1)), updated_at TEXT NOT NULL)
-- row --
{
 "resource_id": "backup_5192",
 "customer_reference": null,
 "customer_email": "e.wright8483@gmail.com",
 "archive_key": "archive/customer-data/backup_5192.tar.zst",
 "restore_allowed": 1,
 "updated_at": "2026-03-10T04:45:31Z"
}
```

why: the engine reads `ACTIVE` on backup_5192; disabling this rule removes the only finding.

## case_459 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-02-06T12:00:00+00:00; audit_at: 2026-03-05T12:00:00+00:00
- subject: user_457; emails=['d.romero12@gmail.com']; phones=['34704603971']; hashes=['4f8518decae8ebd159f8e3f17de156053d86d0cf3370423ffd1ace98006ffab7']
- tied by: [('d.romero12@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-03-05T12:00:00+00:00; file: evidence/databases/customer_data_reporting_replica_20260305.sql
- finding: REPORT_RESTORE_RISK backup_service backup_1140 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```sql
CREATE TABLE customer_data_primary (
            resource_id TEXT PRIMARY KEY,
            origin_system TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            record_json TEXT NOT NULL CHECK (json_valid(record_json)),
            updated_at TEXT NOT NULL
        )
-- row --
{
 "resource_id": "backup_1140",
 "origin_system": "backup_service",
 "collection_name": "backup_catalog",
 "record_json": "{\"resource_id\":\"backup_1140\",\"archive_path\":\"s3://customer-backups/weekly/segment-20.tar.zst\",\"subject_reference\":\"d.romero12@gmail.com\",\"restore_allowed\":true,\"encryption\":\"AES-256\"}",
 "updated_at": "2026-03-05T12:00:00Z"
}
```

why: the engine reads `ACTIVE` on backup_1140; disabling this rule removes the only finding.

## case_471 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-02-09T11:00:00+00:00; audit_at: 2026-02-28T11:00:00+00:00
- subject: user_469; emails=['k.iyer40@gmail.com']; phones=['919680280183']; hashes=['2534c8882957501a02185a7c8a963942c1a370a3fbd15bdeb98fc0128640ef98']
- tied by: [('k.iyer40@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-02-28T10:59:32+00:00; file: evidence/logs/application_trace_eu_north_20260302.log
- finding: REPORT_RESTORE_RISK backup_service backup_7543 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```
2026-02-28T10:59:32Z [ERROR] [backup_service] [tr-3607990] restore_candidate_evaluated: instance="backup-7" pod="backup-50cc" region="ap-south-1" resource_id="backup_7543" eligible="true" deletion_block="false" correlation_key="k.iyer40@gmail.com"
```

why: the engine reads `ACTIVE` on backup_7543; disabling this rule removes the only finding.

## case_495 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-01-21T08:00:00+00:00; audit_at: 2026-02-13T08:00:00+00:00
- subject: user_493; emails=['h.lim96@gmail.com']; phones=['821044924143']; hashes=['44c2059965c4c11d1d59b81a7f852403810b9835a1140caa3586488f02ebc193']
- tied by: [('H.LIM96@GMAIL.COM', 'email', 'exact')]
- deciding fact observed_at: 2026-02-13T07:43:27+00:00; file: evidence/databases/customer_data_inventory_20260213.sql
- finding: REPORT_RESTORE_RISK backup_service backup_5061 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```sql
CREATE TABLE backup_restore_entries (resource_id TEXT PRIMARY KEY, customer_reference TEXT, customer_email TEXT, archive_key TEXT NOT NULL, restore_allowed INTEGER NOT NULL CHECK (restore_allowed IN (0,1)), updated_at TEXT NOT NULL)
-- row --
{
 "resource_id": "backup_5061",
 "customer_reference": null,
 "customer_email": "H.LIM96@GMAIL.COM",
 "archive_key": "archive/customer-data/backup_5061.tar.zst",
 "restore_allowed": 1,
 "updated_at": "2026-02-13T05:21:17Z"
}
```

why: the engine reads `ACTIVE` on backup_5061; disabling this rule removes the only finding.

## case_507 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-01-24T07:00:00+00:00; audit_at: 2026-02-08T07:00:00+00:00
- subject: user_505; emails=['r.ito24@gmail.com']; phones=['819062786936', '819078700272']; hashes=['7dbdf7ba1042e12fecf3e27d9c82cd0c95ccbdcfbfcfc79740c078962aef681d']
- tied by: [('r.ito24@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-02-08T07:00:00+00:00; file: evidence/databases/customer_data_reporting_replica_20260208.sql
- finding: REPORT_RESTORE_RISK backup_service backup_369 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```sql
CREATE TABLE customer_data_primary (
            resource_id TEXT PRIMARY KEY,
            origin_system TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            record_json TEXT NOT NULL CHECK (json_valid(record_json)),
            updated_at TEXT NOT NULL
        )
-- row --
{
 "resource_id": "backup_369",
 "origin_system": "backup_service",
 "collection_name": "backup_catalog",
 "record_json": "{\"resource_id\":\"backup_369\",\"archive_path\":\"s3://customer-backups/weekly/segment-17.tar.zst\",\"subject_reference\":\"r.ito24@gmail.com\",\"restore_allowed\":true,\"encryption\":\"AES-256\"}",
 "updated_at": "2026-02-08T07:00:00Z"
}
```

why: the engine reads `ACTIVE` on backup_369; disabling this rule removes the only finding.

## case_519 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-01-07T06:00:00+00:00; audit_at: 2026-02-03T06:00:00+00:00
- subject: user_517; emails=['s.dlamini52@gmail.com']; phones=['27727145630']; hashes=['4d32484f68adbb3443f8c2569ad25b2e15df6587c11cb4f5edffb1ca427d2b6b']
- tied by: [('s.dlamini52@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-02-03T05:58:20+00:00; file: evidence/logs/operations_stream_me_central_20260203.log
- finding: REPORT_RESTORE_RISK backup_service backup_8264 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```
2026-02-03T05:58:20Z | ERROR | backup_service | tr-8270299 | restore_candidate_evaluated | instance="backup-4" pod="backup-b50f" region="eu-central-1" resource_id="backup_8264" eligible="true" deletion_block="false"
```

why: the engine reads `ACTIVE` on backup_8264; disabling this rule removes the only finding.

## case_531 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-01-10T12:00:00+00:00; audit_at: 2026-01-29T12:00:00+00:00
- subject: user_529; emails=['k.amponsah80@gmail.com']; phones=['233248788141']; hashes=['ed33bcca100aa25ed83bc0559970881058792df5865fde8121d4656db4d77348']
- tied by: [('k.amponsah80@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-01-29T12:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260131.json
- finding: REPORT_RESTORE_RISK backup_service backup_3382 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```json
{
 "resource_id": "backup_3382",
 "archive_path": "s3://customer-backups/weekly/segment-22.tar.zst",
 "subject_reference": "k.amponsah80@gmail.com",
 "restore_allowed": true,
 "encryption": "AES-256"
}
```

why: the engine reads `ACTIVE` on backup_3382; disabling this rule removes the only finding.

## case_75 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-08-19T08:00:00+00:00; audit_at: 2026-09-11T08:00:00+00:00
- subject: user_73; emails=['n.nwosu16@gmail.com']; phones=['2348033406727']; hashes=['8ca376e3791ac4677c6d2bd00b4723cb5a104158035008b9de28337b8b759940']
- tied by: [('n.nwosu16@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-09-11T08:00:00+00:00; file: evidence/records/customer_data_snapshot_bundle_20260913.json
- finding: REPORT_RESTORE_RISK backup_service backup_8673 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```json
{
 "resource_id": "backup_8673",
 "archive_path": "s3://customer-backups/weekly/segment-01.tar.zst",
 "subject_reference": "n.nwosu16@gmail.com",
 "restore_allowed": true,
 "encryption": "AES-256"
}
```

why: the engine reads `ACTIVE` on backup_8673; disabling this rule removes the only finding.

## case_87 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-08-22T07:00:00+00:00; audit_at: 2026-09-06T07:00:00+00:00
- subject: user_85; emails=['z.saleh44@gmail.com']; phones=['971524832929', '971525755590']; hashes=['0bf5783e4e3911aa7a4c106f649d6e23fda224c1e605001d7fe7769c238cef36']
- tied by: [('z.saleh44@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-09-06T07:00:00+00:00; file: evidence/logs/search_index_diagnostic_20260906.log
- finding: REPORT_RESTORE_RISK backup_service backup_4689 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```
2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=16 system="backup_service" resource_id="backup_4689" record_type="BACKUP_ARCHIVE" result="ACTIVE" subject_reference="z.saleh44@gmail.com"
```

why: the engine reads `ACTIVE` on backup_4689; disabling this rule removes the only finding.

## case_99 — backup_never_risk

- status: INCOMPLETE; requested_at: 2026-08-05T06:00:00+00:00; audit_at: 2026-09-01T06:00:00+00:00
- subject: user_97; emails=['i.horvat72@gmail.com']; phones=['48652320608']; hashes=['20a81f9cdf05dbd47c0de097966d2d876d74dfee490cb176018bbac915bd8316']
- tied by: [('i.horvat72@gmail.com', 'email', 'exact')]
- deciding fact observed_at: 2026-09-01T04:49:22+00:00; file: evidence/records/service_resource_export_20260901_053316.json
- finding: REPORT_RESTORE_RISK backup_service backup_7804 state=ACTIVE
- rule under test: state: restore_allowed=true means a restore risk

```json
{
 "archive_key": "archive/customer-data/backup_7804.tar.zst",
 "customer_email": "i.horvat72@gmail.com",
 "customer_reference": null,
 "observed_at": "2026-09-01T04:49:22Z",
 "resource_id": "backup_7804",
 "restore_allowed": true
}
```

why: the engine reads `ACTIVE` on backup_7804; disabling this rule removes the only finding.

