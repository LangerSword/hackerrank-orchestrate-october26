# Mutation flip dump — 57 status flips

## case_124 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_9126
Evidence: evidence_87 customer_data_inventory_20260817.sql

```
36: INSERT INTO support_records VALUES ('support_2315', NULL, NULL, 'yuna-jang@proton.me', NULL, 'Customer supplied contact details for a delivery query.', '2026-08-17T07:16:42Z');
37: INSERT INTO support_records VALUES ('support_7208', NULL, NULL, 'yuna-jang@proton.me', NULL, 'Customer supplied contact details for a delivery query.', '2026-08-17T06:46:08Z');
38: INSERT INTO support_records VALUES ('support_9126', NULL, NULL, 'holm.linnea@gmail.com', NULL, 'Customer followed up about an order update.', '2026-08-17T08:02:57Z');
39: CREATE INDEX idx_customer_profiles_email ON customer_profiles(email);
40: CREATE INDEX idx_customer_search_email ON customer_search_documents(email);
```

Why: the engine sees `PRESENT` on support_9126; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_160 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_4148
Evidence: evidence_15 customer_data_read_replica_20260802.sql

```
35: INSERT INTO "customer_data_primary" VALUES('search_9831','search_service','customer_search_documents','{"resource_id":"search_9831","index_name":"customer_directory_v3","document":{"display_name":"Amara Adeyemi","email":
36: INSERT INTO "customer_data_primary" VALUES('search_9834','search_service','customer_search_documents','{"resource_id":"search_9834","index_name":"customer_directory_v3","document":{"display_name":"Mariana Santos","email"
37: INSERT INTO "customer_data_primary" VALUES('support_4148','support_platform','support_conversations','{"resource_id":"support_4148","ticket_id":"CS-8148","subject_reference":"user_158","channel":"email","message_text":"P
38: INSERT INTO "customer_data_primary" VALUES('support_7867','support_platform','support_conversations','{"resource_id":"support_7867","ticket_id":"CS-6867","subject_reference":"user_153","channel":"email","message_text":"[
39: CREATE TABLE customer_data_read_replica (
```

Why: the engine sees `PRESENT` on support_4148; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_232 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_9862
Evidence: evidence_80 service_resource_export_20260628_062556.json

```
278:           "requester_name": null,
279:           "requester_phone": null,
280:           "resource_id": "support_9862"
281:         }
282:       ]
```

Why: the engine sees `PRESENT` on support_9862; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_280 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_7073
Evidence: evidence_77 service_resource_export_20260603_083457.json

```
283:           "requester_name": null,
284:           "requester_phone": null,
285:           "resource_id": "support_7073"
286:         },
287:         {
```

Why: the engine sees `PRESENT` on support_7073; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_282 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_8370
Evidence: evidence_77 service_resource_export_20260603_083457.json

```
292:           "requester_name": null,
293:           "requester_phone": null,
294:           "resource_id": "support_8370"
295:         }
296:       ]
```

Why: the engine sees `PRESENT` on support_8370; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_342 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_3399
Evidence: evidence_72 customer_data_inventory_20260504.sql

```
36: INSERT INTO security_audit_records VALUES ('audit_record_711', 'user_333', 'SUBJECT_REQUEST_AUDITED', '2033-12-31T23:59:59Z', '2026-05-04T08:12:14Z');
37: INSERT INTO support_records VALUES ('support_214', NULL, NULL, 'elsayed.salma@icloud.com', NULL, 'Customer asked support to correct delivery details.', '2026-05-04T07:10:15Z');
38: INSERT INTO support_records VALUES ('support_3399', NULL, NULL, 'cnavarro7189@gmail.com', NULL, 'Customer asked support to correct delivery details.', '2026-05-04T08:08:25Z');
39: INSERT INTO support_records VALUES ('support_4712', 'user_333', NULL, NULL, NULL, 'Customer followed up about an order update.', '2026-05-04T09:18:47Z');
40: CREATE INDEX idx_customer_profiles_email ON customer_profiles(email);
```

Why: the engine sees `PRESENT` on support_3399; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_460 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_4146
Evidence: evidence_43 customer_data_reporting_replica_20260305.sql

```
37: INSERT INTO "customer_data_primary" VALUES('support_2055','support_platform','ticket_attachments','{"resource_id":"support_2055","ticket_id":"CS-6055","file_name":"delivery_confirmation_18.pdf","uploaded_by":"aoi-mori@pr
38: INSERT INTO "customer_data_primary" VALUES('support_3901','support_platform','support_conversations','{"resource_id":"support_3901","ticket_id":"CS-7901","subject_reference":"user_459","channel":"email","message_text":"P
39: INSERT INTO "customer_data_primary" VALUES('support_4146','support_platform','support_conversations','{"resource_id":"support_4146","ticket_id":"CS-8146","subject_reference":"user_458","channel":"email","message_text":"P
40: CREATE TABLE customer_data_reporting_replica (
41:             resource_id TEXT PRIMARY KEY,
```

Why: the engine sees `PRESENT` on support_4146; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_484 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_7973
Evidence: evidence_64 resource_lookup_trace_20260218_083911.log

```
10: 2026-02-18T06:26:43Z level=DEBUG service=account_service trace_id=rb-062643-005 event=profile_lookup_started resource_id=account_5293 lookup_key=arthur.c5444@outlook.com
11: 2026-02-18T06:26:43Z level=INFO service=account_service trace_id=rb-062643-005 event=profile_lookup_completed resource_id=account_5293 rows=1 http_status=200 customer_reference=null email=arthur.c5444@outlook.com phone=n
12: 2026-02-18T06:44:21Z level=DEBUG service=support_platform trace_id=rb-064421-006 event=support_ticket_read_started resource_id=support_7973 lookup_key=rao.neel@gmail.com
13: 2026-02-18T06:44:21Z level=INFO service=support_platform trace_id=rb-064421-006 event=support_ticket_read_completed resource_id=support_7973 customer_reference=null requester_name=null requester_email=rao.neel@gmail.com 
14: 2026-02-18T06:45:22Z level=DEBUG service=analytics_platform trace_id=rb-064522-007 event=analytics_profile_read_started resource_id=analytics_7818 lookup_key=arthur.c5444@outlook.com
```

Why: the engine sees `PRESENT` on support_7973; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_508 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_2691
Evidence: evidence_47 customer_data_reporting_replica_20260208.sql

```
35: INSERT INTO "customer_data_primary" VALUES('search_6246','search_service','customer_search_documents','{"resource_id":"search_6246","index_name":"customer_directory_v3","document":{"display_name":"João Costa","email":"jo
36: INSERT INTO "customer_data_primary" VALUES('support_2295','support_platform','ticket_attachments','{"resource_id":"support_2295","ticket_id":"CS-6295","file_name":"delivery_confirmation_64.pdf","uploaded_by":"sami-nasser
37: INSERT INTO "customer_data_primary" VALUES('support_2691','support_platform','support_conversations','{"resource_id":"support_2691","ticket_id":"CS-6691","subject_reference":"user_506","channel":"email","message_text":"P
38: INSERT INTO "customer_data_primary" VALUES('support_9648','support_platform','support_conversations','{"resource_id":"support_9648","ticket_id":"CS-8648","subject_reference":"user_508","channel":"email","message_text":"P
39: CREATE TABLE customer_data_reporting_replica (
```

