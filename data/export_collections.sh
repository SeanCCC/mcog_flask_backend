mongoexport --db test --collection activities --out activities.json
mongoexport --db test --collection body_compositions --out body_compositions.json
mongoexport --db test --collection dailies --out dailies.json
mongoexport --db test --collection daiepochs --out epochs.json
mongoexport --db test --collection manually_updated_activities --out manually_updated_activities.json
mongoexport --db test --collection moveIQ --out moveIQ.json
mongoexport --db test --collection pulse_ox --out pulse_ox.json
mongoexport --db test --collection sleeps --out sleeps.json
mongoexport --db test --collection stress --out stress.json
mongoexport --db test --collection third_party_dailies --out third_party_dailies.json
mongoexport --db test --collection user_metrics --out user_metrics.json

mongoexport --db mcog --collection devicedump --out devicedump.json
mongoexport --db mcog --collection surveydump --out surveydump.json
mongoexport --db mcog --collection tripdump --out tripdump.json
mongoexport --db mcog --collection servicecheck --out servicecheck.json
mongoexport --db mcog --collection tracking --out tracking.json
mongoexport --db mcog --collection lastpos --out lastpos.json