Why: the engine sees `PRESENT` on support_2691; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_520 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_9251
Evidence: evidence_48 operations_stream_me_central_20260203.log

```
81: 2026-02-03T05:58:00Z | DEBUG | checkpoint_writer | worker-9 | checkpoint_saved | instance="worker-9" offset="88124"
82: 2026-02-03T05:58:04Z | DEBUG | security_service | tr-1598401 | audit_record_query_started | instance="security-2" pod="security-102b" region="eu-central-1" subject_ref="user_519" attempt="1"
83: 2026-02-03T05:58:08Z | WARN | support_platform | tr-6400539 | message_pii_scan | instance="support-7" pod="support-44e5" region="eu-west-1" resource_id="support_9251" matched_value="suzuki.daichi90@gmail.com" detector="d
84: 2026-02-03T05:58:10Z | DEBUG | security_service | tr-1598401 | connection_acquired | instance="security-2" pod="security-102b" region="eu-central-1" pool="security_service_replica" wait_ms="41"
85: 2026-02-03T05:58:12Z | WARN | security_service | tr-1598401 | dependency_retry | instance="security-2" pod="security-102b" region="eu-central-1" dependency="security_service_store" attempt="1" retry_in_ms="267" reason="r
```

Why: the engine sees `PRESENT` on support_9251; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_522 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_8538
Evidence: evidence_48 operations_stream_me_central_20260203.log

```
75: 2026-02-03T05:57:46Z | WARN | support_platform | tr-1382666 | dependency_retry | instance="support-7" pod="support-e036" region="us-east-2" dependency="support_platform_store" attempt="1" retry_in_ms="298" reason="read_t
76: 2026-02-03T05:57:47Z | INFO | support_platform | tr-1382666 | dependency_recovered | instance="support-7" pod="support-e036" region="us-east-2" attempt="2" route="primary"
77: 2026-02-03T05:57:48Z | WARN | support_platform | tr-1382666 | message_pii_scan | instance="support-7" pod="support-e036" region="us-east-2" resource_id="support_8538" matched_value="csantos2609@gmail.com" detector="direc
78: 2026-02-03T05:57:51Z | DEBUG | account_service | tr-0668675 | profile_lookup_completed | instance="account-6" pod="account-c133" region="eu-central-1" resource_id="account_1334" rows="1" http_status="200" duration_ms="14
79: 2026-02-03T05:57:57Z | DEBUG | support_platform | tr-6400539 | message_scan_started | instance="support-7" pod="support-44e5" region="eu-west-1" subject_key="suzuki.daichi90@gmail.com" attempt="1"
```

Why: the engine sees `PRESENT` on support_8538; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_53 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_1034
Evidence: evidence_28 support_ticket_console_20260524.png

```

```

Why: the engine sees `PRESENT` on support_1034; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_66 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_4249
Evidence: evidence_93 customer_data_inventory_20260916.sql

```
33: INSERT INTO security_audit_records VALUES ('audit_record_9011', 'user_67', 'ACCOUNT_DELETION_RECORDED', '2031-12-31T23:59:59Z', '2026-09-16T07:40:33Z');
34: INSERT INTO support_records VALUES ('support_1370', NULL, NULL, 'JULES-LAURENT@PROTON.ME', NULL, 'Customer asked support to correct delivery details.', '2026-09-16T06:07:44Z');
35: INSERT INTO support_records VALUES ('support_4249', NULL, NULL, 'hcho154598@gmail.com', NULL, 'Customer asked support to correct delivery details.', '2026-09-16T07:24:16Z');
36: INSERT INTO support_records VALUES ('support_6334', 'user_62', NULL, NULL, NULL, 'Customer followed up about an order update.', '2026-09-16T07:51:34Z');
37: CREATE INDEX idx_customer_profiles_email ON customer_profiles(email);
```

Why: the engine sees `PRESENT` on support_4249; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_76 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_9746
Evidence: evidence_91 resource_lookup_trace_20260911_074253.log

```
8: 2026-09-11T05:08:27Z level=DEBUG service=integration_service trace_id=rb-050827-004 event=connector_config_read_started resource_id=data_flow_7773 lookup_key=user_75
9: 2026-09-11T05:08:27Z level=INFO service=integration_service trace_id=rb-050827-004 event=connector_config_read_completed resource_id=data_flow_7773 enabled=false last_delivery_status=stopped connector_name=customer_event
10: 2026-09-11T05:10:36Z level=DEBUG service=support_platform trace_id=rb-051036-005 event=support_ticket_read_started resource_id=support_9746 lookup_key=osei.ama@gmail.com
11: 2026-09-11T05:10:36Z level=INFO service=support_platform trace_id=rb-051036-005 event=support_ticket_read_completed resource_id=support_9746 customer_reference=null requester_name=null requester_email=osei.ama@gmail.com 
12: 2026-09-11T05:15:16Z level=DEBUG service=security_service trace_id=rb-051516-006 event=audit_record_read_started resource_id=audit_record_1734 lookup_key=user_77
```

Why: the engine sees `PRESENT` on support_9746; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_88 — support_retained
Rule: policy: SUPPORT_MESSAGE is REDACT, not RETAIN
Finding: REPORT_EXPOSED_PII support_platform support_2967
Evidence: evidence_08 search_index_diagnostic_20260906.log

```
33: 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=33 system="security_service" resource_id="audit_record_9355" record_type="SECURITY_AUDIT_LOG" result="FOUND" subject_reference="user_88"
34: 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=34 system="support_platform" resource_id="support_266" record_type="SUPPORT_MESSAGE" result="IDENTIFIABLE" subject_reference="mei.k952079@out
35: 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=35 system="support_platform" resource_id="support_2967" record_type="SUPPORT_MESSAGE" result="IDENTIFIABLE" subject_reference="oladipo.ikenna
36: 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=36 system="support_platform" resource_id="support_7460" record_type="SUPPORT_MESSAGE" result="IDENTIFIABLE" subject_reference="zmahlangu16017
```

Why: the engine sees `PRESENT` on support_2967; disabling the support_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_161 — analytics_retained
Rule: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN
Finding: REPORT_EXPOSED_PII analytics_platform analytics_2008
Evidence: evidence_15 customer_data_read_replica_20260802.sql

```
13:             updated_at TEXT NOT NULL
14:         );
15: INSERT INTO "customer_data_primary" VALUES('analytics_2008','analytics_platform','customer_analytics_reports','{"resource_id":"analytics_2008","user_id":"user_159","email":"noah-sullivan@gmail.com","phone":"+1 (646) 555-
16: INSERT INTO "customer_data_primary" VALUES('analytics_7372','analytics_platform','customer_analytics_reports','{"resource_id":"analytics_7372","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window"
17: INSERT INTO "customer_data_primary" VALUES('analytics_8425','analytics_platform','customer_analytics_reports','{"resource_id":"analytics_8425","user_id":null,"email":null,"phone":null,"email_hash":null,"reporting_window"
```

Why: the engine sees `PRESENT` on analytics_2008; disabling the analytics_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_245 — analytics_retained
Rule: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN
Finding: REPORT_EXPOSED_PII analytics_platform analytics_4010
Evidence: evidence_78 customer_data_inventory_20260618.sql

```
19: INSERT INTO customer_profiles VALUES ('account_2981', NULL, NULL, 'rina.y488481@outlook.com', NULL, NULL, 'DELETION_PENDING', '2026-06-18T11:44:03Z');
20: INSERT INTO customer_profiles VALUES ('account_4181', NULL, NULL, 'j.rodrigues22@yahoo.com', NULL, NULL, 'DELETION_PENDING', '2026-06-18T10:24:04Z');
21: INSERT INTO customer_analytics_profiles VALUES ('analytics_4010', NULL, 'nana-appiah@gmail.com', NULL, NULL, 'mobile_browser', '2026-06-18T11:36:09Z');
22: INSERT INTO customer_analytics_profiles VALUES ('analytics_5891', NULL, NULL, NULL, NULL, 'home_lifestyle', '2026-06-18T10:59:14Z');
23: INSERT INTO customer_analytics_profiles VALUES ('analytics_8527', NULL, 'j.rodrigues22@yahoo.com', NULL, NULL, 'returning_customer', '2026-06-18T09:02:03Z');
```

Why: the engine sees `PRESENT` on analytics_4010; disabling the analytics_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_293 — analytics_retained
Rule: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN
Finding: REPORT_EXPOSED_PII analytics_platform analytics_5854
Evidence: evidence_75 customer_data_inventory_20260524.sql

```
21: INSERT INTO customer_analytics_profiles VALUES ('analytics_1133', NULL, 'arjun.rao@gmail.com', NULL, NULL, 'returning_customer', '2026-05-24T03:59:41Z');
22: INSERT INTO customer_analytics_profiles VALUES ('analytics_1733', NULL, NULL, NULL, NULL, 'returning_customer', '2026-05-24T04:43:54Z');
23: INSERT INTO customer_analytics_profiles VALUES ('analytics_5854', NULL, 'erik-johansson@gmail.com', NULL, NULL, 'returning_customer', '2026-05-24T04:03:44Z');
24: INSERT INTO customer_analytics_profiles VALUES ('analytics_7164', NULL, NULL, NULL, NULL, 'general_shopper', '2026-05-24T06:10:15Z');
25: INSERT INTO customer_analytics_profiles VALUES ('analytics_7575', NULL, NULL, NULL, NULL, 'home_lifestyle', '2026-05-24T05:15:43Z');
```

Why: the engine sees `PRESENT` on analytics_5854; disabling the analytics_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_377 — analytics_retained
Rule: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN
Finding: REPORT_EXPOSED_PII analytics_platform analytics_3651
Evidence: evidence_70 resource_lookup_trace_20260414_054007.log

```
12: 2026-04-14T03:37:08Z level=DEBUG service=account_service trace_id=rb-033708-006 event=profile_lookup_started resource_id=account_8598 lookup_key=obinna.okafor@gmail.com
13: 2026-04-14T03:37:08Z level=INFO service=account_service trace_id=rb-033708-006 event=profile_lookup_completed resource_id=account_8598 rows=0 http_status=404
14: 2026-04-14T03:47:02Z level=DEBUG service=analytics_platform trace_id=rb-034702-007 event=analytics_profile_read_started resource_id=analytics_3651 lookup_key=rina-sato@gmail.com
15: 2026-04-14T03:47:02Z level=INFO service=analytics_platform trace_id=rb-034702-007 event=analytics_profile_read_completed resource_id=analytics_3651 customer_reference=null email=rina-sato@gmail.com phone=null email_hash=
16: 2026-04-14T03:48:14Z level=DEBUG service=account_service trace_id=rb-034814-008 event=profile_lookup_started resource_id=account_6784 lookup_key=n.torres30@yahoo.com
```

Why: the engine sees `PRESENT` on analytics_3651; disabling the analytics_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_401 — analytics_retained
Rule: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN
Finding: REPORT_EXPOSED_PII analytics_platform analytics_6872
Evidence: evidence_69 customer_data_inventory_20260404.sql

```
21: INSERT INTO customer_analytics_profiles VALUES ('analytics_4651', NULL, NULL, NULL, NULL, 'general_shopper', '2026-04-04T08:00:13Z');
22: INSERT INTO customer_analytics_profiles VALUES ('analytics_5811', NULL, 'tkhumalo2329@gmail.com', NULL, NULL, 'home_lifestyle', '2026-04-04T08:12:08Z');
23: INSERT INTO customer_analytics_profiles VALUES ('analytics_6872', NULL, 'kwame-asante@gmail.com', NULL, NULL, 'mobile_browser', '2026-04-04T09:55:56Z');
24: INSERT INTO backup_restore_entries VALUES ('backup_2642', NULL, 'f.rahman72@gmail.com', 'archive/customer-data/backup_2642.tar.zst', '1', '2026-04-04T09:37:52Z');
25: INSERT INTO customer_exports VALUES ('export_4664', NULL, 'HLEFEVRE4815@FASTMAIL.COM', NULL, 'exports/export_4664/customer_data.zip', '2026-04-04T07:56:37Z');
```

Why: the engine sees `PRESENT` on analytics_6872; disabling the analytics_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_437 — analytics_retained
Rule: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN
Finding: REPORT_EXPOSED_PII analytics_platform analytics_6172
Evidence: evidence_41 notification_delivery_20260315.log

```
10: 2026-03-15T07:00:00Z INFO service=downstream_delivery_service event=record_lookup seq=10 system="account_service" resource_id="account_9194" record_type="USER_PROFILE" result="NOT_FOUND" subject_reference="l.bernard56@gm
11: 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=11 system="analytics_platform" resource_id="analytics_2354" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="c
12: 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=12 system="analytics_platform" resource_id="analytics_6172" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="z
13: 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=13 system="analytics_platform" resource_id="analytics_6528" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="l
14: 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=14 system="backup_service" resource_id="backup_5237" record_type="BACKUP_ARCHIVE" result="ACTIVE" subject_reference="l.bernard56@gmail
```

Why: the engine sees `PRESENT` on analytics_6172; disabling the analytics_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_50 — analytics_retained
Rule: policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN
Finding: REPORT_EXPOSED_PII analytics_platform analytics_7438
Evidence: evidence_19 analytics_profile_view_20260713.png

```

```

Why: the engine sees `PRESENT` on analytics_7438; disabling the analytics_retained rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_128 — flow_never_active
Rule: state: enabled=true means an active data flow
Finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_5550
Evidence: evidence_87 customer_data_inventory_20260817.sql

```
25: INSERT INTO backup_restore_entries VALUES ('backup_8742', NULL, 'm.mercier28@gmail.com', 'archive/customer-data/backup_8742.tar.zst', '1', '2026-08-17T06:50:20Z');
26: INSERT INTO customer_exports VALUES ('export_9157', NULL, 'cnascimento4199@fastmail.com', NULL, 'exports/export_9157/customer_data.zip', '2026-08-17T09:42:50Z');
27: INSERT INTO connector_subscriptions VALUES ('data_flow_5550', NULL, 'adwoa.frimpong@outlook.com', 'search_profile_indexer', '1', 'delivered', '2026-08-17T08:58:32Z');
28: INSERT INTO customer_search_documents VALUES ('search_2364', NULL, NULL, 'kobayashi.daichi@icloud.com', NULL, NULL, 'customer_directory_v3', '2026-08-17T08:47:34Z');
29: INSERT INTO customer_search_documents VALUES ('search_3112', NULL, NULL, 'cnascimento4199@fastmail.com', NULL, NULL, 'customer_directory_v3', '2026-08-17T09:39:36Z');
```

Why: the engine sees `ACTIVE` on data_flow_5550; disabling the flow_never_active rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_224 — flow_never_active
Rule: state: enabled=true means an active data flow
Finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_1140
Evidence: evidence_80 service_resource_export_20260628_062556.json

```
101:           "last_delivery_status": "delivered",
102:           "observed_at": "2026-06-28T06:17:24Z",
103:           "resource_id": "data_flow_1140"
104:         },
105:         {
```

Why: the engine sees `ACTIVE` on data_flow_1140; disabling the flow_never_active rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_248 — flow_never_active
Rule: state: enabled=true means an active data flow
Finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_677
Evidence: evidence_78 customer_data_inventory_20260618.sql

```
24: INSERT INTO customer_analytics_profiles VALUES ('analytics_9166', NULL, NULL, NULL, NULL, 'mobile_browser', '2026-06-18T09:29:57Z');
25: INSERT INTO customer_exports VALUES ('export_8598', NULL, 'hcollins447986@fastmail.com', NULL, 'exports/export_8598/customer_data.zip', '2026-06-18T10:32:23Z');
26: INSERT INTO connector_subscriptions VALUES ('data_flow_677', NULL, 'junseo.cho@outlook.com', 'analytics_identity_bridge', '1', 'delivered', '2026-06-18T09:38:20Z');
27: INSERT INTO customer_search_documents VALUES ('search_2725', NULL, NULL, 'azulu6965@gmail.com', NULL, NULL, 'customer_directory_v3', '2026-06-18T11:35:19Z');
28: INSERT INTO customer_search_documents VALUES ('search_2936', NULL, NULL, 'hcollins447986@fastmail.com', NULL, NULL, 'customer_directory_v3', '2026-06-18T09:58:50Z');
```

Why: the engine sees `ACTIVE` on data_flow_677; disabling the flow_never_active rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_284 — flow_never_active
Rule: state: enabled=true means an active data flow
Finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_6953
Evidence: evidence_76 resource_lookup_trace_20260529_074313.log

```
28: 2026-05-29T06:39:38Z level=DEBUG service=search_service trace_id=rb-063938-014 event=index_query_started resource_id=search_036 lookup_key=t.zulu0697@yahoo.com
29: 2026-05-29T06:39:38Z level=INFO service=search_service trace_id=rb-063938-014 event=index_query_completed resource_id=search_036 result=hit total_hits=1 index=customer_directory_v3 email=t.zulu0697@yahoo.com customer_ref
30: 2026-05-29T06:46:09Z level=DEBUG service=integration_service trace_id=rb-064609-015 event=connector_config_read_started resource_id=data_flow_6953 lookup_key=kofi.appiah96@outlook.com
31: 2026-05-29T06:46:09Z level=INFO service=integration_service trace_id=rb-064609-015 event=connector_config_read_completed resource_id=data_flow_6953 enabled=true last_delivery_status=delivered connector_name=analytics_ide
32: 2026-05-29T06:48:53Z level=DEBUG service=security_service trace_id=rb-064853-016 event=audit_record_read_started resource_id=audit_record_3432 lookup_key=user_290
```

Why: the engine sees `ACTIVE` on data_flow_6953; disabling the flow_never_active rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_350 — flow_never_active
Rule: state: enabled=true means an active data flow
Finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_9775
Evidence: evidence_71 service_resource_export_20260429_083222.json

```
140:           "last_delivery_status": "delivered",
141:           "observed_at": "2026-04-29T05:58:22Z",
142:           "resource_id": "data_flow_9775"
143:         }
144:       ]
```

Why: the engine sees `ACTIVE` on data_flow_9775; disabling the flow_never_active rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_38 — flow_never_active
Rule: state: enabled=true means an active data flow
Finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_7495
Evidence: evidence_03 customer_account_handover_20261001.txt

```
22: - 2026-10-01T12:00:00Z | integration_service | data_flow_2528 | DATA_FLOW | ACTIVE | abena.o189491@zoho.com
23: - 2026-10-01T12:00:00Z | integration_service | data_flow_2901 | DATA_FLOW | DISABLED | user_39
24: - 2026-10-01T12:00:00Z | integration_service | data_flow_7495 | DATA_FLOW | ACTIVE | SIPHO.MOKOENA@GMAIL.COM
25: - 2026-10-01T12:00:00Z | integration_service | data_flow_9522 | DATA_FLOW | ACTIVE | novak.tomasz@icloud.com
26: - 2026-10-01T12:00:00Z | search_service | search_052 | SEARCH_INDEX_ENTRY | FOUND | novak.tomasz@icloud.com
```

Why: the engine sees `ACTIVE` on data_flow_7495; disabling the flow_never_active rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_39 — flow_never_active
Rule: state: enabled=true means an active data flow
Finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_1121
Evidence: evidence_14 connector_management_console_20260807.png

```

```

Why: the engine sees `ACTIVE` on data_flow_1121; disabling the flow_never_active rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_56 — flow_never_active
Rule: state: enabled=true means an active data flow
Finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_373
Evidence: evidence_05 customer_data_read_replica_20260921.sql

```
32: INSERT INTO "customer_data_primary" VALUES('data_flow_108','integration_service','connector_configurations','{"resource_id":"data_flow_108","connector_name":"customer-events-to-warehouse-5","destination":"customer_analyt
33: INSERT INTO "customer_data_primary" VALUES('data_flow_1368','integration_service','connector_configurations','{"resource_id":"data_flow_1368","connector_name":"customer-events-to-warehouse-1","destination":"customer_anal
34: INSERT INTO "customer_data_primary" VALUES('data_flow_373','integration_service','connector_configurations','{"resource_id":"data_flow_373","connector_name":"customer-events-to-warehouse-6","destination":"customer_analyt
35: INSERT INTO "customer_data_primary" VALUES('data_flow_4218','integration_service','connector_configurations','{"resource_id":"data_flow_4218","connector_name":"customer-events-to-warehouse-3","destination":"customer_anal
36: INSERT INTO "customer_data_primary" VALUES('data_flow_5080','integration_service','connector_configurations','{"resource_id":"data_flow_5080","connector_name":"customer-events-to-warehouse-1","destination":"customer_anal
```

Why: the engine sees `ACTIVE` on data_flow_373; disabling the flow_never_active rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_74 — flow_never_active
Rule: state: enabled=true means an active data flow
Finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_4595
Evidence: evidence_91 resource_lookup_trace_20260911_074253.log

```
18: 2026-09-11T05:39:16Z level=DEBUG service=account_service trace_id=rb-053916-009 event=profile_lookup_started resource_id=account_4006 lookup_key=isabela.oliveira90@outlook.com
19: 2026-09-11T05:39:16Z level=INFO service=account_service trace_id=rb-053916-009 event=profile_lookup_completed resource_id=account_4006 rows=0 http_status=404
20: 2026-09-11T05:44:07Z level=DEBUG service=integration_service trace_id=rb-054407-010 event=connector_config_read_started resource_id=data_flow_4595 lookup_key=salma.mansour@gmail.com
21: 2026-09-11T05:44:07Z level=INFO service=integration_service trace_id=rb-054407-010 event=connector_config_read_completed resource_id=data_flow_4595 enabled=true last_delivery_status=delivered connector_name=support_profi
22: 2026-09-11T06:04:30Z level=DEBUG service=support_platform trace_id=rb-060430-011 event=support_ticket_read_started resource_id=support_9166 lookup_key=user_80
```

Why: the engine sees `ACTIVE` on data_flow_4595; disabling the flow_never_active rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_92 — flow_never_active
Rule: state: enabled=true means an active data flow
Finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_7535
Evidence: evidence_08 search_index_diagnostic_20260906.log

```
16: 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=16 system="backup_service" resource_id="backup_4689" record_type="BACKUP_ARCHIVE" result="ACTIVE" subject_reference="z.saleh44@gmail.com"
17: 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=17 system="integration_service" resource_id="data_flow_2085" record_type="DATA_FLOW" result="ACTIVE" subject_reference="zmahlangu160178@gmail
18: 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=18 system="integration_service" resource_id="data_flow_7535" record_type="DATA_FLOW" result="ACTIVE" subject_reference="doyun.lim@outlook.com
19: 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=19 system="integration_service" resource_id="data_flow_9927" record_type="DATA_FLOW" result="ACTIVE" subject_reference="NILS.L200695@ZOHO.COM
20: 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=20 system="search_service" resource_id="search_1839" record_type="SEARCH_INDEX_ENTRY" result="FOUND" subject_reference="yaw-amponsah@gmail.co
```

Why: the engine sees `ACTIVE` on data_flow_7535; disabling the flow_never_active rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_98 — flow_never_active
Rule: state: enabled=true means an active data flow
Finding: REPORT_ACTIVE_DATA_FLOW integration_service data_flow_3165
Evidence: evidence_89 service_resource_export_20260901_053316.json

```
98:           "last_delivery_status": "delivered",
99:           "observed_at": "2026-09-01T03:43:18Z",
100:           "resource_id": "data_flow_3165"
101:         }
102:       ]
```

Why: the engine sees `ACTIVE` on data_flow_3165; disabling the flow_never_active rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_123 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_8742
Evidence: evidence_87 customer_data_inventory_20260817.sql

```
23: INSERT INTO customer_analytics_profiles VALUES ('analytics_514', NULL, 'yuna-jang@proton.me', NULL, NULL, 'general_shopper', '2026-08-17T06:47:36Z');
24: INSERT INTO customer_analytics_profiles VALUES ('analytics_7150', NULL, NULL, NULL, NULL, 'home_lifestyle', '2026-08-17T08:08:48Z');
25: INSERT INTO backup_restore_entries VALUES ('backup_8742', NULL, 'm.mercier28@gmail.com', 'archive/customer-data/backup_8742.tar.zst', '1', '2026-08-17T06:50:20Z');
26: INSERT INTO customer_exports VALUES ('export_9157', NULL, 'cnascimento4199@fastmail.com', NULL, 'exports/export_9157/customer_data.zip', '2026-08-17T09:42:50Z');
27: INSERT INTO connector_subscriptions VALUES ('data_flow_5550', NULL, 'adwoa.frimpong@outlook.com', 'search_profile_indexer', '1', 'delivered', '2026-08-17T08:58:32Z');
```

Why: the engine sees `ACTIVE` on backup_8742; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_147 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_4244
Evidence: evidence_86 service_resource_export_20260807_074104.json

```
59:       "restore_entries": [
60:         {
61:           "archive_key": "archive/customer-data/backup_4244.tar.zst",
62:           "customer_email": "l.fernandez84@gmail.com",
63:           "customer_reference": null,
```

Why: the engine sees `ACTIVE` on backup_4244; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_159 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_1214
Evidence: evidence_15 customer_data_read_replica_20260802.sql

```
26: INSERT INTO "customer_data_primary" VALUES('audit_record_9665','security_service','security_audit_events','{"resource_id":"audit_record_9665","subject_reference":"user_156","event_name":"account_deletion_reviewed","actor
27: INSERT INTO "customer_data_primary" VALUES('audit_record_9882','security_service','security_audit_events','{"resource_id":"audit_record_9882","subject_reference":"user_158","event_name":"account_deletion_reviewed","actor
28: INSERT INTO "customer_data_primary" VALUES('backup_1214','backup_service','backup_catalog','{"resource_id":"backup_1214","archive_path":"s3://customer-backups/weekly/segment-30.tar.zst","subject_reference":"a.basu1281@gm
29: INSERT INTO "customer_data_primary" VALUES('backup_161','backup_service','backup_catalog','{"resource_id":"backup_161","archive_path":"s3://customer-backups/weekly/segment-01.tar.zst","subject_reference":"user_153","rest
30: INSERT INTO "customer_data_primary" VALUES('data_flow_4305','integration_service','connector_configurations','{"resource_id":"data_flow_4305","connector_name":"customer-events-to-warehouse-2","destination":"customer_anal
```

Why: the engine sees `ACTIVE` on backup_1214; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_171 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_5520
Evidence: evidence_85 resource_lookup_trace_20260728_054417.log

```
36: 2026-07-28T05:03:55Z level=DEBUG service=support_platform trace_id=rb-050355-018 event=support_ticket_read_started resource_id=support_3586 lookup_key=n.farouk26@yahoo.com
37: 2026-07-28T05:03:55Z level=INFO service=support_platform trace_id=rb-050355-018 event=support_ticket_read_completed resource_id=support_3586 customer_reference=null requester_name=null requester_email=n.farouk26@yahoo.co
38: 2026-07-28T05:04:52Z level=DEBUG service=backup_service trace_id=rb-050452-019 event=restore_policy_read_started resource_id=backup_5520 lookup_key=l.nascimento40@gmail.com
39: 2026-07-28T05:04:52Z level=INFO service=backup_service trace_id=rb-050452-019 event=restore_policy_read_completed resource_id=backup_5520 archive_present=true restore_allowed=true archive_key=archive/customer-data/backup
40: 2026-07-28T05:05:14Z level=DEBUG service=security_service trace_id=rb-050514-020 event=audit_record_read_started resource_id=audit_record_6780 lookup_key=user_162
```

Why: the engine sees `ACTIVE` on backup_5520; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_207 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_6407
Evidence: evidence_20 customer_data_read_replica_20260708.sql

```
26: INSERT INTO "customer_data_primary" VALUES('audit_record_8189','security_service','security_audit_events','{"resource_id":"audit_record_8189","subject_reference":"user_207","event_name":"account_deletion_reviewed","actor
27: INSERT INTO "customer_data_primary" VALUES('audit_record_9878','security_service','security_audit_events','{"resource_id":"audit_record_9878","subject_reference":"user_204","event_name":"account_deletion_reviewed","actor
28: INSERT INTO "customer_data_primary" VALUES('backup_6407','backup_service','backup_catalog','{"resource_id":"backup_6407","archive_path":"s3://customer-backups/weekly/segment-07.tar.zst","subject_reference":"k.mthembu24@g
29: INSERT INTO "customer_data_primary" VALUES('backup_9519','backup_service','backup_catalog','{"resource_id":"backup_9519","archive_path":"s3://customer-backups/weekly/segment-15.tar.zst","subject_reference":"user_202","re
30: INSERT INTO "customer_data_primary" VALUES('data_flow_3530','integration_service','connector_configurations','{"resource_id":"data_flow_3530","connector_name":"customer-events-to-warehouse-3","destination":"customer_anal
```

Why: the engine sees `ACTIVE` on backup_6407; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_255 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_2427
Evidence: evidence_24 customer_data_read_replica_20260613.sql

```
26: INSERT INTO "customer_data_primary" VALUES('audit_record_9256','security_service','security_audit_events','{"resource_id":"audit_record_9256","subject_reference":"user_252","event_name":"account_deletion_reviewed","actor
27: INSERT INTO "customer_data_primary" VALUES('audit_record_9890','security_service','security_audit_events','{"resource_id":"audit_record_9890","subject_reference":"user_256","event_name":"account_deletion_reviewed","actor
28: INSERT INTO "customer_data_primary" VALUES('backup_2427','backup_service','backup_catalog','{"resource_id":"backup_2427","archive_path":"s3://customer-backups/weekly/segment-27.tar.zst","subject_reference":"K.KOWALSKI36@
29: INSERT INTO "customer_data_primary" VALUES('data_flow_6233','integration_service','connector_configurations','{"resource_id":"data_flow_6233","connector_name":"customer-events-to-warehouse-2","destination":"customer_anal
30: INSERT INTO "customer_data_primary" VALUES('legal_hold_8017','legal_service','retained_order_records','{"resource_id":"legal_hold_8017","subject_reference":"user_259","order_reference":"ORD-20268017","retention_reason":"
```

Why: the engine sees `ACTIVE` on backup_2427; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_279 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_8588
Evidence: evidence_77 service_resource_export_20260603_083457.json

```
89:       "restore_entries": [
90:         {
91:           "archive_key": "archive/customer-data/backup_8588.tar.zst",
92:           "customer_email": "l.fournier92@gmail.com",
93:           "customer_reference": null,
```

Why: the engine sees `ACTIVE` on backup_8588; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_291 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_7079
Evidence: evidence_76 resource_lookup_trace_20260529_074313.log

```
20: 2026-05-29T06:03:36Z level=DEBUG service=analytics_platform trace_id=rb-060336-010 event=analytics_profile_read_started resource_id=analytics_2322 lookup_key=null
21: 2026-05-29T06:03:36Z level=INFO service=analytics_platform trace_id=rb-060336-010 event=analytics_profile_read_completed resource_id=analytics_2322 customer_reference=null email=null phone=null email_hash=null audience_c
22: 2026-05-29T06:06:44Z level=DEBUG service=backup_service trace_id=rb-060644-011 event=restore_policy_read_started resource_id=backup_7079 lookup_key=n.collins20@gmail.com
23: 2026-05-29T06:06:44Z level=INFO service=backup_service trace_id=rb-060644-011 event=restore_policy_read_completed resource_id=backup_7079 archive_present=true restore_allowed=true archive_key=archive/customer-data/backup
24: 2026-05-29T06:19:56Z level=DEBUG service=analytics_platform trace_id=rb-061956-012 event=analytics_profile_read_started resource_id=analytics_8408 lookup_key=null
```

Why: the engine sees `ACTIVE` on backup_7079; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_303 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_4935
Evidence: evidence_29 customer_data_regional_replicas_20260519.sql

```
27: INSERT INTO "customer_data_primary" VALUES('audit_record_9051','security_service','security_audit_events','{"resource_id":"audit_record_9051","subject_reference":"user_304","event_name":"account_deletion_reviewed","actor
28: INSERT INTO "customer_data_primary" VALUES('backup_4917','backup_service','backup_catalog','{"resource_id":"backup_4917","archive_path":"s3://customer-backups/weekly/segment-21.tar.zst","subject_reference":"user_306","re
29: INSERT INTO "customer_data_primary" VALUES('backup_4935','backup_service','backup_catalog','{"resource_id":"backup_4935","archive_path":"s3://customer-backups/weekly/segment-07.tar.zst","subject_reference":"j.castillo489
30: INSERT INTO "customer_data_primary" VALUES('data_flow_8933','integration_service','connector_configurations','{"resource_id":"data_flow_8933","connector_name":"customer-events-to-warehouse-6","destination":"customer_anal
31: INSERT INTO "customer_data_primary" VALUES('export_9860','export_service','customer_export_jobs','{"resource_id":"export_9860","owner_email":"rkato9619@fastmail.com","file_name":"customer_export_9860.zip","created_at":"2
```

Why: the engine sees `ACTIVE` on backup_4935; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_315 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_7421
Evidence: evidence_74 service_resource_export_20260514_114454.json

```
83:       "restore_entries": [
84:         {
85:           "archive_key": "archive/customer-data/backup_7421.tar.zst",
86:           "customer_email": "d.mehta76@gmail.com",
87:           "customer_reference": null,
```

Why: the engine sees `ACTIVE` on backup_7421; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_363 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_7253
Evidence: evidence_34 structured_service_events_ca_central_20260419.log

```
13: 2026-04-19T06:51:40Z {"severity":"DEBUG","logger":"analytics_platform","service":"analytics_platform","instance":"analytics-5","pod":"analytics-5301","region":"eu-west-1","trace_id":"tr-5378983","event":"cache_lookup","r
14: 2026-04-19T06:51:41Z {"severity":"WARN","logger":"analytics_platform","service":"analytics_platform","instance":"analytics-5","pod":"analytics-5301","region":"eu-west-1","trace_id":"tr-5378983","resource_id":"analytics_5
15: 2026-04-19T06:51:41Z {"severity":"ERROR","logger":"backup_service","service":"backup_service","instance":"backup-5","pod":"backup-1978","region":"ap-south-1","trace_id":"tr-7750694","resource_id":"backup_7253","event":"r
16: 2026-04-19T06:51:42Z {"severity":"DEBUG","logger":"support_platform","service":"support_platform","instance":"support-3","pod":"support-e0d2","region":"us-east-2","trace_id":"tr-7341934","event":"message_scan_started","s
17: 2026-04-19T06:51:45Z {"severity":"WARN","logger":"support_platform","service":"support_platform","instance":"support-3","pod":"support-e0d2","region":"us-east-2","trace_id":"tr-7341934","resource_id":"support_3294","even
```

Why: the engine sees `ACTIVE` on backup_7253; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_387 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_1668
Evidence: evidence_36 customer_export_manifest_20260409.json

```
151:       "recorded_at": "2026-04-09T12:00:00Z",
152:       "system": "backup_service",
153:       "resource_id": "backup_1668",
154:       "record_type": "BACKUP_ARCHIVE",
155:       "result": "ACTIVE",
```

Why: the engine sees `ACTIVE` on backup_1668; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_399 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_2642
Evidence: evidence_69 customer_data_inventory_20260404.sql

```
22: INSERT INTO customer_analytics_profiles VALUES ('analytics_5811', NULL, 'tkhumalo2329@gmail.com', NULL, NULL, 'home_lifestyle', '2026-04-04T08:12:08Z');
23: INSERT INTO customer_analytics_profiles VALUES ('analytics_6872', NULL, 'kwame-asante@gmail.com', NULL, NULL, 'mobile_browser', '2026-04-04T09:55:56Z');
24: INSERT INTO backup_restore_entries VALUES ('backup_2642', NULL, 'f.rahman72@gmail.com', 'archive/customer-data/backup_2642.tar.zst', '1', '2026-04-04T09:37:52Z');
25: INSERT INTO customer_exports VALUES ('export_4664', NULL, 'HLEFEVRE4815@FASTMAIL.COM', NULL, 'exports/export_4664/customer_data.zip', '2026-04-04T07:56:37Z');
26: INSERT INTO connector_subscriptions VALUES ('data_flow_626', NULL, 'jonas.s2734@zoho.com', 'search_profile_indexer', '1', 'delivered', '2026-04-04T07:48:30Z');
```

Why: the engine sees `ACTIVE` on backup_2642; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_435 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_5237
Evidence: evidence_41 notification_delivery_20260315.log

```
12: 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=12 system="analytics_platform" resource_id="analytics_6172" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="z
13: 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=13 system="analytics_platform" resource_id="analytics_6528" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="l
14: 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=14 system="backup_service" resource_id="backup_5237" record_type="BACKUP_ARCHIVE" result="ACTIVE" subject_reference="l.bernard56@gmail
15: 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=15 system="integration_service" resource_id="data_flow_1283" record_type="DATA_FLOW" result="ACTIVE" subject_reference="javier.m7818@z
16: 2026-03-15T07:00:00Z WARN service=downstream_delivery_service event=record_lookup seq=16 system="integration_service" resource_id="data_flow_3226" record_type="DATA_FLOW" result="ACTIVE" subject_reference="lkhalil7413@gm
```

Why: the engine sees `ACTIVE` on backup_5237; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_447 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_5192
Evidence: evidence_66 customer_data_inventory_20260310.sql

```
23: INSERT INTO customer_analytics_profiles VALUES ('analytics_7270', NULL, NULL, NULL, NULL, 'returning_customer', '2026-03-10T04:11:03Z');
24: INSERT INTO customer_analytics_profiles VALUES ('analytics_8202', NULL, 'advorak2441@gmail.com', NULL, NULL, 'returning_customer', '2026-03-10T03:35:06Z');
25: INSERT INTO backup_restore_entries VALUES ('backup_5192', NULL, 'e.wright8483@gmail.com', 'archive/customer-data/backup_5192.tar.zst', '1', '2026-03-10T04:45:31Z');
26: INSERT INTO customer_exports VALUES ('export_4293', NULL, 'bsouza4927@fastmail.com', NULL, 'exports/export_4293/customer_data.zip', '2026-03-10T04:28:04Z');
27: INSERT INTO connector_subscriptions VALUES ('data_flow_1068', NULL, 'elena.rios@gmail.com', 'analytics_identity_bridge', '1', 'delivered', '2026-03-10T03:32:16Z');
```

Why: the engine sees `ACTIVE` on backup_5192; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_459 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_1140
Evidence: evidence_43 customer_data_reporting_replica_20260305.sql

```
27: INSERT INTO "customer_data_primary" VALUES('audit_record_6750','security_service','security_audit_events','{"resource_id":"audit_record_6750","subject_reference":"user_456","event_name":"account_deletion_reviewed","actor
28: INSERT INTO "customer_data_primary" VALUES('audit_record_8176','security_service','security_audit_events','{"resource_id":"audit_record_8176","subject_reference":"user_454","event_name":"account_deletion_reviewed","actor
29: INSERT INTO "customer_data_primary" VALUES('backup_1140','backup_service','backup_catalog','{"resource_id":"backup_1140","archive_path":"s3://customer-backups/weekly/segment-20.tar.zst","subject_reference":"d.romero12@gm
30: INSERT INTO "customer_data_primary" VALUES('data_flow_4612','integration_service','connector_configurations','{"resource_id":"data_flow_4612","connector_name":"customer-events-to-warehouse-5","destination":"customer_anal
31: INSERT INTO "customer_data_primary" VALUES('legal_hold_5622','legal_service','retained_order_records','{"resource_id":"legal_hold_5622","subject_reference":"user_458","order_reference":"ORD-20265622","retention_reason":"
```

Why: the engine sees `ACTIVE` on backup_1140; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_471 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_7543
Evidence: evidence_65 service_resource_export_20260228_103637.json

```
93:         },
94:         {
95:           "archive_key": "archive/customer-data/backup_7543.tar.zst",
96:           "customer_email": "k.iyer40@gmail.com",
97:           "customer_reference": null,
```

Why: the engine sees `ACTIVE` on backup_7543; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_495 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_5061
Evidence: evidence_63 customer_data_inventory_20260213.sql

```
22: INSERT INTO customer_analytics_profiles VALUES ('analytics_5893', NULL, NULL, NULL, NULL, 'home_lifestyle', '2026-02-13T05:54:17Z');
23: INSERT INTO customer_analytics_profiles VALUES ('analytics_6565', NULL, NULL, NULL, NULL, 'home_lifestyle', '2026-02-13T06:46:55Z');
24: INSERT INTO backup_restore_entries VALUES ('backup_5061', NULL, 'H.LIM96@GMAIL.COM', 'archive/customer-data/backup_5061.tar.zst', '1', '2026-02-13T05:21:17Z');
25: INSERT INTO connector_subscriptions VALUES ('data_flow_006', NULL, 'INES.ROUSSEAU@OUTLOOK.COM', 'customer_events_connector', '1', 'delivered', '2026-02-13T07:20:06Z');
26: INSERT INTO customer_search_documents VALUES ('search_2799', NULL, NULL, 'O.ERIKSEN10@YAHOO.COM', NULL, NULL, 'customer_directory_v3', '2026-02-13T05:05:05Z');
```

Why: the engine sees `ACTIVE` on backup_5061; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_507 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_369
Evidence: evidence_47 customer_data_reporting_replica_20260208.sql

```
25: INSERT INTO "customer_data_primary" VALUES('audit_record_7627','security_service','security_audit_events','{"resource_id":"audit_record_7627","subject_reference":"user_505","event_name":"account_deletion_reviewed","actor
26: INSERT INTO "customer_data_primary" VALUES('audit_record_8154','security_service','security_audit_events','{"resource_id":"audit_record_8154","subject_reference":"user_506","event_name":"account_deletion_reviewed","actor
27: INSERT INTO "customer_data_primary" VALUES('backup_369','backup_service','backup_catalog','{"resource_id":"backup_369","archive_path":"s3://customer-backups/weekly/segment-17.tar.zst","subject_reference":"r.ito24@gmail.c
28: INSERT INTO "customer_data_primary" VALUES('data_flow_5281','integration_service','connector_configurations','{"resource_id":"data_flow_5281","connector_name":"customer-events-to-warehouse-2","destination":"customer_anal
29: INSERT INTO "customer_data_primary" VALUES('export_3120','export_service','customer_export_jobs','{"resource_id":"export_3120","owner_email":"oeze0067@fastmail.com","file_name":"customer_export_3120.zip","created_at":"20
```

Why: the engine sees `ACTIVE` on backup_369; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_519 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_8264
Evidence: evidence_48 operations_stream_me_central_20260203.log

```
87: 2026-02-03T05:58:14Z | DEBUG | security_service | tr-1598401 | audit_record_read_completed | instance="security-2" pod="security-102b" region="eu-central-1" resource_id="audit_record_3567" integrity_check="passed" rows="
88: 2026-02-03T05:58:15Z | DEBUG | backup_service | tr-8270299 | restore_policy_check_started | instance="backup-4" pod="backup-b50f" region="eu-central-1" subject_key="s.dlamini52@gmail.com" attempt="1"
89: 2026-02-03T05:58:20Z | ERROR | backup_service | tr-8270299 | restore_candidate_evaluated | instance="backup-4" pod="backup-b50f" region="eu-central-1" resource_id="backup_8264" eligible="true" deletion_block="false"
90: 2026-02-03T05:58:49Z | DEBUG | support_platform | tr-2266561 | message_scan_started | instance="support-7" pod="support-4249" region="eu-west-1" subject_key="andersson.linnea@icloud.com" attempt="1"
91: 2026-02-03T05:58:55Z | DEBUG | support_platform | tr-2266561 | connection_acquired | instance="support-7" pod="support-4249" region="eu-west-1" pool="support_platform_replica" wait_ms="29"
```

Why: the engine sees `ACTIVE` on backup_8264; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_531 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_3382
Evidence: evidence_62 service_resource_export_20260129_114459.json

```
101:       "restore_entries": [
102:         {
103:           "archive_key": "archive/customer-data/backup_3382.tar.zst",
104:           "customer_email": "k.amponsah80@gmail.com",
105:           "customer_reference": null,
```

Why: the engine sees `ACTIVE` on backup_3382; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_75 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_8673
Evidence: evidence_91 resource_lookup_trace_20260911_074253.log

```
12: 2026-09-11T05:15:16Z level=DEBUG service=security_service trace_id=rb-051516-006 event=audit_record_read_started resource_id=audit_record_1734 lookup_key=user_77
13: 2026-09-11T05:15:16Z level=INFO service=security_service trace_id=rb-051516-006 event=audit_record_read_completed resource_id=audit_record_1734 rows=1 subject_reference=user_77 event_code=ACCOUNT_DELETION_RECORDED retent
14: 2026-09-11T05:22:44Z level=DEBUG service=backup_service trace_id=rb-052244-007 event=restore_policy_read_started resource_id=backup_8673 lookup_key=n.nwosu16@gmail.com
15: 2026-09-11T05:22:44Z level=INFO service=backup_service trace_id=rb-052244-007 event=restore_policy_read_completed resource_id=backup_8673 archive_present=true restore_allowed=true archive_key=archive/customer-data/backup
16: 2026-09-11T05:29:07Z level=DEBUG service=support_platform trace_id=rb-052907-008 event=support_ticket_read_started resource_id=support_008 lookup_key=user_75
```

Why: the engine sees `ACTIVE` on backup_8673; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_87 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_4689
Evidence: evidence_08 search_index_diagnostic_20260906.log

```
14: 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=14 system="analytics_platform" resource_id="analytics_8539" record_type="ANALYTICS_PROFILE" result="IDENTIFIABLE" subject_reference="mei.k952
15: 2026-09-06T07:00:00Z INFO service=search_index_service event=record_lookup seq=15 system="analytics_platform" resource_id="analytics_9500" record_type="ANALYTICS_PROFILE" result="ANONYMIZED" subject_reference=""
16: 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=16 system="backup_service" resource_id="backup_4689" record_type="BACKUP_ARCHIVE" result="ACTIVE" subject_reference="z.saleh44@gmail.com"
17: 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=17 system="integration_service" resource_id="data_flow_2085" record_type="DATA_FLOW" result="ACTIVE" subject_reference="zmahlangu160178@gmail
18: 2026-09-06T07:00:00Z WARN service=search_index_service event=record_lookup seq=18 system="integration_service" resource_id="data_flow_7535" record_type="DATA_FLOW" result="ACTIVE" subject_reference="doyun.lim@outlook.com
```

Why: the engine sees `ACTIVE` on backup_4689; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

## case_99 — backup_never_risk
Rule: state: restore_allowed=true means a restore risk
Finding: REPORT_RESTORE_RISK backup_service backup_7804
Evidence: evidence_89 service_resource_export_20260901_053316.json

```
59:       "restore_entries": [
60:         {
61:           "archive_key": "archive/customer-data/backup_7804.tar.zst",
62:           "customer_email": "i.horvat72@gmail.com",
63:           "customer_reference": null,
```

Why: the engine sees `ACTIVE` on backup_7804; disabling the backup_never_risk rule removes the only finding, flipping INCOMPLETE→COMPLETE.

